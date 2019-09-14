"""
回测容器模块, 回测
"""
from multiprocessing import Process

from ctpbee.log import VLogger
from ctpbee.looper.account import Account
from ctpbee.looper.data import VessData
from ctpbee.looper.interface import LocalLooper


class Vessel:
    """
    策略运行容器
    """

    def __init__(self):
        self.ready = False
        self.looper_data: VessData = None
        self.logger = VLogger("Vessel")
        self.account = Account()
        self.risk = None
        self.strategy = None
        self.interface = LocalLooper(self.strategy, risk=self.risk, account=self.account)
        self.looper_pattern = ""

    def add_strategy(self, strategy):
        """ 添加策略到本容器 """
        pass

    def add_data(self, data):
        """ 添加data到本容器, 如果没有经过处理 """
        d = VessData(data)
        d.convert_data_to_inner()
        self.looper_data = d
        # todo: 根据添加的数据类型来知晓回测类型 以及产品

    def add_risk(self, risk):
        """ 添加风控 """

    def cal_result(self):
        """ 计算回测结果，生成回测报告 """
        return None

    def letsgo(self):
        if self.looper_data.init_flag:
            self.logger.info(f"数据提供商: {self.looper_data.provider}")
            self.logger.info(f"产品: {self.looper_data.product}")
        while True:
            try:
                p = next(self.looper_data)
                self.interface(p)
            except StopIteration:
                break

        self.logger.info("回测结束,正在生成回测报告")
        result = self.cal_result()
        return result

    def run(self):
        """ 开始运行回测 """
        p = Process(target=self.letsgo)
        p.start()
