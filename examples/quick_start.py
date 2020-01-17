from time import sleep
from datetime import datetime
from ctpbee import Action
from ctpbee import CtpBee
from ctpbee import CtpbeeApi
from ctpbee import RiskLevel
from ctpbee import VLogger
from ctpbee import hickey
from ctpbee.constant import PositionData, AccountData, LogData, BarData


class Vlog(VLogger):

    def handler_record(self, record):
        """ 处理日志信息代码 """
        pass


class ActionMe(Action):

    def __init__(self, app):
        super().__init__(app)


class RiskMe(RiskLevel):

    def realtime_check(self):
        pass

    def after_cancel_order(self, result):
        """ 撤单之后 """

    def after_send_order(self, result):
        """ 发单之后 """

    def before_short(self, *args, **kwargs):
        """"""
        # do something  ??
        self.info("发单")
        return True, args, kwargs

    def after_short(self, result):

        cal = 0
        self.info("我在执行short后的事后检查")
        while True:
            sleep(1)
            if cal > 3:
                break
            cal += 1
            self.info("正在检查呢 ")
            # do something


# 启动过程  --- strategy/ .py  --- app.add_extension(ext)

class DataRecorder(CtpbeeApi):
    def __init__(self, name, app=None):
        super().__init__(name, app, init_position=True)
        self.instrument_set = set(["rb2001.SHFE"])
        self.comming_in = None
        self.id = None
        self.f_init = False

    def on_trade(self, trade):
        pass

    def on_contract(self, contract):
        # 通过本地的
        if contract.local_symbol in self.instrument_set:
            self.app.action.subscribe(contract.local_symbol)

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
        """tick processself-control  && kill your  function"""
        print(tick)

    def on_bar(self, bar):
        """bar process function"""

        # self.action.short(bar.high_price, 1, bar)
        print(bar)

    def on_log(self, log: LogData):
        """ 可以用于将log信息推送到外部 """
        pass

    def on_realtime(self):
        """  """
        pos = self.level_position_manager.get_position("rb2001.SHFE")
        if pos:
            print(pos)
        # for x in self.app.recorder.get_all_active_orders():
        #     self.action.cancel(x.local_order_id)
        # print(self.app.recorder.generators["rb2001.SHFE"].get_min_1_bar)

    def on_init(self, init):
        self.info("初始化")
        if init:
            self.flag = False
            # print("初始化完成")
            # 获取主力合约
            # main_contract = self.app.recorder.get_main_contract_by_code("ap")
            #
            # # 获取合约的价格
            # # #  如果你需要该合约的handlerevent最新的行情价格 你可能需要通过self.app.trader.request_market_data() 来更新最新的深度行情，回调函数会自动更新行情数据，
            # # 也许在风控那边一直肿发送请求数据或者在start()之后开个单独线程来请求是个不错的选择
            # print(self.app.recorder.get_contract_last_price("AP910.CZCE"))
            #
            # # 获取主力合约列表
            # print(self.app.recorder.main_contract_list)
            main_contract = self.app.recorder.get_main_contract_by_code("ap")
            if main_contract:
                self.instrument_set.add(main_contract.local_symbol)
            # print(app.recorder.get_contract("ag1912.SHFE"))


def create_app():
    app = CtpBee("last", __name__, action_class=ActionMe, logger_class=Vlog, refresh=True,
                 risk=RiskMe)

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

    """ 启动 """
    return [app]


if __name__ == '__main__':
    # 7*24 小时运行模块
    # hickey.start_all(app_func=create_app, in_front=700)
    app = create_app()
    app[0].start()
