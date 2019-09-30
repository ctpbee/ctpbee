import asyncio
from datetime import datetime

from ctpbee import AsyncApi
from ctpbee import CtpBee, RiskLevel
from ctpbee.constant import PositionData, AccountData, LogData


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

            def buy(self, *args, **kwargs)
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
        # print(f"\r {self.app.recorder.get_all_active_orders()}", end="")
        # print(f"\r {self.app.recorder.get_all_active_orders()}", end="")
        # self.action.cover
        x = self.app.recorder.get_all_active_orders()
        for i in x:
            print(f"我要发起撤单了 单号:{i.local_order_id}")
            self.action.cancel(i.local_order_id)

    def before_send_order(self) -> bool:
        """ 返回True不阻止任何操作 """
        return True

    def before_cancel_order(self) -> bool:
        """ 返回True不阻止任何操作 """
        return True

    def after_cancel_order(self, result):
        """ 撤单之后 """

    def after_send_order(self, result):
        """ 发单之后 """


class DataRecorder(AsyncApi):
    def __init__(self, name, app=None):
        super().__init__(name, app)
        self.instrument_set = set(["ag1912.SHFE"])

    async def on_trade(self, trade):
        pass

    async def on_contract(self, contract):
        # 订阅所有
        # self.app.subscribe(contract.symbol)

        # 或者 单独制定
        if contract.local_symbol in self.instrument_set:
            print(contract.local_symbol)
            print(contract.size)
            self.app.subscribe(contract.local_symbol)
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

    async def on_bar(self, bar):
        """bar process function"""
        print(datetime.now().timestamp())

    async def on_shared(self, shared):
        """ 处理分时图数据 """
        pass

    async def on_init(self, init):
        print("init")

    async def on_log(self, log: LogData):
        """ 可以用于将log信息推送到外部 """
        await asyncio.sleep(1)


def go():
    app = CtpBee("last", __name__, engine_method="async")
    info = {
        "CONNECT_INFO": {
            "userid": "089131",
            "password": "350888",
            "brokerid": "9999",
            # 24小时
            # "md_address": "tcp://180.168.146.187:10131",
            # "td_address": "tcp://180.168.146.187:10130",
            # # 移动
            "md_address": "tcp://218.202.237.33:10112",
            "td_address": "tcp://218.202.237.33:10102",
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
    app.update_risk_gateway(RiskMe)

    """ 
        载入用户层定义层 你可以编写多个继承CtpbeeApi ,然后实例化它, 记得传入app, 当然你可以通过app.remove_extension("data_recorder")
        data_recorder 就是下面传入的插件名字

    """
    data_recorder = DataRecorder("data_recorder", app)

    """ 启动 """
    app.start()


if __name__ == '__main__':
    go()
