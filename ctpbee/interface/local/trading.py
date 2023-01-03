from ctpbee.constant import Event


class TdApi:
    def __init__(self, app_signal):
        self.app_signal = app_signal

    def on_event(self, type_, data):
        event = Event(type=type_, data=data)
        signal = getattr(self.app_signal, f"{type_}_signal")
        signal.send(event)

    def connect(self, info: dict):
        raise NotImplemented

    def send_order(self, order):
        raise NotImplemented

    def cancel_order(self, order):
        raise NotImplemented

    def query_account(self):
        pass

    def query_position(self):
        pass
