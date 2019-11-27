"""
ctpbee里面的核心数据访问模块

此模块描述了ctpbee里面默认的数据访问中心，同时它也可以被回测模块所调用
整齐高于混乱
"""
from abc import ABC


class Missing:
    def __str__(self):
        return "属性缺失/ Attribute Missing"


missing = Missing()


class PositionModel:

    def __init__(self, iterable):
        pass

    def pos_long(self):
        """ 长头持仓 """

    def pos_short(self):
        """ 空头持仓 """


class BasicCenterModel(ABC):
    __dict__ = {}

    def __new__(cls, app):
        # temp = cls.__init__(cls, app)
        super(BasicCenterModel, cls).__new__(cls)

    def __getattr__(self, item):
        """ 返回"""
        if item not in self.__dict__:
            return missing

    def __setattr__(self, key, value):
        """ 拦截任何设置属性的操作 它应该不运行任何关于set的操作 """
        return


class Center(BasicCenterModel):

    def __init__(self, app):
        super().__init__(app)

    def __str__(self):
        return "ctpbee 统一数据调用接口"

    @property
    def orders(self):
        """ 返回所有的报单 """
        return self.app.recorder.get_all_orders()

    @property
    def active_orders(self):
        """ 返回所有的为成交单 """
        return self.app.recorder.get_all_active_orders()

    @property
    def trades(self):
        """ 返回所有的成交单 """
        return self.app.recorder.get_all_trades()

    @property
    def account(self):
        return self.app.recorder.get_account()

    def get_tick(self, local_symbol):
        """ 获取指定合约最近的一条tick"""
        try:
            return self.app.recorder.get_tick(local_symbol)[:-1]
        except IndexError:
            return missing

    def get_active_order(self, local_symbol):
        """ 拿到指定合约的最佳"""
        return self.app.recorder.get_all_active_orders(local_symbol)

    def get_position(self, local_symbol):
        """ 返回指定合约的持仓信息 """


