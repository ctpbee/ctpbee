from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import TradeData, OrderData, ContractData, Exchange
import pandas as pd

data = pd.read_csv("kline.csv")
data = data.drop("Unnamed: 0", axis=1)
data = [list(reversed(data.to_dict("index").values()))]


class DoubleMaStrategy(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.instrument_set = ["rb2401.SHFE"]
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
        self.count = 0

    def on_trade(self, trade: TradeData):
        pass

    def on_order(self, order: OrderData) -> None:
        pass

    def on_bar(self, bar):
        """ """
        self.count += 1
        if self.count % 5 == 0:
            self.action.buy_open(bar.close_price, 1, bar)
        # print(bar.close_price, self.center.get_position("rb2010.CTP"))

    def on_tick(self, tick):
        pass

    def on_init(self, init: bool):
        print("初始化成功了")


if __name__ == '__main__':
    from ctpbee import CtpbeeApi

    code = "rb2401.SHFE"
    app = CtpBee("looper", __name__)
    info = {
        "PATTERN": "looper",
        "LOOPER": {
            "initial_capital": 100000,
            "margin_ratio": {
                code: 0.00003,
            },
            "commission_ratio": {
                code: {
                    "close": 0.00001
                },
            },
            "size_map": {
                code: 10
            }
        }
    }
    app.config.from_mapping(info)
    app.add_local_contract(ContractData(local_symbol=code, exchange=Exchange.SHFE, symbol=code.split(".")[0],
                                        size=10, pricetick=1))
    strategy = DoubleMaStrategy("ma")
    app.add_extension(strategy)
    app.add_data(*data)
    app.start()
    result = app.get_result(report=True, auto_open=True)
