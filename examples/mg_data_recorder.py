from datetime import datetime
from time import sleep

from ctpbee import CtpbeeApi, auth_time
from queue import Queue

from functools import total_ordering


@total_ordering
class TimeIt:
    """ 主要是来实现一个减法"""

    def __init__(self, datetime_obj: datetime):
        self._datetime = datetime_obj

    def __sub__(self, other: datetime):
        """
        实现减法操作
        返回绝对值
        """
        if not isinstance(other, TimeIt) and not isinstance(other, datetime):
            raise ValueError("参数类型不同无法使用减法")
        if isinstance(other, datetime):
            return int(abs(self._datetime.timestamp() - other.timestamp()))
        elif isinstance(other, TimeIt):
            return int(abs(self._datetime.timestamp() - other._datetime.timestamp()))

    def __eq__(self, other):
        if isinstance(other, datetime):
            return self._datetime == other
        elif isinstance(other, TimeIt):
            return self._datetime == other._datetime

    def __lt__(self, other):
        if isinstance(other, datetime):
            return self._datetime < other
        elif isinstance(other, TimeIt):
            return self._datetime < other._datetime


class Market(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        # 创建一个datetime队列
        self.datetime_queue = Queue()
        # 队列长度
        self.queue_length = 5

    def on_bar(self, bar):
        """ 处理k线数据 """

    def on_tick(self, tick):
        """ 处理tick信息 """
        if not auth_time(tick.datetime.time()):
            """ 过滤非交易时间段的数据 """
            return

        if self.datetime_queue.empty():
            self.datetime_queue.put(TimeIt(tick.datetime))




if __name__ == '__main__':
    a = datetime.now()
    print(a)
    sleep(3)
    b = TimeIt(datetime.now())

    print("value: ", b - a)
    print(a > b)
    print(a < b)
