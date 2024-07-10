from time import sleep

from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import *


class Main(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.init = False
        self.ok = 0
        self.pos = None
        self.pos_init = False

    def on_tick(self, tick: TickData) -> None:
        if self.init and self.ok == 0:
            self.action.buy_open(int(tick.ask_price_1) + 10, 1, tick)
            self.ok = 1

    def on_trade(self, trade: TradeData) -> None:
        print("成交回报", trade)

    def on_order(self, order: OrderData) -> None:
        if self.init:
            print("订单回报: ", order)
        print(order)

    def on_position(self, position: PositionData) -> None:
        # print("持仓回报", position)
        pos = self.center.get_position("ag2406.SHFE")
        print(pos.long_volume, pos.short_volume)
        # if pos != self.pos:
        #     print("===>", pos)
        #     self.pos = pos
        #     if not self.pos_init:
        #         self.pos_init = True

    def on_contract(self, contract: ContractData):
        if contract.symbol == "ag2406":
            self.action.subscribe(contract.local_symbol)

    def on_init(self, init: bool):
        self.init = True


if __name__ == '__main__':
    app = CtpBee("market", __name__, refresh=True)
    example = Main("DailyCTA")
    app.config.from_json("config.json")
    app.add_extension(example)
    app.start(log_output=True)
