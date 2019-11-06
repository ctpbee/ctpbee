"""
回测数据模块

数据应该是需要被特殊处理的， 这样才可以达到最佳访问速度
--------- >
"""

# todo: 将各家数据转化为从ctpbee数据包 ^_^ alse it will be a good idea to
from itertools import chain


class Bumblebee(dict):
    """  """
    __slots__ = ['last_price', 'datetime', 'open_price', "high_price", "low_price", "close_price", "volume", "type"]
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __getattribute__ = dict.get

    # def __getattribute__(self, item):
    #     return dict.get(item)

    def __init__(self, **kwargs):
        if "last_price" in kwargs:
            self['type'] = "tick"
        else:
            self['type'] = "bar"
        super().__init__(**kwargs)
        # [setattr(self, key, kwargs.get(key)) for key in kwargs if key in self.__slots__]


class VessData:
    """
        本类存在的意义就是整合各家数据， 提供数据统一的解决方案 ^_^ hope you will relax it
        如果数据想接进来, 请提交pr

    """

    def __init__(self, data):
        self.init_flag = False
        self.data = data
        # 数据供应商默认设置为ctpbee
        self.data_provider = "ctpbee"
        # 数据类型默认设置为tick
        # 默认的产品类型
        self.product_type = "future"
        # 应该是个生成器
        self.data_type = Bumblebee(**data[0]).type
        try:
            self.inner_data = chain(map(lambda x: Bumblebee(**x), data))
            self.init_flag = True
        except Exception:
            pass

        self.slice = 0

    def __next__(self):
        """ 实现生成器协议使得这个类可以被next函数不断调用 """
        # 实际上是不断调用 inner_data的__next__协议
        result = next(self.inner_data)
        return result

    def __iter__(self):
        return iter(self.inner_data)

    @property
    def length(self):
        return len(self.data)

    @property
    def type(self):
        """ 数据类型 """
        return self.data_type

    @property
    def product(self):
        """ 产品类型 """
        return self.product_type
