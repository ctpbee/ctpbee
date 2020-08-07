from ctpbee import CtpbeeApi
from ctpbee.constant import BarData, TickData, ContractData


class Api(CtpbeeApi):

    def __init__(self, name):
        pass

    def on_bar(self, bar: BarData) -> None:
        pass

    def on_tick(self, tick: TickData) -> None:
        pass

    def on_realtime(self):
        pass

    def on_contract(self, contract: ContractData):
        pass


if __name__ == '__main__':
    pass
