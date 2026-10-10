"""asyncio 消费桥: 同步 blinker 热路径 → asyncio 消费者(async 路线 Phase 0)。

背景(2026-10-10 实测, Python 3.13 / Windows Proactor, 见 agentic.md):
CTP 行情来自 C++ 回调线程, 事件循环无法被直接进入, 必须跨线程桥接。
朴素做法(每事件一次 call_soon_threadsafe)实测 ~20µs/事件, 是同步 blinker
分发(~2µs)的 10 倍; 而「邮箱 + 批量唤醒」把生产侧成本压到 ~0.03µs/事件
(端到端 ~0.1µs/事件, 8.7M 事件/s) —— 每批事件只跨一次线程边界。

设计契约:
  * 生产侧(CTP 回调线程)只做 deque.append + 原子 flag 节流唤醒,
    永不阻塞、永不抛异常(即使 loop 已关闭);
  * 排水在 loop 线程完成, 经有界 asyncio.Queue 交付, 满时丢最旧
    (与 Dispatcher 行情队列同策略: 最新行情优先);
  * 单生产者下严格保序;
  * filter 在 loop 线程执行, 生产侧零额外成本;
  * 不改变 blinker 既有分发的任何行为(只是多了一个普通接收者)。

用法:
    from ctpbee.aio import AsyncFeed
    from ctpbee.signals import common_signals

    feed = AsyncFeed(common_signals.tick_signal)   # 可桥接多个信号

    async def main():
        async with ...:  # 或显式 await feed.start() / await feed.close()
            async for event in feed:               # event 即 blinker 收到的 sender
                print(event.type, event.data)

    # 回调风格:
    async def on_event(event): ...
    # 自行包一层: async for event in feed: await on_event(event)
"""
import asyncio
from collections import deque

__all__ = ["AsyncFeed"]

# 关闭时投递的毒丸: 解除等待中的 __anext__
_SENTINEL = object()


