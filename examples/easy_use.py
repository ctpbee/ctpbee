from ctpbee import CtpbeeApi, CtpBee, helper
from ctpbee.constant import *


class JustUse(CtpbeeApi):

    def __init__(self, name):
        super().__init__(name)
        self.i = 0

    def on_account(self, account: AccountData) -> None:
        pass

    def on_order(self, order: OrderData) -> None:
        pass

    def on_trade(self, trade: TradeData) -> None:
        pass

    def on_position(self, position: PositionData) -> None:
        pass

    def on_tick(self, tick: TickData) -> None:
        """ """
        # print(tick)

    def on_bar(self, bar: BarData) -> None:
        """ """
        if bar.symbol == "rb2010":
            self.action.buy(bar.high_price, 1, bar)

    def on_contract(self, contract: ContractData):
        """ """
        # if contract.local_symbol in self.instrument_set:
        # self.app.subscribe(contract.local_symbol)
        # self.app.subscribe(contract.local_symbol)

    def on_init(self, init: bool):
        pass


class Main(CtpbeeApi):
    def on_tick(self, tick: TickData) -> None:
        """ """
        # print(tick)

    def on_bar(self, bar: BarData) -> None:
        pass

    def on_contract(self, contract: ContractData):
        if contract.symbol == "rb2010":
            print(contract)
        x = self.action.subscribe(contract.local_symbol)


if __name__ == '__main__':
    app = CtpBee("test", __name__, refresh=True)
    just_use = JustUse("Hi")
    app.config.from_json("config.json")
    app.add_extension(just_use)
    app.start(log_output=True)
    print("one start")
    info = {
        "CONNECT_INFO": {
            "userid": "089131",
            "password": "350888",
            "brokerid": "9999",
            "md_address": "tcp://218.202.237.33:10112",
            "td_address": "tcp://218.202.237.33:10102",
            "product_info": "",
            "appid": "simnow_client_test",
            "auth_code": "0000000000000000"
        },
        "INTERFACE": "ctp",  # 接口声明
        "TD_FUNC": True,  # 开启交易功能
        "MD_FUNC": True,
        "XMIN": [1, 3, 6]
    }

    market = CtpBee("market", __name__)
    main = Main("main")
    market.config.from_mapping(info)
    market.add_extension(main)
    market.start(log_output=False)
    print("second start")
