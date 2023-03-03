from time import sleep

from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import *
from ctpbee import VLogger


@VLogger()
def process_log(**data):
    print(data)


from ctpbee import Tool
from ctpbee.constant import ToolRegisterType
from ctpbee.level import tool_register


class FTool(Tool):

    @tool_register(ToolRegisterType.TICK)
    def on_tick(self, tick: TickData):
        return tick.last_price

    @tool_register(ToolRegisterType.ORDER)
    def on_order(self, order: OrderData):
        return order.order_id

    @tool_register(ToolRegisterType.WHATEVER)
    def on_order(self, data):
        return "any data"


class Main(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.init = False

    def on_tick(self, tick: TickData) -> None:
        # if not self.init:
        #     return
        # else:
        #     self.action.sell_open(tick.last_price, 1, tick)
        #     self.init = False
        print("tick回报", tick)

    def on_trade(self, trade: TradeData) -> None:
        print("成交回报", trade)

    def on_account(self, account: AccountData) -> None:
        print("账户回报", account)

    def on_order(self, order: OrderData) -> None:
        print("订单回报: ", order)

    def on_position(self, position: PositionData) -> None:
        # print("持仓回报", position)
        pass

    def on_next_tick(self, price):
        print(price)

    def on_after_order(self, order_id):
        print("get order_id", order_id)

    def on_tool_data(self, data):
        print(data)

    def on_realtime(self):
        pass

    def on_contract(self, contract: ContractData):
        if contract.symbol == "rb2305":
            self.action.subscribe(contract.local_symbol)

    def on_init(self, init: bool):
        self.info("账户初始化成功回报")
        self.init = True
        # tool的tick回调
        self.subscribe("hello", self.on_next_tick, ToolRegisterType.TICK)
        # tool的order回调
        self.subscribe("hello", self.on_after_order, ToolRegisterType.ORDER)
        # tool的自定义数据流回调
        self.subscribe("hello", self.on_tool_data, ToolRegisterType.WHATEVER)


if __name__ == '__main__':
    tol = FTool("hello")
    app = CtpBee("market", __name__, refresh=True).with_tools(tol)
    example = Main("DailyCTA")
    app.config.from_json("config.json")
    app.add_extension(example)
    app.start(log_output=True)
