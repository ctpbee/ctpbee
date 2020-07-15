"""
双均线策略实现

"""

from ctpbee import CtpbeeApi
from ctpbee.constant import BarData
from ctpbee.indicator import ArrayManager


class DoubleMa(CtpbeeApi):

    def __init__(self, name: str, code=None):
        # 初始化策略参数
        super().init_app(name)
        self.indicator = ArrayManager()
        self.fast_windows = 5
        self.slow_window = 10

    def on_bar(self, bar: BarData) -> None:
        self.indicator.update_bar(bar)

        if self.indicator.inited:
            return

        ma, sig, his = self.indicator.macd(fast_period=self.fast_windows, slow_period=self.slow_window, signal_period=1)


    def on_realtime(self):
        pass




if __name__ == '__main__':
    pass