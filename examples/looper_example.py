from ctpbee.constant import Offset, TradeData, Direction
from ctpbee import CtpbeeApi, CtpBee
from ctpbee.qa_support import QADataSupport
from ctpbee.indicator.ta_lib import ArrayManager


class DoubleMaStrategy(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.manager = ArrayManager(500)
        self.instrument_set = ["rb2010.SHFE"]
        self.fast_window = 10
        self.slow_window = 20
        self.pos = 0
        self.open = False
        self.price = []
        self.open = False
        self.open_price = None
        self.buy = 0
        self.sell = 0
        self.slow = 60
        self.fast = 30

    def on_trade(self, trade: TradeData):
        if trade.offset == Offset.OPEN:
            if trade.direction == Direction.LONG:
                self.buy += trade.volume
            else:
                self.sell += trade.volume
        else:
            if trade.direction == Direction.LONG:
                self.sell -= trade.volume
            else:
                self.buy -= trade.volume

    def on_bar(self, bar):
        """ """
        self.manager.add_data(bar)
        if not self.manager.inited:
            return
        fast_avg = self.manager.sma(self.fast, array=True)
        slow_avg = self.manager.sma(self.slow, array=True)

        if slow_avg[-2] < fast_avg[-2] and slow_avg[-1] >= fast_avg[-1]:
            self.action.cover(bar.close_price, self.buy, bar)
            self.action.sell(bar.close_price, 3, bar)

        if fast_avg[-2] < slow_avg[-2] and fast_avg[-1] >= slow_avg[-1]:
            self.action.sell(bar.close_price, self.sell, bar)
            self.action.buy(bar.close_price, 3, bar)

    def on_tick(self, tick):
        pass


if __name__ == '__main__':
    from ctpbee import QADataSupport, CtpbeeApi

    data_support = QADataSupport()
    app = CtpBee("looper", __name__)
    strategy = DoubleMaStrategy("ma")
    # data = data_support.get_future_min("rb2010.SHFE", frq="1min", start="2019-10-01", end="2020-07-15")
    # app.add_data(data)
    info = {
        "PATTERN": "looper",
    }
    app.config.from_mapping(info)
    app.add_extension(strategy)
    app.start()
    # runnning.run()
    # result = runnning.get_result(report=True, auto_open=True)
