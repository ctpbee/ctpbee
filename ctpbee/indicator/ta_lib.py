"""
Vnpy里面提高的指标系统
需要你自行安装TA-LIB

I
"""

import numpy as np
import warnings

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

    def update_bar(self, bar):
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

        self.open_array[-1] = bar.open_price
        self.high_array[-1] = bar.high_price
        self.low_array[-1] = bar.low_price
        self.close_array[-1] = bar.close_price
        self.volume_array[-1] = bar.volume

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

    def macd_scta(self, params=[5, 10, 22, 63, 252], array=False):
        try:
            import pandas as pd
        except ImportError:
            raise ValueError("请安装pandas以继续使用此指标")
        S_days = params[0]
        I_days = params[1]
        L_days = params[2]
        PW = params[3]
        SW = params[4]

        S_hl = np.log(0.5) / np.log(1 - 1 / S_days)
        I_hl = np.log(0.5) / np.log(1 - 1 / I_days)
        L_hl = np.log(0.5) / np.log(1 - 1 / L_days)

        price_df = pd.DataFrame(self.close)

        S_Macd = price_df.ewm(halflife=S_hl, min_periods=S_days).mean() - price_df.ewm(halflife=3 * S_hl,
                                                                                       min_periods=3 * S_days).mean()
        I_Macd = price_df.ewm(halflife=I_hl, min_periods=I_days).mean() - price_df.ewm(halflife=3 * I_hl,
                                                                                       min_periods=3 * I_days).mean()
        L_Macd = price_df.ewm(halflife=L_hl, min_periods=L_days).mean() - price_df.ewm(halflife=3 * L_hl,
                                                                                       min_periods=3 * L_days).mean()

        PW_std = price_df.rolling(window=PW).std()

        S_y = S_Macd / PW_std
        I_y = I_Macd / PW_std
        L_y = L_Macd / PW_std

        S_z = S_y / S_y.rolling(window=SW).std()
        I_z = I_y / I_y.rolling(window=SW).std()
        L_z = L_y / L_y.rolling(window=SW).std()
        S_u = S_z * np.exp(-(S_z ** 2) / 4) / 0.89
        I_u = I_z * np.exp(-(I_z ** 2) / 4) / 0.89
        L_u = L_z * np.exp(-(L_z ** 2) / 4) / 0.89

        scta = (S_u + I_u + L_u) / 3

        scta = scta.to_numpy().T[0]

        if array:
            return scta
        return scta[-1]
