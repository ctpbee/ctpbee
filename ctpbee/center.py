"""
ctpbee里面的核心数据访问模块

此模块描述了ctpbee里面默认的数据访问中心，同时它也可以被回测模块所调用

"""
from abc import ABC

from ctpbee.constant import Direction


class Missing:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"> {self.name}  [属性缺失 / Attribute Missing]"

    @classmethod
    def create_obj(cls, name):
        return Missing(name=name)


class PositionModel(dict):
    """
    单个合约的标准持仓对象
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    v_ext = ['exchange', 'symbol', "local_symbol"]
    u_ext = ['direction', 'local_position_id']

    def __init__(self, long, short):
        dict.__init__(self)
        self._update_attr(long, "long")
        self._update_attr(short, "short")

    def _update_attr(self, attr, direction):
        if direction == "long":
            for i, v in attr._to_dict().items():
                if i in self.v_ext:
                    setattr(self, i, v)
                elif i in self.u_ext:
                    continue
                else:
                    setattr(self, "long_" + i, v)

        elif direction == "short":
            for i, v in attr._to_dict().items():
                if i in self.v_ext:
                    setattr(self, i, v)
                elif i in self.u_ext:
                    continue
                else:
                    setattr(self, "short_" + i, v)


class BasicCenterModel(ABC):
    __dict__ = {}

    def __getattr__(self, item):
        """ 返回"""

        if item not in self.__dict__.keys():
            return Missing.create_obj(item)
        return self.__dict__[item]

    def __setattr__(self, key, value):
        """ 拦截任何设置属性的操作 它应该不运行任何关于set的操作 """
        self.__dict__[key] = value


class Center(BasicCenterModel, dict):
    """
    本来作为集成类，并不附加多少额外功能，主要是将其他模块的函数功能统一集中过来，
    达到一种统一接口的方式
    整齐高于混乱
    """

    def __init__(self, app):
        dict.__init__(self)
        self.app = app

    def __getitem__(self, extension_name):
        """ 重写此处API
            item应该作为插件名字
        """
        return self.app._extensions.get(extension_name, None)

    def __delitem__(self, key):
        import warnings
        warnings.warn("警告，操作危险！你现在不具备这种操作权限，请调用账户级别的API")
        return

    def __str__(self):
        return "ctpbee 统一数据调用接口"

    @property
    def orders(self):
        """ 返回所有的报单 """
        return self.app.recorder.get_all_orders()

    @property
    def last_order_id(self):
        return self.orders[-1].order_id

    @property
    def last_order(self):
        return self.orders[-1]

    @property
    def active_orders(self):
        """ 返回所有的未成交单 """
        return self.app.recorder.get_all_active_orders()

    @property
    def trades(self):
        """ 返回所有的成交单 """
        return self.app.recorder.get_all_trades()

    @property
    def account(self):
        return self.app.recorder.get_account()

    @property
    def positions(self):
        return self.app.recorder.position_manager.get_all_positions()

    def get_tick(self, local_symbol):
        """ 获取指定合约最近的一条tick"""
        try:
            return self.app.recorder.get_tick(local_symbol)[:-1]
        except IndexError:
            return Missing.create_obj("get_tick")

    def get_active_order(self, local_symbol):
        """ 拿到指定合约的未成交单子"""
        return self.app.recorder.get_all_active_orders(local_symbol)

    def get_position(self, local_symbol) -> PositionModel:
        """
        返回指定合约的持仓信息
        注意你返回是一个PositionModel对象
        for exmaple:
            ag_model = self.get_position("ag1912.SHFE")
            打印长头持仓数目
            print(ag_model.long_pos)
        """
        position_long = self.app.recorder.position_manager.get_position_by_ld(local_symbol, Direction.LONG)
        position_short = self.app.recorder.position_manager.get_position_by_ld(local_symbol, Direction.SHORT)
        if position_short is None and position_long is None:
            return None
        else:
            return PositionModel(position_long, position_short)
