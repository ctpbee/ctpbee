"""
回测容器模块, 回测
"""


class Vessel:
    """
    策略运行容器
    """

    def __init__(self):
        self.ready = False

    def add_strategy(self, strategy):
        """ 添加策略到本容器 """
        pass

    def add_data(self, data):
        """ 添加data到本容器, 如果没有经过处理 """

    def add_risk(self, risk):
        """ 添加风控 """

    def run(self):
        """ 开始运行回测 """
