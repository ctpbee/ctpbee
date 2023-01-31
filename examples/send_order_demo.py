"""
下单示例
"""

from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import ContractData, LogData, TickData, BarData, OrderData, \
    TradeData, PositionData, AccountData


class Demo(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.instrument_set = ["rb2101.SHFE"]
        self.isok = False

    def on_contract(self, contract: ContractData):
        """ 处理推送的合约信息 """
        if contract.local_symbol in self.instrument_set:
            self.app.subscribe(contract.local_symbol)

    def on_tick(self, tick: TickData) -> None:
        """ 处理推送的tick """
        if not self.isok:
            return None

        self.action.buy_open(tick.ask_price_1, 1, tick)
        self.action.buy_close(tick.bid_price_1, 1, tick)

    def on_init(self, init):
        if init:
            self.isok = True

    def on_order(self, order: OrderData) -> None:
        """ 报单回报 """
        pass

    def on_trade(self, trade: TradeData) -> None:
        """ 成交回报 """
        # print(trade, "\n")

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
