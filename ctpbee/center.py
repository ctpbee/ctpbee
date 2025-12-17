"""
ctpbee里面的核心数据访问模块

此模块描述了ctpbee里面默认的数据访问中心,同时它也可以被回测模块所调用

"""

from abc import ABC
from typing import Text, List

from ctpbee.constant import (
    Direction,
    TickData,
    ContractData,
    OrderData,
    TradeData,
    AccountData,
)


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
    v_ext = ["exchange", "symbol", "local_symbol"]
    u_ext = ["direction", "local_position_id"]

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
        """返回"""
        if item not in self.__dict__.keys():
            return Missing.create_obj(item)
        return self.__dict__[item]

    def __setattr__(self, key, value):
        """拦截任何设置属性的操作 它应该不运行任何关于set的操作"""
        self.__dict__[key] = value


class Center(BasicCenterModel, dict):
    """
    本来作为集成类,并不附加多少额外功能,主要是将其他模块的函数功能统一集中过来,
    达到一种统一接口的方式
    整齐高于混乱
    """

    def __init__(self, app):
        dict.__init__(self)
        self.app = app

    def __getitem__(self, extension_name):
        """
        重写此处API
        item应该作为插件名字
        """
        return self.app._extensions.get(extension_name, None)

    def __delitem__(self, key):
        import warnings

        warnings.warn("警告,操作危险！你现在不具备这种操作权限,请调用账户级别的API")
        return

    def __str__(self):
        return "ctpbee 统一数据调用接口"

    @property
    def orders(self) -> List[OrderData]:
        """返回所有的报单"""
        return self.app.recorder.get_all_orders()

    @property
    def last_order_id(self) -> str:
        """
        返回最新的一个orderid
        """
        if not self.orders:
            return None
        return self.orders[-1].order_id

    @property
    def last_order(self) -> OrderData:
        """
        返回最新的一个报单
        """
        if not self.orders:
            return None
        return self.orders[-1]

    @property
    def active_orders(self) -> List[OrderData]:
        """
        返回所有的未成交单
        """
        return self.app.recorder.get_all_active_orders()

    @property
    def trades(self) -> List[TradeData]:
        """
        返回所有的成交单
        """
        return self.app.recorder.get_all_trades()

    @property
    def account(self) -> AccountData:
        """
        返回账户信息
        """
        return self.app.recorder.get_account()

    @property
    def positions(self):
        """
        返回所有的仓位信息
        """
        return self.app.recorder.position_manager.get_all_positions()

    @property
    def snapshot(self):
        """
        返回所有行情的切面快照
        """
        return self.app.recorder.ticks

    def get_tick(self, local_symbol) -> List[TickData] or None:
        """
        获取指定合约的tick数列信息
        在合约不存在的情况返回为空

        Args:
          local_symbol(Text): 合约代码
        """
        try:
            return self.app.recorder.get_tick(local_symbol)
        except IndexError:
            return Missing.create_obj("get_tick")

    def get_contract(self, local_symbol: Text) -> ContractData or None:
        """
        获取指定合约信息

        Args:
          local_symbol(Text): 合约代码

        Return:
          ContractData: 合约信息
        """
        return self.app.recorder.get_contract(local_symbol)

    def get_active_order(self, local_symbol) -> List[OrderData]:
        """
        拿到指定合约的未成交单子

        Args:
          local_symbol(Text): 合约代码

        Return:
            List[OrderData]
        """
        return self.app.recorder.get_all_active_orders(local_symbol)

    def get_position(self, local_symbol: str) -> PositionModel or None:
        """
        返回指定合约的持仓信息
        注意你返回是一个PositionModel对象

        Args:
          local_symbol(Text): 合约代码

        Examples:
          ag_model = self.get_position("ag1912.SHFE")
          打印持仓信息
          print(ag_model.long_volume)
        """
        return self.app.recorder.position_manager.get_position(local_symbol)
