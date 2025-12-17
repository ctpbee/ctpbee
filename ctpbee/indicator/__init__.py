"""

提供指标纯向量化计算方法

todo: 提供任意结构组合的向量化回测结果
"""

import numpy as np


def read_indicator_from_data():
    raise NotImplemented


class Indicator:
    def __init__(self, n=10):
        self._n = n

    def flush(self):
        raise NotImplemented
