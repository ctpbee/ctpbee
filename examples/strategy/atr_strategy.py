from ctpbee.constant import TickData, BarData
from ctpbee import CtpbeeApi
from ctpbee.indicator.indicator import atr, sma
from ctpbee.log import VLogger


class ATRStrategy(CtpbeeApi):
    """基于平均真实波动幅度(ATR)的策略，结合均线和ATR止损"""

    atr_period = 14
    sma_period = 20
    stop_loss_multiplier = 2  # 止损倍数
    take_profit_multiplier = 3  # 止盈倍数
    logger = VLogger

    def __init__(self, name: str, code):
        super().__init__(
            name,
        )
        self.instrument_set = set([code])
        self.length = max(self.atr_period, self.sma_period)
        self.close = []
        self.high = []
        self.low = []
        self.pos = 0
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.init = False
        self.name = name
        self.logger.info(
            f"ATR策略初始化 - 合约: {code}, ATR周期: {self.atr_period}, SMA周期: {self.sma_period}, 止损倍数: {self.stop_loss_multiplier}, 止盈倍数: {self.take_profit_multiplier}",
            owner=self.name,
        )

    def code(self):
        return list(self.instrument_set)[0]

    def on_tick(self, tick: TickData) -> None:
        pass

    def on_bar(self, bar: BarData):
        if bar is None or not self.init:
            return
        self.logger.debug(
            f"收到K线数据 - {bar.local_symbol} {bar.datetime.strftime('%Y-%m-%d %H:%M:%S')} 最高价: {bar.high_price}, 最低价: {bar.low_price}, 收盘价: {bar.close_price}",
            owner=self.name,
        )

        self.close.append(bar.close_price)
        self.high.append(bar.high_price)
        self.low.append(bar.low_price)

        if len(self.close) <= self.length * 2:
            self.logger.debug(
                f"数据不足，需要至少 {self.length * 2} 根K线，当前 {len(self.close)} 根",
                owner=self.name,
            )
            return

        # 计算SMA和ATR
        current_sma = sma(self.close, self.sma_period)[-1]
        current_atr = atr(self.high, self.low, self.close, self.atr_period)[-1]
        recent_atr = atr(self.high, self.low, self.close, self.atr_period)[-10:]
        max_recent_atr = max(recent_atr)

        # 趋势判断：价格在SMA上方为上涨趋势，下方为下跌趋势
        trend_up = bar.close_price > current_sma
        trend_down = bar.close_price < current_sma

        self.logger.debug(
            f"指标计算 - SMA: {current_sma:.2f}, ATR: {current_atr:.2f}, 最近10日最大ATR: {max_recent_atr:.2f}, 趋势: {'上涨' if trend_up else '下跌' if trend_down else '横盘'}",
            owner=self.name,
        )

        # 交易逻辑
        if self.pos == 0:
            # 买入信号：上涨趋势且ATR较小（波动性低）
            if trend_up and current_atr < max_recent_atr:
                self.logger.info(
                    f"买入信号 - 上涨趋势且波动性降低: SMA {current_sma:.2f}, 价格 {bar.close_price:.2f}, ATR {current_atr:.2f} < 最近10日最大ATR {max_recent_atr:.2f}",
                    owner=self.name,
                )
                self.pos = 1
                self.entry_price = bar.close_price
                self.stop_loss = (
                    self.entry_price - current_atr * self.stop_loss_multiplier
                )
                self.take_profit = (
                    self.entry_price + current_atr * self.take_profit_multiplier
                )
                self.logger.success(
                    f"开仓买入 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 止损: {self.stop_loss:.2f}, 止盈: {self.take_profit:.2f}, 当前仓位: {self.pos}",
                    owner=self.name,
                )
                self.action.buy_open(bar.close_price, 1, bar)
            # 卖出信号：下跌趋势且ATR较小（波动性低）
            elif trend_down and current_atr < max_recent_atr:
                self.logger.info(
                    f"卖出信号 - 下跌趋势且波动性降低: SMA {current_sma:.2f}, 价格 {bar.close_price:.2f}, ATR {current_atr:.2f} < 最近10日最大ATR {max_recent_atr:.2f}",
                    owner=self.name,
                )
                self.pos = -1
                self.entry_price = bar.close_price
                self.stop_loss = (
                    self.entry_price + current_atr * self.stop_loss_multiplier
                )
                self.take_profit = (
                    self.entry_price - current_atr * self.take_profit_multiplier
                )
                self.logger.success(
                    f"开仓卖出 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 止损: {self.stop_loss:.2f}, 止盈: {self.take_profit:.2f}, 当前仓位: {self.pos}",
                    owner=self.name,
                )
                self.action.sell_open(bar.close_price, 1, bar)
        elif self.pos == 1:
            # 多头止损和止盈
            if bar.low_price <= self.stop_loss:
                self.logger.info(
                    f"多头止损触发 - 合约: {bar.local_symbol}, 当前最低价: {bar.low_price:.2f} <= 止损价: {self.stop_loss:.2f}",
                    owner=self.name,
                )
                self.logger.success(
                    f"平仓卖出 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 0",
                    owner=self.name,
                )
                self.action.buy_close(bar.close_price, 1, bar)
                self.pos = 0
            elif bar.high_price >= self.take_profit:
                self.logger.info(
                    f"多头止盈触发 - 合约: {bar.local_symbol}, 当前最高价: {bar.high_price:.2f} >= 止盈价: {self.take_profit:.2f}",
                    owner=self.name,
                )
                self.logger.success(
                    f"平仓卖出 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 0",
                    owner=self.name,
                )
                self.action.buy_close(bar.close_price, 1, bar)
                self.pos = 0
        elif self.pos == -1:
            # 空头止损和止盈
            if bar.high_price >= self.stop_loss:
                self.logger.info(
                    f"空头止损触发 - 合约: {bar.local_symbol}, 当前最高价: {bar.high_price:.2f} >= 止损价: {self.stop_loss:.2f}",
                    owner=self.name,
                )
                self.logger.success(
                    f"平仓买入 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 0",
                    owner=self.name,
                )
                self.action.sell_close(bar.close_price, 1, bar)
                self.pos = 0
            elif bar.low_price <= self.take_profit:
                self.logger.info(
                    f"空头止盈触发 - 合约: {bar.local_symbol}, 当前最低价: {bar.low_price:.2f} <= 止盈价: {self.take_profit:.2f}",
                    owner=self.name,
                )
                self.logger.success(
                    f"平仓买入 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 0",
                    owner=self.name,
                )
                self.action.sell_close(bar.close_price, 1, bar)
                self.pos = 0
