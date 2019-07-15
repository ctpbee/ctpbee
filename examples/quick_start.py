from time import sleep

from ctpbee import CtpBee
from ctpbee import ExtAbstract
from ctpbee.interface.ctp.constant import PositionData, AccountData


class DataRecorder(ExtAbstract):
    def __init__(self, name, app=None):
        super().__init__(name, app)
        self.subscribe_set = set(["MA002", "AP001", "IC1909"])

    def on_trade(self, trade):
        pass

    def on_contract(self, contract):
        # 订阅所有
        # self.app.subscribe(contract.symbol)

        # 或者 单独制定
        if contract.symbol in self.subscribe_set:
            self.app.subscribe(contract.symbol)
            # 或者
            # current_app.subscribe(contract.symbol)

    def on_order(self, order):
        pass

    def on_position(self, position: PositionData) -> None:
        # print(position)
        pass

    def on_account(self, account: AccountData) -> None:
        # print(account)
        pass

    def on_tick(self, tick):
        """tick process function"""
        # print(tick)
        print(tick)
        pass

    def on_bar(self, bar):
        """bar process function"""
        bar.exchange = bar.exchange.value
        interval = bar.interval
        print(bar)

    def on_shared(self, shared):
        """process shared function"""
        # print(shared)
        pass

    """
     "md_address": "tcp://218.202.237.33:10112",
    "td_address": "tcp://218.202.237.33:10102",
            """


def go():
    app = CtpBee("last", __name__)
    info = {
        "CONNECT_INFO": {
            "userid": "089131",
            "password": "350888",
            "brokerid": "9999",

            # "md_address": "tcp://180.168.146.187:10131",
            # "td_address": "tcp://180.168.146.187:10130",
            "md_address": "tcp://218.202.237.33:10112",
            "td_address": "tcp://218.202.237.33:10102",

            "product_info":"",
            "appid": "simnow_client_test",
            "auth_code": "0000000000000000",
        },
        "INTERFACE": "ctp",
        "TD_FUNC": True,
        "MD_FUNC": True,
        "XMIN": [1, 3, 5],
    }
    """ 载入配置信息 """
    app.config.from_mapping(info)

    """ 载入用户层 """
    data_recorder = DataRecorder("data_recorder", app)

    """ 启动 """
    app.start()
    sleep(1)

    for con in app.recorder.get_all_contracts():
        # print(app.subscribe(con.symbol))
        pass
    print(app.recorder.get_all_contracts())
    app.query_position()

    sleep(1)
    # print(app.recorder.get_all_positions())


if __name__ == '__main__':
    go()
