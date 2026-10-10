"""
交易流实现
订单协议


"""
import json
import logging
import queue
import time
from collections import OrderedDict
from threading import Thread

from ctpbee.constant import TickData, OrderData, OrderRequest, CancelRequest, ContractData, QueryContract, TradeData, PositionData, AccountData
from ctpbee.level import CtpbeeApi

from redis import Redis

logger = logging.getLogger("ctpbee.stream")

# 节流告警: 同类告警第 1 次与此后每 N 次输出一行, 故障期间不刷爆日志
_LOG_STATE = {}


def _warn_throttled(key: str, msg: str, every: int = 100) -> None:
    n = _LOG_STATE.get(key, 0) + 1
    _LOG_STATE[key] = n
    if n == 1 or n % every == 0:
        logger.warning("%s (x%d)", msg, n)


class UDDR:
    """
    上行消息 订单数据
    """

    def __init__(self, msg, index=0, parse: bool = True):
        self.index = index
        self.obj = None
        if parse:
            try:
                self.__parse__(msg)
            except Exception as e:
                _warn_throttled("uddr_parse", f"上行消息解析失败: {e!r}")
        else:
            self.obj = msg

    def encode(self):
        from ctpbee import dumps
        return json.dumps(dict(
            data=dumps(self.obj),
            index=self.index
        ),
            ensure_ascii=False)

    def __parse__(self, msg):

        msg = json.loads(msg)
        from ctpbee import loads
        self.index = msg["index"]
        self.obj = loads(msg["data"])


class DDDR:
    """
    下行消息
    """

    def __init__(self, obj, index=None, parse=False):
        self.index = None
        self.order = None
        if not parse:
            self.order = obj
            self.index = index
        else:
            self.__parse__(obj)

    def __parse__(self, obj):
        """解析下行消息。

        loads 对 DDDR.encode 的产物会直接还原实体对象(TickData/OrderData/
        TradeData/ContractData...)——此时无需嗅探重建, 直接采用; 只有当
        data 是普通 dict(旧客户端手工构造的载荷)时才走键嗅探分支。
        """
        from ctpbee import loads
        locken = loads(obj)
        self.index = locken["index"]
        msg = loads(locken["data"])
        if not isinstance(msg, dict):
            self.order = msg
            return
        if "order_id" in msg.keys() and "tradeid" in msg.keys():
            self.order = TradeData(**msg)
        elif "order_id" in msg.keys() and "tradeid" not in msg.keys():
            self.order = OrderData(**msg)
        elif "pricetick" in msg.keys() and "size" in msg.keys():
            self.order = ContractData(**msg)
        else:
            self.order = None

    def encode(self) -> str:
        from ctpbee import dumps
        return json.dumps(dict(
            data=dumps(self.order),
            index=self.index,
        ),
            ensure_ascii=False)


