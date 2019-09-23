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
            self.logger = VLogger(app_name="Vessel")

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

    def __init__(self, pattern="T0"):
        self.ready = False
        self.looper_data: VessData = None
        self.logger = LooperLogger()
        self.account = Account()
        self.risk = None
        self.strategy = None
        self.interface = LocalLooper(logger=self.logger, strategy=self.strategy, risk=self.risk, account=self.account)
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
        self._risk_status = False

    def add_strategy(self, strategy):
        """ 添加策略到本容器 """
        self.strategy = strategy 
        try:
            self.interface.update_strategy(strategy)
            self._strategy_status = True
        except Exception:
            self._strategy_status = False
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

    def add_risk(self, risk):
        """ 添加风控 """
        self._risk_status = True
        self.interface.update_risk(risk)
        self.check_if_ready()

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
                    self._looper_status = "finished"
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
        p = Process(name="looper", target=self.letsgo, args=(self.params, self.ready,))
        p.start()


if __name__ == '__main__':
    main = Vessel()
