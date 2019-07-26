from ctpbee import CtpbeeApi
from ctpbee.constant import TradeData


class Module(CtpbeeApi):

    def on_trade(self, trade: TradeData) -> None:
        pass


extension = Module("name")

ext = (extension, )
