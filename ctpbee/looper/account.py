"""
* 账户模块, 存储资金修改, 负责对外部的成交单进行成交撮合 并扣除手续费 等操作
* 需要向外提供API
    trading: 发起交易
    is_traded: 是否可以进行交易
    result: 回测结果
"""

from collections import defaultdict
from copy import deepcopy
import math

try:
    from statistics import geometric_mean
except ImportError:
    def geometric_mean(xs):
        return math.exp(math.fsum(math.log(x) for x in xs) / len(xs))

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
        self.size_map = {}
        # 每日下单限制
        self.daily_limit = 20
        self.pre_balance = 0
        # 账户当前的日期
        self.date = None
        self.count_statistics = 0
        # 初始资金
        self.initial_capital = 0
        # 账户权益
        # 保证金占用
        self.long_margin = 0
        self.short_margin = 0
        # 冻结的保证金
        self.long_frozen_margin = {}
        self.short_frozen_margin = {}
        # 冻结的手续费
        self.frozen_fee = {}
        # 多头净值
        self.long_balance = 0
        # 空头净值
        self.short_balance = 0
        self.frozen_premium = 0
        self.count = 0
        """ 
        fee应该是一个 {
            ag2012.SHFE: 200.1
        }
        """
        self.fee = {}
        self.init_position_manager_flag = False
        self.init = False
        self.position_manager = None
        self.margin_ratio = {}
        # commission_ratio 应该为{"ag2012.SHFE": {"close_today": 0.005, "close":0.005 }
        self.commission_ratio = defaultdict(dict)
        self.close_profit = {}
        self.turnover = 0

    @property
    def margin(self):
        result = 0
        for x in self.position_manager.get_all_positions():
            result += x["price"] * x["volume"] * self.size_map.get(
                x["local_symbol"]) * self.margin_ratio.get(
                x["local_symbol"])
        return result

    @property
    def frozen_margin(self):
        return sum(list(self.long_frozen_margin.values())) + sum(list(self.short_frozen_margin.values()))

    @property
    def to_object(self) -> AccountData:
        return AccountData._create_class(dict(accountid=self.account_id,
                                              local_account_id=f"{self.account_id}.SIM",
                                              frozen=self.frozen,
                                              balance=self.balance,
                                              ))

    @property
    def pnl_of_every_symbol(self):
        result = {}
        for key, value in self.fee.items():
            result[key] = -value
        for key, value in self.close_profit.items():
            if key in result.keys():
                result[key] += value
            else:
                result[key] = value
        for pos in self.position_manager.get_all_positions():
            if pos['direction'] == "long":
                pnl = (self.interface.price_mapping[pos["local_symbol"]] - pos["price"]) * pos[
                    "volume"] * self.size_map.get(
                    pos["local_symbol"])
            else:
                pnl = (pos["price"] - self.interface.price_mapping[pos["local_symbol"]]) * pos[
                    "volume"] * self.size_map.get(
                    pos["local_symbol"])
            if pos["local_symbol"] in result.keys():
                result[pos["local_symbol"]] += pnl
            else:
                result[pos["local_symbol"]] = pnl
        return result

    @property
    def frozen(self):
        return sum(self.frozen_fee.values())

    @property
    def float_pnl(self):
        result = 0
        for pos in self.position_manager.get_all_positions():
            if pos['direction'] == "long":
                result += (self.interface.price_mapping[pos["local_symbol"]] - pos["price"]) * pos[
                    "volume"] * self.size_map.get(
                    pos["local_symbol"])
            else:
                result += (pos["price"] - self.interface.price_mapping[pos["local_symbol"]]) * pos[
                    "volume"] * self.size_map.get(
                    pos["local_symbol"])
        return result

    @property
    def balance(self) -> float:
        return self.available + self.margin

    @property
    def available(self):
        """ 可用资金 = 前日权益 + 平仓盈亏 + 浮动盈亏  - 手续费  - 冻结手续费 - 保证金 """
        return self.pre_balance + sum(self.close_profit.values()) + self.float_pnl - sum(
            self.fee.values()) - self.frozen - self.margin - self.frozen_margin

    @property
    def logger(self):
        return self.interface.logger

    def update_account_from_trade(self, data: TradeData or OrderData):
        """ 更新基础属性方法
        # 下单更新冻结的保证金
        # 成交更新持仓的保证金
        开仓手续费 /平仓手续费 平今手续费
        """
        if isinstance(data, TradeData):
            """ 成交属性 """
            if data.order_id in self.frozen_fee.keys():  # 如果已经成交那么清除手续费冻结..
                self.frozen_fee.pop(data.order_id)
            try:
                if data.offset == Offset.CLOSETODAY:
                    ratio = self.commission_ratio.get(data.local_symbol)["close_today"]
                else:
                    ratio = self.commission_ratio.get(data.local_symbol)["close"]
            except KeyError:
                raise ValueError("请在对应品种设置合理的手续费")
            if self.fee.get(data.local_symbol) is None:
                self.fee[data.local_symbol] = data.price * data.volume * ratio * self.size_map.get(data.local_symbol)
            else:
                self.fee[data.local_symbol] += data.price * data.volume * ratio * self.size_map.get(data.local_symbol)
            """ 余额减去实际发生手续费用 """
            if self.pnl_of_every_symbol.get(data.local_symbol) is None:
                self.pnl_of_every_symbol[data.local_symbol] = data.price * data.volume * ratio * self.size_map.get(
                    data.local_symbol)
            else:
                self.pnl_of_every_symbol[data.local_symbol] += data.price * data.volume * ratio * self.size_map.get(
                    data.local_symbol)

            if data.offset == Offset.OPEN:
                """  开仓增加保证金 """
                self.count += data.volume
                if data.direction == Direction.LONG:
                    if data.order_id in self.long_frozen_margin.keys():  # 如果成交, 那么清除多头的保证金冻结
                        self.long_frozen_margin.pop(data.order_id)
                else:
                    if data.order_id in self.short_frozen_margin.keys():  # 如果成交, 那么清除空头的保证金冻结
                        self.short_frozen_margin.pop(data.order_id)
                self.turnover += data.volume * data.price
            else:

                """ 计算平仓产生的盈亏"""

                """ 注意此处需要判断是否是当天持仓当天平还是当天持仓隔日平
                1. 因为每天都进行了自动结算机制,账户都用了收盘价成为仓位的一个成本，所以账户在平仓的时候计算盈亏需要计算他是否是当天平仓，
                那这个时候需要判断这个仓位是否已经过了多少天
                2. 因此当日某个品种开仓的一个成本还有手数需要被记录下来
                如果一个场景下存在螺纹钢昨日开仓3手,收盘价p1.今日开仓3手开仓价 p2, 平3手平仓价p3,再开3手开仓价p4 ,今日收盘价p5
                那么今日单个品种的盈亏按照优先平今或者优先平昨天规则分别进行计算
                优先平今
                pnl = (p3 - p2) * 3 + (p5 - p4) * 3 + (p5 - p1) * 3 +  ]       3p3  + 6p5 - 3p4 - 3p1 -3p2
                优先平昨
                pnl = (p3 - p1) * 3 + (p5 - p2) * 3 + (p5 - p4) * 3 + 手续费    6p5 + 3p3 -3p1 - 3p2 + 3p4
                """
                if data.direction == Direction.LONG:
                    pos = self.position_manager.get_position_by_ld(data.local_symbol, Direction.SHORT)
                    assert pos.volume >= data.volume
                    close_profit = (pos.price - data.price) * data.volume * self.size_map.get(data.local_symbol)

                else:
                    pos = self.position_manager.get_position_by_ld(data.local_symbol, Direction.LONG)
                    assert pos.volume >= data.volume
                    close_profit = (data.price - pos.price) * data.volume * self.size_map.get(data.local_symbol)
                if self.close_profit.get(data.local_symbol) is None:
                    self.close_profit[data.local_symbol] = close_profit
                else:
                    self.close_profit[data.local_symbol] += close_profit

        else:
            raise TypeError("错误的数据类型，期望成交单数据 TradeData 而不是 {}".format(type(data)))

    def update_account_from_order(self, order: OrderData):
        """
        从order里面更新订单信息
        """
        if order.offset == Offset.CLOSETODAY:
            self.frozen_fee[order.order_id] = self.commission_ratio.get(
                order.local_symbol)["close_today"] * order.price * order.volume * self.size_map.get(order.local_symbol)
        else:
            self.frozen_fee[order.order_id] = self.commission_ratio.get(
                order.local_symbol)["close"] * order.price * order.volume * self.size_map.get(order.local_symbol)
        if order.offset == Offset.OPEN:
            """ 开仓增加保证金占用 """
            if order.direction == Direction.LONG:
                self.long_frozen_margin[order.order_id] = self.margin_ratio.get(
                    order.local_symbol) * order.price * order.volume * self.size_map.get(order.local_symbol)
            else:
                self.short_frozen_margin[order.order_id] = self.margin_ratio.get(
                    order.local_symbol) * order.price * order.volume * self.size_map.get(order.local_symbol)

        self.position_manager.update_order(order)

    def pop_order(self, order: OrderData):
        if order.direction == Direction.LONG:
            self.long_frozen_margin.pop(order.order_id)
        if order.direction == Direction.SHORT:
            self.short_frozen_margin.pop(order.order_id)
        self.frozen_fee.pop(order.order_id)

    def clear_frozen(self):
        """ 撤单的时候应该要清除所有的单子 并同时清除保证金占用和手续费冻结 """
        self.interface.pending.clear()
        self.frozen_fee.clear()
        self.long_frozen_margin.clear()
        self.short_frozen_margin.clear()

    def reset_attr(self):
        self.frozen_premium = 0
        self.count = 0
        self.turnover = 0
        self.pnl_of_every_symbol.clear()
        self.close_profit.clear()
        self.interface.today_volume = 0
        for x in self.fee.keys():
            self.fee[x] = 0

    @property
    def position_amount(self):
        return sum([self.interface.price_mapping.get(x['local_symbol']) * x["volume"] * self.size_map.get(
            x["local_symbol"]) * self.margin_ratio.get(x["local_symbol"]) for x in
                    self.position_manager.get_all_positions()])

    def is_traded(self, order: OrderData) -> bool:
        """ 当前账户是否足以支撑成交 """
        # 根据传入的单子判断当前的账户可用资金是否足以成交此单

        if order.offset != Offset.OPEN:
            """ 交易是否可平不足？ """
            if order.direction == Direction.LONG:
                pos = self.position_manager.get_position_by_ld(order.local_symbol, Direction.SHORT)
                if not pos or order.volume > pos.volume:
                    """ 仓位不足 """
                    return False
            else:
                pos = self.position_manager.get_position_by_ld(order.local_symbol, Direction.LONG)
                if not pos or order.volume > pos.volume:
                    return False
        order_amount = order.price * order.volume * self.size_map.get(
            order.local_symbol) * self.margin_ratio.get(
            order.local_symbol) + order.price * order.volume
        if self.available < order_amount or self.available < 0:
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
        self.update_account_from_trade(trade)
        self.position_manager.update_trade(trade=trade)

    def settle(self, interface_date=None):
        """ 生成今天的交易数据， 同时更新前日数据 ，然后进行持仓结算 """
        if not self.date:
            date = interface_date
        else:
            date = self.date
        """ 结算撤掉所有单 归还冻结 """
        self.clear_frozen()
        p = AliasDayResult(
            **{"balance": self.balance,
               "margin": self.margin,
               "available": self.available,
               "short_balance": self.short_balance,
               "ery": self.pnl_of_every_symbol,
               "long_balance": self.long_balance,
               "date": date,
               "commission": sum([x for x in self.fee.values()]),
               "net_pnl": self.balance - self.pre_balance,
               "count": self.count,
               "turnover": self.turnover
               })
        self.daily_life[date] = deepcopy(p._to_dict())
        self.pre_balance = self.balance
        self.long_balance = self.balance
        self.short_balance = self.balance
        self.reset_attr()
        self.position_manager.covert_to_yesterday_holding()

        # 归还所有的冻结
        self.date = interface_date

    def via_aisle(self):
        self.position_manager.update_size_map(self.interface.params)
        if self.interface.date != self.date:
            self.date = self.interface.date
        else:
            pass

    def update_params(self, params: dict):
        """ 更新本地账户回测参数 """
        for i, v in params.items():
            if i == "initial_capital" and not self.init:
                # self.balance = v
                self.pre_balance = v
                self.initial_capital = v
                self.long_balance = v
                self.short_balance = v
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
        try:
            df = DataFrame.from_dict(result).set_index("date")
        except KeyError:
            print("-------------------------------------------------")
            print("|          好像没有结算数据哦!                    |")
            print("-------------------------------------------------")
            return {}
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
        result['initial_capital / 初始资金'] = self.initial_capital
        result['start_date / 起始日期'] = df.index[0]
        result['end_date / 结束日期'] = df.index[-1]
        result['total_days / 交易天数'] = len(df)
        result['profit_days / 盈利天数'] = len(df[df["net_pnl"] > 0])
        result['loss_days / 亏损天数'] = len(df[df["net_pnl"] < 0])
        result['end_balance / 结束资金'] = round(df["balance"].iloc[-1], 2)
        result['max_draw_down / 最大回撤'] = round(df["draw_down"].min(), 2)
        result['max_dd_percent / 最大回撤百分比'] = str(round(df["dd_percent"].min(), 2)) + "%"
        result['total_pnl / 总盈亏'] = round(df["net_pnl"].sum(), 2)
        result['daily_pnl / 平均日盈亏'] = round(result['total_pnl / 总盈亏'] / result['total_days / 交易天数'], 2)
        result['total_commission / 总手续费'] = round(df["commission"].sum(), 2)
        result['daily_commission / 日均手续费'] = round(result['total_commission / 总手续费'] / result['total_days / 交易天数'], 2)
        # result['total_slippage'] = df["slippage"].sum()
        # result['daily_slippage'] = result['total_slippage'] / result['total_days']
        result['total_turnover / 开仓总资金'] = round(df["turnover"].sum(), 2)
        result['daily_turnover / 每日平均开仓资金'] = round(result['total_turnover / 开仓总资金'] / result['total_days / 交易天数'], 2)
        result['total_count / 总成交次数'] = df["count"].sum()
        result['daily_count / 日均成交次数'] = round(result['total_count / 总成交次数'] / result['total_days / 交易天数'], 2)
        result['total_return / 总收益率'] = str(
            round((result['end_balance / 结束资金'] / self.initial_capital - 1) * 100, 2)) + "%"
        by_year_return_std = df["return"].std() * np.sqrt(245)
        df["return_x"] = df["return"] + 1
        profit_ratio = geometric_mean(df["return_x"].to_numpy()) ** 245 - 1
        result['annual_return / 年化收益率'] = str(round(profit_ratio * 100, 2)) + "%"
        result['return_std / 年化标准差'] = str(round(by_year_return_std * 100, 2)) + "%"
        result['volatility / 波动率'] = str(round(df["return"].std() * 100, 2)) + "%"
        if by_year_return_std != 0:
            result['sharpe / 年化夏普率'] = (profit_ratio - 2.5 / 100) / by_year_return_std
        else:
            result['sharpe / 年化夏普率'] = "计算出错"
        return result
