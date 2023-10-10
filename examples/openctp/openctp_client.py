from time import sleep

from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import *
from ctpbee import VLogger


class Main(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.init = False
        self.count = 0

    def on_tick(self, tick: TickData) -> None:
        if self.count % 2 == 0:
            self.action.buy_open(tick.ask_price_5, 1, tick, price_type=OrderType.FOK)
        elif self.count % 5 != 0:
            self.action.buy_close(tick.bid_price_5, 1, tick, price_type=OrderType.FOK)
        self.count += 1
        print("tick回报", tick)

    def on_trade(self, trade: TradeData) -> None:
        print("成交回报", trade)

    def on_account(self, account: AccountData) -> None:
        print("账户回报", account)

    def on_order(self, order: OrderData) -> None:
        print("订单回报: ", order)

    def on_contract(self, contract: ContractData):
        print("contract回报: ", contract)

    def on_init(self, init: bool):
        self.info("账户初始化成功回报")
        self.init = True
        self.action.subscribe("rb2310")


if __name__ == '__main__':
    app = CtpBee("openctp", __name__, refresh=True)
    example = Main("DailyCTA")
    config = {
        "CONNECT_INFO": {
            "host": "127.0.0.1",
            "index": 0,
            "port": 6379,
            "db": 0
        },
        "INTERFACE": "local",
        "MD_FUNC": True,
        "TD_FUNC": True,
    }
    app.config.from_mapping(config)
    app.add_extension(example)
    app.start(log_output=True)
    app.action.subscribe("rb2310.SHFE")
