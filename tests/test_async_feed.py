# -*- coding: utf-8 -*-
"""AsyncFeed(asyncio 消费桥, async 路线 Phase 0)的回归测试。

覆盖:
  T1  端到端: 真实 common_signals.tick_signal 上的跨线程投递
  T2  单生产者严格保序(1000 事件)
  T3  慢消费者 + 有界队列: 丢最旧保最新, 最新事件存活
  T4  filter 在 loop 侧执行, filtered 计数正确
  T5  多信号桥接到一条流
  T6  不干扰 blinker 既有同步接收者(Recorder 语义)
  T7  close(): 停止接收、排空余量、async for 正常终止
  T8  压力守恒: consumed+qsize+dropped+filtered+filter_errors == 发送数
  T9  loop 已关闭时生产侧不抛异常(CTP 回调链安全)
  T10 首次迭代自动 start
  T11 审查回归: 队列满时 close() 毒丸挤出腾位, 消费者必定终止
  T12 审查回归: filter 抛异常不杀死排水(flag 不卡死, 后续批次照常)
  T13 审查回归: 未 start 即 close 的 feed 上 async for 干净终止
  基准: 生产侧每事件成本(挂 feed vs 裸信号)

直接运行: python tests/test_async_feed.py
"""
import asyncio
import os
import sys
import threading
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import warnings

warnings.simplefilter("ignore")

from blinker import NamedSignal

from ctpbee.aio import AsyncFeed
from ctpbee.constant import TickData
from ctpbee.signals import common_signals

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))


