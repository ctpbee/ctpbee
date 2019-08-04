from ctpbee import CtpBee
from ctpbee import CtpbeeApi
from ctpbee.constant import PositionData, AccountData, LogData


class DataRecorder(CtpbeeApi):
    def __init__(self, name, app=None):
        super().__init__(name, app, api_type="data")
        self.subscribe_set = set(["rb1910"])

    def on_trade(self, trade):
        pass

    def on_contract(self, contract):
        # 订阅所有
        self.app.subscribe(contract.symbol)

        # 或者 单独制定
        # if contract.symbol in self.subscribe_set:
        #     self.app.subscribe(contract.symbol)
            # 或者
            # current_app.subscribe(contract.symbol)

    def on_order(self, order):
        pass

    def on_position(self, position: PositionData) -> None:
        # print(position)
        pass

    def on_account(self, account: AccountData) -> None:
        # print(account)
        print(account)
        pass

    def on_tick(self, tick):
        """tick process function"""
        # print(tick._to_dict())
        print(tick)

    def on_bar(self, bar):
        """bar process function"""
        interval = bar.interval
        #
        # req = helper.generate_order_req_by_var(symbol=bar.symbol, exchange=bar.exchange, type=OrderType.LIMIT, volume=2,
        #                                        direction=Direction.LONG, offset=Offset.OPEN, price=bar.open_price)

        # req = helper.generate_order_req_by_str(symbol=bar.symbol, exchange="shfe", type="limit", volume=2,
        #                                        price=bar.open_price, direction="long"
        #                                        , offset="open")
        # vt_id = self.app.send_order(req)
        pass

    def on_shared(self, shared):
        """ 处理分时图数据 """
        pass

    def on_log(self, log: LogData):
        """ 可以用于将log信息推送到外部 """
        pass


def go():
    app = CtpBee("last", __name__)

    # 风险控制层
    @app.risk_gateway.connect_via()
    def conn(app: CtpBee):
        """
        用户可以在每个app实例下面来使用app.risk_control.connect_via() 来装饰函数
        接受一个参数来访问到当前app的实例, 以此判断是否进行下单 , 需要注意, 如果一旦返回错误, 那么函数这单将无法下载
        """
        return False  # return True

    #  或者
    # def conn(app: CtpBee):
    #     return False  # return True
    # app.risk_control.connect(conn)

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
    app.start()
    # while True:
    #     app.query_position()
    #     sleep(1)
    #     from pprint import pprint
    #     pprint(app.recorder.get_all_positions())


if __name__ == '__main__':
    go()
