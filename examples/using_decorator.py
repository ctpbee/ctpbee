from datetime import datetime
from time import sleep

from ctpbee import Action, hickey
from ctpbee import CtpBee
from ctpbee import CtpbeeApi
from ctpbee import RiskLevel
from ctpbee import VLogger


class Vlog(VLogger):

    def handler_record(self, record):
        """ 处理日志信息代码 """
        print(record)


class ActionMe(Action):

    def __init__(self, app):
        super().__init__(app)
        self.add_risk_check(self.short)
        self.add_risk_check(self.cancel)




class RiskMe(RiskLevel):

    def realtime_check(self, cur):
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
            if cal > 3: break
            cal += 1
            self.info("正在检查呢 ")
            # do something

    def realtime_check(self):
        """ """


api = CtpbeeApi(extension_name="hi")


@api.register()
def get_it(self, hel):
    print(hel)


@api.route(handler="bar")
def handle_bar(self, bar):
    """ """
    self.action.sell(bar.high_price, 1, bar)


@api.route(handler="tick")
def handle_tick(self, tick):
    """ """
    self.get_it("hhhh")
    print("当前时间: ", str(datetime.now()))
    print("tick时间: ", str(tick.datetime))


@api.route(handler="contract")
def handle_contract(self, contract):
    if contract.local_symbol == "zn1911.SHFE":
        self.app.subscribe(contract.local_symbol)


@api.route(handler="timer")
def realtime(self):
    """ """


@api.route(handler="position")
def handle_position(self, position):
    """ """


@api.route(handler="account")
def handle_account(self, account):
    """ """


@api.route(handler="order")
def handle_order(self, order):
    """ """


@api.route(handler="trade")
def handle_trade(self, trade):
    """ """


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
    app.add_extension(api)

    """ 启动 """
    return [app]


if __name__ == '__main__':
    hickey.start_all(app_func=create_app)
