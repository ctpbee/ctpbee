"""
回测数据模块

数据应该是需要被特殊处理的， 这样才可以达到最佳访问速度
--------- >
"""
from itertools import chain

# todo: 将各家数据转化为从ctpbee数据包 ^_^ alse it will be a good idea to
from time import time
from typing import Iterable


class Bumblebee:
    """  """
    __slots__ = ['last_price', 'datetime', 'open_price', "high_price", "low_price", "close_price", "type"]

    def __init__(self, **kwargs):
        if "last_price" in kwargs:
            self.type = "tick"
        else:
            self.type = "bar"
        [setattr(self, key, kwargs.get(key)) for key in kwargs if key in self.__slots__]


class VessData:
    """
        本类存在的意义就是整合各家数据， 提供数据统一的解决方案 ^_^ hope you will relax it
        如果数据想接进来, 请提交pr

    """
    support_cn = ["ctpbee", "rice_quant", "vnpy", "jq"]

    def __init__(self, data):
        self.init_flag = False
        self.data = data
        # 数据供应商默认设置为ctpbee
        self.data_provider = "ctpbee"
        # 数据类型默认设置为tick
        self.data_type = "tick"
        # 默认的产品类型
        self.product_type = "future"
        # 应该是个生成器
        self.inner_data = ()
        self.func_mapping = {
            "ctpbee": self.ctpbee_data,
            "vnpy": self.vnpy_data,
            "jq": self.jq_data,
            "rice_quant": self.rice_data
        }
        self.slice = 0

    def convert_data_to_inner(self) -> bool:
        """ 将本地的数据[ ctpbee录制数据， 米筐数据, jq数据.... ]转换为本地回测所需要的数据包 """
        func = self.analyse_data(self.data)
        self.inner_data = func(self.data)
        self.init_flag = True

    def analyse_data(self, data):
        """ 分析数据类型并返回处理函数/analyse the origin of data and return the process func"""
        # 实现分析数据格式
        self.data_provider, self.product_type, self.data_type = "ctpbee.future.tick".split(".")
        if self.data_provider not in self.support_cn:
            raise TypeError(f"请检查你的数据是否符合要求, 当前ctpbee只支持{' '.join(self.support_cn)}")
        return self.func_mapping.get(self.data_provider)

    def __next__(self):
        """ 实现生成器协议使得这个类可以被next函数不断调用 """
        # 实际上是不断调用 inner_data的__next__协议

        result = next(self.inner_data)
        return result

    def __iter__(self):
        return iter(self.inner_data)

    def ctpbee_data(self, data: Iterable) -> Iterable:
        """ 实现数据转换后转换为dict """
        d = map(lambda x: Bumblebee(**x), data)
        return chain(d)

    def rice_data(self, data: Iterable) -> Iterable:
        return chain(data)

    def jq_data(self, data: Iterable) -> Iterable:
        return chain(data)

    def vnpy_data(self, data: Iterable) -> Iterable:
        return chain(data)

    @property
    def length(self):
        return len(self.data)

    @property
    def provider(self):
        """ 数据提供商 """
        return self.data_provider

    @property
    def type(self):
        """ 数据类型 """
        return self.data_type

    @property
    def product(self):
        """ 产品类型 """
        return self.product_type


if __name__ == '__main__':
    # data = [{"local_symbol": x * 1} for x in range(5000000)]
    # App = VessData(data)
    # App.convert_data_to_inner()
    # start_time = time()
    # for x in App:
    #     pass
    # end_time = time()
    # print(f"for循环遍历耗时{(end_time - start_time)*1000}ms")
    # App = VessData(data)
    # App.convert_data_to_inner()
    # start = time()
    # while True:
    #     try:
    #         next(App)
    #     except StopIteration:
    #         break
    # end = time()
    # print(f"next遍历耗时{(end - start)*1000}ms")
    a = Bumblebee(**{"last_price": 1})
    start_time = time()
    print(a.last_price)
    end_time = time()
    print(f"属性访问耗时{(end_time - start_time) * 1000}ms")


    a = {"last_price": 1}
    start_time = time()
    print(a['last_price'])
    end_time = time()
    print(f"字典访问耗时{(end_time - start_time) * 1000}ms")
