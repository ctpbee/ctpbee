# coding:utf-8
import os
import sys
from time import sleep

from werkzeug.datastructures import ImmutableDict

from ctpbee.helpers import locked_cached_property, find_package
from ctpbee.exceptions import ConfigError
from ctpbee.record import Recorder
from ctpbee.context import proxy
from ctpbee.ctp import BeeMdApi, BeeTdApi
from ctpbee.config import Config
from ctpbee.func import DataSolve
from ctpbee.event_engine import controller


class CtpBee(object):
    """默认的设置"""
    default_config = ImmutableDict(
        dict(LOG_OUTPUT=True, TD_FUNC=False, MD_FUNC=True, TICK_DB="tick_me", XMIN=[], ALL_SUBSCRIBE=False))
    config_class = Config

    # 数据记录载体
    recorder = Recorder()

    __active = False

    #  交易api与行情api
    market = None
    trader = None
    import_name = None

    # 插件系统
    extensions = {}

    def __init__(self, import_name, instance_path=None):
        """this will be developed in the next version"""
        self.import_name = import_name
        if instance_path is None:
            instance_path = self.auto_find_instance_path()
        elif not os.path.isabs(instance_path):
            raise ValueError(
                'If an instance path is provided it must be absolute.'
                ' A relative path was given instead.'
            )
        self.instance_path = instance_path
        self.config = self.make_config()
        proxy.push(self)

    def make_config(self):
        """ 生成class类"""
        defaults = dict(self.default_config)
        return self.config_class(self.instance_path, defaults)

    def auto_find_instance_path(self):
        prefix, package_path = find_package(self.import_name)
        if prefix is None:
            return os.path.join(package_path)
        return os.path.join(prefix, 'var', self.name + '-instance')

    def _load_ext(self):
        self.__active = True
        if "CONNECT_INFO" in self.config.keys():
            info = self.config.get("CONNECT_INFO")
        else:
            raise ConfigError(message="没有相应的登录信息", args=("没有发现登录信息",))
        if self.config.get("TD_FUNC"):
            self.trader = BeeTdApi()
            self.trader.connect(info)
            sleep(1)
        self.market = BeeMdApi()
        self.market.connect(info)

    @locked_cached_property
    def name(self):
        if self.import_name == '__main__':
            fn = getattr(sys.modules['__main__'], '__file__', None)
            if fn is None:
                return '__main__'
            return os.path.splitext(os.path.basename(fn))[0]
        return self.import_name

    def start(self, log_output=True):
        """init data process extension and start engine to process data."""
        self.extensions['data_pointer'] = DataSolve()
        self.config["LOG_OUTPUT"] = log_output
        controller.start()
        self._load_ext()
