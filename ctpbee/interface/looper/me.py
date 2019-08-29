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

    def check_capital(self):
        """ 校验资金是否足够"""

    def update_attr(self, **kwargs):
        """ 外部更新资金等相关情况 """
        for i, v in kwargs.items():
            setattr(self, i, v)

    def is_traded(self, trade):
        """ 当前账户是否足以支撑成交 """

    def trading(self, trade: TradeData):
        """
        进行交易
        :param trade:
        :return:
        """

    def result(self):
        # 计算并获取最后的结果
        df = DataFrame.from_dict(self.daily_life).set_index("date")
        return
