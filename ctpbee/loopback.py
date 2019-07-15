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
//        ┃　　　┃   Datetime: 2019/7/7 下午10:36  ---> 无知即是罪恶
//        ┃　　　┗━━━━━━━━━┓
//        ┃　　　　　　　    ┣┓
//        ┃　　　　         ┏┛
//        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
//          ┃ ┫ ┫   ┃ ┫ ┫
//          ┗━┻━┛   ┗━┻━┛
//
"""

# 回测模块

from functools import wraps
from threading import Thread

from ctpbee.constant import EVENT_TICK, TickData, BarData, AccountData
from ctpbee.event_engine import Event
from ctpbee.signals import tick_sender


def send_tick(tick):
    tick_event = Event(EVENT_TICK, tick)
    tick_sender.send(tick_event)


def load_data(func):
    """ 载入装饰器 """

    @wraps
    def wrapper(*args, **kwargs):
        tick = func(*args, **kwargs)
        p = Thread(target=send_tick, args=tick)
        p.start()
        return None
    return wrapper


# An easy use

if __name__ == '__main__':
    from ctpbee import CtpBee
    from ctpbee import ExtAbstract

    app = CtpBee("ctpbee", __name__)
    class LoopbackTest(ExtAbstract):
        """
            你的策略   这个地方应该导入Cta
            发单处理之后调用发送账户事件回来. 计算自己本地持仓后
            然后等待回测结束之后

        """

        def __init__(self, name, app):
            super().__init__(name, app)

            def func(tick):
                self.on_tick(tick)
            tick_sender.connect(func)

        def on_tick(self, tick: TickData) -> None:
            pass

        def on_bar(self, bar: BarData) -> None:
            pass

        def on_account(self, account: AccountData) -> None:
            pass

    @load_data
    def read_book():
        """ 我在读取数据 用户自定义 ----> maybe should make """
        ...
        return ("tick1", "tick2",)
