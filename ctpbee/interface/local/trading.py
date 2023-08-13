from redis.client import Redis

from ctpbee.constant import Event, EVENT_LOG


class TdApi:
    def __init__(self, app_signal):
        self.app_signal = app_signal
        self.rd = None
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
        self.index = info.pop("index", 0)
        self.rd = Redis(**info)
        self.info = info
        self.on_event(EVENT_LOG, "交易连接成功")

    def send_order(self, order):
        raise NotImplemented

    def cancel_order(self, order):
        raise NotImplemented

    def query_account(self):
        pass

    def query_position(self):
        pass
