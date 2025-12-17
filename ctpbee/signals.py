from uuid import uuid4

from blinker import signal, NamedSignal


class CommonSignal:
    # 全局级别的signal
    def __init__(self):
        self.event = ["timer", "tick", "bar"]
        self.timer_signal = NamedSignal("timer")
        self.bar_signal = NamedSignal("bar")
        self.tick_signal = NamedSignal("tick")


class AppSignal:
    """Here"""

    def __init__(self, app_name, ids=uuid4()):
        """账户级别的相关信号"""
        self.app_name = app_name
        self.id = ids
        self.event = [
            "order",
            "trade",
            "contract",
            "warning",
            "position",
            "init",
            "account",
            "last",
            "log",
            "error",
        ]
        self.order_signal = NamedSignal(f"{ids}+order")
        self.trade_signal = NamedSignal(f"{ids}+trade")
        self.position_signal = NamedSignal(f"{ids}+position")
        self.init_signal = NamedSignal(f"{ids}+init")
        self.account_signal = NamedSignal(f"{ids}+account")
        self.last_signal = NamedSignal(f"{ids}+last")
        self.log_signal = NamedSignal(f"{ids}+log")
        self.contract_signal = NamedSignal(f"{ids}+contract")
        self.error_signal = NamedSignal(f"{ids}+error")
        self.warning_signal = NamedSignal(f"{ids}+warning")


common_signals = CommonSignal()
