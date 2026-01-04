from ctpbee.constant import TickData, BarData
from ctpbee import CtpbeeApi
from ctpbee.indicator.indicator import macd
from ctpbee.log import VLogger


class MACDStrategy(CtpbeeApi):
    """基于MACD指标的策略"""

    fast_period = 12
    slow_period = 26
    signal_period = 9
    logger = VLogger

    def __init__(self, name: str, code):
        super().__init__(
            name,
        )
        self.instrument_set = set([code])
        self.length = self.slow_period + self.signal_period
        self.close = []
        self.pos = 0
        self.name = name
        self.logger.info(
            f"MACD策略初始化 - 合约: {code}, 快速周期: {self.fast_period}, 慢速周期: {self.slow_period}, 信号周期: {self.signal_period}",
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

        # 计算MACD
        macd_line, signal_line, histo = macd(
            self.close, self.fast_period, self.slow_period, self.signal_period
        )

        # 计算当前和前一根MACD值
        current_macd = macd_line[-1]
        previous_macd = macd_line[-2]
        current_signal = signal_line[-1]
        previous_signal = signal_line[-2]
        current_histo = histo[-1]

        self.logger.debug(
            f"MACD计算 - MACD线: 当前 {current_macd:.2f}, 前值 {previous_macd:.2f}; 信号线: 当前 {current_signal:.2f}, 前值 {previous_signal:.2f}; 柱状图: 当前 {current_histo:.2f}",
            owner=self.name,
        )

        # 金叉买入，死叉卖出
        buy_signal = current_macd > current_signal and previous_macd <= previous_signal
        sell_signal = current_macd < current_signal and previous_macd >= previous_signal

        if buy_signal:
            self.logger.info(
                f"买入信号 - MACD金叉形成: MACD线 {current_macd:.2f} 上穿信号线 {current_signal:.2f}, 柱状图 {current_histo:.2f}",
                owner=self.name,
            )
        if sell_signal:
            self.logger.info(
                f"卖出信号 - MACD死叉形成: MACD线 {current_macd:.2f} 下穿信号线 {current_signal:.2f}, 柱状图 {current_histo:.2f}",
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
