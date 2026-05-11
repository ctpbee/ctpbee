from strategy.atr_strategy import ATRStrategy

from ctpbee import CtpBee, CtpbeeApi
from ctpbee import Mode
from ctpbee.constant import *


class Main(ATRStrategy):
    def __init__(self, name, code):
        super().__init__(name, code)
        self.init = False
        self.ok = 0
        self.pos = None
        self.pos_init = False

    def on_tick(self, tick: TickData) -> None:
        # if self.code() == tick.symbol:
        #     if self.ok % 2 == 0:
        #         self.action.buy_open(int(tick.ask_price_1) + 10, 1, tick)
        #     else:
        #         self.action.buy_close(int(tick.ask_price_1) - 10, 1, tick)
        #     self.ok += 1
        # print(tick.symbol, tick.last_price)
        pass

    def on_trade(self, trade: TradeData) -> None:
        if self.init:
            print("成交回报", trade)
        # pos = self.center.get_position(f"{self.code}.SHFE")
        # print(pos.long_volume, pos.short_volume)
        pass

    def on_order(self, order: OrderData) -> None:
        if self.init:
            print("订单回报: ", order)
        print(order)

    def on_position(self, position: PositionData) -> None:
        pass

    def on_contract(self, contract: ContractData):
        # if contract.symbol == self.code():
        if len(contract.symbol) <= 6:
            self.info(f"subscribe {contract.local_symbol}")
            self.action.subscribe(contract.local_symbol)

    def on_init(self, init: bool):
        self.init = True


if __name__ == "__main__":
    app = CtpBee("market", __name__,  work_mode=Mode.DISPATCHER, refresh=True)
    example = Main("ag2606", "ag2606")
    app.config.from_json("config.json")
    app.add_extension(example)
    app.start(log_output=True)
