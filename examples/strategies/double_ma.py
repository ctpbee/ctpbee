"""
双均线策略实现

"""

from ctpbee import CtpbeeApi
from ctpbee.constant import BarData
from ctpbee.indicator import ArrayManager


class DoubleMa(CtpbeeApi):

    def __init__(self, name: str, code=None):
        # 初始化策略参数
        super().init_app(name)
        self.indicator = ArrayManager()

    def on_bar(self, bar: BarData) -> None:
        pass

    def on_realtime(self):
        pass
