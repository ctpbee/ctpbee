"""
使用装饰器示例
"""

from datetime import datetime
from time import sleep

from ctpbee.constant import *
from ctpbee import Action, hickey
from ctpbee import CtpBee
from ctpbee import CtpbeeApi
from ctpbee import RiskLevel
from ctpbee import VLogger
from ctpbee import helper


class M(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.a = 0
        self.sta = False

    def on_bar(self, bar: BarData) -> None:
        pass

    def on_tick(self, tick: TickData) -> None:
        print(tick)

    def on_contract(self, contract: ContractData):
        if contract.symbol == "jm2009":
            print(contract)
        self.action.subscribe(contract.local_symbol)

    def on_order(self, order: OrderData) -> None:
        # print(order)

        pass



def create_app():
    app = CtpBee("last", __name__, refresh=True)

    """ 
        载入配置信息 
    """
    app.config.from_json("config.json")

    """ 
        载入用户层定义层 你可以编写多个继承CtpbeeApi ,然后实例化它, 记得传入app, 当然你可以通过app.remove_extension("data_recorder")
        data_recorder 就是下面传入的插件名字

    """
    m = M("name")
    app.add_extension(m)

    """ 启动 """
    return [app]


if __name__ == '__main__':
    # hickey.start_all(app_func=create_app)
    app = create_app()
    app[0].start()

    # def generate_order_req_by_str(cls, symbol: str, exchange: str, direction: str, offset: str, type: str, volume,
    #                               price: float):
