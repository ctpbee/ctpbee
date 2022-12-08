from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import *


class Main(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.ok = False

        self.init = False

    def on_tick(self, tick: TickData) -> None:
        """ """
        model = self.center.get_position("rb2205.SHFE")
        if model is not None:
            print(model.long_float_pnl, model.short_float_pnl)
        pass

    def on_trade(self, trade: TradeData) -> None:
        pass

    def on_position(self, position: PositionData) -> None:
        # print(position.local_symbol, position.direction, position.float_pnl)
        pass

    def on_bar(self, bar: BarData) -> None:
        pass

    def on_realtime(self):
        pass
        # pos = self.center.get_position("rb2205.SHFE")
        # print(pos)

    def on_contract(self, contract: ContractData):
        # setup the code and subscribe market
        # also you can use app.subscribe()
        pass
        if contract.local_symbol == "rb2205.SHFE":
            self.action.subscribe(contract.local_symbol)

    def on_init(self, init: bool):
        print("Init Successful")
        self.init = True


if __name__ == '__main__':
    app = CtpBee("market", __name__, refresh=True)
    example = Main("DailyCTA")
    app.config.from_json("config.json")
    app.add_extension(example)
    app.start(log_output=True)
    # while True:
    #     pass
