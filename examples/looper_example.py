from ctpbee.constant import Offset, TradeData, Direction
from ctpbee.looper import LooperApi, Vessel
from ctpbee.qa_support import QADataSupport

from ctpbee.indicator.ta_lib import ArrayManager


class DoubleMa(LooperApi):
    def __init__(self, name):
        super(DoubleMa, self).__init__(name)
        self.manager = ArrayManager(500)
        self.instrument_set = ["FG2009.CZCE"]
        self.fast_window = 10
        self.slow_window = 20
        self.pos = 0
        self.open = False
        self.price = []
        self.open = False
        self.open_price = None
        self.buy = 0
        self.sell = 0

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
        # self.manager.update_bar(bar)
        # if not self.manager.inited:
        #     return
        # ex = self.manager.macd_scta()
        # # print(ex)
        # if -1 < ex < 1:
        #     if ex > 0:
        #         self.action.sell(bar.close_price, self.sell, bar)
        #         volume = int(ex * 10)
        #         if volume > self.buy:
        #             self.action.buy(bar.close_price, volume - self.buy, bar)
        #         elif volume == self.buy:
        #             pass
        #         else:
        #             self.action.cover(bar.close_price, self.buy - volume, bar)
        #     elif ex == 0:
        #         self.action.sell(bar.close_price, self.sell, bar)
        #         self.action.cover(bar.close_price, self.buy, bar)
        #     else:
        #         volume = abs(int(ex * 10))
        #         self.action.cover(bar.close_price, self.buy, bar)
        #         if volume > self.sell:
        #             self.action.short(bar.close_price, volume - self.sell, bar)
        #         elif volume == self.sell:
        #             pass
        #         else:
        #             self.action.sell(bar.close_price, abs(volume - self.sell), bar)

    def on_tick(self, tick):
        pass


if __name__ == '__main__':
    from ctpbee import QADataSupport

    data_support = QADataSupport(host="127.0.0.1", port=27027)
    runnning = Vessel()
    strategy = DoubleMa("ma")
    data = data_support.get_future_min("FG009.CZCE", frq="1min", start="2020-04-01", end="2020-07-15")
    print(data[1])

    runnning.add_data(data)
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
    runnning.params = params
    runnning.run()
    result = runnning.get_result(report=True, auto_open=True)
