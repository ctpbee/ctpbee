"""
下单示例
"""

from ctpbee import CtpbeeApi, helper, CtpBee
from ctpbee.constant import ContractData, LogData, TickData, BarData, OrderType, Offset, OrderData, \
    TradeData, PositionData, Direction, AccountData, Exchange


class Demo(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.instrument_set = ["rb2101.SHFE"]
        self.isok = False

    def on_contract(self, contract: ContractData):
        """ 处理推送的合约信息 """
        if contract.local_symbol in self.instrument_set:
            self.app.subscribe(contract.local_symbol)

    def on_log(self, log: LogData):
        """ 处理日志信息 ,特殊需求才用到 """
        pass

    def on_tick(self, tick: TickData) -> None:
        """ 处理推送的tick """
        # print(self.center.positions)
        # if not self.isok:
        # print(tick.datetime, tick.symbol)
        #     return
        # print(self.center.get_position("rb2010.SHFE"))
        # print(tick.datetime, tick.last_price)

    def on_bar(self, bar: BarData) -> None:
        """ 处理ctpbee生成的bar """
        print(bar.interval, bar.datetime, bar.close_price, bar.volume)
        # self.action.cover(bar.close_price, 1, bar, price_type=OrderType.MARKET)

    def on_init(self, init):
        if init:
            self.isok = True
            print("初始化完成")

    def on_order(self, order: OrderData) -> None:
        """ 报单回报 """
        pass

    def on_trade(self, trade: TradeData) -> None:
        """ 成交回报 """

    def on_position(self, position: PositionData) -> None:
        """ 处理持仓回报 """

    def on_account(self, account: AccountData) -> None:
        """ 处理账户信息 """


def letsgo():
    app = CtpBee(name="demo", import_name=__name__, refresh=True)
    # 创建对象
    demo = Demo("test")
    # 添加对象, 你可以继承多个类 然后实例化不同的插件 再载入它, 这些都是极其自由化的操作
    app.add_extension(demo)

    app.config.from_json("config.json")
    app.start(log_output=True)
    # 单独开一个线程来进行查询持仓和账户信息


if __name__ == '__main__':
    letsgo()
