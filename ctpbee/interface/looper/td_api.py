from collections import defaultdict

from ctpbee.constant import OrderRequest, EVENT_TRADE, CancelRequest
from ctpbee.event_engine import Event


class LocalLooperApi():
    """
    本地化回测的API
    """

    def __init__(self, event_engine, app):
        super().__init__()
        self.md_address = 0
        self.event_engine = event_engine
        self.pending_order = dict()
        # 账户数据
        self.account_data = defaultdict(list)
        # 在载入回测的时候需要传入app来知道配置
        self.init_config(app)

    def init_config(self, app):
        for idx, value in app.config['LOOPER']:
            setattr(self, idx, value)

    @property
    def start_date(self) -> str:
        """ 开始日期 """
        return ""

    @property
    def end_date(self) -> str:
        """ 结束日期 """
        return " "

    def send_order(self, order: OrderRequest):
        """收到发单请求  进行操作"""

        # 本地撮合成交

        # 推送成交事件
        trade = None
        event = Event(EVENT_TRADE, trade)

    def cancel_order(self, order: CancelRequest):
        #
        if order.order_id in self.pending_order:
            self.pending_order.pop(order.order_id)

    @property
    def looper_result(self):
        return self.account_data
