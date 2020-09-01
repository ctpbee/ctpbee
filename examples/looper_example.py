from ctpbee.constant import Offset, TradeData, Direction, OrderData
from ctpbee import CtpbeeApi, CtpBee
from ctpbee.qa_support import QADataSupport
from ctpbee.indicator.ta_lib import ArrayManager
from data_api import DataApi


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
        self.buy = False

    def on_trade(self, trade: TradeData):
        print(trade)

    def on_order(self, order: OrderData) -> None:
        print(order)

    def on_bar(self, bar):
        """ """
        print(bar)
        # print(bar.close_price, self.center.get_position("rb2010.CTP"))

    def on_tick(self, tick):
        pass

    def on_init(self, init: bool):
        print("初始化成功了")


if __name__ == '__main__':
    from ctpbee import QADataSupport, CtpbeeApi

    data_support = QADataSupport()
    app = CtpBee("looper", __name__)
    info = {
        "PATTERN": "looper",
        "LOOPER": {
            "initial_capital": 100000,
            "margin_ratio": {
                "rb2010.CTP": 0.00003,
            },
            "commission_ratio": {
                "rb2010.CTP": {
                    "close": 0.00001
                },
            },
            "size_map": {
                "rb2010.CTP": 10
            }
        }
    }
    app.config.from_mapping(info)
    strategy = DoubleMaStrategy("ma")

    data_api = DataApi()
    data = data_api.get_tick("rb2010", start_date="2020-04-10", end_date="2020-07-21",today=False)
    # data = data_support.get_future_min("rb2010.SHFE", frq="1min", start="2019-10-01", end="2020-07-15")
    app.add_data(data)
    app.add_extension(strategy)
    app.start()
    result = app.get_result(report=True, auto_open=True)
