from threading import Thread

from redis.client import Redis

from ctpbee.constant import Event, EVENT_LOG, OrderRequest, CancelRequest, OrderData, EVENT_ORDER, TradeData, \
    EVENT_TRADE, ContractData, EVENT_CONTRACT
from ctpbee.stream import UDDR, DDDR


class TdApi:
    def __init__(self, app_signal):
        self.order_down_kernel = None
        self.order_up_kernel = None
        self.app_signal = app_signal
        self.rd: Redis or None = None
        self.index = 0
        self.info = {}
        self.tick_kernel = ""

    def on_event(self, type_, data):
        event = Event(type=type_, data=data)
        signal = getattr(self.app_signal, f"{type_}_signal")
        signal.send(event)

    def connect(self, info: dict):
        info["decode_responses"] = True
        self.tick_kernel = info.pop("tick_kernel", "TICK_KERNEL")
        self.order_up_kernel = info.pop("order_up_kernel", "ctpbee_order_up_kernel")
        self.order_down_kernel = info.pop("order_down_kernel", "ctpbee_order_down_kernel")
        self.index = info.pop("index", 0)
        self.rd = Redis(**info)
        self.info = info
        thread = Thread(target=self.listen)
        thread.start()
        self.on_event(EVENT_LOG, "交易连接成功")

    def listen(self):
        pub = self.rd.pubsub()
        pub.subscribe(self.order_down_kernel)
        for item in pub.listen():
            tick_data = item["data"]
            if type(tick_data) == int:
                continue
            order = DDDR(obj=tick_data, parse=True)
            if order.index != self.index:
                continue
            if order.order is None:
                continue
            elif type(order.order) == OrderData:
                self.on_event(EVENT_ORDER, data=order.order)
            elif type(order.order) == TradeData:
                self.on_event(EVENT_TRADE, data=order.order)
            elif type(order.order) == ContractData:
                self.on_event(EVENT_CONTRACT, order.order)

    def send_order(self, order: OrderRequest):
        order_msg = UDDR(msg=order, index=self.index, parse=False)
        self.rd.publish(self.order_up_kernel, order_msg.encode())

    def cancel_order(self, cancel: CancelRequest):
        order_msg = UDDR(msg=cancel, index=self.index, parse=False)
        self.rd.publish(self.order_up_kernel, order_msg.encode())

    def query_account(self):
        pass

    def query_position(self):
        pass
