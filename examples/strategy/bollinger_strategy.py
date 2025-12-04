from ctpbee.constant import TickData, BarData
from ctpbee import CtpbeeApi
from ctpbee.indicator.indicator import bollinger_bands
from ctpbee.log import VLogger


class BollingerStrategy(CtpbeeApi):
    """基于布林带指标的策略"""
    window_size = 20
    num_of_std = 2
    logger = VLogger
    
    def __init__(self, name: str, code):
        super().__init__(name, )
        self.instrument_set = set([code])
        self.length = self.window_size
        self.close = []
        self.name = name 
        self.pos = 0
        self.logger.info(f"布林带策略初始化 - 合约: {code}, 窗口大小: {self.window_size}, 标准差倍数: {self.num_of_std}", owner=self.name)

    def on_tick(self, tick: TickData) -> None:
        pass

    def on_bar(self, bar: BarData):
        self.logger.debug(f"收到K线数据 - {bar.local_symbol} {bar.datetime.strftime('%Y-%m-%d %H:%M:%S')} 收盘价: {bar.close_price}", owner=self.name)
        
        self.close.append(bar.close_price)
        if len(self.close) <= self.length * 2:
            self.logger.debug(f"数据不足，需要至少 {self.length * 2} 根K线，当前 {len(self.close)} 根", owner=self.name)
            return
        
        # 计算布林带
        upper_band, middle_band, lower_band = bollinger_bands(self.close, self.window_size, self.num_of_std)
        
        # 计算当前和前一根布林带值
        current_upper = upper_band[-1]
        current_middle = middle_band[-1]
        current_lower = lower_band[-1]
        previous_upper = upper_band[-2]
        previous_middle = middle_band[-2]
        previous_lower = lower_band[-2]
        
        self.logger.debug(f"布林带计算 - 上轨: {current_upper:.2f}, 中轨: {current_middle:.2f}, 下轨: {current_lower:.2f}", owner=self.name)
        
        # 价格突破下带买入，突破上带卖出
        buy_signal = bar.close_price > current_lower and self.close[-2] <= previous_lower
        sell_signal = bar.close_price < current_upper and self.close[-2] >= previous_upper
        
        if buy_signal:
            self.logger.info(f"买入信号 - 价格突破下轨: 当前价格 {bar.close_price:.2f} > 下轨 {current_lower:.2f}, 前值 {self.close[-2]:.2f} <= 前下轨 {previous_lower:.2f}", owner=self.name)
        if sell_signal:
            self.logger.info(f"卖出信号 - 价格突破上轨: 当前价格 {bar.close_price:.2f} < 上轨 {current_upper:.2f}, 前值 {self.close[-2]:.2f} >= 前上轨 {previous_upper:.2f}", owner=self.name)
        
        # 交易逻辑
        if self.pos == 1 and sell_signal:
            self.logger.success(f"平仓卖出 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 0", owner=self.name)
            self.action.buy_close(bar.close_price, 1, bar)
            self.pos = 0
        elif self.pos == -1 and buy_signal:
            self.logger.success(f"平仓买入 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 0", owner=self.name)
            self.action.sell_close(bar.close_price, 1, bar)
            self.pos = 0
        elif buy_signal and self.pos == 0:
            self.logger.success(f"开仓买入 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 1", owner=self.name)
            self.pos = 1
            self.action.buy_open(bar.close_price, 1, bar)
        elif sell_signal and self.pos == 0:
            self.logger.success(f"开仓卖出 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> -1", owner=self.name)
            self.pos = -1
            self.action.sell_open(bar.close_price, 1, bar)
