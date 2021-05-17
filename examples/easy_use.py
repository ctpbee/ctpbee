from time import sleep

from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import *


class Main(CtpbeeApi):
    def on_tick(self, tick: TickData) -> None:
        """ """
        print(tick)

    def on_bar(self, bar: BarData) -> None:
        pass

    def on_contract(self, contract: ContractData):
        if contract.symbol == "rb2110":
            x = self.action.subscribe(contract.local_symbol)


if __name__ == '__main__':
    # app = CtpBee("test", __name__, refresh=True)
    # just_use = JustUse("Hi")
    # app.config.from_json("config.json")
    # app.add_extension(just_use)
    # app.start(log_output=True)
    # print("one start")

    market = CtpBee("market", __name__)
    main = Main("DailyCTA")
    market.config.from_json("config.json")
    market.add_extension(main)
    market.start(log_output=True)
