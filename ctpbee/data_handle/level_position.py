import io
import os
from json import load, dump, JSONDecodeError

from ctpbee.constant import TradeData, PositionData


class PositionModel:

    def __init__(self, local_symbol):
        self.local_symbol = local_symbol

        # 持仓方向
        self.direction = None

        # 昨日持仓
        self.y_pos: int = 0

        # 今日持仓
        self.t_pos: int = 0

        # 持仓均价
        self.price: float = 0

        # 持仓数目
        self.volume: int = 0

        # 交易所代码
        self.exchange = None

        # 网关名字
        self.gateway_name = None

    def update_trade(self, trade):
        """根据立即成交的信息来更新本地持仓 """
        self.direction = trade.direction
        cost = self.price * self.volume
        cost += trade.volume * trade.price
        new_pos = self.volume + trade.volume
        if new_pos:
            self.price = cost / new_pos
        else:
            self.price = 0

    def update_postition(self, position: PositionData):
        """ 根据返回的查询持仓信息来更新持仓信息 """
        self.t_pos = position.volume - position.yd_volume
        self.y_pos = position.yd_volume
        self.exchange = position.exchange
        self.price = position.price
        self.volume = position.volume
        self.direction = position.direction
        self.gateway_name = position.gateway_name

    def to_dict(self):
        """ 将持仓信息构建为字典的信息"""
        return {
            "direction": self.direction,
            "y_pos": self.y_pos,
            "t_pos": self.t_pos
        }

    def to_position(self):
        """ 返回为持仓 """
        try:
            return PositionData(symbol=self.local_symbol.split(".")[0], exchange=self.exchange, volume=self.volume,
                                price=self.price)
        except Exception:
            raise ValueError(f"本地维护符号有问题,请检查,当前符号为{self.local_symbol}")

    def to_df(self):
        """ 将持仓信息构建为DataFrame """
        pass

    @classmethod
    def create_model(cls, local, **kwargs):
        """
        根据字典数据创建PositionModel实例
        """
        instance = cls(local)
        {setattr(instance, key, value) for key, value in kwargs.items()}
        return instance


class ApiPositionManager(dict):

    def __init__(self, name, cache_path=None, init_flag: bool = False):
        """
        策略持仓管理的基本信息,注意你需要确保没有在其他地方进行下单， 否则会影响到持仓信息的准确性
        * name: 策略名称
        * cache_path： 缓存文件地址,注意如果是默认的策略持仓参数会被放置到用户目录下的.ctpbee/api目录下
        """
        self.filename = name + ".json"
        dict.__init__(self)
        self.cache_path = cache_path
        file_path = cache_path + "/" + self.filename
        with open(file_path, "w+") as f:
            if init_flag:
                data = {}
                dump(obj=data, fp=f)
            else:
                try:
                    data = load(f)
                except JSONDecodeError:
                    data = {}
                    dump(obj=data, fp=f)

        self.init_data(data)

    def init_data(self, data):
        """
        初始化数据
        """

        def create_position_model(local, data: dict):
            """
            将地点数据解析为PositionModel
            """
            return PositionModel.create_model(local, **data)

        if not data:
            return
        else:
            for local, position_detail in data:
                self[local] = create_position_model(local, position_detail)

    def on_trade(self, trade: TradeData):
        """
        更新成交单
        """
        local = trade.local_symbol + "." + trade.direction.value
        if local not in self.keys():
            self[local] = PositionModel(local_symbol=trade.local_symbol)

        self[local].update_trade(trade=trade)

    def on_order(self, order):
        pass

    def on_position(self, position: PositionData):
        """
        更新持仓
        """
        local = position.local_symbol + "." + position.direction.value
        if local not in self.keys():
            self[local] = PositionModel(local_symbol=position.local_symbol)

        self[local].update_position(position=position)

    def get_position_by_ld(self, local_symbol, direction) -> PositionModel:
        """ 通过local_symbol和direction获得持仓信息 """
        return self[local_symbol + "." + direction.value]
