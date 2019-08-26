from ctpbee import CtpBee, helper
from ctpbee import CtpbeeApi
from ctpbee import RiskLevel
from ctpbee.constant import PositionData, AccountData, LogData, Direction, Offset, OrderType


class RiskMe(RiskLevel):
    """
        约定 1. before_** 函数中 都需要返回True/False, 用于是否阻断操作
            2. 被装饰的函数必须返回一个结果  -->这个值会被传入到after_**函数中
            3. after_** 函数必须接受一个参数， 用于知晓执行函数的结果

        你在任何你想要操作的层中 通过func = self.app.risk_gateway_class(func) 执行主动添加事前和事后风控, 但是前提是你需要写好对应的处理函数

        for example:
        在你策略代码中
        class MyStrategy(CtpbeeApi):

            def __init__(self, name, app=None):
                super().__init__(name, app)
                # 主动对buy操作添加一个风控
                self.buy = self.app.risk_gateway_class(self.buy)

            def buy(*args, **kwargs)
                # 函数最后需要返回一个结果
                return True


        在你风控代码中与此同时也要实现对bug的两个操作
        class Risk(RiskLevel):
            def before_buy(self):
                pass

            def after_buy(self, result):
                pass

        在你的启动代码中
            ....
        app.add_risk_gateway(Risk)
        strategy = MyStrategy("fly_into_sky", app)
        app.start()

        特别注意：
            1, 如果你想在你的策略代码想使用风控， 在你载入策略之前必须先通过app.add_risk_gateway(Risk， risk=False) 将风控代码载入进去，风控在运行的时候能够通过
                self.app 访问所有你想要的数据
            2, add_risk_gateway的参数risk默认为True将对发单和撤单进行风控检查, 你需要在Risk里面实现before_send_order, before_cancel_order,
                                                                    after_cancel_order, after_send_order等四个方法.反之不用
            3. realtime_check(self): 是一直在运行的函数, 一秒一次

    """

    def realtime_check(self):
        """ 一秒一次的扫描 """
        print("实时扫描")

    def before_send_order(self) -> bool:
        """ 返回True不阻止任何操作 """
        return True

    def before_cancel_cancel(self) -> bool:
        """ 返回True不阻止任何操作 """
        return True

    def after_cancel_order(self, result):
        """ 撤单之后 """

    def after_send_order(self, result):
        """ 发单之后 """


class DataRecorder(CtpbeeApi):
    def __init__(self, name, app=None):
        super().__init__(name, app)
        self.subscribe_set = set(["UR2001"])

    def on_trade(self, trade):
        pass

    def on_contract(self, contract):
        # 订阅单个
        if contract.symbol in self.subscribe_set:
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
        req = helper.generate_order_req_by_var(symbol=bar.symbol, exchange=bar.exchange, price=bar.high_price,
                                               direction=Direction.LONG, type=OrderType.LIMIT, volume=3,
                                               offset=Offset.OPEN)
        # # 调用绑定的app进行发单
        id = self.app.send_order(req)

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
    app.add_risk_gateway(RiskMe)

    data_recorder = DataRecorder("data_recorder", app)

    """ 添加自定义的风控 """


    """ 启动 """
    app.start(log_output=True)


if __name__ == '__main__':
    go()
