from ctpbee.constant import Offset, TradeData, Direction

from ctpbee.indicator.ta_lib import ArrayManager


class DoubleMaStrategy(LooperApi):
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

        self.slow = 30
        self.fast = 15

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
        self.manager.update_bar(bar)
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


class OIDoubleMaStrategy(LooperApi):
    def __init__(self, name):
        super().__init__(name)
        self.manager = ArrayManager(500)
        self.instrument_set = ["OI2009.CZCE"]
        self.fast_window = 10
        self.slow_window = 20
        self.pos = 0
        self.open = False
        self.price = []
        self.open = False
        self.open_price = None
        self.buy = 0
        self.sell = 0

        self.slow = 30
        self.fast = 15

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
    from ctpbee import QADataSupport

    data_support = QADataSupport()
    runnning = Vessel()
    strategy = DoubleMaStrategy("rb")
    strategy_2 = OIDoubleMaStrategy("oi")
    data = data_support.get_future_min("rb2010.SHFE", frq="1min", start="2020-04-01", end="2020-07-15")
    data1 = data_support.get_future_min("OI009.CZCE", frq="1min", start="2020-04-01", end="2020-07-15")
    runnning.add_data(data, data1)
    params = {
        "looper":
            {
                "initial_capital": 100000,
                "deal_pattern": "price",
                # 合约乘数
                "size_map": {"rb2010.SHFE": 10,
                             "OI2009.CZCE": 10,
                             "FG2009.CZCE": 20,
                             },
                # 手续费收费
                "commission_ratio": {
                    "OI2009.CZCE": {"close": 0.00003, "close_today": 0},
                    "rb2010.SHFE": {"close": 0.0001, "close_today": 0.0001},
                    "FG2009.CZCE": {"close": 0.00001, "close_today": 0.00001},
                },
                # 保证金占用
                "margin_ratio": {
                    "rb2010.SHFE": 0.1,
                    "OI2009.CZCE": 0.06,
                    "FG2009.CZCE": 0.05
                },
                "slippage_sell": 0,
                "slippage_cover": 0,
                "slippage_buy": 0,
                "slippage_short": 0,
                "close_pattern": "yesterday",
            },
        "strategy":
            {

            }
    }
    runnning.add_strategy(strategy)
    runnning.add_strategy(strategy_2)
    runnning.params = params
    runnning.run()
    result = runnning.get_result(report=True, auto_open=True)
