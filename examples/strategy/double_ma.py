from ctpbee.constant import TickData, BarData
from ctpbee import CtpbeeApi
from ctpbee.indicator.indicator import ma
from ctpbee.log import VLogger


class DoubleMa(CtpbeeApi):
    fast_period = 2
    slow_period = 10
    logger = VLogger

    def __init__(self, name: str, code):
        super().__init__(name, )
        self.instrument_set = set([code])
        self.length = self.slow_period
        self.close = []
        self.pos = 0
        self.name = name 
        self.logger.info(f"双均线策略初始化 - 合约: {code}, 快速周期: {self.fast_period}, 慢速周期: {self.slow_period}", owner=self.name)

    def on_tick(self, tick: TickData) -> None:
        pass

    def on_bar(self, bar: BarData):
        self.logger.debug(f"收到K线数据 - {bar.local_symbol} {bar.datetime.strftime('%Y-%m-%d %H:%M:%S')} 收盘价: {bar.close_price}", owner=self.name)
        
        self.close.append(bar.close_price)
        if len(self.close) <= self.length * 2:
            self.logger.debug(f"数据不足，需要至少 {self.length * 2} 根K线，当前 {len(self.close)} 根", owner=self.name)
            return
        
        close_array = self.close[-self.length * 2:]
        fast_ma = ma(close_array, self.fast_period)
        slow_ma = ma(close_array, self.slow_period)
        
        # 计算当前和前一根MA值
        current_fast = fast_ma[-1]
        previous_fast = fast_ma[-2]
        current_slow = slow_ma[-1]
        previous_slow = slow_ma[-2]
        
        self.logger.debug(f"MA计算 - 快速MA: 当前 {current_fast:.2f}, 前值 {previous_fast:.2f}; 慢速MA: 当前 {current_slow:.2f}, 前值 {previous_slow:.2f}", owner=self.name)
        
        buy = current_fast > current_slow and previous_fast < previous_slow
        sell = current_fast < current_slow and previous_fast > previous_slow
        
        if buy:
            self.logger.info(f"买入信号 - 金叉形成: 快速MA {current_fast:.2f} 上穿慢速MA {current_slow:.2f}", owner=self.name)
        if sell:
            self.logger.info(f"卖出信号 - 死叉形成: 快速MA {current_fast:.2f} 下穿慢速MA {current_slow:.2f}", owner=self.name)
        
        # 交易逻辑
        if self.pos == 1 and sell:
            self.logger.success(f"平仓卖出 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 0", owner=self.name)
            self.action.buy_close(bar.close_price, 1, bar)
            self.pos = 0
        elif self.pos == -1 and buy:
            self.logger.success(f"平仓买入 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 0", owner=self.name)
            self.action.sell_close(bar.close_price, 1, bar)
            self.pos = 0
        elif buy and self.pos == 0:
            self.logger.success(f"开仓买入 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> 1", owner=self.name)
            self.pos = 1
            self.action.buy_open(bar.close_price, 1, bar)
        elif sell and self.pos == 0:
            self.logger.success(f"开仓卖出 - 合约: {bar.local_symbol}, 价格: {bar.close_price}, 当前仓位: {self.pos} -> -1", owner=self.name)
            self.pos = -1
            self.action.sell_open(bar.close_price, 1, bar)
