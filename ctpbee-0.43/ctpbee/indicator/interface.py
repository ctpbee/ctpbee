from .plot import Scheduler


class Interface:

    @property
    def open(self):
        """
        Get open price time series.
        """
        return Scheduler.ret_open

    @property
    def high(self):
        """
        Get high price time series.
        """
        return Scheduler.ret_high

    @property
    def low(self):
        """
        Get low price time series.
        """
        return Scheduler.ret_low

    @property
    def close(self):
        """
        Get low price time series
        :return:
        """
        return Scheduler.ret_close

    def open_csv(self, file: str, start_time=None, end_time=None):
        """
        open TXT file
            data_type:
                Date,Open,High,Low,Close,Volume
                '2019-01-07 00:00:00', 3831.0, 3847.0, 3831.0, 3840.0, 554
                '2019-01-08 00:00:00', 3841.0, 3841.0, 3833.0, 3836.0, 554
                ...
        :param file: name
        :param start_time:
        :param end_time:
        :return:
        """
        return Scheduler.open_csv(file, start_time, end_time)

    def open_json(self, file: str, start_time=None, end_time=None):
        """
        open JSON file
            data_type:
                {"zn1912.SHFE": [
                        ["2014-01-01", 18780.0, 18780.0, 18770.0, 18775.0, 266],
                        ["2014-01-02", 18775.0, 18780.0, 18770.0, 18770.0, 312],
                            ...
                        ]
                }
        :param file: name
        :param start_time:
        :param end_time:
        :return:
        """
        return Scheduler.open_json(file, start_time, end_time)

    def open_cache(self, data: list):
        """
        read CACHE data
            data_type:
                [["2014-01-01", 22, 44, 55, 55, 6666], ["2014-01-02", 22, 44, 55, 55, 6666], ...]
        :param data:
        :return:
        """
        return Scheduler.open_cache(data)

    def add_bar(self, data, opens=False):
        """
        new bar push in array
        :param data: bar
        :param opens: if True save file  else not save (default False)
        :return:
        """
        Scheduler.update_bar(data, opens)

    def sma(self, n=15):
        data = Scheduler.ret_close
        return Scheduler.sma(data, n)

    def ema(self, n=12, alpha=None):
        data = Scheduler.ret_close
        return Scheduler.ema(data, n, alpha)

    def wma(self, n=30):
        data = Scheduler.ret_close
        return Scheduler.wma(data, n)

    def kd(self, n=14, f=3):
        data = Scheduler.ret_close
        return Scheduler.kd(data, n, f)

    def macd(self, n=12, m=20, f=9):
        data = Scheduler.ret_close
        return Scheduler.macd(data, n, m, f)

    def rsi(self, n=14, l=1):
        data = Scheduler.ret_close
        return Scheduler.rsi(data, n, l)

    def smma(self, n=10, alpha=15):
        data = Scheduler.ret_close
        return Scheduler.smma(data, n, alpha)

    def atr(self, n=14):
        data = Scheduler.ret_close
        return Scheduler.atr(data, n)

    def stdDev(self, n=20):
        data = Scheduler.ret_close
        return Scheduler.stdDev(data, n)

    def boll(self, n=20, m=2):
        data = Scheduler.ret_close
        return Scheduler.boll(data, n, m)

    def trix(self, n=15, m=1):
        data = Scheduler.ret_close
        return Scheduler.trix(data, n, m)

    def roc(self, n=12):
        data = Scheduler.ret_close
        return Scheduler.roc(data, n)

    def mtm(self, n=12):
        data = Scheduler.ret_close
        return Scheduler.mtm(data, n)

    def tema(self, n=25):
        data = Scheduler.ret_close
        return Scheduler.tema(data, n)

    def wr(self, n=14):
        data = Scheduler.ret_close
        return Scheduler.wr(data, n)

    def cci(self, n=20, f=0.015):
        return Scheduler.cci(n, f)

    def sar(self, n=2, af=0.02, afmax=0.20):
        data = Scheduler.ret_close
        return Scheduler.sar(data, n, af, afmax)

    def UltimateOscillator(self):
        pass

    def AroonIndicator(self):
        pass

    def plot(self, width=8, height=6, color="k", lw=0.5):
        Scheduler.plot(width=width, height=height, color=color, lw=lw)


api = Interface