class AsyncFeed:
    """把一个或多个 blinker 信号桥接成 `async for` 可消费的事件流。

    Args:
        *signals: blinker 信号对象(如 common_signals.tick_signal、
            app.app_signal.order_signal)。send(event) 的 event 即本流
            的产出。
        maxsize: 交付队列上限, 满时丢最旧; 默认 100_000。
        filter: 可选谓词 `filter(event) -> bool`, 在 loop 线程执行,
            不满足的事件直接丢弃(不占用队列)。
        loop: 指定事件循环; 缺省在 start() 时取 running loop。

    计数器(诊断用, GIL 下读写安全):
        received: 生产侧收到的事件数(过滤前)
        delivered: 进入交付队列的事件数(含后来被挤出队列的)
        dropped: 队列满时被丢弃的最旧事件数
        filtered: 被 filter 谓词拒绝的事件数
        qsize: 交付队列当前积压(消费侧)

    守恒律(任意静息时刻): 已消费 + qsize + dropped + filtered + 邮箱残留
    == received。dropped 的事件曾入队(delivered 已计), 故 delivered 不
    出现在等式右侧。
    """

    def __init__(self, *signals, maxsize: int = 100_000, filter=None, loop=None):
        if not signals:
            raise ValueError("至少提供一个 blinker 信号")
        if maxsize < 1:
            raise ValueError("maxsize 必须 >= 1")
        self._signals = list(signals)
        self._maxsize = maxsize
        self._filter = filter
        self._loop = loop

        self._mailbox = deque()
        # 唤醒标志的配对约定(单写者各自一侧, GIL 下逐语句原子):
        #   生产侧必须【先 append 后查 flag】;
        #   排水侧必须【先清 flag 后复查邮箱】。
        # 任一交错下, 事件要么被本轮排水带走, 要么触发下一次唤醒,
        # 不会滞留邮箱。改动此顺序会引入丢事件的竞态!
        self._wake_pending = False

        self._queue = None
        self._started = False
        self._closed = False

        self.received = 0
        self.delivered = 0
        self.dropped = 0
        self.filtered = 0

    # ------------------------------------------------------------------ #
    # 生产侧: CTP 回调线程
    # ------------------------------------------------------------------ #
    def _on_signal(self, sender, **kwargs):
        """blinker 接收者 —— 热路径, 只做入队与(节流后的)唤醒"""
        if self._closed or self._queue is None:
            return
        self.received += 1
        self._mailbox.append(sender)
        if self._wake_pending:
            return
        self._wake_pending = True
        try:
            self._loop.call_soon_threadsafe(self._drain)
        except RuntimeError:
            # loop 已关闭: 放弃本次唤醒, 不让异常进入 CTP 回调链
            self._wake_pending = False

    # ------------------------------------------------------------------ #
    # 消费侧: loop 线程
    # ------------------------------------------------------------------ #
    def _drain(self):
        """排空邮箱并转入交付队列(每次唤醒只执行一次循环)"""
        mailbox = self._mailbox
        queue = self._queue
        filter_ = self._filter
        while True:
            try:
                event = mailbox.popleft()
            except IndexError:
                break
            if filter_ is not None and not filter_(event):
                self.filtered += 1
                continue
            try:
                queue.put_nowait(event)
                self.delivered += 1
            except asyncio.QueueFull:
                # 丢最旧保最新, 与 Dispatcher._tick_queue 同策略
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
                self.dropped += 1
                try:
                    queue.put_nowait(event)
                    self.delivered += 1
                except asyncio.QueueFull:
                    pass
        # 先放行 flag 再复查邮箱 —— 见 _wake_pending 处的配对约定
        self._wake_pending = False
        if mailbox:
            self._schedule_wake_in_loop()

    def _schedule_wake_in_loop(self):
        """loop 线程内部补一次唤醒(竞争窗口兜底)"""
        if self._wake_pending:
            return
        self._wake_pending = True
        self._loop.call_soon(self._drain)

    # ------------------------------------------------------------------ #
    # 生命周期
    # ------------------------------------------------------------------ #
    async def start(self):
        """连接信号并创建交付队列(幂等)。也可省略 —— 首次迭代自动调用。"""
        if self._closed:
            raise RuntimeError("feed 已关闭, 不能重新启动")
        if self._started:
            return self
        if self._loop is None:
            self._loop = asyncio.get_running_loop()
        # asyncio.Queue 绑定 loop, 必须在 loop 线程创建
        self._queue = asyncio.Queue(maxsize=self._maxsize)
        for signal in self._signals:
            signal.connect(self._on_signal, weak=False)
        self._started = True
        return self

    async def close(self):
        """断开信号并结束迭代; 已在队列中的事件仍可被消费完"""
        if self._closed:
            return
        self._closed = True
        for signal in self._signals:
            try:
                signal.disconnect(self._on_signal)
            except Exception:  # noqa: BLE001 —— 断开失败不应中断关闭流程
                pass
        self._put_sentinel()

    def _put_sentinel(self):
        loop = self._loop
        if loop is None or self._queue is None:
            return

        def _send():
            try:
                self._queue.put_nowait(_SENTINEL)
            except asyncio.QueueFull:
                pass  # 满则等待中的消费者自会取到数据后再次 get

        if loop.is_closed():
            return
        try:
            running = asyncio.get_running_loop() is loop
        except RuntimeError:
            running = False
        if running:
            _send()
        else:
            try:
                loop.call_soon_threadsafe(_send)
            except RuntimeError:
                pass

    # ------------------------------------------------------------------ #
    # 异步迭代
    # ------------------------------------------------------------------ #
    @property
    def qsize(self) -> int:
        """交付队列当前积压数(loop 侧读取最准确; 诊断用)"""
        if self._queue is None:
            return 0
        return self._queue.qsize()

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._started:
            await self.start()
        while True:
            event = await self._queue.get()
            if event is _SENTINEL:
                if self._closed:
                    raise StopAsyncIteration
                continue  # 他人误投的毒丸(不应发生), 继续取
            return event

    def __repr__(self):
        state = "closed" if self._closed else ("started" if self._started else "idle")
        return (f"<AsyncFeed {state} signals={len(self._signals)} "
                f"received={self.received} delivered={self.delivered} "
                f"dropped={self.dropped} filtered={self.filtered}>")
