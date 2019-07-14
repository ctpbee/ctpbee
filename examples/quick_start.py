from time import sleep
from ctpbee import ExtAbstract, subscribe
from ctpbee import CtpBee
from ctpbee.interface.ctp.constant import PositionData, AccountData


class DataRecorder(ExtAbstract):
    def __init__(self, name, app=None):
        super().__init__(name, app)

    def on_trade(self, trade):
        pass

    def on_contract(self, contract):
        pass

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


def go():
    app = CtpBee("last", __name__)
    info = {
        "CONNECT_INFO": {
            "userid": "089131",
            "password": "350888",
            "brokerid": "9999",
            "md_address": "tcp://218.202.237.33:10112",
            "td_address": "tcp://218.202.237.33:10102",
            "appid": "simnow_client_test",
            "auth_code": "0000000000000000",
        },
        "INTERFACE": "ctp",
        "TD_FUNC": True,
        "MD_FUNC": True
    }
    app.config.from_mapping(info)
    data_recorder = DataRecorder("data_recorder", app)
    app.start()
    sleep(1)
    for contract in app.recorder.get_all_contracts():
        subscribe(contract.symbol)


if __name__ == '__main__':
    go()
