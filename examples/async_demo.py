import asyncio

from ctpbee import CtpBee
from ctpbee import CtpbeeApi
from ctpbee.constant import PositionData, AccountData, LogData
from ctpbee.func import AsyncApi


class DataRecorder(AsyncApi):
    def __init__(self, name, app=None):
        super().__init__(name, app)
        self.subscribe_set = set(["rb1910"])

    async def on_trade(self, trade):
        pass

    async def on_contract(self, contract):
        # 订阅所有
        # self.app.subscribe(contract.symbol)

        # 或者 单独制定
        if contract.symbol in self.subscribe_set:
            self.app.subscribe(contract.symbol)
            # 或者
            # current_app.subscribe(contract.symbol)

    async def on_order(self, order):
        pass

    async def on_position(self, position: PositionData) -> None:
        # print(position)
        pass

    async def on_account(self, account: AccountData) -> None:
        # print(account)
        print(account)
        pass

    async def on_tick(self, tick):
        """tick process function"""
        # print(tick._to_dict())
        print(tick)

    async def on_bar(self, bar):
        """bar process function"""

    async def on_shared(self, shared):
        """ 处理分时图数据 """
        pass

    async def on_log(self, log: LogData):
        """ 可以用于将log信息推送到外部 """
        await asyncio.sleep(1)


def go():
    app = CtpBee("last", __name__, "async")
    info = {
        "CONNECT_INFO": {
            "userid": "089131",
            "password": "350888",
            "brokerid": "9999",
            # 24小时
            "md_address": "tcp://180.168.146.187:10131",
            "td_address": "tcp://180.168.146.187:10130",
            # 移动
            # "md_address": "tcp://218.202.237.33:10112",
            # "td_address": "tcp://218.202.237.33:10102",
            "product_info": "",
            "appid": "simnow_client_test",
            "auth_code": "0000000000000000",
        },
        "INTERFACE": "ctp",
        "TD_FUNC": True,
        "MD_FUNC": True,
    }
    """ 
        载入配置信息 

    """
    app.config.from_mapping(info)

    """ 
        载入用户层定义层 你可以编写多个继承CtpbeeApi ,然后实例化它, 记得传入app, 当然你可以通过app.remove_extension("data_recorder")
        data_recorder 就是下面传入的插件名字

    """
    data_recorder = DataRecorder("data_recorder", app)

    """ 启动 """
    app.start()


if __name__ == '__main__':
    go()
