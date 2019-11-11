"""
如何计算夏普率等策略指标

"""


class Indicator(object):
    """  这个可能是一个比较麻烦的类 阿西吧 """

    def __init__(self, account):
        self.account = account
        self._sharp_rate = ""

    @property
    def sharp_rate(self):
        """ 返回夏普率"""
        return self._sharp_rate
