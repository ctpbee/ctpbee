from ctpbee import CtpbeeApi, CtpBee
from ctpbee import VLogger
from ctpbee.constant import *


class OK(VLogger):
    def handle_record(self):
        pass


class Main(CtpbeeApi):
    def on_tick(self, tick: TickData) -> None:
        """ """
        # print tick data information
        print(tick)

        # print position data information
        print(self.center.positions)

    def on_bar(self, bar: BarData) -> None:
        pass

    def on_contract(self, contract: ContractData):
        # setup the code and subscribe market
        # also you can use app.subscribe()
        if contract.symbol == "rb2110":
            self.action.subscribe(contract.local_symbol)


if __name__ == '__main__':
    app = CtpBee("market", __name__, refresh=True)
    example = Main("DailyCTA")
    app.config.from_json("config.json")
    app.add_extension(example)
    app.start(log_output=True)
