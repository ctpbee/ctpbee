"""
回测容器模块, 回测
"""
from multiprocessing import Process
from time import sleep

from ctpbee.log import VLogger
from ctpbee.looper.account import Account
from ctpbee.looper.data import VessData
from ctpbee.looper.interface import LocalLooper


class LooperLogger:
    def __init__(self, v_logger=None):
        if v_logger:
            self.logger = v_logger
        else:
            self.logger = VLogger("Vessel")

    def info(self, msg, **kwargs):
        self.logger.info(msg=msg, extra={"owner": "Looper"}, **kwargs)

    def error(self, msg, **kwargs):
        self.logger.error(msg=msg, extra={"owner": "Looper"}, **kwargs)

    def debug(self, msg, **kwargs):
        self.logger.debug(msg=msg, extra={"owner": "Looper"}, **kwargs)

    def warning(self, msg, **kwargs):
        self.logger.warning(msg=msg, extra={"owner": "Looper"}, **kwargs)

    def __repr__(self):
        return "LooperLogger -----> just enjoy it"


class Vessel:
    """
    策略运行容器

    本地回测与在线数据回测
    >> 基于在线数据推送的模式 是否可以减少本机器的内存使用量

    """

    def __init__(self, pattern="T0"):
        self.ready = False
        self.looper_data: VessData = None
        self.logger = LooperLogger()
        self.account = Account()
        self.risk = None
        self.strategy = None
        self.interface = LocalLooper(self.strategy, risk=self.risk, account=self.account, logger=self.logger)
        self.params = dict()
        self.looper_pattern = pattern

    def add_strategy(self, strategy):
        """ 添加策略到本容器 """
        self.strategy = strategy
        self.interface

    def add_data(self, data):
        """ 添加data到本容器, 如果没有经过处理 """
        d = VessData(data)
        d.convert_data_to_inner()
        self.looper_data = d

    def add_risk(self, risk):
        """ 添加风控 """
        pass

    def cal_result(self):
        """ 计算回测结果，生成回测报告 """
        return None

    def letsgo(self, parmas, ready):
        if self.looper_data.init_flag:
            self.logger.info(f"数据提供商: {self.looper_data.provider}")
            self.logger.info(f"产品: {self.looper_data.product}")
            self.logger.info(f"回测模式: {self.looper_pattern}")
        while True:
            if ready:
                """ 如果处于就绪状态 那么直接开始继续回测 """
                try:
                    p = next(self.looper_data)
                    self.interface(p, parmas)
                except StopIteration:
                    break
            else:
                """ 如果处于未就绪状态 那么暂停回测 """
                sleep(1)
        self.logger.info("回测结束,正在生成回测报告")
        result = self.cal_result()
        return result

    def suspend_looper(self):
        """ 暂停回测 """
        self.ready = False

    def enable_looper(self):
        """ 继续回测 """
        self.ready = True

    def run(self):
        """ 开始运行回测 """
        p = Process(name="looper", target=self.letsgo, args=(self.params, self.ready,))
        p.start()
