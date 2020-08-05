from ctpbee.constant import Offset
from ctpbee.looper import LooperApi, Vessel
from ctpbee.qa_support import QADataSupport

from ctpbee.indicator.ta_lib import ArrayManager


class DoubleMa(LooperApi):
    def __init__(self, name):
        super(DoubleMa, self).__init__(name)
        self.manager = ArrayManager()
        self.instrument_set = ["rb2010.SHFE"]
        self.fast_window = 10
        self.slow_window = 20
        self.pos = 0
        self.open = False
        self.price = []
        self.open = False
        self.open_price = None

    def on_trade(self, trade):
        if trade.offset == Offset.OPEN:
            self.open_price = trade.price
        else:
            self.open_price = None
            self.open = False
            self.price.clear()

    def on_bar(self, bar):
        # if len(self.price) == 0:
        #     self.price.append(bar.close_price)
        # else:
        #     if bar.close_price < self.price[-1]:
        #         self.price.append(bar.close_price)
        #     else:
        #         self.price.clear()
        # if len(self.price) >= 5:
        #     if not self.open:
        #         self.action.short(bar.close_price, 3, bar)
        #         self.open = True
        #     else:
        #         if abs(bar.close_price - self.open_price) > 10:
        #             self.action.sell(bar.close_price, 3, bar)
        self.action.buy(bar.close_price, 3, bar)

    def on_tick(self, tick):
        pass


if __name__ == '__main__':

    from ctpbee import QADataSupport
    data_support = QADataSupport(host="127.0.0.1", port=27017)
    runnning = Vessel()
    strategy = DoubleMa("ma")
    data = data_support.get_future_min("rb2010.SHFE", frq="1min", start="2020-03-01", end="2020-07-15")
    runnning.add_data(data)
    params = {
        "looper":
            {
                "initial_capital": 50000,
                "deal_pattern": "price",
                # 合约乘数
                "size_map": {"rb2010.SHFE": 10},
                # 手续费收费
                "commission_ratio": {
                    "rb2010.SHFE": {"close": 0.0005, "close_today": 0.0003}
                },
                # 保证金占用
                "margin_ratio": {
                    "rb2010.SHFE": 0.1
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
    runnning.params = params
    runnning.run()
    result = runnning.get_result(report=True, auto_open=True)
