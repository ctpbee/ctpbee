"""
 本地模拟示例
"""
from datetime import datetime
from time import sleep

from ctpbee import CtpBee
from ctpbee import CtpbeeApi
from ctpbee.constant import BarData, TickData

api = CtpbeeApi("实盘")

pre = CtpbeeApi("模拟")

class Me(CtpbeeApi):

    def on_tick(self, tick: TickData) -> None:
        print(tick)

    def on_bar(self, bar: BarData) -> None:
        print(bar)


@api.route(handler="tick")
def handle_tick(self, tick):
    """ """
    # print("当前时间: ", str(datetime.now()))
    # print("tick时间: ", str(tick.datetime))


@api.route(handler="contract")
def handle_contract(self, contract):
    self.app.subscribe(contract.local_symbol)


@api.route(handler="bar")
def handle_bars(self, bar):
    """ """


if __name__ == '__main__':
    core_app = CtpBee("sim", __name__)
    info = {
        "CONNECT_INFO": {
            "userid": "089131",
            "password": "350888",
            "brokerid": "9999",
            "md_address": "tcp://218.202.237.33:10112",
            "td_address": "tcp://218.202.237.33:10102",
            "product_info": "",
            "appid": "simnow_client_test",
            "auth_code": "0000000000000000",
        },
        "INTERFACE": "sim",
        "TD_FUNC": True,
        "MD_FUNC": True,
    }
    core_app.config.from_mapping(info)
    core_app.add_extension(Me("模拟"))
    core_app.start()
    print("模拟已经启动")

    market_app = CtpBee("market", __name__)
    market_app.config.from_mapping({
        "CONNECT_INFO": {
            "userid": "170874",
            "password": "he071201",
            "brokerid": "9999",
            "md_address": "tcp://218.202.237.33:10112",
            "td_address": "tcp://218.202.237.33:10102",
            "product_info": "",
            "appid": "simnow_client_test",
            "auth_code": "0000000000000000",
        },
        "INTERFACE": "ctp",
        "TD_FUNC": True,
        "MD_FUNC": True,
    })
    market_app.add_extension(api)
    market_app.start()
