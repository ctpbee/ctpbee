import json
from threading import Thread

from redis.client import Redis

import ctpbee.signals
from blinker import NamedSignal

from ctpbee.constant import EVENT_TICK, Event, EVENT_LOG


class MdApi:
    def __init__(self, app_signal):
        self.order_down_kernel = None
        self.order_up_kernel = None
        self.app_signal = app_signal
        self.rd = None
        self.subscribe_items = []
        self.index = 0
        self.info = {}
        self.tick_kernel = ""

    def connect(self, info: dict):
        info["decode_responses"] = True
        info["encoding"] = "utf8"
        self.tick_kernel = info.pop("tick_kernel", "ctpbee_tick_kernel")
        self.index = info.pop("index", 0)
        self.order_up_kernel = info.pop("order_up_kernel", "ctpbee_order_up_kernel")
        self.order_down_kernel = info.pop(
            "order_down_kernel", "ctpbee_order_down_kernel"
        )
        self.rd = Redis(**info)
        self.info = info
        self.on_event(EVENT_LOG, "行情连接成功")
        thread = Thread(target=self.run)
        thread.start()

    def run(self):
        pub = self.rd.pubsub()
        pub.subscribe(self.tick_kernel)
        from ctpbee import loads

        for item in pub.listen():
            tick_data = item["data"]
            if type(tick_data) == int:
                continue
            tick = loads(json.loads(tick_data)["data"])
            if tick.symbol in self.subscribe_items:
                self.on_event(EVENT_TICK, tick)

    def subscribe(self, local_symbol):
        symbol = local_symbol.split(".")[0] if "." in local_symbol else local_symbol
        self.subscribe_items.append(symbol)

    def unsubscribe(self, local_symbol):
        symbol = local_symbol.split(".")[0] if "." in local_symbol else local_symbol
        if symbol in self.subscribe_items:
            self.subscribe_items.remove(symbol)

    def on_event(self, type_, data):
        if type_ == EVENT_TICK:
            event = Event(type=type_, data=data)
            signal = getattr(ctpbee.signals.common_signals, f"{type_}_signal")
            signal.send(event)
        else:
            event = Event(type=type_, data=data)
            signal: NamedSignal = getattr(self.app_signal, f"{type_}_signal")
            signal.send(event)
