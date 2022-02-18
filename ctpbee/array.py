from abc import ABC
from typing import Any, Iterable, List

import numpy as np
import pandas as pd


class Array:

    def __init__(self, length=None):
        self._array = []
        self._length = length

    def push(self, value: Any):
        self._array.append(value)

    def last(self):
        return self._array[-1]

    def first(self):
        return self._array[0]

    def index(self, value: Any):
        """
        索引元素存在的位置
        """
        return self._array.index(value)

    def pop(self, i=0):
        """
        删除指定位置的元素
        """
        return self._array.pop(i)

    def clear(self):
        """
        清空数组
        """
        return self._array.clear()

    def count(self, element) -> int:
        """
        返回数量
        """
        return self._array.count(element)

    def update(self, array: Iterable):
        """
        将Array里面的值更新进当前数组
        """
        for i in array:
            self._array.append(i)

    @property
    def length(self):
        return len(self._array)

    def len(self):
        return len(self._array)

    def std(self):
        return np.std(self._array)

    def variance(self):
        return np.var(self._array)

    def mean(self):
        return np.mean(self._array)

    def plot(self, **kwargs):
        pd.Series(self._array).plot(**kwargs)

    def max(self) -> Any:
        return max(self._array)

    def min(self) -> Any:
        return min(self._array)

    def median(self) -> Any:
        return np.median(self._array)

    def atr(self) -> Any:
        x = self.max() - self.min()
        return x

    def btr(self) -> Any:
        return self.last() - self.first()

    def __rolling(self, n) -> Iterable:
        start = 0
        end = n
        while end <= len(self._array) - 1:
            data = self._array[start:end]
            start += 1
            end += 1
            yield data

    def rolling(self, n: int):
        """
        简单的实现的一个rolling方法
        将返回的结果全部收回
        """
        # 生成rolling数据
        return from_iterator(self.__rolling(n))

    def __chunks(self, n) -> Iterable:
        start = 0
        end = n
        length = len(self._array) - 1
        while end < length:
            data = self._array[start:end]
            start = start + n
            end = end + n
            yield data

        if start < length:
            yield self._array[start:length]

    def collect(self) -> List[Any]:
        return self._array

    def chunks(self, n: int):
        """
        实现指定数字间隔读取
        """
        return from_iterator(self.__chunks(n))

    def apply(self, func):
        """
        对元素统一实现函数方法,类似于pandas -> apply方法
        """
        return from_iterator(self.map(func))

    def map(self, func) -> Iterable:
        return map(func, self._array)

    def filter(self, f) -> Iterable:
        return filter(f, self._array)

    def to_list(self):
        return self._array

    def sum(self):
        return sum(self._array)

    def as_series(self):
        return pd.Series(self._array)

    def delta(self):
        return self._array[-1] - self._array[0]

    # 指标相关
    def adx(self, chunks) -> pd.Series:
        """ 根据给定的数量来计算当前的adx指标值 """
        try:
            import talib
        except ImportError:
            raise ImportError("请前往 https://www.lfd.uci.edu/~gohlke/pythonlibs/ 下载安装TA-Lib对应安装库")
        iterator = self.chunks(chunks).apply(lambda d: (np.max(d), np.min(d), d[-1])).collect()
        pa = pd.DataFrame(iterator, columns=["high", "low", "close"])
        adx_value = talib.ADX(pa.high, pa.low, pa.close).values
        return adx_value

    def __iter__(self):
        for i in self._array:
            yield i

    def __getitem__(self, key):
        return self._array.__getitem__(key)

    def __str__(self):
        return f"<Array:(Length={self._length}\n [{','.join(self._array)}]\n)>"

    def __repr__(self):
        return f"<Array:(Length={self._length}\n [{','.join(self._array)}]\n)>"

    def __reversed__(self):
        return reversed(self._array)


class LArray(Array, ABC):
    """固定长度的数组"""

    def __init__(self, length=100):
        super().__init__(length)
        self.ready = False

    def push(self, value: Any):
        self._array.append(value)

        if self.length > self._length:
            self.ready = True
            self._array.pop(0)

    def __str__(self):
        return f"<LArray:(Length={self._length} {self._array})>"

    def __repr__(self):
        return f"<LArray:(Length={self._length} {self._array})>"


def from_iterator(value: Iterable) -> Array:
    acc = Array()
    acc.update(value)
    return acc


if __name__ == '__main__':
    a = [1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 21, 1]
    app = LArray(value_type="any")
    app.update(a)
    d = app.chunks(3).apply(lambda x: x)
    print(d)
