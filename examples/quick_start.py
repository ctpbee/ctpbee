# # # coding:utf-8
# # """
# # this is an example program which used to record tick data
# # database:pymongo / redis
# #
# # :keyword 补录数据  ---> will be developed in marrd https://github.com/somewheve/marrd
# # 关于补录数据的一点想法:
# # 能不能构建多个类似的程序运行在不同的服务， 然后将数据提交到 同时提交到web服务器，
# # web服务器经过校验之后（出错数据， 缺失数据进行修正和补录）写入到内存（or redis）中，负责提供每天的数据。
# # 这样每天的数据应该基本不会出错，然后外部程序每天访问这个web服务器提供的数据接口，
# # 将数据维护到自己本地
# # """
from time import sleep

from ctpbee import ExtAbstract
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
        print(tick)
        pass

    def on_bar(self, bar):
        """bar process function"""
        bar.exchange = bar.exchange.value
        interval = bar.interval

    def on_shared(self, shared):
        """process shared function"""
        # print(shared)
        pass


def go():
    app = CtpBee("last", __name__)
    # info = {
    #     "CONNECT_INFO"
    #     : {
    #         "userid": "089131",
    #         "password": "350888",
    #         "brokerid": "9999",
    #         "md_address": "tcp://180.168.146.187:10101",
    #         "td_address": "tcp://180.168.146.187:10111",
    #         "appid": "simnow_client_test",
    #         "auth_code": "0000000000000000",
    #     },
    #     "TD_FUNC": True,
    # }
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
        "TD_FUNC": True,
        "MD_FUNC": True
    }
    app.config.from_mapping(info)
    data_recorder = DataRecorder("data_recorder", app)
    app.start(log_output=True)
    sleep(1)
    # for contract in app.recorder.get_all_contracts():
    #     if contract.symbol == "ag1912":
    #         subscribe(contract.symbol)


if __name__ == '__main__':
    go()

