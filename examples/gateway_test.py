from time import sleep

from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import *
from ctpbee import VLogger

class RohanCallback(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.init = False


    def on_trade(self, trade: TradeData) -> None:
        print("成交回报", trade)

    def on_account(self, account: AccountData) -> None:
        print("账户回报", account)

    def on_order(self, order: OrderData) -> None:
        print("订单回报: ", order)

    def on_position(self, position: PositionData) -> None:
        print("持仓回报", position)
        pass


if __name__ == '__main__':
    app = CtpBee("rohon_test", __name__, refresh=True)
    config = {
        "CONNECT_INFO": {
            "userid": "xzr11111",
            "password": "1111111",
            "brokerid": "RohonReal",
            "md_address": "tcp://124.74.248.120:47215",
            "td_address": "tcp://47.111.85.73:11001",
            "appid": "client_shentu_1.0",
            "auth_code": "w6a4n8mWgKa9E5NF"
        },
        "INTERFACE": "rohon",
        "REFRESH_INTERVAL": 30,
        "MD_FUNC": True,
        "TD_FUNC": True
    }

    rohon_callback = RohanCallback("rohon_callback")
    app.config.from_mapping(config)
    app.add_extension(rohon_callback)
    app.start(log_output=True)
