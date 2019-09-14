import collections
import random

from ctpbee.looper.data import Bumblebee


class AliasDayResult:
    """
    每天的结果
    """

    def __init__(self, **kwargs):
        """ 实例化进行调用 """
        for i, v in kwargs:
            setattr(self, i, v)


class Action():
    def __init__(self):
        """ 将action这边报单 """

    def buy(self, price, volume, origin, **kwargs):
        pass

    def short(self, price, volume, origin, **kwargs):
        pass

    def sell(self, price, volume, origin, **kwargs):
        pass

    def cover(self, price, volume, origin, **kwargs):
        pass


class LocalLooper():
    def __init__(self, strategy, risk, account, logger):
        self.pending = collections.deque()
        self.sessionid = random.randint(1000, 10000)
        self.frontid = random.randint(10001, 500000)
        # 日志输出器
        self.logger = logger

        self.strategy = strategy
        # 覆盖里面的action和logger属性
        setattr(self.strategy, "action", Action(self))
        setattr(self.strategy, "logger", self.logger)
        setattr(self.strategy, "info", self.logger.info)
        setattr(self.strategy, "debug", self.logger.debug)
        setattr(self.strategy, "error", self.logger.error)
        setattr(self.strategy, "warning", self.logger.warning)

        # 风控/risk control todo:完善
        self.risk = risk

        # 账户属性
        self.account = account

        # 发单的ref集合
        self.order_ref_set = set()
        # 已经order_id ---- 成交单
        self.traded_order_mapping = {}
        # 已经order_id --- 报单
        self.order_id_pending_mapping = {}

    def send_order(self, order_req):
        """ 发单的操作"""

    def cancel(self, cancel_req):
        """ 撤单机制 """

    def gateway(self):
        """ 拦截网关 """
        pass

    def match_deal(self, data):
        """ 撮合成交 """

    def init_params(self, params):
        """ 回测参数设置 """
        # todo: 本地设置回测参数

    def __init_params(self, params):
        """ 初始化参数设置  """
        if not isinstance(params, dict):
            raise AttributeError("回测参数类型错误，请检查是否为字典")
        self.strategy.init_params(params.get("strategy"))
        self.init_params(params.get("looper"))

    def __call__(self, *args, **kwargs):
        """ 回测周期 """
        p_data: Bumblebee = args[0]
        params = args[1]
        self.__init_params(params)
        if p_data.type == "tick":
            self.strategy.on_tick(tick=p_data.to_tick())

        if p_data.type == "bar":
            self.strategy.on_bar(tick=p_data.to_bar())
