import collections
from collections import defaultdict

from ctpbee.constant import OrderRequest, CancelRequest, PositionData


class AliasDayResult:
    """
    每天的结果
    """

    def __init__(self, **kwargs):
        """ 实例化进行调用 """
        for i, v in kwargs:
            setattr(self, i, v)


class LocalLooperApi():
    """
    本地化回测的服务端 ---> this will be a very interesting thing!

    """
    cash = 100000

    def __init__(self, event_engine, app):
        super().__init__()

        # 接入事件引擎
        self.event_engine = event_engine
        self.pending_order = dict()

        # 账户数据
        self.account_data = defaultdict(list)

        # 基础数据结构
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

        # 独立回测
        self.p = collections.defaultdict(collections.deque)
        self._ocos = dict()
        self._ocol = collections.defaultdict(list)

        # 根据外部配置覆盖配置
        self.init_config(app)

    def set_attribute(self, **attr):
        """ 通过外部设置参数 """
        for i, v in attr:
            setattr(self, i, v)

    def init_config(self, app):
        """ 初始化设置 """
        for idx, value in app.config['LOOPER']:
            setattr(self, idx, value)

    def send_order(self, order: OrderRequest):
        """ 发单
        --- > 实现操作应该有
        买多
        卖空
        做多
        做空
        """

    def cancel_order(self, order: CancelRequest):
        """ 撤单 """
        pass

    def submit(self, order, check=True):
        """ 提交order """

    def check_submitted(self):
        """ 检查是否提交 """

    def calculate_result(self):
        """ 计算每日结果输出信息 """
        result = dict()
        return result
