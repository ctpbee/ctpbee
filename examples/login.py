"""
此策略为AI生成 不构成实际交易基础
请进行修改
"""

from ctpbee_kline import Kline

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


class CTA(CtpbeeApi):
    def __init__(
        self,
        name,
    ) -> None:
        super().__init__(name)

    def on_contract(self, contract: ContractData) -> None:
        if len(contract.symbol) > 6:
            return
        self.action.subscribe(contract.local_symbol)
        print("subscribe: ", contract.local_symbol)

    def on_tick(self, tick: TickData) -> None:
        """
        可以在此处做出tick级别的止损
        """
        print(tick)

    def on_init(self, init: bool):
        # 此API被回调完成后告知策略执行成功
        self.init = True
        self.info("init success")


if __name__ == "__main__":
    kline = Kline()
    app = CtpBee("market", __name__, refresh=True).with_tools(kline)
    cta = CTA("all")
    # app.config.from_json("config.json")
    # 使用simnow 24小时
    app.config.from_json("config_24.json")
    app.add_extension(cta)
    app.start(log_output=True)
