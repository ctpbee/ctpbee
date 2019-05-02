"""
function used to cancle order, sender, qry_position and qry_account

"""
from ctpbee.context import proxy, current_app
from ctpbee.api.custom_var import OrderRequest, CancelRequest
from ctpbee.exceptions import TraderError, ContextError


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


class DataResolve(object):
    def __init__(self):
        pass

    @classmethod
    def process_tick(self, tick):
        func = getattr(self, "on_tick")
        func(tick)

    @classmethod
    def process_bar(self, bar):
        func = getattr(self, "on_tick")
        func(bar)

    @classmethod
    def on_tick(self, tick):
        """用户收到tick的处理"""
        pass

    @classmethod
    def on_bar(self, bar):
        """用户收到bar的处理"""
        pass
