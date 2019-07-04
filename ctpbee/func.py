"""

面向用户的函数

"""
from typing import Text

from blinker import signal

from ctpbee.context import current_app
from ctpbee.ctp.constant import OrderRequest, CancelRequest, EVENT_TRADE, EVENT_SHARED, EVENT_ORDER, OrderData, \
    TradeData, PositionData, AccountData, TickData, SharedData, BarData, EVENT_POSITION, EVENT_ACCOUNT
from ctpbee.event_engine import Event
from ctpbee.ctp.constant import EVENT_TICK, EVENT_BAR, OrderRequest, CancelRequest
from ctpbee.exceptions import TraderError

send_monitor = signal("send_order")
cancle_monitor = signal("cancle_cancle")


def send_order(order_req: OrderRequest):
    """发单"""
    app = current_app
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    send_monitor.send(order_req)
    return app.trader.send_order(order_req)


def cancle_order(cancle_req: CancelRequest):
    """撤单"""
    app = current_app
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    cancle_monitor.send(cancle_req)
    app.trader.cancel_order(cancle_req)


def subscribe(symbol: Text) -> None:
    """订阅"""
    app = current_app
    app.market.subscribe(symbol)


def query_func(type: Text) -> None:
    """查询持仓 or 账户"""
    app = current_app
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    if type == "position":
        app.trader.query_position()
    if type == "account":
        app.trader.query_account()


class ExtAbstract(object):
    """
    数据模块
    策略模块
        如果你要开发上述插件需要继承此抽象demo
        usage:
        ## coding:
            class Processor(ApiAbstract):
                ...

            data_processor = Processor("data_processor", app)
                        or
            data_processor = Processor("data_processor")
            data_processor.init_app(app)
    """

    def __init__(self, name, app=None):
        """
        init function
        :param name: extension name , development
        :param app: CtpBee instance
        """
        self.extension_name = name
        self.app = app
        if self.app is not None:
            self.init_app(self.app)

    def on_order(self, order: OrderData) -> None:
        raise NotImplemented

    def on_shared(self, shared: SharedData) -> None:
        raise NotImplemented

    def on_bar(self, bar: BarData) -> None:
        raise NotImplemented

    def on_tick(self, tick: TickData) -> None:
        raise NotImplemented

    def on_trade(self, trade: TradeData) -> None:
        raise NotImplemented

    def on_position(self, position: PositionData) -> None:
        raise NotImplemented

    def on_account(self, account: AccountData) -> None:
        raise NotImplemented

    def init_app(self, app):
        if app is not None:
            self.app = app
            self.app.extensions[self.extension_name] = self

    def __call__(self, event: Event):
        from functools import partial
        func = self.map[event.type]
        func(self, event.data)

    def __init_subclass__(cls, **kwargs):
        setattr(cls, "__call__", getattr(ExtAbstract, "__call__"))
        map = {
            EVENT_TICK: cls.on_tick,
            EVENT_BAR: cls.on_bar,
            EVENT_ORDER: cls.on_order,
            EVENT_SHARED: cls.on_shared,
            EVENT_TRADE: cls.on_trade,
            EVENT_POSITION: cls.on_position,
            EVENT_ACCOUNT: cls.on_account,
        }

        parmeter = {
            EVENT_POSITION: "position",
            EVENT_TRADE: "trade",
            EVENT_BAR: "bar",
            EVENT_TICK: "tick",
            EVENT_ORDER: "order",
            EVENT_SHARED: "shared",
            EVENT_ACCOUNT: "account"
        }

        setattr(cls, "map", map)
        setattr(cls, "parmeter", parmeter)


class ApplyTransmission:
    # todo  申请穿透式 代码
    """
        # 简单使用
        from ctpbee import ApplyTransmission
        ctp = ApplyTransmission()
        ctp.connect(account)
        ctp.send(...)
        ctp.cancle(...)

    """

    def connect(self, info):
        pass

    def send(self, request):
        pass

    def cancle(self):
        pass

    def query_position(self):
        pass

    def query_account(self):
        pass


class Helper():
    """ 工具函数 帮助你快速构建发单请求 """

    @staticmethod
    def generate_order_req_from_tick(**kwargs):
        """ 根据tick生成req """
        pass

    @staticmethod
    def generate_order_req_from_bar(**kwargs):
        pass

    @staticmethod
    def generate_order_req(**kwargs):
        """ 手动构造发单请求 """
        # req = OrderRequest()


helper = Helper()
