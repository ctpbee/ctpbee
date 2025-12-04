from ctpbee import  CtpBee
from ctpbee.constant import *
from ctpbee_kline import Kline
from strategy import ATRStrategy

# 此处替换继承的策略类 
"""
可替换策略类型
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
        
    def on_init(self, init: bool):
        # 此API被回调完成后告知策略执行成功
        self.init = True
        self.info("init success")


if __name__ == '__main__':
    kline = Kline()
    app = CtpBee("market", __name__, refresh=True).with_tools(kline)
    example = CTA("rb2605", "rb2605")
    app.config.from_json("config_24.json")
    app.add_extension(example)
    app.start(log_output=True)
