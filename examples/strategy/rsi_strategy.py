from ctpbee.constant import TickData, BarData
from ctpbee import CtpbeeApi
from ctpbee.indicator.indicator import rsi
from ctpbee.log import VLogger


class RSIStrategy(CtpbeeApi):
    """基于相对强弱指标(RSI)的超买超卖策略"""

    rsi_period = 14
    over_bought = 70
    over_sold = 30
    logger = VLogger

    def __init__(self, name: str, code):
        super().__init__(
            name,
        )
        self.instrument_set = set([code])
        self.length = self.rsi_period
        self.close = []
        self.pos = 0
        self.name = name
        self.init = False
        self.logger.info(
            f"RSI策略初始化 - 合约: {code}, 周期: {self.rsi_period}, 超买阈值: {self.over_bought}, 超卖阈值: {self.over_sold}",
            owner=self.name,
        )

    def on_tick(self, tick: TickData) -> None:
        pass

    def on_bar(self, bar: BarData):
        self.logger.debug(
            f"收到K线数据 - {bar.local_symbol} {bar.datetime.strftime('%Y-%m-%d %H:%M:%S')} 收盘价: {bar.close_price}",
            owner=self.name,
        )

        self.close.append(bar.close_price)
        if len(self.close) <= self.length * 2:
            self.logger.debug(
                f"数据不足，需要至少 {self.length * 2} 根K线，当前 {len(self.close)} 根",
                owner=self.name,
            )
            return

        # 计算RSI
        rsi_value = rsi(self.close, self.rsi_period)
        current_rsi = rsi_value[-1]
        previous_rsi = rsi_value[-2]

        self.logger.debug(
            f"RSI计算 - 当前值: {current_rsi:.2f}, 前值: {previous_rsi:.2f}, 超买: {self.over_bought}, 超卖: {self.over_sold}",
            owner=self.name,
        )

        # 超卖买入，超买卖出
        buy_signal = current_rsi > self.over_sold and previous_rsi <= self.over_sold
        sell_signal = (
            current_rsi < self.over_bought and previous_rsi >= self.over_bought
        )

        if buy_signal:
            self.logger.info(
                f"买入信号 - RSI从 {previous_rsi:.2f} 上穿超卖阈值 {self.over_sold}，当前值 {current_rsi:.2f}",
                owner=self.name,
            )
        if sell_signal:
            self.logger.info(
                f"卖出信号 - RSI从 {previous_rsi:.2f} 下穿超买阈值 {self.over_bought}，当前值 {current_rsi:.2f}",
                owner=self.name,
            )

        # 交易逻辑
        if self.pos == 1 and sell_signal:
            self.logger.success(
                f"平仓卖出 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 0",
                owner=self.name,
            )
            self.action.buy_close(bar.close_price, 1, bar)
            self.pos = 0
        elif self.pos == -1 and buy_signal:
            self.logger.success(
                f"平仓买入 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 0",
                owner=self.name,
            )
            self.action.sell_close(bar.close_price, 1, bar)
            self.pos = 0
        elif buy_signal and self.pos == 0:
            self.logger.success(
                f"开仓买入 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 1",
                owner=self.name,
            )
            self.pos = 1
            self.action.buy_open(bar.close_price, 1, bar)
        elif sell_signal and self.pos == 0:
            self.logger.success(
                f"开仓卖出 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> -1",
                owner=self.name,
            )
            self.pos = -1
            self.action.sell_open(bar.close_price, 1, bar)
