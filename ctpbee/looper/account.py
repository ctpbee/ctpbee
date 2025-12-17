"""
* 账户模块, 存储资金修改, 负责对外部的成交单进行成交撮合 并扣除手续费 等操作
* 需要向外提供API
    trading: 发起交易
    is_traded: 是否可以进行交易
    result: 回测结果
"""

import math
from collections import defaultdict
from copy import deepcopy
from datetime import datetime

from ctpbee.record import Recorder

try:
    from statistics import geometric_mean
except ImportError:

    def geometric_mean(xs):
        return math.exp(math.fsum(math.log(x) for x in xs) / len(xs))


import numpy as np
from pandas import DataFrame

from ctpbee.constant import (
    TradeData,
    OrderData,
    Offset,
    Direction,
    AccountData,
    EVENT_WARNING,
)
from ctpbee.data_handle.local_position import LocalPositionManager
import uuid


class AliasDayResult:
    """
    每天的结果
    """

    def __init__(self, **kwargs):
        """实例化进行调用"""
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
    此账户可以作为一个基本的账户类进行使用， 但是不能作为完整一个App.
    需要配合 Interface 提供实时价格和收盘价格进行使用.

    详细参见函数API
    """

    def __init__(self, interface, name=None):
        """
        核心账户
        Args

        """
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
        self.contracts = {}

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
        self.basic_info = None
        self.commission_ratio = defaultdict(dict)
        self.close_profit = {}
        self.turnover = 0
        self.pre_float = 0
        self.position_manager = LocalPositionManager(self)
        self.code_pnl = {}

    @property
    def margin(self):
        result = 0
        for x in self.position_manager.get_all_positions():
            result += (
                x["price"]
                * x["volume"]
                * self.get_size_from_map(x["local_symbol"])
                * self.get_margin_ration(x["local_symbol"])
            )
        return result

    @property
    def frozen_margin(self):
        return sum(list(self.long_frozen_margin.values())) + sum(
            list(self.short_frozen_margin.values())
        )

    def add_contract(self, contract):
        self.contracts[contract.local_symbol] = contract

    def get_contract(self, local_symbol):
        return self.contracts.get(local_symbol)

    @property
    def to_object(self) -> AccountData:
        return AccountData._create_class(
            dict(
                accountid=self.account_id,
                local_account_id=f"{self.account_id}.SIM",
                frozen=self.frozen,
                balance=self.balance,
            )
        )

    @property
    def frozen(self):
        return sum(self.frozen_fee.values())

    @property
    def float_pnl(self):
        result = 0
        for pos in self.position_manager.get_all_positions():
            if pos["direction"] == "long":
                result += (
                    (self.interface.price_mapping[pos["local_symbol"]] - pos["price"])
                    * pos["volume"]
                    * self.get_size_from_map(pos["local_symbol"])
                )
            else:
                result += (
                    (pos["price"] - self.interface.price_mapping[pos["local_symbol"]])
                    * pos["volume"]
                    * self.get_size_from_map(pos["local_symbol"])
                )
        return result

    def get_code_float_pnl(self):
        """获取每个品种当时的浮动盈亏"""
        result = {}
        for pos in self.position_manager.get_all_positions():
            if pos["direction"] == "long":
                pnl = (
                    (self.interface.price_mapping[pos["local_symbol"]] - pos["price"])
                    * pos["volume"]
                    * self.get_size_from_map(pos["local_symbol"])
                )
            else:
                pnl = (
                    (pos["price"] - self.interface.price_mapping[pos["local_symbol"]])
                    * pos["volume"]
                    * self.get_size_from_map(pos["local_symbol"])
                )
            if result.get(pos["local_symbol"]) is None:
                result[pos["local_symbol"]] = pnl
            else:
                result[pos["local_symbol"]] += pnl
        return result

    def get_code_pnl(self):
        pnl = {}
        pnl.update(self.code_pnl)
        for code, profit in self.get_code_float_pnl().items():
            if code in pnl:
                pnl[code] += profit
            else:
                pnl[code] = profit
        return pnl

    @property
    def balance(self) -> float:
        return self.available + self.margin

    @property
    def available(self):
        """可用资金 = 前日权益 + 平仓盈亏 + 浮动盈亏  - 手续费  - 冻结手续费 - 保证金"""
        return (
            self.pre_balance
            + sum(self.close_profit.values())
            + self.float_pnl
            - sum(self.fee.values())
            - self.frozen
            - self.margin
            - self.frozen_margin
        )

    @property
    def logger(self):
        return self.interface.logger

    def get_margin_ration(self, local_symbol):
        """获取保证金比率"""
        if self.basic_info is not None:
            if "." in local_symbol:
                local_symbol = local_symbol.split(".")[0]
            lc = "".join(filter(str.isalpha, local_symbol))
            return self.basic_info[lc][self.interface.date].margin
        else:
            return self.margin_ratio.get(local_symbol)

    def get_commission(self, order: OrderData or TradeData, close_today=False):
        """获取手续费比率"""
        if self.basic_info is not None:
            if "." in order.local_symbol:
                local_symbol = order.local_symbol.split(".")[0]
            else:
                local_symbol = order.local_symbol
            lc = "".join(filter(str.isalpha, local_symbol))
            n = self.basic_info[lc][self.interface.date]  # """ 切换到下一个交易日 """
            if n.commission_type == 2:
                if close_today:
                    """平今"""
                    return (
                        n.close_today_ratio
                        * order.price
                        * order.volume
                        * self.get_size_from_map(order.local_symbol)
                    )
                else:
                    return (
                        n.close_ratio
                        * order.price
                        * order.volume
                        * self.get_size_from_map(order.local_symbol)
                    )
            else:
                if close_today:
                    return n.close_today_ratio * order.volume
                else:
                    return n.close_ratio * order.volume
        else:
            if close_today:
                return (
                    self.commission_ratio.get(order.local_symbol)["close_today"]
                    * order.volume
                    * order.price
                    * self.get_size_from_map(order.local_symbol)
                )
            else:
                return (
                    self.commission_ratio.get(order.local_symbol)["close"]
                    * order.volume
                    * order.price
                    * self.get_size_from_map(order.local_symbol)
                )

    def get_size_from_map(self, local_symbol):
        """获取合约乘数"""
        if self.basic_info is not None:
            if "." in local_symbol:
                local_symbol = local_symbol.split(".")[0]
            lc = "".join(filter(str.isalpha, local_symbol))
            return self.basic_info[lc][self.interface.date].size
        else:
            return self.size_map.get(local_symbol)

    def get_commission_mapping(self):
        """获取每个合约的手续费信息"""

    def update_account_from_trade(self, data: TradeData or OrderData):
        """更新基础属性方法
        # 下单更新冻结的保证金
        # 成交更新持仓的保证金
        开仓手续费 /平仓手续费 平今手续费
        """
        if isinstance(data, TradeData):
            """成交属性"""
            if (
                data.order_id in self.frozen_fee.keys()
            ):  # 如果已经成交那么清除手续费冻结..
                self.frozen_fee.pop(data.order_id)
            try:
                if data.offset == Offset.CLOSETODAY:
                    fee = self.get_commission(data, close_today=True)
                else:
                    fee = self.get_commission(data)
            except KeyError:
                raise ValueError("请在对应品种设置合理的手续费")
            if self.fee.get(data.local_symbol) is None:
                self.fee[data.local_symbol] = fee
            else:
                self.fee[data.local_symbol] += fee

            if data.offset == Offset.OPEN:
                """开仓增加保证金"""
                self.count += data.volume
                if data.direction == Direction.LONG:
                    if (
                        data.order_id in self.long_frozen_margin.keys()
                    ):  # 如果成交, 那么清除多头的保证金冻结
                        self.long_frozen_margin.pop(data.order_id)
                else:
                    if (
                        data.order_id in self.short_frozen_margin.keys()
                    ):  # 如果成交, 那么清除空头的保证金冻结
                        self.short_frozen_margin.pop(data.order_id)
                self.turnover += data.volume * data.price
            else:
                if data.direction == Direction.LONG:
                    pos = self.position_manager.get_position_by_ld(
                        data.local_symbol, Direction.SHORT
                    )
                    try:
                        assert pos.volume >= data.volume
                    except Exception:
                        print(pos.volume, data.volume)
                        raise ValueError
                    close_profit = (
                        (pos.price - data.price)
                        * data.volume
                        * self.get_size_from_map(data.local_symbol)
                    )
                else:
                    pos = self.position_manager.get_position_by_ld(
                        data.local_symbol, Direction.LONG
                    )
                    assert pos.volume >= data.volume
                    close_profit = (
                        (data.price - pos.price)
                        * data.volume
                        * self.get_size_from_map(data.local_symbol)
                    )
                if self.close_profit.get(data.local_symbol) is None:
                    self.close_profit[data.local_symbol] = close_profit
                else:
                    self.close_profit[data.local_symbol] += close_profit

                if self.code_pnl.get(data.local_symbol) is None:
                    self.code_pnl[data.local_symbol] = close_profit
                else:
                    self.code_pnl[data.local_symbol] += close_profit

        else:
            raise TypeError(
                "错误的数据类型，期望成交单数据 TradeData 而不是 {}".format(type(data))
            )

    def update_account_from_order(self, order: OrderData):
        """
        从order里面更新订单信息
        """
        if order.offset == Offset.CLOSETODAY:
            self.frozen_fee[order.order_id] = self.get_commission(
                order, close_today=True
            )
        else:
            self.frozen_fee[order.order_id] = self.get_commission(order)
        if order.offset == Offset.OPEN:
            """开仓增加保证金占用"""
            if order.direction == Direction.LONG:
                self.long_frozen_margin[order.order_id] = (
                    self.get_margin_ration(order.local_symbol)
                    * order.price
                    * order.volume
                    * self.get_size_from_map(order.local_symbol)
                )
            else:
                self.short_frozen_margin[order.order_id] = (
                    self.get_margin_ration(order.local_symbol)
                    * order.price
                    * order.volume
                    * self.get_size_from_map(order.local_symbol)
                )

        self.position_manager.update_order(order)

    def pop_order(self, order: OrderData):
        if order.direction == Direction.LONG:
            if order.order_id in self.long_frozen_margin:
                self.long_frozen_margin.pop(order.order_id)
        if order.direction == Direction.SHORT:
            if order.order_id in self.short_frozen_margin:
                self.short_frozen_margin.pop(order.order_id)
        if order.order_id in self.frozen_fee:
            self.frozen_fee.pop(order.order_id)

    def clear_frozen(self):
        """撤单的时候应该要清除所有的单子 并同时清除保证金占用和手续费冻结"""
        # for order in list(self.interface.pending.values()):
        #     """ 结算后需要把未所有的单子撤掉 """
        #     order.status = Status.CANCELLED
        #     order.time.hour = 15
        #     order.time.minute = 1
        #     self.interface.on_event(EVENT_ORDER, order)

        self.interface.pending.clear()
        self.frozen_fee.clear()
        self.long_frozen_margin.clear()
        self.short_frozen_margin.clear()
        self.position_manager.clear_frozen()

    def reset_attr(self):
        """重新设置属性"""
        self.frozen_premium = 0
        self.count = 0
        self.turnover = 0
        self.close_profit.clear()
        self.code_pnl.clear()
        self.interface.today_volume = 0
        for x in self.fee.keys():
            self.fee[x] = 0

    def close_position_by_amount(self, amount, price_mapping):
        """通过指定金额来金额来平仓直到available为正"""
        self.logger.info(f"{self.date} 正在按照指定金额进行平仓: {amount}")
        for position in self.position_manager.get_all_positions():
            margin = (
                position["price"]
                * position["volume"]
                * self.get_size_from_map(position["local_symbol"])
                * self.get_margin_ration(position["local_symbol"])
            )
            if margin > amount:
                volume = amount / (
                    position["price"]
                    * self.get_size_from_map(position["local_symbol"])
                    * self.get_margin_ration(position["local_symbol"])
                )
                if volume % 1 != 0:
                    volume = int(volume) + 1
                else:
                    volume = int(volume)
                amount = 0
            else:
                volume = position["volume"]
                amount -= margin

            if position["direction"] == "long":
                self.interface.action.cover(
                    price_mapping[position["local_symbol"]], volume, position
                )
            else:
                self.interface.action.sell(
                    price_mapping[position["local_symbol"]], volume, position
                )
            if amount <= 0:
                self.logger.info("已经发完足够包含指定保证金的平仓单")
                break
        if amount > 0:
            raise ValueError(
                f"你爆仓了!!!!, 什么策略????? 你的保证金: {self.margin} 可用:{self.available}"
            )

    def is_traded(self, order: OrderData) -> bool:
        """当前账户是否足以支撑成交"""
        # 根据传入的单子判断当前的账户可用资金是否足以成交此单
        if order.offset != Offset.OPEN:
            """交易是否可平不足？"""
            poss = self.position_manager.get_position(order.local_symbol)
            if not poss:
                return False, "此合约上无仓位"

            if order.direction == Direction.LONG:
                if order.volume > poss.short_pos:
                    """仓位不足"""
                    return (
                        False,
                        f"平空头仓位不足 {order.local_symbol} volume: {order.volume}  持仓量: {poss.short_pos}",
                    )
                else:
                    return True, None
            else:
                if order.volume > poss.long_pos:
                    return (
                        False,
                        f"平多头仓位不足 {order.local_symbol} volume: {order.volume}  持仓量: {poss.long_pos}",
                    )
                else:
                    return True, None
        order_amount = (
            order.price
            * order.volume
            * self.get_size_from_map(order.local_symbol)
            * self.get_margin_ration(order.local_symbol)
        )
        if self.available < order_amount or self.available < 0:
            """可用不足"""
            return (
                False,
                f"资金可用不足, 当前可用: {self.available} 当前冻结保证金: {self.frozen_margin}",
            )
        return True, None

    def update_trade(self, trade: TradeData) -> None:
        """
        当前选择调用这个接口的时候就已经确保了这个单子是可以成交的，
        make sure it can be traded if you choose to call this method,
        :param trade:交易单子/trade
        :return:
        """
        self.update_account_from_trade(trade)
        self.position_manager.update_trade(trade=trade)
        tr = ""
        assert trade.volume > 0
        for pos in self.position_manager.get_all_positions():
            if pos["direction"] == "long":
                tr += f"{pos['local_symbol']}  long :{pos['volume']} \n"
            else:
                tr += f"{pos['local_symbol']}  short :{pos['volume']} \n"
        if isinstance(trade.time, datetime):
            self.interface.position_detail[trade.time.strftime("%Y-%m-%d %H:%M:%S")] = (
                tr
            )
        elif isinstance(trade.time, str):
            self.interface.position_detail[trade.time] = tr

    def settle(self, interface_date=None):
        """生成今天的交易数据， 同时更新前日数据 ，然后进行持仓结算"""
        if not self.date:
            date = interface_date
        else:
            date = self.date
        """ 结算撤掉所有单 归还冻结 """
        self.clear_frozen()
        if self.available < 0:
            self.logger.info("你的可用不足, 进行减仓")
            self.close_position_by_amount(
                abs(self.available), self.interface.price_mapping
            )

        p = AliasDayResult(
            **{
                "balance": self.balance,
                "margin": self.margin,
                "available": self.available,
                "short_balance": self.short_balance,
                "long_balance": self.long_balance,
                "date": date,
                "commission": sum([x for x in self.fee.values()]),
                "net_pnl": self.balance - self.pre_balance,
                "count": self.count,
                "turnover": self.turnover,
            }
        )
        code_pnl = self.get_code_pnl()
        self.interface.on_event(
            EVENT_WARNING,
            "Settlement:  "
            + str(date)
            + f" net: {round(self.balance, 2)}"
            + f" margin: {round(self.margin, 2)}"
            f" net_pnl: {self.balance - self.pre_balance} "
            f" close_profit: {round(sum(self.close_profit.values()), 2)}"
            f" float_pnl: {round(self.float_pnl, 2)}"
            f" code_pnl: {code_pnl}"
            f" fee:{round(sum(self.fee.values()), 2)} ",
        )
        self.pre_float = self.float_pnl
        self.daily_life[date] = deepcopy(p._to_dict())
        self.pre_balance = self.balance
        self.long_balance = self.balance
        self.short_balance = self.balance
        self.reset_attr()
        self.position_manager.covert_to_yesterday_holding(
            **self.interface.price_mapping
        )
        # 归还所有的冻结
        self.date = interface_date

    def via_aisle(self):
        self.position_manager.update_size_map(self.interface.params)
        if self.interface.date != self.date:
            self.date = self.interface.date
        else:
            pass

    def update_params(self, params: dict):
        """更新本地账户回测参数"""
        for i, v in params.items():
            if i == "initial_capital" and not self.init:
                self.pre_balance = v
                self.initial_capital = v
                self.long_balance = v
                self.short_balance = v
                self.init = True
                continue
            else:
                pass
            setattr(self, i, v)

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

            df["balance"].plot()
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
        df["return"] = (df["balance"] / df["balance"].shift(1) - 1).fillna(0)
        df["high_level"] = (
            df["balance"].rolling(min_periods=1, window=len(df), center=False).max()
        )
        df["draw_down"] = df["balance"] - df["high_level"]
        df["dd_percent"] = df["draw_down"] / df["high_level"] * 100
        result["initial_capital / 初始资金"] = self.initial_capital
        result["start_date / 起始日期"] = df.index[0]
        result["end_date / 结束日期"] = df.index[-1]
        result["total_days / 交易天数"] = len(df)
        result["profit_days / 盈利天数"] = len(df[df["net_pnl"] > 0])
        result["loss_days / 亏损天数"] = len(df[df["net_pnl"] < 0])
        result["end_balance / 结束资金"] = round(df["balance"].iloc[-1], 2)
        result["max_draw_down / 最大回撤"] = round(df["draw_down"].min(), 2)
        result["max_dd_percent / 最大回撤百分比"] = (
            str(round(df["dd_percent"].min(), 2)) + "%"
        )
        result["total_pnl / 总盈亏"] = round(df["net_pnl"].sum(), 2)
        result["daily_pnl / 平均日盈亏"] = round(
            result["total_pnl / 总盈亏"] / result["total_days / 交易天数"], 2
        )
        result["total_commission / 总手续费"] = round(df["commission"].sum(), 2)
        result["daily_commission / 日均手续费"] = round(
            result["total_commission / 总手续费"] / result["total_days / 交易天数"], 2
        )
        result["total_turnover / 开仓总资金"] = round(df["turnover"].sum(), 2)
        result["daily_turnover / 每日平均开仓资金"] = round(
            result["total_turnover / 开仓总资金"] / result["total_days / 交易天数"], 2
        )
        result["total_count / 总成交次数"] = df["count"].sum()
        result["daily_count / 日均成交次数"] = round(
            result["total_count / 总成交次数"] / result["total_days / 交易天数"], 2
        )
        result["total_return / 总收益率"] = (
            str(
                round(
                    (result["end_balance / 结束资金"] / self.initial_capital - 1) * 100,
                    2,
                )
            )
            + "%"
        )
        # 2021-04-29   somewheve
        # solution: fix to use function  to calculate shape
        #
        # by_year_return_std = df["return"].std() * np.sqrt(245)
        # df["return_x"] = df["return"] + 1
        # try:
        #     profit_ratio = geometric_mean(df["return_x"].to_numpy()) ** 245 - 1
        # except ValueError:
        #     print("boom 计算几何平均数存在负数, 本次回测作废")
        #     return {}
        # result['annual_return / 年化收益率'] = str(round(profit_ratio * 100, 2)) + "%"
        # result['return_std / 年化标准差'] = str(round(by_year_return_std * 100, 2)) + "%"
        # result['volatility / 波动率'] = str(round(df["return"].std() * 100, 2)) + "%"
        # if by_year_return_std != 0:
        #     result['sharpe / 年化夏普率'] = (profit_ratio - 2.5 / 100) / by_year_return_std
        # else:
        #     result['sharpe / 年化夏普率'] = "计算出错"
        (
            result["annual_return / 年化收益率"],
            result["return_std / 年化标准差"],
            result["volatility / 波动率"],
            result["sharpe / 年化夏普率"],
        ) = shape_cal(df["return"])

        return result


def shape_cal(rt):
    """
    根据收益率计算
        年化收益率,

    """
    by_year_return_std = rt.std() * np.sqrt(245)
    rtx = rt + 1
    try:
        profit_ratio = geometric_mean(rtx.to_numpy()) ** 245 - 1
    except ValueError:
        print("boom 计算几何平均数存在负数, 本次计算出错 作废")
        return 0, 0, 0, 0
    annual_return = str(round(profit_ratio * 100, 2)) + "%"
    volatility = str(round(rt.std() * 100, 2)) + "%"
    return_std = str(round(by_year_return_std * 100, 2)) + "%"
    if by_year_return_std != 0:
        shape = (profit_ratio - 2.5 / 100) / by_year_return_std
    else:
        shape = "计算出错"
    return annual_return, return_std, volatility, shape
