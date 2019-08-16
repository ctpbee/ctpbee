from threading import Thread
from time import sleep

from ctpbee import CtpbeeApi, helper, CtpBee
from ctpbee.constant import ContractData, LogData, TickData, BarData, OrderType, Offset, OrderData, SharedData, \
    TradeData, PositionData, Direction, AccountData


class Demo(CtpbeeApi):
    contract_set = set(["rb1910"])

    # 当前插件绑定的CtpBee的数据记录信息都在self.app.recorder下面

    def on_contract(self, contract: ContractData):
        """ 处理推送的合约信息 """
        if contract.symbol in self.contract_set:
            self.app.subscribe(contract.symbol)

    def on_log(self, log: LogData):
        """ 处理日志信息 ,特殊需求才用到 """

        pass

    def on_tick(self, tick: TickData) -> None:
        """ 处理推送的tick """
        pass

    def on_bar(self, bar: BarData) -> None:
        """ 处理ctpbee生成的bar """
        # 构建发单请求
        req = helper.generate_order_req_by_var(symbol=bar.symbol, exchange=bar.exchange, price=bar.high_price,
                                               direction=Direction.LONG, type=OrderType.LIMIT, volume=3,
                                               offset=Offset.OPEN)
        # 调用绑定的app进行发单
        id = self.app.send_order(req)
        print("返回id", id)

        sleep(1)

    def on_order(self, order: OrderData) -> None:
        """ 报单回报 """
        print("order", order)

    def on_shared(self, shared: SharedData) -> None:
        pass

    def on_trade(self, trade: TradeData) -> None:
        """ 成交回报 """
        print("成交", trade)

    def on_position(self, position: PositionData) -> None:
        """ 处理持仓回报 """

    def on_account(self, account: AccountData) -> None:
        """ 处理账户信息 """


def letsgo():
    app = CtpBee(name="demo", import_name=__name__)
    # 创建对象
    demo = Demo("test")
    # 添加对象, 你可以继承多个类 然后实例化不同的插件 再载入它, 这些都是极其自由化的操作
    app.add_extension(demo)
    app.config.from_json("config.json")
    app.start()

    def query(time=1):
        nonlocal app
        while True:
            app.query_position()
            sleep(time)
            app.query_account()
            sleep(time)

    # 单独开一个线程来进行查询持仓和账户信息
    p = Thread(target=query, args=(2,))
    p.setDaemon(daemonic=True)
    p.start()


if __name__ == '__main__':
    letsgo()
