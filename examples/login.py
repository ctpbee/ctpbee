"""
此策略为AI生成 不构成实际交易基础
请进行修改
"""

from ctpbee_kline import Kline
from strategy.atr_strategy import ATRStrategy

from ctpbee import CtpBee, CtpbeeApi
from ctpbee.constant import *

"""
此处替换继承的策略类
ATRStrategy
BollingerStrategy
DoubleMa
MACDStrategy
RSIStrategy
"""


class CTA(ATRStrategy):
    def on_contract(self, contract: ContractData) -> None:
        if len(contract.symbol) > 6:
            return
        if contract.symbol in self.instrument_set:
            self.action.subscribe(contract.local_symbol)
            self.info("subscribe: ", contract.local_symbol)

    def on_tick(self, tick: TickData) -> None:
        pass

    def on_realtime(self):
        print(self.center.get_position("ag2602.SHFE"))

    def on_init(self, init: bool):
        # 此API被回调完成后告知策略执行成功
        self.init = True
        self.info("init success")


if __name__ == "__main__":
    kline = Kline()
    app = CtpBee(
        "market",
        __name__,
    ).with_tools(kline)
    cta = CTA("all", "ag2602")
    # app.config.from_json("config.json")
    # 使用simnow 24小时
    app.config.from_json("config_24.json")
    app.add_extension(cta)
    app.start(log_output=True)
