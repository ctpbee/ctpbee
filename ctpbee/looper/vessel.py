"""
回测容器模块, 回测
"""
import os
from threading import Thread
from time import sleep

from ctpbee.log import VLogger
from ctpbee.looper.data import VessData
from ctpbee.looper.interface import LocalLooper
from ctpbee.cprint_config import CP

class LooperApi:
    def __init__(self, name):
        self.name = name

    def on_bar(self, bar):
        raise NotImplemented

    def on_tick(self, tick):
        raise NotImplemented

    def on_trade(self, trade):
        raise NotImplemented

    def on_order(self, order):
        raise NotImplemented

    def on_position(self, position):
        raise NotImplemented

    def on_account(self, account):
        raise NotImplemented

    def on_contract(self, contract):
        raise NotImplemented

    def init_params(self, data):
        """ 用户需要继承此方法"""
        # print("我在设置策略参数")


class LooperLogger:
    def __init__(self, v_logger=None):
        if v_logger:
            self.logger = v_logger
        else:
            self.logger = VLogger(CP,app_name="Vessel")
            self.logger.set_default(name=self.logger.app_name, owner='App')

    def info(self, msg, **kwargs):
        self.logger.info(msg, owner="Looper", **kwargs)

    def error(self, msg, **kwargs):
        self.logger.error(msg, owner="Looper", **kwargs)

    def debug(self, msg, **kwargs):
        self.logger.debug(msg, owner="Looper", **kwargs)

    def warning(self, msg, **kwargs):
        self.logger.warning(msg, owner="Looper", **kwargs)

    def __repr__(self):
        return "LooperLogger -----> just enjoy it"


class Vessel:
    """
    策略运行容器

    本地回测与在线数据回测
    >> 基于在线数据推送的模式 是否可以减少本机器的内存使用量

    """

    def __init__(self, logger_class=None, pattern="T0"):
        self.ready = False
        self.looper_data: VessData = None
        if logger_class:
            self.logger = logger_class()
        else:
            self.logger = LooperLogger()

        self.risk = None
        self.strategy = None
        self.interface = LocalLooper(logger=self.logger, strategy=self.strategy, risk=self.risk)
        self.params = dict()
        self.looper_pattern = pattern

        """
        _data_status : 数据状态, 准备就绪时候应该被修改为True
        _looper_status: 回测状态, 分为五个
            "unready": 未就绪
            "ready":就绪
            "running": 运行中
            "stopped":暂停
            "finished":结束
        _strategy_status: 策略状态, 载入后应该被修改True
        _risk_status: "风控状态"
        """
        self._data_status = False
        self._looper_status = "unready"
        self._strategy_status = False
        self._risk_status = True

    def add_strategy(self, strategy):
        """ 添加策略到本容器 """
        self.strategy = strategy

        self.interface.update_strategy(strategy)
        self._strategy_status = True

        self.check_if_ready()

    def add_data(self, data):
        """ 添加data到本容器, 如果没有经过处理 """
        d = VessData(data)
        self.looper_data = d
        self._data_status = True
        self.check_if_ready()

    def check_if_ready(self):
        if self._data_status and self._strategy_status and self._risk_status:
            self._looper_status = "ready"
        self.ready = True

    def add_risk(self, risk):
        """ 添加风控 """
        self._risk_status = True
        self.interface.update_risk(risk)
        self.check_if_ready()

    def set_params(self, params):
        if not isinstance(params, dict):
            raise ValueError(f"配置信息格式出现问题， 你当前的配置信息为 {type(params)}")
        self.params = params

    def get_result(self):
        """ 计算回测结果，生成回测报告 """
        return self.interface.account.result

    def letsgo(self, parmas, ready):
        if self.looper_data.init_flag:
            self.logger.info(f"产品: {self.looper_data.product}")
            self.logger.info(f"回测模式: {self.looper_pattern}")
        for x in range(self.looper_data.length):
            if ready:
                """ 如果处于就绪状态 那么直接开始继续回测 """
                try:
                    p = next(self.looper_data)
                    self.interface(p, parmas)

                except StopIteration:
                    self._looper_status = "finished"
                    break
            else:
                """ 如果处于未就绪状态 那么暂停回测 """
                sleep(1)
        self.logger.info("回测结束,正在生成回测报告")

    def suspend_looper(self):
        """ 暂停回测 """
        self.ready = False
        self._looper_status = "stopped"

    def enable_looper(self):
        """ 继续回测 """
        self.ready = True
        self._looper_status = "running"

    @property
    def looper_status(self):
        return self._looper_status

    @property
    def risk_status(self):
        return self._risk_status

    @property
    def data_status(self):
        return self._data_status

    @property
    def strategy_status(self):
        return self._strategy_status

    @property
    def status(self):
        return (self._looper_status, self._risk_status, self._strategy_status, self._data_status)

    def run(self):
        """ 开始运行回测 """
        p = Thread(name="looper", target=self.letsgo, args=(self.params, self.ready,))
        p.start()
        p.join()

    def __repr__(self):
        return "ctpbee Backtesting Vessel powered by ctpbee current version: 0.1"
