"""
function used to cancle order, sender, qry_position and qry_account

"""
from ctpbee.context import proxy, current_app
from ctpbee.api.custom_var import OrderRequest, CancelRequest
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
    def __init__(self, app=None):
        app.extensions['data_pointer'] = self

    def data_solve(self, event):
        """基础数据处理方法"""
        pass

    def on_bar(self, bar):
        pass

    def on_tick(self, tick):
        pass

    def init_app(self, app):
        app['data_pointer'] = self
