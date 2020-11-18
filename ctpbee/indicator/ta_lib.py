"""
Vnpy里面提高的指标系统
需要你自行安装TA-LIB
"""

import numpy as np
import warnings

from ctpbee.constant import TickData

try:
    import talib
except ImportError:
    warnings.warn("please install ta-lib by yourself")


def round_to(value: float, target: float) -> float:
    """
    Round price to price tick value.
    """
    return int(round(value / target)) * target


class ArrayManager(object):
    """
    For:
    1. time series container of bar data
    2. calculating technical indicator value
    """

    def __init__(self, size=100):
        """Constructor"""
        self.count = 0
        self.size = size
        self.inited = False

        self.open_array = np.zeros(size)
        self.high_array = np.zeros(size)
        self.low_array = np.zeros(size)
        self.close_array = np.zeros(size)
        self.volume_array = np.zeros(size)

    def add_data(self, data, type="bar"):
        """
        Update new bar data into array manager.
        """
        self.count += 1
        if not self.inited and self.count >= self.size:
            self.inited = True

        self.open_array[:-1] = self.open_array[1:]
        self.high_array[:-1] = self.high_array[1:]
        self.low_array[:-1] = self.low_array[1:]
        self.close_array[:-1] = self.close_array[1:]
        self.volume_array[:-1] = self.volume_array[1:]

        self.open_array[-1] = data.open_price
        self.high_array[-1] = data.high_price
        self.low_array[-1] = data.low_price
        if type == "bar":
            self.close_array[-1] = data.close_price
        else:
            self.close_array[-1] = data.last_price
        self.volume_array[-1] = data.volume

    @property
    def open(self):
        """
        Get open price time series.
        """
        return self.open_array

    @property
    def high(self):
        """
        Get high price time series.
        """
        return self.high_array

    @property
    def low(self):
        """
        Get low price time series.
        """
        return self.low_array

    @property
    def close(self):
        """
        Get close price time series.
        """
        return self.close_array

    @property
    def volume(self):
        """
        Get trading volume time series.
        """
        return self.volume_array

    def sma(self, n, array=False):
        """
        Simple moving average.
        """
        result = talib.SMA(self.close, n)
        if array:
            return result
        return result[-1]

    def std(self, n, array=False):
        """
        Standard deviation
        """
        result = talib.STDDEV(self.close, n)
        if array:
            return result
        return result[-1]

    def cci(self, n, array=False):
        """
        Commodity Channel Index (CCI).
        """
        result = talib.CCI(self.high, self.low, self.close, n)
        if array:
            return result
        return result[-1]

    def atr(self, n, array=False):
        """
        Average True Range (ATR).
        """
        result = talib.ATR(self.high, self.low, self.close, n)
        if array:
            return result
        return result[-1]

    def rsi(self, n, array=False):
        """
        Relative Strenght Index (RSI).
        """
        result = talib.RSI(self.close, n)
        if array:
            return result
        return result[-1]

    def macd(self, fast_period, slow_period, signal_period, array=False):
        """
        MACD.
        """
        macd, signal, hist = talib.MACD(
            self.close, fast_period, slow_period, signal_period
        )
        if array:
            return macd, signal, hist
        return macd[-1], signal[-1], hist[-1]

    def adx(self, n, array=False):
        """
        ADX.
        """
        result = talib.ADX(self.high, self.low, self.close, n)
        if array:
            return result
        return result[-1]

    def boll(self, n, dev, array=False):
        """
        Bollinger Channel.
        """
        mid = self.sma(n, array)
        std = self.std(n, array)

        up = mid + std * dev
        down = mid - std * dev

        return up, down

    def keltner(self, n, dev, array=False):
        """
        Keltner Channel.
        """
        mid = self.sma(n, array)
        atr = self.atr(n, array)

        up = mid + atr * dev
        down = mid - atr * dev

        return up, down

    def donchian(self, n, array=False):
        """
        Donchian Channel.
        """
        up = talib.MAX(self.high, n)
        down = talib.MIN(self.low, n)

        if array:
            return up, down
        return up[-1], down[-1]

    @staticmethod
    def get_open_interest_delta_forward(open_interest_delta, volume_delta):
        """根据成交量的差和持仓量的差来获取仓位变化的方向
            return: open_interest_delta_forward_enum
        """
        if open_interest_delta == 0 and volume_delta == 0:
            """ 持仓量和成交量没有发生变化 """
            local_open_interest_delta_forward = "NONE"
        elif open_interest_delta == 0 and volume_delta > 0:
            """ 持仓量不变 但是发生了成交 """
            local_open_interest_delta_forward = "EXCHANGE"
        elif open_interest_delta > 0:
            """ 持仓量增大 说明发生了开仓  """
            if open_interest_delta - volume_delta == 0:
                """ 如果持仓量的变化 要大于成交量  --> 双开 """
                local_open_interest_delta_forward = "OPENFWDOUBLE"
            else:
                """ 否则是多开 """
                local_open_interest_delta_forward = "OPEN"
        elif open_interest_delta < 0:
            """" 持仓量减少 说明发生了平仓 """
            if open_interest_delta + volume_delta == 0:
                local_open_interest_delta_forward = "CLOSEFWDOUBLE"
            else:
                local_open_interest_delta_forward = "CLOSE"
        else:
            raise ValueError("这里不可能被触发")
        return local_open_interest_delta_forward

    def get_order_direction(self, last_tick: TickData, pre_tick: TickData, volume_delta_flag=True,
                            open_interest_delta_flag=False):
        """获取成交的区域，根据当前tick的成交价和上个tick的ask和bid价格进行比对
           return: order_forward_enum
        """
        assert last_tick.local_symbol == pre_tick.local_symbol
        if last_tick.last_price >= pre_tick.ask_price_1:
            direction = "UP"
        elif last_tick.last_price <= pre_tick.bid_price_1:
            direction = "DOWN"
        else:
            if last_tick.last_price >= last_tick.ask_price_1:
                direction = "UP"
            elif last_tick.last_price <= last_tick.bid_price_1:
                direction = "DOWN"
            else:
                direction = "MIDDLE"
        if volume_delta_flag:
            volume_delta = last_tick.volume
        else:
            volume_delta = last_tick.volume - pre_tick.volume
        if open_interest_delta_flag:
            open_delta = last_tick.open_interest
        else:
            open_delta = last_tick.open_interest - pre_tick.open_interest
        offset = self.get_open_interest_delta_forward(volume_delta=volume_delta, open_interest_delta=open_delta)
        result = f"{direction}-{offset}"
        return result, volume_delta, open_delta
