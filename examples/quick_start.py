from datetime import datetime
from time import sleep

from ctpbee import Action
from ctpbee import CtpBee
from ctpbee import CtpbeeApi
from ctpbee import RiskLevel
from ctpbee.constant import PositionData, AccountData, LogData


class ActionMe(Action):

    def __init__(self, app):
        super().__init__(app)
        self.add_risk_check(self.short)
        self.add_risk_check(self.cancel)

    def before_cancel(self, *args, **kwargs):
        id = args[0]
        if id in self.app.recorder.get_all_active_orders():
            return True
        return False

    def after_cancel(self, result):
        pass

    def before_short(self, *args, **kwargs):
        price, volume, origin = args
        return True

    def after_cancel(self, result):
        pass


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

    def realtime_check(self, cur):
        pass

    def after_cancel_order(self, result):
        """ 撤单之后 """

    def after_send_order(self, result):
        """ 发单之后 """

    def before_short(self, *args, **kwargs):
        """"""

        # do something  ??
        print("发单")
        return True, args, kwargs

    def after_short(self, result):
        # print(result)
        cal = 0
        while True:
            sleep(1)
            if cal > 3: break
            cal += 1
            # do something


# 启动过程  --- strategy/ .py  --- app.add_extension(ext)

class DataRecorder(CtpbeeApi):
    def __init__(self, name, app=None):
        super().__init__(name, app)
        self.instrument_set = set(["ag1912.SHFE"])
        self.comming_in = None
        self.id = None

    def on_trade(self, trade):
        pass

    def on_contract(self, contract):
        # 通过本地的
        if contract.local_symbol in self.instrument_set:
            self.app.subscribe(contract.local_symbol)

    def on_order(self, order):
        """ """
        # if order.status == Status.CANCELLED or order.status == Status.ALLTRADED:
        # assert self.id == order.local_order_id

    def on_position(self, position: PositionData) -> None:
        pass

    def on_account(self, account: AccountData) -> None:
        """ """
        # print(account)

    def on_tick(self, tick):
        """tick process function"""
        # print(tick)

    def on_bar(self, bar):
        """bar process function"""
        ids = self.action.short(bar.high_price, 20, bar)
        print(ids)
        # self.action.sell(ids)

    def on_shared(self, shared):
        """ 处理分时图数据 """
        print(shared)

    def on_log(self, log: LogData):
        """ 可以用于将log信息推送到外部 """
        pass

    def on_realtime(self, timed: datetime):
        """  """
        # for x in self.app.recorder.get_all_active_orders():
        #     self.action.cancel(x.local_order_id)

    def on_init(self, init):
        print("初始化")
        if init:
            self.flag = False
            # print("初始化完成")
            # 获取主力合约
            # main_contract = self.app.recorder.get_main_contract_by_code("ap")
            #
            # # 获取合约的价格
            # # #  如果你需要该合约的最新的行情价格 你可能需要通过self.app.trader.request_market_data() 来更新最新的深度行情，回调函数会自动更新行情数据，
            # # 也许在风控那边一直发送请求数据或者在start()之后开个单独线程来请求是个不错的选择
            # print(self.app.recorder.get_contract_last_price("AP910.CZCE"))
            #
            # # 获取主力合约列表
            # print(self.app.recorder.main_contract_list)
            #
            main_contract = self.app.recorder.get_main_contract_by_code("ap")
            self.instrument_set.add(main_contract.local_symbol)

            # print(app.recorder.get_contract("ag1912.SHFE"))


def create_app():
    app = CtpBee("last", __name__, action_class=ActionMe, refresh=True, risk=RiskMe)

    """ 
        载入配置信息 
    """
    app.config.from_json("config.json")

    """ 
        载入用户层定义层 你可以编写多个继承CtpbeeApi ,然后实例化它, 记得传入app, 当然你可以通过app.remove_extension("data_recorder")
        data_recorder 就是下面传入的插件名字
      
    """

    data_recorder = DataRecorder("data_recorder")
    app.add_extension(data_recorder)
    """ 添加自定义的风控 """

    """ 启动 """
    app.start(log_output=True)
    return app
    # print(current_app.name)


if __name__ == '__main__':
    app = create_app()
    # del_app(app.name)
