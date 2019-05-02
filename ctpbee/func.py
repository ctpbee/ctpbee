"""
function used to cancle order, sender, qry_position and qry_account

"""
from ctpbee.context import proxy
from ctpbee.api.custom_var import OrderRequest, CancelRequest
from ctpbee.exceptions import TraderError, ContextError


def send_order(order_req: OrderRequest):
    if len(proxy) == 0:
        raise ContextError(message="不存在访问内容， 请确保登录", args=("不存在访问内容， 请确保登录",))

    td = list(proxy.app)[0]
    if not td.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    td.trader.send_order(order_req)


def cancle_order(cancle_req: CancelRequest):
    if len(proxy) == 0:
        raise ContextError(message="不存在访问内容， 请确保登录", args=("不存在访问内容， 请确保登录",))
    td = list(proxy.app)[0]
    if not td.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    td.trader.cancle_order(cancle_req)


def subscribe(symbol):
    if len(proxy) == 0:
        raise ContextError(message="不存在访问内容， 请确保登录", args=("不存在访问内容， 请确保登录",))
    md = list(proxy.app)[0]
    md.market.subscribe(symbol)


class DataResolve(object):
    def process_tick(self, tick):
        func = getattr(self, "on_tick")
        func(tick)

    def process_bar(self, bar):
        func = getattr(self, "on_tick")
        func(bar)

    def on_tick(self, tick):
        """用户收到tick的处理"""
        pass

    def on_bar(self, bar):
        """用户收到bar的处理"""
        pass
