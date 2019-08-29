from collections import defaultdict

from pandas import DataFrame

from ctpbee.constant import TradeData


class Account:
    """
    账户类

    支持成交之后修改资金 ， 对外提供API

    """

    def __init__(self):
        self.positions = defaultdict(dict)
        # 每日资金情况
        self.daily_life = defaultdict(list)

        # 起始资金 默认10w 以及冻结
        self.balance = 100000
        self.frozen = 0

        self.size = 5
        self.pricetick = 10

        self.daily_limit = 20

        # 佣金
        self.commission: float = 0

        # 滑点相关设置
        self.slip_page: float = 0

        self.slip_fixed: float = 0
        self.slip_open: bool = False
        self.slip_match: bool = True
        self.slip_limit: bool = True
        self.slip_out: bool = False

    def update_attr(self, **kwargs):
        """ 从外部更新资金等相关情况 """
        {setattr(self, i, v) for i, v in kwargs.items() if hasattr(self, i)}

    def is_traded(self, trade: TradeData) -> bool:
        """ 当前账户是否足以支撑成交 """
        # 根据传入的单子判断当前的账户资金和冻结 是否足以成交此单
        if trade.price * trade.volume < self.balance - self.frozen:
            """ 可用不足"""
            return False
        return True

    def trading(self, trade: TradeData) -> None:
        """
        进行交易
        :param trade:交易单子
        :return:
        """

    def result(self):
        # 计算并获取最后的结果
        df = DataFrame.from_dict(self.daily_life).set_index("date")
        return
