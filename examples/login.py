from time import sleep

from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import *


class Main(CtpbeeApi):
    def __init__(self, code="ag2406"):
        super().__init__(code)
        self.init = False
        self.ok = 0
        self.pos = None
        self.pos_init = False
        self.code = code

    def on_tick(self, tick: TickData) -> None:
        if self.init and self.ok == 0:
            self.action.buy_open(int(tick.ask_price_1) + 10, 1, tick)
            self.ok = 1

    def on_trade(self, trade: TradeData) -> None:
        print("成交回报", trade)

        pos = self.center.get_position(f"{self.code}.SHFE")
        print(pos.long_volume, pos.short_volume)

    def on_order(self, order: OrderData) -> None:
        if self.init:
            print("订单回报: ", order)
        print(order)

    def on_position(self, position: PositionData) -> None:
        pos = self.center.get_position(f"{self.code}.SHFE")
        print(pos.long_volume, pos.short_volume)

    def on_contract(self, contract: ContractData):
        if contract.symbol == self.code:
            self.action.subscribe(contract.local_symbol)

    def on_init(self, init: bool):
        self.init = True

if __name__ == '__main__':
    app = CtpBee("market", __name__, refresh=True)
    example = Main("rb2410")
    app.config.from_json("config.json")
    app.add_extension(example)
    app.start(log_output=True)
