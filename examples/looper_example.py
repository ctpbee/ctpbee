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

    def on_bar(self, bar):
        self.manager.update_bar(bar)
        if not self.manager.inited:
            return
        # print(self.position_manager.get_all_positions())
        fast_ma = self.manager.sma(self.fast_window, array=True)
        self.fast_ma0 = fast_ma[-1]
        self.fast_ma1 = fast_ma[-2]
        slow_ma = self.manager.sma(self.slow_window, array=True)
        self.slow_ma0 = slow_ma[-1]
        self.slow_ma1 = slow_ma[-2]
        cross_over = self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1
        cross_below = self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1
        # print(cross_below)
        if cross_over:
            self.action.buy(bar.close_price, 1, bar)
            self.open = True
        # elif cross_below and self.open:
        #     self.action.cover(bar.close_price, 1, bar)
        #     self.open = False


    def on_tick(self, tick):
        pass


if __name__ == '__main__':
    data_support = QADataSupport(host="quantaxis.tech", port=27027)
    runnning = Vessel()
    strategy = DoubleMa("ma")
    data = data_support.get_future_min("rb2010.SHFE", frq="1min", start="2020-07-01", end="2020-07-15")
    runnning.add_data(data)
    params = {
        "looper":
            {
                "initial_capital": 100000,
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
