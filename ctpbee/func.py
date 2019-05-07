"""
function used to cancle order, sender, qry_position and qry_account

"""
from ctpbee.context import proxy, current_app
from ctpbee.api.custom_var import OrderRequest, CancelRequest
from ctpbee.event_engine import Event
from ctpbee.api.custom_var import EVENT_TICK, EVENT_BAR
from ctpbee.exceptions import TraderError


def send_order(order_req: OrderRequest):
    app = current_app()
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    app.trader.send_order(order_req)


def cancle_order(cancle_req: CancelRequest):
    app = current_app()
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    app.trader.cancle_order(cancle_req)


def subscribe(symbol):
    app = current_app()
    app.market.subscribe(symbol)


def query_func(type):
    app = current_app()
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    if type == "position":
        app.trader.query_position()
    if type == "account":
        app.trader.query_account()


class DataSolve(object):

    def data_solve(self, event: Event):
        """基础数据处理方法"""
        if event.type == EVENT_TICK:
            self.on_tick(tick=event.data)
        if event.type == EVENT_BAR:
            self.on_bar(bar=event.data, interval=event.interval)

    def on_bar(self, bar, interval):
        pass

    def on_tick(self, tick):
        pass

    def __init_subclass__(cls, **kwargs):
        """get all the  attribute of child class and copy it to parent"""
        for key in dir(cls):
            try:
                setattr(DataSolve, key, getattr(cls, key))
            except AttributeError:
                pass
            except TypeError:
                pass

