from time import sleep

from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import *


class Main(CtpbeeApi):
    def __init__(self, code="ag2406"):
        super().__init__(code)
        self.init = False
        self.ok = 0
        self.pos = None
        self.pos_init = False
        self.code = code
        self.mapping = {}

    def on_tick(self, tick: TickData) -> None:
        if self.init and self.ok == 0:
            self.action.buy_open(int(tick.ask_price_1) + 10, 1, tick)
            self.ok = 1

    def on_trade(self, trade: TradeData) -> None:
        # 成交回报单独回报
        print("成交回报", trade)
        pos = self.center.get_position(f"{self.code}.SHFE")
        print(pos.long_volume, pos.short_volume)

    def on_order(self, order: OrderData) -> None:
        # 报单回报函数
        if self.init:
            print("订单回报: ", order)
        print(order)

    def on_contract(self, contract: ContractData):
        # 合约信息回报函数
        # if contract.symbol == self.code:
        #     self.action.subscribe(contract.local_symbol)
        if len(contract.symbol) > 6:
            return
        strs = "".join(filter(str.isalpha, contract.symbol))
        # print(strs)
        self.mapping[strs] = contract.pricetick

    def on_realtime(self):
        # 定期触发函数 注意 因为函数执行时间的远古 会不断产生偏移
        pass

    def on_init(self, init: bool):
        # 此API被回调完成后告知策略执行成功
        self.init = True
        self.info("init success")
        print(self.mapping)


if __name__ == '__main__':
    app = CtpBee("market", __name__, refresh=True)
    example = Main("rb2510")
    app.config.from_json("config_24.json")
    app.add_extension(example)
    app.start(log_output=True)
