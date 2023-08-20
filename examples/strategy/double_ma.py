from ctpbee.constant import TickData, BarData

from ctpbee import CtpbeeApi


class DoubleMa(CtpbeeApi):
    fast_period = 10
    slow_period = 20

    def __init__(self, name: str, length: int):
        super().__init__(name)
        self.length = length
        self.close = []

    def on_tick(self, tick: TickData) -> None:
        pass

    def on_bar(self, bar: BarData):
        if len(self.length) <= self.length:
            return
        close_array = self.close[-self.length:]
        fast_ma = s.sma(close_array, self.fast_period)
        slow_ma = self.indicator.sma(close_array, self.slow_period)

        if fast_ma[-1] > slow_ma[-1] and fast_ma[-2] <= slow_ma[-2]:
            self.action.buy(bar.close_price, 1, bar)
        elif fast_ma[-1] < slow_ma[-1] and fast_ma[-2] >= slow_ma[-2]:
            self.action.short(bar.close_price, 1, bar)
