"""
* 账户模块, 存储资金修改, 负责对外部的成交单进行成交撮合 并扣除手续费 等操作
* 需要向外提供API
    trading: 发起交易
    is_traded: 是否可以进行交易
    result: 回测结果
"""

from collections import defaultdict

from pandas import DataFrame

from ctpbee.constant import TradeData
from ctpbee.data_handle.local_position import LocalPositionManager


class AliasDayResult:
    """
    每天的结果
    """

    def __init__(self, **kwargs):
        """ 实例化进行调用 """
        for i, v in kwargs.items():
            setattr(self, i, v)

    def __repr__(self):
        result = "DailyResult: { "
        for x in dir(self):
            if x.startswith("_"):
                continue
            result += f"{x}:{getattr(self, x)} "
        return result + "}"


class Account:
    """
    账户类

    支持成交之后修改资金 ， 对外提供API

    """
    balance = 100000
    frozen = 0
    size = 5
    pricetick = 10
    daily_limit = 20
    commission: float = 0

    def __init__(self, interface):
        self.interface = interface
        self.position_manager = LocalPositionManager(interface.params)
        # 每日资金情况
        self.daily_life = defaultdict(AliasDayResult)
        self.date = None

    def is_traded(self, trade: TradeData) -> bool:
        """ 当前账户是否足以支撑成交 """
        # 根据传入的单子判断当前的账户资金和冻结 是否足以成交此单
        if trade.price * trade.volume < self.balance - self.frozen:
            """ 可用不足"""
            return False
        return True

    def update_trade(self, trade: TradeData) -> None:
        """
        当前选择调用这个接口的时候就已经确保了这个单子是可以成交的，

        make sure it can be traded if you choose to call this method,

        :param trade:交易单子/trade_id
        :return:
        """
        # 根据单子 更新当前的持仓 ----->
        if not self.date:
            self.date = self.interface.date
        if self.interface.date != self.date:
            """ 新的一天 """
            self.get_new_day()
            self.date = self.interface.date
        if self.commission != 0:
            commission_expense = trade.price * trade.volume
        else:
            commission_expense = 0
        self.balance -= commission_expense
        # todo : 更新本地账户数据， 如果是隔天数据， 那么统计战绩 -----> AliasDayResult，然后推送到字典 。 以日期为key
        self.position_manager.update_trade(trade=trade)

    def get_new_day(self, interface_date):
        """ 获取到新的一天数据 """
        p = AliasDayResult(
            **{"balance": self.balance, "frozen": self.frozen, "available": self.balance - self.frozen})
        if not self.date:
            date = interface_date
        else:
            date = self.date
        print(date, p)
        self.daily_life[date] = p

    def via_aisle(self):
        if self.interface.date != self.date:
            self.get_new_day(self.interface.date)
            self.date = self.interface.date
        else:
            pass

    @property
    def result(self):
        # 计算并获取最后的结果
        df = DataFrame.from_dict(self.daily_life).set_index("date")
        return df
