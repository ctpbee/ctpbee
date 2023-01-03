from time import sleep

from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import *


class Main(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.init = False

    def on_tick(self, tick: TickData) -> None:
        # self.action.cancel_all()
        print("tick回报", tick)

    def on_trade(self, trade: TradeData) -> None:
        print("成交回报", trade)

    def on_account(self, account: AccountData) -> None:
        print("账户回报", account)

    def on_order(self, order: OrderData) -> None:
        print("订单回报: ", order)

    def on_position(self, position: PositionData) -> None:
        print("持仓回报", position)

    def on_bar(self, bar: BarData) -> None:
        print("k线回报: ", bar)

    def on_realtime(self):
        print("定时触发", datetime.now())

        # pos = self.center.get_position("rb2205.SHFE")

    # print(pos)

    def on_contract(self, contract: ContractData):
        # setup the code and subscribe market
        # also you can use app.subscribe()
        if contract.local_symbol == "rb2305.SHFE":
            self.action.subscribe(contract.local_symbol)

    def on_init(self, init: bool):
        print("账户初始化成功回报", init)
        pos = self.recorder.get_all_positions()
        print(pos)
        self.init = True


if __name__ == '__main__':
    app = CtpBee("market", __name__, refresh=False)
    example = Main("DailyCTA")
    app.config.from_json("config.json")
    app.add_extension(example)
    app.start(log_output=True)
    sleep(3)
    app.action.query_account()
    sleep(1)
    app.action.query_position()

    # while True:
    #     pass
