import collections
from collections import defaultdict

from ctpbee.constant import OrderRequest, EVENT_TRADE, CancelRequest, PositionData
from ctpbee.event_engine import Event


class LocalLooperApi():
    """
    本地化回测的服务端 ---> this will be a very interesting thing!
    """

    def __init__(self, event_engine, app):
        super().__init__()
        self.md_address = 0
        self.event_engine = event_engine
        self.pending_order = dict()
        # 账户数据
        self.account_data = defaultdict(list)
        # 在载入回测的时候需要传入app来知道配置

        self.starting_cash = self.cash
        self.order = list()
        self._value_mkt = 0.0
        self._leverage = 1.0
        self._un_realized = 0
        self._value_level = 0.0
        self._value_mkt_level = 0.0
        self.pending = collections.deque()
        self._to_activate = collections.deque()
        self.positions = collections.defaultdict(PositionData)
        self.d_credit = collections.defaultdict(float)
        self.notifs = collections.deque()
        self.submitted = collections.deque()

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

    def submit(self, order, check=True):
        ## 提交order到这里

        pass

    def check_submitted(self):
        cash = self.cash
        positions = dict()
        while self.submitted:
            pass

    def submit_accept(self, order):
        pass
