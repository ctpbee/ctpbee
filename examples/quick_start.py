from threading import Thread
from threading import Thread
from time import sleep

from ctpbee import CtpBee, dumps, loads
from ctpbee import CtpbeeApi
from ctpbee.constant import PositionData, AccountData, LogData


class DataRecorder(CtpbeeApi):
    def __init__(self, name, app=None):
        super().__init__(name, app)
        self.subscribe_set = set(["UR2001"])

    def on_trade(self, trade):
        pass

    def on_contract(self, contract):
        # 订阅所有
        self.app.subscribe(contract.symbol)

    def on_order(self, order):
        pass

    def on_position(self, position: PositionData) -> None:
        pass

    def on_account(self, account: AccountData) -> None:
        pass

    def on_tick(self, tick):
        """tick process function"""
        pass

    def on_bar(self, bar):
        """bar process function"""

        # self.app.recorder.get_all_positions()
        #
        # interval = bar.interval
        #
        # req = helper.generate_order_req_by_var(symbol=bar.symbol, exchange=bar.exchange, price=bar.high_price,
        #                                        direction=Direction.LONG, type=OrderType.LIMIT, volume=3,
        #                                        offset=Offset.OPEN)
        # # 调用绑定的app进行发单
        # id = self.app.send_order(req)

        # print("返回id", id)

    def on_shared(self, shared):
        """ 处理分时图数据 """
        print(shared)

    def on_log(self, log: LogData):
        """ 可以用于将log信息推送到外部 """
        pass


def go():
    app = CtpBee("last", __name__)

    info = {
        "CONNECT_INFO": {
            "userid": "089131",
            "password": "350888",
            "brokerid": "9999",
            "md_address": "tcp://180.168.146.187:10131",
            "td_address": "tcp://180.168.146.187:10130",
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
    app.start(log_output=False)

    def run_query(app):
        for _ in range(2):
            app.query_position()
            sleep(1)

            app.query_account()
            sleep(1)

    p = Thread(target=run_query, args=(app,))
    p.start()


if __name__ == '__main__':
    go()
