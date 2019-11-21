"""
Notice : 神兽保佑 ，测试一次通过
//      
//      ┏┛ ┻━━━━━┛ ┻┓
//      ┃　　　　　　 ┃
//      ┃　　　━　　　┃
//      ┃　┳┛　  ┗┳　┃
//      ┃　　　　　　 ┃
//      ┃　　　┻　　　┃
//      ┃　　　　　　 ┃
//      ┗━┓　　　┏━━━┛
//        ┃　　　┃   Author: somewheve
//        ┃　　　┃   Datetime: 2019/7/6 下午2:13  ---> 无知即是罪恶
//        ┃　　　┗━━━━━━━━━┓
//        ┃　　　　　　　    ┣┓
//        ┃　　　　         ┏┛
//        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
//          ┃ ┫ ┫   ┃ ┫ ┫
//          ┗━┻━┛   ┗━┻━┛
//
"""
from blinker import signal


class CommonSignal:
    # 全局级别的signal
    def __init__(self):
        self.event = ["timer", "tick", "bar", "error"]
        self.timer_signal = signal("timer")
        # tick
        self.tick_signal = signal("tick")
        # bar
        self.bar_signal = signal("bar")

        self.error_signal = signal("error")


class AppSignal:
    """ Here """

    def __init__(self, app):
        """ 账户级别的相关信号 """
        self.event = ['order', "trade", "contract", "position", "init", "account", "last", "log"]
        self.app = app
        self.order_signal = signal("order")
        self.trade_signal = signal("trade")
        self.position_signal = signal("position")
        self.init_signal = signal("init")
        self.account_signal = signal("account")
        self.last_signal = signal("last")
        self.log_signal = signal("log")
        self.contract_signal = signal("contract")


# 发单监视器
send_monitor = signal("send_order")
# 撤单监视器
cancel_monitor = signal("cancel_order")

common_signals = CommonSignal()
