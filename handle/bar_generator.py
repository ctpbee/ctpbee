# encoding: UTF-8


import sys_signal
from setting import XMIN
from vnpy.trader.vtObject import VtBarData
from event_engine.engine import Event
from event_engine import event_engine

########################################################################
from sys_constant import EVENT_BAR


class BarGenerator(object):
    """
    K线合成器，支持：
    1. 基于Tick合成1分钟K线
    2. 基于1分钟K线合成X分钟K线（X可以是2、3、5、10、15、30	）
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.bar = None  # 1分钟K线对象
        self.lastTick = None  # 上一TICK缓存对象
        self._generator()

    def _generator(self):
        for x in XMIN:
            setattr(self, "min_{}".format(x), x)
            setattr(self, "min_{}_bar".format(x), None)

    # ----------------------------------------------------------------------
    def updateTick(self, tick):
        """TICK更新"""
        newMinute = False  # 默认不是新的一分钟

        # 尚未创建对象
        if not self.bar:
            self.bar = VtBarData()
            newMinute = True
        # 新的一分钟
        elif self.bar.datetime.minute != tick.datetime.minute:
            # 生成上一分钟K线的时间戳
            self.bar.datetime = self.bar.datetime.replace(second=0, microsecond=0)  # 将秒和微秒设为0
            self.bar.date = self.bar.datetime.strftime('%Y%m%d')
            self.bar.time = self.bar.datetime.strftime('%H:%M:%S.%f')

            # 推送已经结束的上一分钟K线
            # sys_signal.bar_signal_map.get("1").send(db=1, bar=self.bar)
            # 推送 xmin分钟数据
            data = {
                "db": "1",
                "bar": self.bar
            }
            event = Event(type_=EVENT_BAR, dict=data)
            event_engine.put(event)
            for x in XMIN:
                self.updateBar(x, getattr(self, "min_{}_bar".format(x)), self.bar)
            # 创建新的K线对象
            self.bar = VtBarData()
            newMinute = True

        # 初始化新一分钟的K线数据
        if newMinute:
            self.bar.vtSymbol = tick.vtSymbol
            self.bar.symbol = tick.symbol
            self.bar.exchange = tick.exchange

            self.bar.open = tick.lastPrice
            self.bar.high = tick.lastPrice
            self.bar.low = tick.lastPrice
        # 累加更新老一分钟的K线数据
        else:
            self.bar.high = max(self.bar.high, tick.lastPrice)
            self.bar.low = min(self.bar.low, tick.lastPrice)

        # 通用更新部分
        self.bar.close = tick.lastPrice
        self.bar.datetime = tick.datetime
        self.bar.openInterest = tick.openInterest

        if self.lastTick:
            volumeChange = tick.volume - self.lastTick.volume  # 当前K线内的成交量
            self.bar.volume += max(volumeChange, 0)  # 避免夜盘开盘lastTick.volume为昨日收盘数据，导致成交量变化为负的情况

        # 缓存Tick
        self.lastTick = tick

    # ----------------------------------------------------------------------
    def updateBar(self, xmin, xmin_bar, bar):
        xmin = xmin
        """x分钟K线更新"""
        # 尚未创建对象
        if not xmin_bar:
            xmin_bar = VtBarData()

            xmin_bar.vtSymbol = bar.vtSymbol
            xmin_bar.symbol = bar.symbol
            xmin_bar.exchange = bar.exchange

            xmin_bar.open = bar.open
            xmin_bar.high = bar.high
            xmin_bar.low = bar.low

            xmin_bar.datetime = bar.datetime  # 以第一根分钟K线的开始时间戳作为X分钟线的时间戳
        # 累加老K线
        else:
            xmin_bar.high = max(xmin_bar.high, bar.high)
            xmin_bar.low = min(xmin_bar.low, bar.low)

        # 通用部分
        xmin_bar.close = bar.close
        xmin_bar.openInterest = bar.openInterest
        xmin_bar.volume += int(bar.volume)

        # X分钟已经走完
        if not (bar.datetime.minute + 1) % xmin:  # 可以用X整除
            # 生成上一X分钟K线的时间戳
            xmin_bar.datetime = xmin_bar.datetime.replace(second=0, microsecond=0)  # 将秒和微秒设为0
            xmin_bar.date = xmin_bar.datetime.strftime('%Y%m%d')
            xmin_bar.time = xmin_bar.datetime.strftime('%H:%M:%S.%f')
            # 推送
            data = {
                "db": xmin,
                "bar": xmin_bar
            }
            event = Event(type_=EVENT_BAR, dict=data)
            event_engine.put(event)

            # 清空老K线缓存对象
            xmin_bar = None

    # ----------------------------------------------------------------------
    def generate(self, **kwargs):
        """手动强制立即完成K线合成"""
        print "强制合成  -----"
        data = {
            "db": "1",
            "bar": self.bar
        }
        event = Event(type_=EVENT_BAR, dict=data)
        event_engine.put(event)
        for x in XMIN:
            data = {
                "db": x,
                "bar": getattr(self, "min_{}_bar".format(x))
            }
            event = Event(type_=EVENT_BAR, dict=data)
            event_engine.put(event)
        self.bar = None
        for x in XMIN:
            setattr(self, "min_{}_bar".format(x), None)
