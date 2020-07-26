"""
* 账户模块, 存储资金修改, 负责对外部的成交单进行成交撮合 并扣除手续费 等操作
* 需要向外提供API
    trading: 发起交易
    is_traded: 是否可以进行交易
    result: 回测结果
"""

from collections import defaultdict

import numpy as np
from pandas import DataFrame

from ctpbee.constant import TradeData, OrderData, Offset, PositionData, Direction, AccountData
from ctpbee.exceptions import ConfigError
from ctpbee.looper.local_position import LocalPositionManager
import uuid


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

    def _to_dict(self):
        return self.__dict__


class Account:
    """
    账户类

    支持成交之后修改资金 ， 对外提供API

    """

    def __init__(self, interface, name=None):
        self.account_id = name if name is not None else uuid.uuid4()
        # 成交接口
        self.interface = interface
        # 每日成交单信息
        self.daily_life = defaultdict(AliasDayResult)

        # 合约乘数
        self.size = 5
        # 每跳价格变化
        self.pricetick = 10
        # 每日下单限制
        self.daily_limit = 20
        # 账户权益
        self.balance = 100000
        # 账户当前的日期
        self.date = None
        # 手续费
        self.commission_expense = 0
        self.count_statistics = 0

        # 初始资金
        self.initial_capital = 0
        # 占用保证金
        self.occupation_margin = 0

        # 仓位是否初始化 static_balance= None
        # 静态权益 （静态权益 = 昨日结算的权益 + 今日入金 - 今日出金, 以服务器查询ctp后返回的金额为准）(不包含期权)
        self.static_balance = 100000
        # 平仓盈亏
        self.close_profit = 0
        # 浮动盈亏
        self.float_profit = 0
        # 权利金
        self.premium = 0
        # 期权市值
        self.option_value = 0
        # 冻结
        self.frozen = 0

        # balance= None
        # 账户权益 （账户权益 = 动态权益 = 静态权益 + 平仓盈亏 + 持仓盈亏 - 手续费 + 权利金 + 期权市值）
        # available= None

        # 可用资金（可用资金 = 账户权益 - 冻结保证金 - 保证金 - 冻结权利金 - 冻结手续费 - 期权市值）
        # ctp_balance= None
        # 期货公司返回的balance（ctp_balance = 静态权益 + 平仓盈亏 + 持仓盈亏 - 手续费 + 权利金）
        self.init_position_manager_flag = False
        self.init = False
        self.position_manager = None

    @property
    def to_object(self) -> AccountData:
        return AccountData._create_class(dict(accountid=self.account_id,
                                              local_account_id=f"{self.account_id}.SIM",
                                              frozen=self.frozen,
                                              balance=self.balance))

    @property
    def available(self) -> float:
        return self.balance - self.frozen - self.occupation_margin - self.frozen_margin - self.frozen_premiu

    def is_traded(self, order: OrderData) -> bool:
        """ 当前账户是否足以支撑成交 """
        # 根据传入的单子判断当前的账户可用资金是否足以成交此单
        if order.price * order.volume * (1 + self.commission) < self.available:
            """ 可用不足"""
            return False
        return True

    def update_trade(self, trade: TradeData) -> None:
        """
        当前选择调用这个接口的时候就已经确保了这个单子是可以成交的，
        make sure it can be traded if you choose to call this method,
        :param trade:交易单子/trade
        :return:
        """
        # 根据当前成交单子 更新当前的持仓 ----->
        if trade.offset == Offset.OPEN:
            if self.commission != 0:
                commission_expense = trade.price * trade.volume * self.commission
            else:
                commission_expense = 0

        elif trade.offset == Offset.CLOSETODAY:
            if self.interface.params.get("today_commission") != 0:
                commission_expense = trade.price * trade.volume * self.interface.params.get("today_commission")
            else:
                commission_expense = 0

        elif trade.offset == Offset.CLOSEYESTERDAY:
            if self.interface.params.get("yesterday_commission") != 0:
                commission_expense = trade.price * trade.volume * self.interface.params.get("yesterday_commission")
            else:
                commission_expense = 0
        else:
            if self.interface.params.get("close_commission") != 0:
                commission_expense = trade.price * trade.volume * self.interface.params.get("close_commission")
            else:
                commission_expense = 0

        if trade.offset == Offset.CLOSETODAY or trade.offset == Offset.CLOSEYESTERDAY or trade.offset == Offset.CLOSE:
            reversed_map = {
                Direction.LONG: Direction.SHORT,
                Direction.SHORT: Direction.LONG
            }
            position: PositionData = self.position_manager.get_position_by_ld(trade.local_symbol,
                                                                              reversed_map[trade.direction])
            if self.interface.params.get("size_map") is None or self.interface.params.get("size_map").get(
                    trade.local_symbol) is None:
                raise ConfigError(message="请检查你的回测配置中是否存在着size配置", args=("回测配置错误",))
            if trade.direction == Direction.LONG:
                """ 平空头 """
                pnl = (position.price - trade.price) * trade.volume * self.interface.params.get("size_map").get(
                    trade.local_symbol)
            else:
                """ 平多头 """
                pnl = (trade.price - position.price) * trade.volume * self.interface.params.get("size_map").get(
                    trade.local_symbol)
            self.balance += pnl

        self.balance -= commission_expense
        self.commission_expense += commission_expense
        self.count_statistics += 1
        self.position_manager.update_trade(trade=trade)

    def update_margin(self, data: OrderData or TradeData, reverse=False):
        """
            更新保证金
            如果出现成交 开方向 ----> 增加保证金--> 默认
            如果出现成交 平方向 ----> 减少保证金
        """
        if reverse:
            """ 开仓增加保证金"""
            self.occupation_margin += data.volume * data.price
            self.balance -= data.volume * data.price
        else:
            """ 平仓移除保证金归还本金 """
            self.occupation_margin -= data.price * data.volume
            self.balance += data.volume * data.price

    def update_frozen(self, order, reverse=False):
        """
        根据reverse判断方向
        如果是False， 那么出现冻结，同时从余额里面扣除
        """
        if reverse:
            """ 成交 """
            self.frozen -= order.volume * order.price
            self.balance += order.volume * order.price
        else:
            """ 未成交 """
            self.frozen += order.volume * order.price
            self.balance -= order.price * order.volume

    def settle(self, interface_date=None):
        """ 生成今天的交易数据， 同时更新前日数据 ，然后进行持仓结算 """
        if not self.date:
            date = interface_date
        else:
            date = self.date
        """ 结算撤掉所有单 归还冻结 """
        for order in self.interface.pending:
            self.update_frozen(order, reverse=True)
        self.interface.pending.clear()
        p = AliasDayResult(
            **{"balance": self.balance + self.occupation_margin,
               "frozen": self.frozen,
               "available": self.balance - self.frozen,
               "date": date, "commission": self.commission_expense - self.pre_commission_expense,
               "net_pnl": self.balance - self.pre_balance,
               "count": self.count_statistics - self.pre_count
               })
        # self._account["static_balance"] = self._account["balance"]
        # self._account["position_profit"] = 0
        # self._account["close_profit"] = 0
        # self._account["commission"] = 0
        # self._account["premium"] = 0
        self.pre_commission_expense = self.commission_expense
        self.pre_balance = self.balance
        self.pre_count = self.count_statistics

        self.commission = 0
        self.interface.today_volume = 0
        self.count_statistics = 0

        self.position_manager.covert_to_yesterday_holding()
        self.daily_life[date] = p._to_dict()
        # 归还所有的冻结
        self.balance += self.frozen
        self.frozen = 0
        self.date = interface_date

    def via_aisle(self):
        self.position_manager.update_size_map(self.interface.params)
        if self.interface.date != self.date:
            self.settle(self.interface.date)
            self.date = self.interface.date
        else:
            pass

    def update_params(self, params: dict):
        """ 更新本地账户回测参数 """
        for i, v in params.items():
            if i == "initial_capital" and not self.init:
                self.balance = v
                self.pre_balance = v
                self.initial_capital = v
                self.init = True
                continue
            else:
                pass
            setattr(self, i, v)
        if not self.init_position_manager_flag:
            self.position_manager = LocalPositionManager(params)
            self.init_position_manager_flag = True
        else:
            pass

    @property
    def result(self):
        # 根据daily_life里面的数据 获取最后的结果
        result = defaultdict(list)
        for daily in self.daily_life.values():
            for key, value in daily.items():
                result[key].append(value)

        df = DataFrame.from_dict(result).set_index("date")
        try:
            import matplotlib.pyplot as plt
            df['balance'].plot()
            plt.show()

        except ImportError as e:
            pass
        finally:
            return self._cal_result(df)

    def get_mapping(self, d):
        mapping = {}
        for i, v in self.daily_life.items():
            mapping[str(i)] = v.get(d)
        return mapping

    def _cal_result(self, df: DataFrame) -> dict:

        result = dict()
        df["return"] = np.log(df["balance"] / df["balance"].shift(1)).fillna(0)
        df["high_level"] = (
            df["balance"].rolling(
                min_periods=1, window=len(df), center=False).max()
        )
        df["draw_down"] = df["balance"] - df["high_level"]
        df["dd_percent"] = df["draw_down"] / df["high_level"] * 100
        result['initial_capital'] = self.initial_capital
        result['start_date'] = df.index[0]
        result['end_date'] = df.index[-1]
        result['total_days'] = len(df)
        result['profit_days'] = len(df[df["net_pnl"] > 0])
        result['loss_days'] = len(df[df["net_pnl"] < 0])
        result['end_balance'] = df["balance"].iloc[-1]
        result['max_draw_down'] = df["draw_down"].min()
        result['max_dd_percent'] = df["dd_percent"].min()
        result['total_pnl'] = df["net_pnl"].sum()
        result['daily_pnl'] = result['total_pnl'] / result['total_days']
        result['total_commission'] = df["commission"].sum()
        result['daily_commission'] = result['total_commission'] / result['total_days']
        # result['total_slippage'] = df["slippage"].sum()
        # result['daily_slippage'] = result['total_slippage'] / result['total_days']
        # result['total_turnover'] = df["turnover"].sum()
        # result['daily_turnover'] = result['total_turnover'] / result['total_days']
        result['total_count'] = df["count"].sum()
        result['daily_count'] = result['total_count'] / result['total_days']
        result['total_return'] = (result['end_balance'] / self.initial_capital - 1) * 100
        result['annual_return'] = result['total_return'] / result['total_days'] * 240
        result['daily_return'] = df["return"].mean() * 100
        result['return_std'] = df["return"].std() * 100
        return result


