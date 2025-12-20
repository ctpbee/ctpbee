from ctpbee.signals import common_signals
from ctpbee.constant import EVENT_TICK, Event


class LooperMe:
    def __init__(self, app_signal):
        self.app_signal = app_signal
        self.gateway_name = "SIM"
        self.login_status = True

    @property
    def md_status(self):
        return self.login_status

    def on_event(self, type, data):
        if type == EVENT_TICK:
            event = Event(type=type, data=data)
            signal = getattr(common_signals, f"{type}_signal")
            signal.send(event)
        # 此处不实现合约推送

    def subscribe(self, code):
        # 虚拟载体 不进行提供代码转换， 但是要实现此接口
        return 1

    def connect(self, info):
        print("虚拟行情已经载入，请使用外部行情")

    def unsubscribe(self, local_symbol):
        import warnings

        warnings.warn("正在回测接口中调用无效的取消订阅接口")
