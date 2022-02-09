from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import *


class Main(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.ok = False

        self.init = False

    def on_tick(self, tick: TickData) -> None:
        """ """
        # Receive Tick in here
        if tick.exchange == Exchange.DCE:
            print(tick.datetime, tick.local_symbol, tick.last_price)

    def on_trade(self, trade: TradeData) -> None:
        if self.init and trade.offset == Offset.OPEN:
            self.action.cover(trade.price - 1, 1, trade)

    def on_position(self, position: PositionData) -> None:
        pass

    def on_bar(self, bar: BarData) -> None:
        pass

    def on_contract(self, contract: ContractData):
        # setup the code and subscribe market
        # also you can use app.subscribe()

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