"""
 def __init__(self, api):
        self._api = api
        #: 币种
        self.currency = ""
        #: 昨日账户权益(不包含期权)
        self.pre_balance = float("nan")
        #: 静态权益 （静态权益 = 昨日结算的权益 + 今日入金 - 今日出金, 以服务器查询ctp后返回的金额为准）(不包含期权)
        self.static_balance = float("nan")
        #: 账户权益 （账户权益 = 动态权益 = 静态权益 + 平仓盈亏 + 持仓盈亏 - 手续费 + 权利金 + 期权市值）
        self.balance = float("nan")
        #: 可用资金（可用资金 = 账户权益 - 冻结保证金 - 保证金 - 冻结权利金 - 冻结手续费 - 期权市值）
        self.available = float("nan")
        #: 期货公司返回的balance（ctp_balance = 静态权益 + 平仓盈亏 + 持仓盈亏 - 手续费 + 权利金）
        self.ctp_balance = float("nan")
        #: 期货公司返回的available（ctp_available = ctp_balance - 保证金 - 冻结保证金 - 冻结手续费 - 冻结权利金）
        self.ctp_available = float("nan")
        #: 浮动盈亏
        self.float_profit = float("nan")
        #: 持仓盈亏
        self.position_profit = float("nan")
        #: 本交易日内平仓盈亏
        self.close_profit = float("nan")
        #: 冻结保证金
        self.frozen_margin = float("nan")
        #: 保证金占用
        self.margin = float("nan")
        #: 冻结手续费
        self.frozen_commission = float("nan")
        #: 本交易日内交纳的手续费
        self.commission = float("nan")
        #: 冻结权利金
        self.frozen_premium = float("nan")
        #: 本交易日内收入-交纳的权利金
        self.premium = float("nan")
        #: 本交易日内的入金金额
        self.deposit = float("nan")
        #: 本交易日内的出金金额
        self.withdraw = float("nan")
        #: 风险度（风险度 = 保证金 / 账户权益）
        self.risk_ratio = float("nan")
        #: 期权市值
        self.market_value = float("nan")

"""
