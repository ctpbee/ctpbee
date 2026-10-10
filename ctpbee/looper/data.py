"""
回测数据模块
数据应该是需要被特殊处理的， 这样才可以达到最佳访问速度
todo: 优化数据访问速度
--------- >
"""
from datetime import datetime
from itertools import chain
from typing import Iterable, Tuple, Sized, Generator

# data_api 是未随 ctpbee 开源的可选数据包(见 app.add_basic_info 的 todo),
# 来自它的实体需要在回放时转成内部的 Bumblebee。
#
# 为什么要缓存探测结果: 【失败】的 import 不会写入 sys.modules, 每次尝试都要把
# PathFinder 的 sys.path 逐条拼接 + stat 走满一遍。last_bar 是每根 bar/tick 都
# 执行一次的回测主循环, 旧实现把这个 import 放在循环体里: cProfile 在 origin/dev
# 上量到每根 bar 9.1 次 nt.stat(19800 根 bar 共 179823 次), 一次 import 探测
# 1.2~1.8ms, 即回测总耗时的 ~8 成。此处改为至多探测一次。
#
# 取值: None 尚未探测 / () data_api 不可用 / (Tick, Kline) 可用类型。
# 空元组让 isinstance 恒为 False, 调用点因此不需要分支。
_DATA_API_TYPES = None


def data_api_types() -> tuple:
    """探测可选依赖 data_api 的 (Tick, Kline); 结果缓存, 至多 import 一次。

    Returns:
      tuple: data_api 可用时为 (Tick, Kline), 否则为空元组
    """
    global _DATA_API_TYPES
    if _DATA_API_TYPES is None:
        try:
            from data_api import Tick, Kline
        except ImportError:
            _DATA_API_TYPES = ()
        else:
            _DATA_API_TYPES = (Tick, Kline)
    return _DATA_API_TYPES


class Bumblebee(dict):
    """  """
    __slots__ = ['last_price', 'datetime', 'open_price', "high_price", "low_price", "close_price", "volume", "type",
                 "ask_price_1", "bid_price_1"]
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __getattribute__ = dict.get

    datetime_type = "datetime"

    def __init__(self, **kwargs):
        if "last_price" in kwargs:
            self['type'] = "tick"
        else:
            self['type'] = "bar"
        super().__init__(**kwargs)
        # 需要在此处自动转换datetime数据类型
        self.datetime = Bumblebee.covert_datetime(self.datetime)

    @staticmethod
    def covert_datetime(datetime_data):
        """
        此函数接受三种格式的数据转换过程
        :param datetime_data  str/int
        """
        if isinstance(datetime_data, datetime):
            return datetime_data
        if isinstance(datetime_data, str):
            """ 支持.f 或者非.f的构建 """
            try:
                return datetime.strptime(datetime_data, "%Y-%m-%d %H:%M:%S")
            except Exception:
                return datetime.strptime(datetime_data, "%Y-%m-%d %H:%M:%S.%f")
        if isinstance(datetime_data, int):
            """
            判断s/us/ns的转换
            """
            return datetime.fromtimestamp(datetime_data)


class VessData:
    def __init__(self, *data):
        self.inner_data = {}
        self.init_flag = False
        self.data: Tuple[Iterable, Sized] = data
        self.the_buffer = {}
        self.product_type = "future"
        if not isinstance(data, Iterable):
            raise ValueError("数据应为可迭代的数据")
        # 数据供应商默认设置为ctpbee
        # try:
        #     from data_api import Tick, Kline
        #     self.data_provider = "ctpbee"
        #     try:
        #         for i in data:
        #             if isinstance(i, Generator):
        #                 temp = next(i)
        #                 self.data_type = temp.type
        #                 self.the_buffer[temp.local_symbol] = temp
        #                 self.inner_data[temp.local_symbol] = i
        #             else:
        #                 temp = next(chain(i))
        #                 self.data_type = temp.type
        #                 self.the_buffer[temp.local_symbol] = temp
        #                 self.inner_data[temp.local_symbol] = chain(i)
        #         self.init_flag = True
        #     except Exception:
        #         raise ValueError("数据格式不合法")
        # except ModuleNotFoundError:
        self.data_provider = "ctpbee"
        # 数据类型默认设置为tick
        # 默认的产品类型

        # 应该是个生成器
        """ 根据每个data """
        self.data_type = Bumblebee(**data[0][0]).type
        try:
            for i in data:
                self.inner_data[i[0]["local_symbol"]] = chain(map(lambda x: Bumblebee(**x), i))
            self.init_flag = True
        except Exception:
            raise ValueError("数据格式不合法")
        self.slice = 0
        self.the_buffer = {}
        for x in self.inner_data:
            origin = next(self.inner_data[x])
            self.the_buffer[origin.local_symbol] = origin

    @property
    def last_bar(self):
        """ 时间缓冲器
        实现同步回放多个数据源， 实现过程为
        先找到实现数据时间探针
        每次pop第一个时间轴最小的data_entity。
        """
        ax = min([x.datetime for x in self.the_buffer.values()])
        for key, value in self.the_buffer.items():
            if ax == value.datetime:
                """ 如果找到了值相等  那么更新里面的值 """
                nx = value
                self.the_buffer[key] = next(self.inner_data[key])
                if isinstance(nx, data_api_types()):
                    """ data_api 的实体需要转换成内部的 Bumblebee 表示 """
                    return nx.to_bumblebee()
                return nx

    def __next__(self):
        """
        实现生成器协议使得这个类可以被next函数不断调用
        主要用来数据的回放控制， 基于此你可以有序的对数据进行回放,实现多个行情的同时进行回放，
        比如A B A A B A
        他们的时间是按照顺序进行回放的
        注意他不是并发推入的 而是一个一个的进行回放。
        """
        return self.last_bar

    def __iter__(self):
        return iter(self.inner_data)

    @property
    def type(self):
        """ 数据类型 """
        return self.data_type

    @property
    def product(self):
        """ 产品类型 """
        return self.product_type
