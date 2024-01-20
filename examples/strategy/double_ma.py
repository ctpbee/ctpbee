from ctpbee.constant import TickData, BarData
from ctpbee import CtpbeeApi
from ctpbee.indicator.indicator import ma


class DoubleMa(CtpbeeApi):
    fast_period = 2
    slow_period = 10

    def __init__(self, name: str, code):
        super().__init__(name, )
        self.instrument_set = set([code])
        self.length = self.slow_period
        self.close = []
        self.pos = 0

    def on_tick(self, tick: TickData) -> None:
        pass

    def on_bar(self, bar: BarData):
        self.close.append(bar.close_price)
        if len(self.close) <= self.length * 2:
            return
        close_array = self.close[-self.length * 2:]
        fast_ma = ma(close_array, self.fast_period)
        slow_ma = ma(close_array, self.slow_period)
        buy = fast_ma[-1] > slow_ma[-1] and fast_ma[-2] < slow_ma[-2]
        sell = fast_ma[-1] < slow_ma[-1] and fast_ma[-2] > slow_ma[-2]
        if self.pos == 1 and sell:
            self.action.buy_close(bar.close_price, 1, bar)
            self.pos = 0
        elif self.pos == -1 and buy:
            self.action.sell_close(bar.close_price, 1, bar)
            self.pos = 0
        elif buy and self.pos == 0:
            self.pos = 1
            self.action.buy_open(bar.close_price, 1, bar)
        elif sell and self.pos == 0:
            self.pos = -1
            self.action.sell_open(bar.close_price, 1, bar)
