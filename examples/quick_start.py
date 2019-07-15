from time import sleep

from ctpbee import CtpBee
from ctpbee import ExtAbstract
from ctpbee import helper
from ctpbee.constant import PositionData, AccountData, OrderType, Offset, Direction


class DataRecorder(ExtAbstract):
    def __init__(self, name, app=None):
        super().__init__(name, app)
        self.subscribe_set = set(["MA002"])

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
        interval = bar.interval

        req = helper.generate_order_req_by_var(symbol=bar.symbol, exchange=bar.exchange, type=OrderType.LIMIT, volume=2,
                                               direction=Direction.LONG, offset=Offset.OPEN, price=bar.open_price)

        # req = helper.generate_order_req_by_str(symbol=bar.symbol, exchange="shfe", type="limit", volume=2,
        #                                        price=bar.open_price,direction="long"
        #                                        ,offset="open")
        self.app.send_order(req)

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
        "XMIN": [1, 3, 5],
    }
    """ 载入配置信息 """
    app.config.from_mapping(info)

    """ 
        载入用户层定义层 你可以编写多个继承ExtAbstract ,然后实例化它, 记得传入app, 当然你可以通过app.remove_extension("data_recorder")
        data_recorder 就是下面传入的插件名字
    
    """
    data_recorder = DataRecorder("data_recorder", app)

    """ 启动 """
    app.start()
    while True:

        sleep(1)
        app.query_position()
        [ print(x) for x in app.recorder.get_all_positions()]

if __name__ == '__main__':
    go()
