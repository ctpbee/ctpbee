import numpy as np
from .readfile import File
import math
import operator
from copy import deepcopy
from functools import wraps


def getAverageName(func):
    """
    此装饰器是获取平均平均值参数名
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        line = func(self, *args, **kwargs)
        func_name = func.__name__
        self.average_message[func_name] = line
        return line
    return wrapper


def getIndicatorName(func):
    """
    此装饰器是获取其他指标值参数名
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        line = func(self, *args, **kwargs)
        func_name = func.__name__
        if func_name == "macd":
            self.indicator_message["MACD"] = self.macds
            self.indicator_message["signal"] = self.signal
            self.indicator_message[func_name] = self.histo
        elif func_name == "kd":
            self.indicator_message["K"] = self.k
            self.indicator_message["D"] = self.percD
        elif func_name == "boll":
            self.indicator_message["mid"] = self.mid
            self.indicator_message["top"] = self.top
            self.indicator_message["bottom"] = self.bottom
        else:
            self.indicator_message[func_name] = line
        return line
    return wrapper


class Indicator(File):
    def __init__(self):
        super().__init__()
        self.average_message = {}
        self.indicator_message = {}

    def calculate(self):
        """
        计算指标
        :return:
        """
        pass

    @getAverageName
    def sma(self, data:object, period=15):
        """
        sma or ma SimpleMovingAverage
        简单移动平均线
        :param period:距离
        :param data:数据 object
        :return:计算值
        """
        self.sma_data = deepcopy(data)
        end = len(data)
        close_line = data
        for i in range(period, end):
            self.sma_data[i] = sum(close_line[i - period + 1:i + 1]) / period
        return self.sma_data

    @getAverageName
    def ema(self, data:object, period:int, alpha=None):
        """
        ema ExponentialMovingAverage
        指数移动平均(period一般取12和26天)
            - self.smfactor -> 2 / (1 + period)
            - self.smfactor1 -> `1 - self.smfactor`
            - movav = prev * (1.0 - smoothfactor) + newdata * smoothfactor
        :param data:
        :param period:
        :return:
        """
        self.ema_data = deepcopy(data)
        end = len(data)
        close_line = data
        self.alpha = alpha
        if self.alpha is None:
            self.alpha = 2.0 / (1.0 + period)
        self.alpha1 = 1.0 - self.alpha
        prev = close_line[period-1]
        for i in range(period, end):
            self.ema_data[i] = prev = prev * self.alpha1 + close_line[i] * self.alpha
        return self.ema_data

    @getAverageName
    def wma(self, data:object, period=30):
        '''
        WeightedMovingAverage 加权移动平均线
            A Moving Average which gives an arithmetic weighting to values with the
            newest having the more weight

            Formula:
              - weights = range(1, period + 1)
              - coef = 2 / (period * (period + 1))
              - movav = coef * Sum(weight[i] * data[period - i] for i in range(period))
            '''
        self.wma_data = deepcopy(data)
        end = len(data)
        close_line = data
        coef = 2.0 / (period * (period + 1.0))
        weights = tuple(float(x) for x in range(1, period + 1))
        for i in range(period, end):
            data = close_line[i - period + 1: i + 1]
            self.wma_data[i] = coef * math.fsum(map(operator.mul, data, weights))
        return self.wma_data

    @getIndicatorName
    def kd(self, data:object, period=14, period_dfast=3):
        """
        随机振荡器 随机指标(KD) : K给出预期信号，以底部或之前的 D给出周转信号，以 D-Slow给出周转确认信号
            The regular (or slow version) adds an additional moving average layer and
            thus:

              - The percD line of the StochasticFast becomes the percK line
              - percD becomes a  moving average of period_dslow of the original percD

            Formula:
                - hh = highest(data.high, period)
              - ll = lowest(data.low, period)
              - knum = data.close - ll
              - kden = hh - ll
              - k = 100 * (knum / kden)
              - d = MovingAverage(k, period_dfast)

              - d-slow = MovingAverage(d, period_dslow)
            See:
                - http://en.wikipedia.org/wiki/Stochastic_oscillator
            :param data:
            :param period:
            :return:
        """
        end = len(data)
        highest = deepcopy(data)
        lowest = deepcopy(data)
        for i in range(period, end):
            highest[i] = max(self.ret_high[i - period + 1: i + 1])
        for i in range(period, end):
            lowest[i] = min(self.ret_low[i - period + 1: i + 1])
        knum = np.array(data) - lowest
        kden = np.array(highest) - np.array(lowest)
        self.k = 100 * (knum/kden)
        self.d = self.sma(self.k, period=period_dfast)
        self.percD = self.sma(self.d, period=period_dfast)
        return self.k, self.percD

    @getIndicatorName
    def macd(self, data:object, period_me1=12, period_me2=26, period_signal=9):
        """
        移动平均趋同/偏离(异同移动平均线) MACDHisto
        Formula:
            - macd = ema(data, me1_period) - ema(data, me2_period)
            - signal = ema(macd, signal_period)
            - histo = macd - signal
        :param data:
        :param period:
        :return:
        """

        me1 = self.ema(data, period=period_me1)
        me2 = self.ema(data, period=period_me2)
        self.macds = np.array(me1) - np.array(me2)
        self.signal = self.ema(self.macds, period=period_signal)
        self.histo = np.array(self.macds) - np.array(self.signal)
        return self.macds, self.signal, self.histo

    @getAverageName
    def rsi(self, data:object,  period=14, lookback=1):
        """
        rsi 相对强度指数
        Formula:
          - up = upday(data)
          - down = downday(data)
          - maup = sma(up, period)      or ema(up, period)
          - madown = sma(down, period)  or ema(down, period)
          - rs = maup / madown
          - rsi = 100 - 100 / (1 + rs)
        :param data:
        :param period:
        :return:
        """
        params = (
            ('period', 14),
            ('upperband', 70.0),
            ('lowerband', 30.0),
            ('safediv', False),
            ('safehigh', 100.0),
            ('safelow', 50.0),
            ('lookback', 1),
        )
        end = len(data)
        upday = deepcopy(data)
        downday = deepcopy(data)
        for i in range(period, end):
            upday[i] = max(data[i]-data[i-1], 0.0)
        for i in range(period, end):
            downday[i] = max(data[i-1]-data[i], 0.0)
        maup = self.ema(upday, period=period)
        madown = self.ema(downday, period=period)
        rs = np.array(maup) / np.array(madown)
        self.rsi_list = []
        for i in rs:
            rsi = 100.0 - 100.0 / (1.0 + i)
            self.rsi_list.append(rsi)
        return self.rsi_list

    @getAverageName
    def smma(self, data:object, period:int, alpha=15):
        """
        smma 平滑移动平均值
        SmoothedMovingAverage
        :param data:
        :param period:
        :return:
        """
        self.ema_data = deepcopy(data)
        end = len(data)
        close_line = data
        self.alpha = alpha
        if self.alpha is None:
            self.alpha = 2.0 / (1.0 + period)
        self.alpha1 = 1.0 - self.alpha

        prev = close_line[period - 1]
        for i in range(period, end):
            self.ema_data[i] = prev = prev * self.alpha1 + close_line[i] * self.alpha
        return self.ema_data

    @getIndicatorName
    def atr(self, data:object, period=14):
        """
        平均真实范围
        AverageTrueRange
        :param data:
        :param period:
        :return:
        """
        truehigh = []
        truelow = []
        end = len(data)
        truehigh = truehigh + [0] * period
        for h in range(period+1, end):
            truehigh.append(max(data[h-1], self.ret_high[h]))
        truelow = truelow + [0] * period
        for l in range(period+1, end):
            truelow.append(min(data[l-1], self.ret_low[l]))
        tr = np.array(truehigh) - np.array(truelow)
        atr = self.sma(tr, period=period)
        return atr

    @getIndicatorName
    def stdDev(self, data:object, period=20):
        """
        StandardDeviation 标准偏差 (StdDev) StandardDeviation
            If 2 datas are provided as parameters, the 2nd is considered to be the
            mean of the first
           Formula:
              - meansquared = SimpleMovingAverage(pow(data, 2), period) 均方
              - squaredmean = pow(SimpleMovingAverage(data, period), 2) 平方平均
              - stddev = pow(meansquared - squaredmean, 0.5)  # square root

            See:
              - http://en.wikipedia.org/wiki/Standard_deviation
        :param data:
        :param period:
        :return:
        """
        meansquared = self.sma(pow(np.array(data), 2), period)
        mead_data = self.sma(data, period)
        squaredmean = pow(mead_data, 2)
        self.stddev = pow(np.array(meansquared)-np.array(squaredmean), 0.5)
        return self.stddev

    @getAverageName
    def boll(self, data:object, period=20, devfactor=2):
        """
        布林带 (BollingerBands boll  。中轨为股价的平均成本，上轨和下轨可分别视为股价的压力线和支撑线。)
        Formula:
          - midband = SimpleMovingAverage(close, period)
          - topband = midband + devfactor * StandardDeviation(data, period)
          - botband = midband - devfactor * StandardDeviation(data, period)

        See:
          - http://en.wikipedia.org/wiki/Bollinger_Bands
        :param data:
        :param period:
        :return: top mid bottom
        """
        self.mid = self.sma(data, period)
        self.top = np.array(self.mid) + devfactor * np.array(self.stdDev(data, period))
        self.bottom = np.array(self.mid) - devfactor * np.array(self.stdDev(data, period))

        return self.top, self.mid, self.bottom

    @getIndicatorName
    def AroonIndicator(self, data:object, period:int):
        """
        Formula:
          - up = 100 * (period - distance to highest high) / period
          - down = 100 * (period - distance to lowest low) / period
        See:
            - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:aroon
        :param data:
        :param period:
        :return:
        """
        pass

    @getAverageName
    def UltimateOscillator(self, data: object, period: int):
        '''
            终极振荡器
            Formula:
              # Buying Pressure = Close - TrueLow
              BP = Close - Minimum(Low or Prior Close)

              # TrueRange = TrueHigh - TrueLow
              TR = Maximum(High or Prior Close)  -  Minimum(Low or Prior Close)

              Average7 = (7-period BP Sum) / (7-period TR Sum)
              Average14 = (14-period BP Sum) / (14-period TR Sum)
              Average28 = (28-period BP Sum) / (28-period TR Sum)

              UO = 100 x [(4 x Average7)+(2 x Average14)+Average28]/(4+2+1)

            See:

              - https://en.wikipedia.org/wiki/Ultimate_oscillator
              - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ultimate_oscillator
        '''
        pass

    @getIndicatorName
    def trix(self, data: object, period: int, rocperiod=1):
        '''
            三重指数平滑移动平均 技术分析(Triple Exponentially Smoothed Moving Average) TR
           Defined by Jack Hutson in the 80s and shows the Rate of Change (%) or slope
           of a triple exponentially smoothed moving average

           Formula:
             - ema1 = EMA(data, period)
             - ema2 = EMA(ema1, period)
             - ema3 = EMA(ema2, period)
             - trix = 100 * (ema3 - ema3(-1)) / ema3(-1)

             The final formula can be simplified to: 100 * (ema3 / ema3(-1) - 1)

           The moving average used is the one originally defined by Wilder,
           the SmoothedMovingAverage

           See:
             - https://en.wikipedia.org/wiki/Trix_(technical_analysis)
             - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:trix
        '''
        ema1 = self.ema(data, period=period)
        ema2 = self.ema(ema1, period=period)
        ema3 = self.ema(ema2, period=period)
        end = len(ema3)
        self.trix_list = ema3
        for i in range(period, end):
            self.trix_list[i] = 100.0 * (ema3[i]/ema3[i-rocperiod] - 1.0)
        return self.trix_list

    @getIndicatorName
    def roc(self, data: object, period=12):
        """
        Formula:
          - roc = (data - data_period) / data_period

        See:
          - http://en.wikipedia.org/wiki/Momentum_(technical_analysis)
        :param data:
        :param period:
        :return:
        """
        self.roc_list = deepcopy(data)
        end = len(data)
        for i in range(period, end):
            self.roc_list[i] = (data[i] - data[i-period]) / data[i-period]
        return self.roc_list

    @getIndicatorName
    def mtm(self, data: object, period: int):
        """
        动量指标(MTM) Momentum
            Formula:
              - momentum = data - data_period

            See:
              - http://en.wikipedia.org/wiki/Momentum_(technical_analysis)
        :param data:
        :param period:
        :return:
        """
        self.momentum_list = deepcopy(data)
        end = len(data)
        for i in range(period, end):
            self.momentum_list[i] = data[i] - data[i-period]
        return self.momentum_list

    @getIndicatorName
    def tema(self, data: object, period: int):
        """
         TripleExponentialMovingAverage(TEMA 试图减少与移动平均数相关的固有滞后)
        Formula:
          - ema1 = ema(data, period)
          - ema2 = ema(ema1, period)
          - ema3 = ema(ema2, period)
          - tema = 3 * ema1 - 3 * ema2 + ema3
        :param data:
        :param period:
        :return:
        """
        ema1 = self.ema(data, period)
        ema2 = self.ema(ema1, period)
        ema3 = self.ema(ema2, period)
        self.tema_list = 3 * np.array(ema1) - 3 * ema2 + ema3
        return self.tema_list

    @getIndicatorName
    def wr(self, data:object, period=14):
        """
        WilliamsR
        Formula:
          - num = highest_period - close
          - den = highestg_period - lowest_period
          - percR = (num / den) * -100.0

        See:
          - http://en.wikipedia.org/wiki/Williams_%25R
        :param data:
        :param period:
        :return:
        """
        end = len(data)
        num = deepcopy(data)
        den = deepcopy(data)
        for i in range(period, end):
            num[i] = max(self.ret_high[i - period + 1: i + 1])
        for i in range(period, end):
            den[i] = min(self.ret_low[i - period + 1: i + 1])
        self.percR = -100 * (np.array(num) / np.array(data)) / (np.array(num) - np.array(den))
        return self.percR

    def mean_dev(self, data, mean, period=20):
        """
        MeanDeviation
        Note:
          - If 2 datas are provided as parameters, the 2nd is considered to be the
            mean of the first

         Formula:
          - mean = MovingAverage(data, period) (or provided mean)
          - absdeviation = abs(data - mean)
          - meandev = MovingAverage(absdeviation, period)

        See:
          - https://en.wikipedia.org/wiki/Average_absolute_deviation
        :param data:
        :param period:
        :return:
        """
        absdev = abs(np.array(data) - np.array(mean))
        meandev = self.sma(absdev, period)
        return meandev

    def cci(self, period=20, factor=0.015):
        """
        商品渠道指数 CommodityChannelIndex
        Formula:
          - tp = typical_price = (high + low + close) / 3
          - tpmean = MovingAverage(tp, period)
          - deviation = tp - tpmean
          - meandev = MeanDeviation(tp)
          - cci = deviation / (meandeviation * factor)

        See:
          - https://en.wikipedia.org/wiki/Commodity_channel_index
            :return:
        """
        tp = (self.ret_high + self.ret_low + self.ret_close) / 3
        tpmean = self.sma(tp, period)
        dev = np.array(tp) - np.array(tpmean)
        meandev = self.mean_dev(tp, tpmean, period)
        self.cci_list = np.array(dev) / (factor * meandev)
        return self.cci_list

    def sar(self, data, period=2, i_af=0.02, afmax=0.02):
        """
        抛物线指标 Parabolic SAR
        See:
          - https://en.wikipedia.org/wiki/Parabolic_SAR
          - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:parabolic_sar

        :return:
        """
        self.sar_list = []
        status = {
            "sar": None,
            "tr": None,
            "af": 0.0,
            "ep": 0.0
        }
        num = len(data)

        sar = (self.ret_high[0] + self.ret_low[0]) / 2.0
        status['sar'] = sar
        status['af'] = i_af
        if data[1] >= data[0]:
            status['tr'] = False
            status['ep'] = self.ret_low[0]
        else:
            status['tr'] = True
            status['ep'] = self.ret_high[0]

        for i in range(num):
            n = i - period + 1
            m = n + 1

            hi = self.ret_high[m]
            lo = self.ret_low[m]

            tr = status['tr']
            sar = status['sar']

            if (tr and sar >= lo) or (not tr and sar <= hi):
                tr = not tr
                sar = status['ep']
                ep = hi if tr else lo
                af = i_af
            else:
                ep = status['ep']
                af = status['af']

            if tr:
                if hi > ep:
                    ep = hi
                    af = min(af + i_af, afmax)
            else:
                if lo < ep:
                    ep = lo
                    af = min(af + i_af, afmax)
            sar = sar + af * (ep - sar)

            if tr:  # long trade
                lo1 = self.ret_low[n]
                if sar > lo or sar > lo1:
                    sar = min(lo, lo1)  # sar not above last 2 lows -> lower
            else:
                hi1 = self.ret_high[n]
                if sar < hi or sar < hi1:
                    sar = max(hi, hi1)
            status['tr'] = tr
            status['sar'] = sar
            status['ep'] = ep
            status['af'] = af
            self.sar_list.append(status)
        return self.sar_list