class Dispatcher(CtpbeeApi):
    """Redis 订单/行情中继(Mode.DISPATCHER)。

    可靠性约定(在原始中继语义之上, 线协议与回调签名完全不变):
      * on_tick 只做入队——序列化与 Redis 发布在独立线程完成, Redis
        故障或慢消费者不会拖慢/打断 CTP 回调链;
      * 所有发布经 _publish: 失败节流告警, 永不向上抛;
      * 订单上行监听线程断线自动重连(固定退避), 单条消息处理失败
        只记日志, 线程不退出;
      * order_key_map 为 LRU 有界, 防止长跑进程无界增长(被淘汰的
        订单号回退到既有的默认索引 0, 与未知订单行为一致)。
    """

    # 行情发布队列上限(满时丢最旧——最新行情优先)
    _TICK_QUEUE_MAX = 100_000
    # 订单号→索引映射上限(LRU)
    _ORDER_MAP_MAX = 10_000
    # 订单通道断线重连退避(秒)
    _RECONNECT_SLEEP = 5.0

    def __init__(self, name, app=None):
        super().__init__(name, app=app)
        tcp_addr = self.app.config.get("RD_CLIENT_ADDR", "127.0.0.1")
        tcp_port = self.app.config.get("RD_CLIENT_PORT", 6379)
        db = self.app.config.get("RD_CLIENT_DB", 0)
        self.order_up_kernel = self.app.config.get("ORDER_UP_KERNEL", "ctpbee_order_up_kernel")
        self.tick_kernel = self.app.config.get("TICK_KERNEL", "ctpbee_tick_kernel")
        self.order_down_kernel = self.app.config.get("ORDER_DOWN_KERNEL", "ctpbee_order_down_kernel")
        self.rd_client = Redis(host=tcp_addr, port=tcp_port, db=db, decode_responses=True, encoding="utf8")
        self.order_key_map = OrderedDict()
        self._tick_queue = queue.Queue(maxsize=self._TICK_QUEUE_MAX)
        self._tick_dropped = 0
        self._closed = False
        threader = Thread(target=self.listen, daemon=True)
        threader.start()
        self._tick_thread = Thread(target=self._tick_publisher, daemon=True)
        self._tick_thread.start()
        self.init = False

    def listen(self):
        """
        监听来自订单通道的消息; 断线自动重连, 单条消息失败不退出线程。
        """
        while not self._closed:
            try:
                pub = self.rd_client.pubsub()
                pub.subscribe(self.order_up_kernel)
                for item in pub.listen():
                    if self._closed:
                        return
                    self._handle_upstream(item)
            except Exception as e:
                _warn_throttled("listen_error",
                                f"订单通道断开({e!r}), {self._RECONNECT_SLEEP:.0f}s 后重连",
                                every=1)
                time.sleep(self._RECONNECT_SLEEP)

    def _handle_upstream(self, item):
        """单条上行消息的隔离处理: 异常只记日志, 不影响后续消息。"""
        try:
            self._dispatch_upstream(item)
        except Exception as e:
            _warn_throttled("handle_error", f"上行消息处理失败: {e!r}")

    def _dispatch_upstream(self, item):
        uddr = UDDR(item["data"], parse=True)
        if uddr.obj is None:
            return
        elif type(uddr.obj) == OrderRequest:
            order_id = self.action.send_order(order=uddr.obj)
            if order_id:
                self._remember_order(order_id, uddr.index)
            else:
                # 未登录/网关未就绪时 send_order 可能返回空值: 不写入映射,
                # 避免污染 order_key_map(未知订单号本就回退默认索引 0)
                _warn_throttled("send_order_empty", "send_order 未返回订单号, 跳过该请求的索引映射")
        elif type(uddr.obj) == CancelRequest:
            self.action.cancel_order(uddr.obj)
            self._remember_order(uddr.obj.order_id, uddr.index)
        elif type(uddr.obj) == QueryContract:
            """
            第一次查询合约的时候需要直接读取全部订单
            """
            for i in self.app.recorder.positions.values():
                dr = DDDR(obj=i, index=uddr.obj.index)
                self._publish(self.order_down_kernel, dr.encode())
            for i in self.app.recorder.get_all_contracts():
                dr = DDDR(obj=i, index=uddr.obj.index, parse=False)
                self._publish(self.order_down_kernel, dr.encode())
            for i in self.app.recorder.get_all_orders():
                dr = DDDR(obj=i, index=uddr.obj.index)
                self._publish(self.order_down_kernel, dr.encode())
            for i in self.app.recorder.get_all_trades():
                dr = DDDR(obj=i, index=uddr.obj.index)
                self._publish(self.order_down_kernel, dr.encode())
            # Send init complete signal (use plain json.dumps — ctpbee dumps returns None for plain dicts)
            init_msg = json.dumps(
                {"data": json.dumps({"type": "init_complete", "count": len(self.app.recorder.get_all_contracts())}), "index": uddr.obj.index},
                ensure_ascii=False,
            )
            self._publish(self.order_down_kernel, init_msg)
            self.info(f"init complete, contracts: {len(self.app.recorder.get_all_contracts())}")
        else:
            return

    def _publish(self, channel, payload) -> bool:
        """Redis 发布; 失败节流告警并返回 False, 永不向上抛——
        Redis 故障不能打断行情/交易回调链。"""
        try:
            self.rd_client.publish(channel, payload)
            return True
        except Exception as e:
            _warn_throttled("publish_error", f"Redis 发布失败({channel}): {e!r}")
            return False

    def _publish_tick(self, tick) -> bool:
        """序列化并发布一条行情(供后台线程调用, 独立成方法便于测试)。"""
        try:
            payload = DDDR(obj=tick, index=None).encode()
        except Exception as e:
            _warn_throttled("tick_encode", f"行情序列化失败: {e!r}")
            return False
        return self._publish(self.tick_kernel, payload)

    def _tick_publisher(self):
        """后台线程: 序列化并发布行情(保持 FIFO 顺序)。"""
        while True:
            tick = self._tick_queue.get()
            if tick is None:
                return
            self._publish_tick(tick)

    def _remember_order(self, order_id, index):
        """记录订单号→客户端索引, LRU 有界。"""
        if not order_id:
            return
        self.order_key_map[order_id] = index
        self.order_key_map.move_to_end(order_id)
        while len(self.order_key_map) > self._ORDER_MAP_MAX:
            self.order_key_map.popitem(last=False)

    def close(self):
        """尽力停止后台线程(线程均为 daemon, 不调用也不影响进程退出)。"""
        self._closed = True
        try:
            self._tick_queue.put_nowait(None)
        except queue.Full:
            pass

    def on_order(self, order: OrderData) -> None:
        index = self.order_key_map.get(order.order_id, 0)
        order_message = DDDR(obj=order, index=index)
        self._publish(self.order_down_kernel, order_message.encode())

    def on_tick(self, tick: TickData) -> None:
        """行情回调只入队(热路径); 队列满时丢最旧, 最新行情优先。"""
        try:
            self._tick_queue.put_nowait(tick)
            return
        except queue.Full:
            pass
        try:
            self._tick_queue.get_nowait()
        except queue.Empty:
            pass
        self._tick_dropped += 1
        if self._tick_dropped == 1 or self._tick_dropped % 1000 == 0:
            logger.warning("行情发布队列满, 累计丢弃最旧行情 %d 条", self._tick_dropped)
        try:
            self._tick_queue.put_nowait(tick)
        except queue.Full:
            pass

    def on_contract(self, contract: ContractData) -> None:
        if not self.init:
            for i in self.app.config.get("SUBSCRIBE_CONTRACT", []):
                self.action.subscribe(i)
            self.info("行情订阅成功")
            self.init = True

    def on_trade(self, trade: TradeData) -> None:
        dr = DDDR(obj=trade, index=None)
        self._publish(self.order_down_kernel, dr.encode())

    def on_position(self, position: PositionData) -> None:
        dr = DDDR(obj=position, index=None)
        self._publish(self.order_down_kernel, dr.encode())

    def on_account(self, account: AccountData) -> None:
        dr = DDDR(obj=account, index=None)
        self._publish(self.order_down_kernel, dr.encode())
