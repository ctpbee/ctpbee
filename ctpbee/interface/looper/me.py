from collections import defaultdict

from pandas import DataFrame

from ctpbee.constant import TradeData, Offset, Direction
from ctpbee.exceptions import DataError


class Account:
    """
    账户类

    支持成交之后修改资金 ， 对外提供API

    """

    def __init__(self):
        self.positions = defaultdict(dict)
        # 每日资金情况
        self.daily_life = defaultdict(list)

        # 回测模式
        self.pattern = "t+0"

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
        {setattr(self, i.lower(), v) for i, v in kwargs.items() if hasattr(self, i)}

    def is_traded(self, trade: TradeData) -> bool:
        """ 当前账户是否足以支撑成交 """
        # 根据传入的单子判断当前的账户资金和冻结 是否足以成交此单
        if trade.price * trade.volume < self.balance - self.frozen:
            """ 可用不足"""
            return False
        return True

    def trading(self, trade: TradeData) -> None:
        """
        当前选择调用这个接口的时候就已经确保了这个单子是可以成交的，

        make sure it can be traded if you choose to call this method,

        :param trade:交易单子/trade_id
        :return:
        """
        # 根据单子 更新当前的持仓和----->
        #  according to the trade to update position and account
        if trade.offset == Offset.OPEN:
            if trade.direction == Direction.LONG:
                self.buy(trade)
            elif trade.direction == Direction.SHORT:
                self.sell(trade)
            else:
                raise DataError(message=f"数据异常， TradeData direction表现为 {trade.direction.value}, 请检查你的发单代码")
        elif trade.offset == Offset.CLOSETODAY:
            # 处理平今/solve the close_today
            self.close_today(trade)
        elif trade.offset == Offset.CLOSEYESTERDAY:
            self.close_yesterday(trade)

        elif trade.offset == Offset.CLOSE:
            self.close(trade)
        else:
            raise DataError(message=f"数据异常， TradeData offset表现为 {trade.offset.value}, 请检查你的发单代码")

    def buy(self, trade: TradeData):
        """ 处理买/buy """
        # 扣除手续费/deduct the commission

        # todo: 如果成交了是否需要归还冻结的资金
        self.balance = self.balance - self.trade.price * trade.volume * self.commission

        # 建立持仓 / make position

    # 需要买多卖空进行反向解析,从而更改回测的时候的属性

    def sell(self, trade):
        pass

    def close(self, trade):
        pass

    def close_today(self, trade):
        """ 平今 """

    def close_yesterday(self, trade):
        """ 平昨"""

    def close(self, trade):

        """ 平 """

    @property
    def result(self):
        # 计算并获取最后的结果
        df = DataFrame.from_dict(self.daily_life).set_index("date")
        return
