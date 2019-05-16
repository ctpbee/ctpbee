"""
function used to cancle order, sender, qry_position and qry_account

"""
from typing import Text

from ctpbee.context import current_app
from ctpbee.ctp.constant import OrderRequest, CancelRequest, EVENT_TRADE, EVENT_SHARED, EVENT_ORDER
from ctpbee.event_engine import Event
from ctpbee.ctp.constant import EVENT_TICK, EVENT_BAR
from ctpbee.exceptions import TraderError


def send_order(order_req: OrderRequest):
    """发单"""
    app = current_app()
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    return app.trader.send_order(order_req)


def cancle_order(cancle_req: CancelRequest):
    """撤单"""
    app = current_app()
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    app.trader.cancel_order(cancle_req)


def subscribe(symbol: Text) -> None:
    """订阅"""
    app = current_app()
    app.market.subscribe(symbol)


def query_func(type: Text) -> None:
    """查询持仓 or 账户"""
    app = current_app()
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    if type == "position":
        app.trader.query_position()
    if type == "account":
        app.trader.query_account()


class DataSolve(object):
    """核心数据处理类，继承此类，根据你的需求编写重写处理函数， ctpbee会自动将你的处理函数用到刀刃上"""

    def data_solve(self, event: Event) -> None:
        """基础数据处理方法"""
        if event.type == EVENT_TICK:
            self.on_tick(tick=event.data)
        if event.type == EVENT_BAR:
            self.on_bar(bar=event.data, interval=event.interval)
        if event.type == EVENT_TRADE:
            self.on_trade(event.data)
        if event.type == EVENT_SHARED:
            self.on_shared(event.data)
        if event.type == EVENT_ORDER:
            self.on_order(event.data)

    def on_order(self, order):
        pass

    def on_shared(self, shared):
        pass

    def on_bar(self, bar, interval):
        pass

    def on_tick(self, tick):
        pass

    def on_trade(self, trade):
        pass

    def __init_subclass__(cls, **kwargs):
        """get all the  attribute of child class and copy it to parent class"""
        for key in dir(cls):
            try:
                setattr(DataSolve, key, getattr(cls, key))
            except AttributeError:
                pass
            except TypeError:
                pass
        DataSolve.__init__(DataSolve)