async def wait_until(cond, timeout=5.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if cond():
            return True
        await asyncio.sleep(0.005)
    return cond()


def tick(symbol="ag2412.SHFE", price=5000.0):
    return TickData(gateway_name="t", local_symbol=symbol,
                    datetime=datetime(2026, 1, 5, 10, 0), last_price=price)


async def main():
    # ------------------------------------------------------------------ T1
    sig = common_signals.tick_signal
    sig.receivers.clear()
    feed = AsyncFeed(sig)
    await feed.start()
    got = []

    async def consume1():
        async for ev in feed:
            got.append(ev)
            if len(got) >= 50:
                break

    c = asyncio.create_task(consume1())
    await asyncio.sleep(0.05)  # 确保 consumer 已在等待

    def produce():
        for i in range(50):
            sig.send(tick(price=5000 + i))

    th = threading.Thread(target=produce)
    th.start()
    await wait_until(lambda: len(got) >= 50)
    th.join()
    await feed.close()
    await asyncio.wait_for(c, timeout=5)
    check("T1 跨线程端到端投递(真实 tick 信号)",
          len(got) == 50 and all(isinstance(g, TickData) for g in got)
          and got[-1].last_price == 5049.0)
    sig.receivers.clear()

    # ------------------------------------------------------------------ T2
    sig2 = NamedSignal("order_t2")
    feed2 = AsyncFeed(sig2)
    await feed2.start()
    out2 = []

    async def consume2():
        async for ev in feed2:
            out2.append(ev)
            if len(out2) >= 1000:
                break

    c2 = asyncio.create_task(consume2())
    await asyncio.sleep(0.05)

    def produce2():
        for i in range(1000):
            sig2.send(i)

    th2 = threading.Thread(target=produce2)
    th2.start()
    await wait_until(lambda: len(out2) >= 1000)
    th2.join()
    await feed2.close()
    await asyncio.wait_for(c2, timeout=5)
    check("T2 单生产者严格保序(1000 事件)",
          out2 == list(range(1000)), f"head={out2[:3]} tail={out2[-3:]}")

    # ------------------------------------------------------------------ T3
    sig3 = NamedSignal("order_t3")
    feed3 = AsyncFeed(sig3, maxsize=10)
    await feed3.start()
    out3 = []

    async def slow_consumer():
        await asyncio.sleep(0.2)  # 制造积压
        async for ev in feed3:
            out3.append(ev)
            if len(out3) >= 10:
                break

    c3 = asyncio.create_task(slow_consumer())
    await asyncio.sleep(0.02)

    def flood():
        for i in range(1000):
            sig3.send(i)

    th3 = threading.Thread(target=flood)
    th3.start()
    th3.join()
    await wait_until(lambda: feed3.delivered + feed3.dropped == 1000)
    await asyncio.wait_for(c3, timeout=5)
    check("T3 满队列丢最旧保最新",
          feed3.dropped > 0 and out3 and out3[-1] == 999,
          f"dropped={feed3.dropped}, 末尾交付={out3[-1] if out3 else None}")
    await feed3.close()

    # ------------------------------------------------------------------ T4
    sig4 = NamedSignal("order_t4")
    feed4 = AsyncFeed(sig4, filter=lambda ev: ev % 2 == 0)
    await feed4.start()
    out4 = []

    async def consume4():
        async for ev in feed4:
            out4.append(ev)
            if len(out4) >= 50:
                break

    c4 = asyncio.create_task(consume4())
    await asyncio.sleep(0.05)

    def produce4():
        for i in range(100):
            sig4.send(i)

    th4 = threading.Thread(target=produce4)
    th4.start()
    await wait_until(lambda: len(out4) >= 50)
    th4.join()
    await feed4.close()
    await asyncio.wait_for(c4, timeout=5)
    check("T4 loop 侧 filter 只交付偶数",
          out4 == [i for i in range(100) if i % 2 == 0]
          and feed4.filtered == 50, f"filtered={feed4.filtered}")

    # ------------------------------------------------------------------ T5
    sa, sb = NamedSignal("t5a"), NamedSignal("t5b")
    feed5 = AsyncFeed(sa, sb)
    await feed5.start()
    out5 = []

    async def consume5():
        async for ev in feed5:
            out5.append(ev)
            if len(out5) >= 60:
                break

    c5 = asyncio.create_task(consume5())
    await asyncio.sleep(0.05)

    def produce5():
        for i in range(30):
            sa.send(("a", i))
            sb.send(("b", i))

    th5 = threading.Thread(target=produce5)
    th5.start()
    await wait_until(lambda: len(out5) >= 60)
    th5.join()
    await feed5.close()
    await asyncio.wait_for(c5, timeout=5)
    a_seq = [i for tag, i in out5 if tag == "a"]
    b_seq = [i for tag, i in out5 if tag == "b"]
    check("T5 多信号汇聚到一条流且各自保序",
          a_seq == list(range(30)) and b_seq == list(range(30)))

    # ------------------------------------------------------------------ T6
    sig6 = NamedSignal("t6")
    feed6 = AsyncFeed(sig6)
    await feed6.start()
    sync_got = []
    sig6.connect(lambda s: sync_got.append(s), weak=False)
    out6 = []

    async def consume6():
        async for ev in feed6:
            out6.append(ev)
            if len(out6) >= 100:
                break

    c6 = asyncio.create_task(consume6())
    await asyncio.sleep(0.05)

    def produce6():
        for i in range(100):
            sig6.send(i)

    th6 = threading.Thread(target=produce6)
    th6.start()
    await wait_until(lambda: len(out6) >= 100)
    th6.join()
    await feed6.close()
    await asyncio.wait_for(c6, timeout=5)
    check("T6 不干扰既有同步接收者",
          sync_got == list(range(100)) and out6 == list(range(100)))

    # ------------------------------------------------------------------ T7
    sig7 = NamedSignal("t7")
    feed7 = AsyncFeed(sig7)
    await feed7.start()
    n_before = len(sig7.receivers)

    def produce7():
        for i in range(20):
            sig7.send(i)

    th7 = threading.Thread(target=produce7)
    th7.start()
    th7.join()
    await wait_until(lambda: feed7.delivered == 20)
    await feed7.close()
    check("T7a close() 断开信号接收者",
          len(sig7.receivers) == n_before - 1 and feed7._on_signal not in
          [getattr(r, "__func__", r) for r in sig7.receivers.values()])

    out7 = []
    try:
        while True:
            out7.append(await asyncio.wait_for(feed7.__anext__(), timeout=2))
    except StopAsyncIteration:
        pass
    check("T7b close() 后队列余量可消费完且正常终止",
          out7 == list(range(20)))

    sig7.send(99)  # close 之后发送不再进入
    await asyncio.sleep(0.05)
    check("T7c close() 后生产侧不再接收", feed7.received == 20)

    # ------------------------------------------------------------------ T8
    sig8 = NamedSignal("t8")
    feed8 = AsyncFeed(sig8, maxsize=500, filter=lambda ev: ev % 3 != 0)
    await feed8.start()
    N8 = 20_000
    out8 = []

    async def consume8():
        async for ev in feed8:
            out8.append(ev)
            if len(out8) >= 5000:
                break
            await asyncio.sleep(0)  # 让生产/排水与消费交错

    c8 = asyncio.create_task(consume8())
    await asyncio.sleep(0.02)

    def stress():
        for i in range(N8):
            sig8.send(i)
            if i % 97 == 0:
                time.sleep(0)  # 制造与排水任务的交错

    th8 = threading.Thread(target=stress)
    th8.start()
    th8.join()
    await wait_until(lambda: feed8.delivered == N8 - feed8.filtered - feed8.filter_errors)
    await feed8.close()
    await asyncio.wait_for(c8, timeout=5)
    expect = [i for i in range(N8) if i % 3 != 0]
    # 守恒律: 已消费 + 队列剩余 + 被挤出 + 被过滤 + 邮箱残留 == 生产侧收到
    check("T8 压力守恒: consumed+qsize+dropped+filtered == 发送数, 无事件滞留",
          feed8.received == N8
          and len(out8) + feed8.qsize + feed8.dropped + feed8.filtered
          + feed8.filter_errors + len(feed8._mailbox) == N8,
          f"recv={feed8.received} consumed={len(out8)} qsize={feed8.qsize} "
          f"drop={feed8.dropped} filt={feed8.filtered}")
    # 丢最旧保最新: 存活者应是 expect 的【尾部】, 且不重复
    check("T8b 交付内容为过滤后的最新尾部且不重复",
          len(out8) >= 1 and out8 == expect[-len(out8):]
          and len(out8) == len(set(out8)) and out8[-1] == expect[-1],
          f"消费 {len(out8)} 条, 末尾 {out8[-1] if out8 else None}")

    # ------------------------------------------------------------------ T9
    sig9 = NamedSignal("t9")
    feed9 = AsyncFeed(sig9)
    await feed9.start()
    closed_loop = asyncio.new_event_loop()
    closed_loop.close()
    real_loop = feed9._loop
    feed9._loop = closed_loop
    feed9._wake_pending = False
    try:
        feed9._on_signal("x")  # loop 已关: 不得抛异常(CTP 回调链安全)
        ok9 = feed9.received == 1 and len(feed9._mailbox) == 1
    except Exception:
        ok9 = False
    feed9._loop = real_loop
    await feed9.close()
    check("T9 loop 已关闭时生产侧不抛异常", ok9)

    # ------------------------------------------------------------------ T10
    sig10 = NamedSignal("t10")
    feed10 = AsyncFeed(sig10)  # 不显式 start
    out10 = []

    async def consume10():
        async for ev in feed10:
            out10.append(ev)
            if len(out10) >= 5:
                break

    c10 = asyncio.create_task(consume10())
    await asyncio.sleep(0.1)  # __anext__ 已自动 start(队列已建)

    def produce10():
        for i in range(5):
            sig10.send(i)

    th10 = threading.Thread(target=produce10)
    th10.start()
    await wait_until(lambda: len(out10) >= 5)
    th10.join()
    await feed10.close()
    await asyncio.wait_for(c10, timeout=5)
    check("T10 首次迭代自动 start", out10 == [0, 1, 2, 3, 4])

    # ------------------------------------------------------------------ T11
    # 审查回归(Bug A): 队列满时 close(), 毒丸须挤出一条腾位, 消费者必须终止
    sig11 = NamedSignal("t11")
    feed11 = AsyncFeed(sig11, maxsize=5)
    await feed11.start()
    gate11 = asyncio.Event()
    out11 = []

    async def gated_consumer():
        await gate11.wait()  # 先不消费, 让排水把队列填满
        async for ev in feed11:  # 无 break, 依赖毒丸终止
            out11.append(ev)

    c11 = asyncio.create_task(gated_consumer())
    await asyncio.sleep(0.05)

    def flood11():
        for i in range(100):
            sig11.send(i)

    th11 = threading.Thread(target=flood11)
    th11.start()
    th11.join()
    await wait_until(lambda: feed11.delivered == 100)
    full_ok = feed11.qsize == 5
    await feed11.close()
    gate11.set()
    try:
        await asyncio.wait_for(c11, timeout=3)
        term_ok = True
    except TimeoutError:
        c11.cancel()
        term_ok = False
    check("T11 队列满时 close(): 毒丸挤出腾位, async for 必定终止",
          full_ok and term_ok and len(out11) == 4
          and feed11.dropped == 96,
          f"qsize_at_close={5 if full_ok else feed11.qsize} consumed={len(out11)} "
          f"dropped={feed11.dropped}")

    # ------------------------------------------------------------------ T12
    # 审查回归(Bug B): filter 抛异常不得杀死排水(flag 卡死/事件滞留)
    sig12 = NamedSignal("t12")

    def bad_filter(ev):
        if ev == 3:
            raise ValueError("user filter bug")
        return True

    feed12 = AsyncFeed(sig12, filter=bad_filter)
    await feed12.start()
    out12 = []

    async def consume12():
        async for ev in feed12:
            out12.append(ev)
            if len(out12) >= 10:
                break

    c12 = asyncio.create_task(consume12())
    await asyncio.sleep(0.05)

    def produce12():
        for i in range(5):
            sig12.send(i)
        time.sleep(0.2)  # 分两个批次, 异常发生在第一批
        for i in range(5, 20):
            sig12.send(i)

    th12 = threading.Thread(target=produce12)
    th12.start()
    th12.join()
    await wait_until(lambda: feed12.delivered == 19)
    await feed12.close()
    await asyncio.wait_for(c12, timeout=5)
    check("T12 filter 抛异常不杀死流: 后续批次照常交付",
          len(out12) == 10 and 3 not in out12
          and feed12.filter_errors == 1 and feed12.delivered == 19
          and not feed12._mailbox and feed12._wake_pending is False,
          f"filter_errors={feed12.filter_errors} delivered={feed12.delivered}")

    # ------------------------------------------------------------------ T13
    # 审查回归(Edge C): 未 start 就 close 的 feed 上 async for 干净终止
    feed13 = AsyncFeed(NamedSignal("t13"))
    await feed13.close()
    out13 = []
    try:
        async for ev in feed13:
            out13.append(ev)
        ok13 = out13 == []
    except RuntimeError:
        ok13 = False
    check("T13 未 start 即 close: async for 干净终止(StopAsyncIteration)", ok13)

    # ------------------------------------------------------------------ 基准
    N_BENCH = 100_000
    bench_sig = NamedSignal("bench")
    bench_sig.connect(lambda s: None, weak=False)

    t0 = time.perf_counter()

    def bench_produce():
        for _ in range(N_BENCH):
            bench_sig.send(None)

    thb = threading.Thread(target=bench_produce)
    thb.start()
    thb.join()
    bare_us = (time.perf_counter() - t0) / N_BENCH * 1e6

    bfeed = AsyncFeed(bench_sig, maxsize=N_BENCH)
    await bfeed.start()
    t0 = time.perf_counter()

    def bench_produce2():
        for _ in range(N_BENCH):
            bench_sig.send(None)

    thb2 = threading.Thread(target=bench_produce2)
    thb2.start()
    thb2.join()
    feed_us = (time.perf_counter() - t0) / N_BENCH * 1e6
    e0 = time.perf_counter()
    await wait_until(lambda: bfeed.delivered + bfeed.dropped == N_BENCH, timeout=10)
    e2e_us = (time.perf_counter() - e0) / N_BENCH * 1e6
    await bfeed.close()

    print(f"\n基准: 裸信号发送 {bare_us:.2f} us/事件 | 挂 AsyncFeed 后 {feed_us:.2f} "
          f"us/事件 (增量 {feed_us - bare_us:.2f}) | 排空 {e2e_us:.3f} us/事件")
    check("BENCH 生产侧增量 < 10 us/事件(远低于朴素桥接的 ~20us)",
          feed_us - bare_us < 10.0, f"delta={feed_us - bare_us:.2f}us")


asyncio.run(main())

failed = [r for r in results if not r[1]]
print()
print("=" * 60)
print(f"{len(results) - len(failed)}/{len(results)} 通过")
if failed:
    for name, _, detail in failed:
        print(f"  FAIL: {name} {detail}")
sys.exit(1 if failed else 0)
