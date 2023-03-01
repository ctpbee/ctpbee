import ctpbee.signals
from blinker import NamedSignal

from ctpbee.constant import EVENT_TICK, Event


class MdApi:
    def __init__(self, app_signal):
        self.app_signal = app_signal
        self.rd = None

    def connect(self, info: dict):
        pass

    def subscribe(self, local_symbol):
        symbol = local_symbol.split(".")[0] if "." in local_symbol else local_symbol
        # todo: open a new thread to listen tick from trading terminal
        raise NotImplemented

    def unsubscribe(self, local_symbol):
        raise NotImplemented

    def on_event(self, type_, data):
        if type_ == EVENT_TICK:
            event = Event(type=type_, data=data)
            signal = getattr(ctpbee.signals.common_signals, f"{type_}_signal")
            signal.send(event)
        else:
            event = Event(type=type_, data=data)
            signal: NamedSignal = getattr(self.app_signal, f"{type_}_signal")
            signal.send(event)
