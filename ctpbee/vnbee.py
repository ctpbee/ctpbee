import os

from ctpbee.exceptions import ConfigError
from ctpbee.record import Recorder
from ctpbee.context import proxy
from ctpbee.api import BeeMdApi, BeeTdApi
from ctpbee.config import Config
from ctpbee.event_engine import controller


class CtpBee:
    recorder = Recorder()
    config = Config(os.path.abspath(os.path.dirname(__file__)))
    __active = False
    market = None
    trader = None

    def __init__(self, name):
        self.name = name
        self.config.from_pyfile("base_setting.py")
        proxy.push(self)

    def _check_info(self):
        self.__active = True
        if "CONNECT_INFO" in self.config.keys():
            info = self.config.get("CONNECT_INFO")
        else:
            raise ConfigError(message="行情没有相应的登录信息", args=("没有发现行情登录信息",))
        self.market = BeeMdApi()
        self.market.connect(info)
        if self.config.get("TD_FUNC"):
            self.trader = BeeTdApi()
            self.trader.connect(info)

    def start(self, log_output=True):
        self.config["LOG_OUTPUT"] = log_output
        controller.start()
        self._check_info()
