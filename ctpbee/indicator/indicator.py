"""
纯numpy实现指标计算方法

注:大部分来自于网上，已修复并扩展
"""

import numpy as np


def rolling(data, window):
    """创建滚动窗口

    Args:
        data: 输入数据数组
        window: 窗口大小

    Returns:
        滚动窗口数组
    """
    shape = data.shape[:-1] + (data.shape[-1] - window + 1, window)
    strides = data.strides + (data.strides[-1],)
    return np.lib.stride_tricks.as_strided(data, shape=shape, strides=strides)


# ------------------------------ 基础指标 ------------------------------


def std(data):
    """计算方差

    Args:
        data: 输入数据数组

    Returns:
        方差值
    """
    return np.std(data, ddof=1)


def sma(data, window):
    """简单移动平均线 (Simple Moving Average)

    Args:
        data: 输入数据数组
        window: 窗口大小

    Returns:
        SMA数组
    """
    weights = np.repeat(1.0, window) / window
    sma = np.convolve(data, weights, "valid")
    return np.concatenate(([np.nan] * (window - 1), sma))


def ma(data, n):
    """移动平均线 (Moving Average)

    Args:
        data: 输入数据数组
        n: 窗口大小

    Returns:
        MA数组
    """
    mv = np.convolve(data, np.ones(n) / n, mode="valid")
    return np.concatenate(([np.nan for k in range(n - 1)], mv))


def wma(values, window):
    """加权移动平均线 (Weighted Moving Average)

    Args:
        values: 输入数据数组
        window: 窗口大小

    Returns:
        WMA数组
    """
    weights = np.arange(window, 0, -1.0)
    weights /= window * (window + 1) / 2
    weighted_moving_averages = np.full(window - 1, np.nan)
    weighted_moving_averages = np.append(
        weighted_moving_averages, np.convolve(values, weights, "valid")
    )
    return weighted_moving_averages


# ------------------------------ EWMA相关函数 ------------------------------


def get_max_row_size(alpha, dtype=float):
    """获取最大行大小

    Args:
        alpha: EWMA的alpha参数
        dtype: 数据类型

    Returns:
        最大行大小
    """
    assert 0.0 <= alpha < 1.0

    # 处理alpha=0.0的情况，避免除以0
    if alpha == 0.0:
        return 1

    epsilon = np.finfo(dtype).tiny
    try:
        return int(np.log(epsilon) / np.log(1 - alpha)) + 1
    except (ZeroDivisionError, OverflowError):
        # 处理可能的异常，返回一个合理的默认值
        return 1000


def ewma_vectorized(data, alpha, offset=None, dtype=None, order="C", out=None):
    """向量化计算指数移动平均线

    Args:
        data: 输入数据
        alpha: EWMA的alpha参数
        offset: 偏移量
        dtype: 数据类型
        order: 数组存储顺序
        out: 输出数组

    Returns:
        EWMA数组
    """
    data = np.asarray(data)

    if dtype is None:
        if data.dtype == np.float32:
            dtype = np.float32
        else:
            dtype = np.float64
    else:
        dtype = np.dtype(dtype)

    if data.ndim > 1:
        data = data.reshape(-1, order)

    if out is None:
        out = np.empty_like(data, dtype=dtype)
    else:
        assert out.shape == data.shape
        assert out.dtype == dtype

    if data.size < 1:
        return out

    if offset is None:
        offset = data[0]

    alpha = np.asarray(alpha).astype(dtype)

    scaling_factors = np.power(
        1.0 - alpha, np.arange(data.size + 1, dtype=dtype), dtype=dtype
    )
    np.multiply(
        data, (alpha * scaling_factors[-2]) / scaling_factors[:-1], dtype=dtype, out=out
    )
    np.cumsum(out, dtype=dtype, out=out)
    out /= scaling_factors[-2::-1]

    if offset != 0:
        offset = np.asarray(offset).astype(dtype)
        out += offset * scaling_factors[1:]

    return out


def ewma_vectorized_2d(
    data, alpha, axis=None, offset=None, dtype=None, order="C", out=None
):
    """二维向量化计算指数移动平均线

    Args:
        data: 输入数据
        alpha: EWMA的alpha参数
        axis: 计算轴
        offset: 偏移量
        dtype: 数据类型
        order: 数组存储顺序
        out: 输出数组

    Returns:
        EWMA数组
    """
    data = np.asarray(data)

    assert data.ndim <= 2

    if dtype is None:
        if data.dtype == np.float32:
            dtype = np.float32
        else:
            dtype = np.float64
    else:
        dtype = np.dtype(dtype)

    if out is None:
        out = np.empty_like(data, dtype=dtype)
    else:
        assert out.shape == data.shape
        assert out.dtype == dtype

    if data.size < 1:
        return out

    if axis is None or data.ndim < 2:
        if isinstance(offset, np.ndarray):
            offset = offset[0]
        return ewma_vectorized(data, alpha, offset, dtype=dtype, order=order, out=out)

    assert -data.ndim <= axis < data.ndim

    out_view = out
    if axis < 0:
        axis = data.ndim - int(axis)

    if axis == 0:
        data = data.T
        out_view = out_view.T

    if offset is None:
        offset = np.copy(data[:, 0])
    elif np.size(offset) == 1:
        offset = np.reshape(offset, (1,))

    alpha = np.asarray(alpha).astype(dtype)

    row_size = data.shape[1]
    row_n = data.shape[0]
    scaling_factors = np.power(
        1.0 - alpha, np.arange(row_size + 1, dtype=dtype), dtype=dtype
    )

    np.multiply(
        data,
        np.multiply(
            alpha * scaling_factors[-2], np.ones((row_n, 1), dtype=dtype), dtype=dtype
        )
        / scaling_factors[np.newaxis, :-1],
        dtype=dtype,
        out=out_view,
    )
    np.cumsum(out_view, axis=1, dtype=dtype, out=out_view)
    out_view /= scaling_factors[np.newaxis, -2::-1]

    if not (np.size(offset) == 1 and offset == 0):
        offset = offset.astype(dtype, copy=False)
        out_view += offset[:, np.newaxis] * scaling_factors[np.newaxis, 1:]

    return out


def ewma(data, period, row_size=None, dtype=None, order="C", out=None):
    """指数加权移动平均线 (Exponential Weighted Moving Average)

    Args:
        data: 输入数据
        period: 周期
        row_size: 行大小
        dtype: 数据类型
        order: 数组存储顺序
        out: 输出数组

    Returns:
        EWMA数组
    """
    data = np.asarray(data)
    alpha = 1.0 - 2.0 / (1.0 + period)

    # 当alpha=0.0时，EWMA等于原始数据，直接返回
    if alpha == 0.0:
        if out is None:
            return data.astype(dtype, copy=True)
        else:
            out[:] = data.astype(dtype, copy=False)
            return out

    if dtype is None:
        if data.dtype == np.float32:
            dtype = np.float32
        else:
            dtype = np.float64
    else:
        dtype = np.dtype(dtype)

    if row_size is not None:
        row_size = int(row_size)
    else:
        row_size = get_max_row_size(alpha, dtype)

    if data.size <= row_size:
        return ewma_vectorized(data, alpha, dtype=dtype, order=order, out=out)

    if data.ndim > 1:
        data = np.reshape(data, -1, order=order)

    if out is None:
        out = np.empty_like(data, dtype=dtype)
    else:
        assert out.shape == data.shape
        assert out.dtype == dtype

    row_n = int(data.size // row_size)
    trailing_n = int(data.size % row_size)
    first_offset = data[0]

    if trailing_n > 0:
        out_main_view = np.reshape(out[:-trailing_n], (row_n, row_size))
        data_main_view = np.reshape(data[:-trailing_n], (row_n, row_size))
    else:
        out_main_view = out
        data_main_view = data

    ewma_vectorized_2d(
        data_main_view,
        alpha,
        axis=1,
        offset=0,
        dtype=dtype,
        order="C",
        out=out_main_view,
    )

    scaling_factors = (1 - alpha) ** np.arange(1, row_size + 1)
    last_scaling_factor = scaling_factors[-1]

    offsets = np.empty(out_main_view.shape[0], dtype=dtype)
    offsets[0] = first_offset
    for i in range(1, out_main_view.shape[0]):
        offsets[i] = offsets[i - 1] * last_scaling_factor + out_main_view[i - 1, -1]

    out_main_view += offsets[:, np.newaxis] * scaling_factors[np.newaxis, :]

    if trailing_n > 0:
        ewma_vectorized(
            data[-trailing_n:],
            alpha,
            offset=out_main_view[-1, -1],
            dtype=dtype,
            order="C",
            out=out[-trailing_n:],
        )
    return out


# ------------------------------ 技术指标 ------------------------------


def std_dev(data, period):
    """标准差 (Standard Deviation)

    Args:
        data: 输入数据
        period: 周期

    Returns:
        标准差数组
    """
    mean_squared = ma(pow(np.array(data), 2), period)
    mead_data = ma(data, period)
    squared_mean = pow(mead_data, 2)
    return pow(np.array(mean_squared) - np.array(squared_mean), 0.5)


def rsi(data, period=14):
    """相对强弱指标 (Relative Strength Index)

    Args:
        data: 输入数据
        period: 周期

    Returns:
        RSI数组
    """
    diff = np.diff(data)
    up = np.where(diff > 0, diff, 0)
    down = np.where(diff < 0, abs(diff), 0)

    # 使用EWMA计算平均涨跌
    avg_up = ewma(up, period)[period - 1 :]
    avg_down = ewma(down, period)[period - 1 :]

    # 处理除零情况
    avg_down[avg_down == 0] = 0.0001

    rs = avg_up / avg_down
    rsi = 100.0 - (100.0 / (1.0 + rs))

    # 填充前period个NaN值
    return np.concatenate(([np.nan] * (period), rsi))


def macd(data, period_me1=12, period_me2=26, period_signal=9):
    """移动平均趋同/偏离 (MACD)

    Args:
        data: 输入数据
        period_me1: 短期EMA周期
        period_me2: 长期EMA周期
        period_signal: 信号线EMA周期

    Returns:
        (macd, signal, histo) 元组
    """
    me1 = ewma(data, period=period_me1)
    me2 = ewma(data, period=period_me2)
    macd = np.array(me1) - np.array(me2)
    signal = ewma(macd, period=period_signal)
    histo = np.array(macd) - np.array(signal)
    return macd, signal, histo


def kdj(close, high, low, n=9, m1=3, m2=3):
    """KDJ指标

    Args:
        close: 收盘价数组
        high: 最高价数组
        low: 最低价数组
        n: KDJ指标长度
        m1: K值权重
        m2: D值权重
    Returns:
        (K, D, J) 元组
    """
    assert len(close) == len(high) == len(low), "输入数组长度必须相同"

    # 计算RSV
    RSV = np.zeros_like(close)
    for i in range(n, len(close)):
        low_n = np.min(low[i - n : i])
        high_n = np.max(high[i - n : i])
        if high_n != low_n:
            RSV[i] = (close[i] - low_n) / (high_n - low_n) * 100
        else:
            RSV[i] = 50

    # 计算K
    K = np.zeros_like(RSV)
    K[:n] = 50
    for i in range(n, len(close)):
        K[i] = K[i - 1] * (m1 - 1) / m1 + RSV[i] * 1 / m1

    # 计算D
    D = np.zeros_like(K)
    D[:n] = 50
    for i in range(n, len(close)):
        D[i] = D[i - 1] * (m2 - 1) / m2 + K[i] * 1 / m2

    # 计算J
    J = 3 * K - 2 * D

    return K, D, J


def stochastic(close, high, low, k_period=14, d_period=3):
    """随机指标 (Stochastic Oscillator)

    Args:
        close: 收盘价数组
        high: 最高价数组
        low: 最低价数组
        k_period: K周期
        d_period: D周期

    Returns:
        (K, D) 元组
    """
    assert len(close) == len(high) == len(low), "输入数组长度必须相同"

    K = np.zeros_like(close)
    for i in range(k_period, len(close)):
        low_k = np.min(low[i - k_period : i])
        high_k = np.max(high[i - k_period : i])
        if high_k != low_k:
            K[i] = (close[i] - low_k) / (high_k - low_k) * 100
        else:
            K[i] = 50

    D = sma(K, d_period)

    return K, D


def bollinger_bands(close, window_size=20, num_of_std=2):
    """布林带 (Bollinger Bands)

    Args:
        close: 收盘价数组
        window_size: 窗口大小
        num_of_std: 标准差倍数

    Returns:
        (upper_band, middle_band, lower_band) 元组
    """
    n = len(close)
    upper_band = np.zeros(n) * np.nan
    middle_band = np.zeros(n) * np.nan
    lower_band = np.zeros(n) * np.nan

    for i in range(window_size - 1, n):
        window = close[i - window_size + 1 : i + 1]
        middle_band[i] = np.mean(window)
        std_dev = np.std(window)
        upper_band[i] = middle_band[i] + (std_dev * num_of_std)
        lower_band[i] = middle_band[i] - (std_dev * num_of_std)

    return upper_band, middle_band, lower_band


def atr(high, low, close, period=14):
    """平均真实波动幅度 (Average True Range)

    Args:
        high: 最高价数组
        low: 最低价数组
        close: 收盘价数组
        period: 周期

    Returns:
        ATR数组
    """
    assert len(high) == len(low) == len(close), "输入数组长度必须相同"

    n = len(close)
    tr = np.zeros(n)

    # 计算真实波动幅度
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr1 = high[i] - low[i]
        tr2 = abs(high[i] - close[i - 1])
        tr3 = abs(low[i] - close[i - 1])
        tr[i] = max(tr1, tr2, tr3)

    # 计算ATR
    atr = ewma(tr, period)
    return atr


def obv(close, volume):
    """能量潮指标 (On Balance Volume)

    Args:
        close: 收盘价数组
        volume: 成交量数组

    Returns:
        OBV数组
    """
    assert len(close) == len(volume), "输入数组长度必须相同"

    obv = np.zeros_like(close)
    obv[0] = volume[0]

    for i in range(1, len(close)):
        if close[i] > close[i - 1]:
            obv[i] = obv[i - 1] + volume[i]
        elif close[i] < close[i - 1]:
            obv[i] = obv[i - 1] - volume[i]
        else:
            obv[i] = obv[i - 1]

    return obv


def roc(close, period=12):
    """变动率指标 (Rate of Change)

    Args:
        close: 收盘价数组
        period: 周期

    Returns:
        ROC数组
    """
    roc = np.zeros_like(close) * np.nan

    for i in range(period, len(close)):
        roc[i] = (close[i] - close[i - period]) / close[i - period] * 100

    return roc


def williams_r(close, high, low, period=14):
    """威廉指标 (Williams %R)

    Args:
        close: 收盘价数组
        high: 最高价数组
        low: 最低价数组
        period: 周期

    Returns:
        Williams %R数组
    """
    assert len(close) == len(high) == len(low), "输入数组长度必须相同"

    wr = np.zeros_like(close) * np.nan

    for i in range(period, len(close)):
        high_n = np.max(high[i - period : i])
        low_n = np.min(low[i - period : i])
        if high_n != low_n:
            wr[i] = (high_n - close[i]) / (high_n - low_n) * -100
        else:
            wr[i] = -50

    return wr


def adx(high, low, close, period=14):
    """平均趋向指标 (Average Directional Index)

    Args:
        high: 最高价数组
        low: 最低价数组
        close: 收盘价数组
        period: 周期

    Returns:
        (ADX, +DI, -DI) 元组
    """
    assert len(high) == len(low) == len(close), "输入数组长度必须相同"

    n = len(close)

    # 计算真实波动幅度
    tr = np.zeros(n)
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr1 = high[i] - low[i]
        tr2 = abs(high[i] - close[i - 1])
        tr3 = abs(low[i] - close[i - 1])
        tr[i] = max(tr1, tr2, tr3)

    # 计算上升和下降趋向
    plus_dm = np.zeros(n)
    minus_dm = np.zeros(n)

    for i in range(1, n):
        up_move = high[i] - high[i - 1]
        down_move = low[i - 1] - low[i]

        if up_move > down_move and up_move > 0:
            plus_dm[i] = up_move
        else:
            plus_dm[i] = 0

        if down_move > up_move and down_move > 0:
            minus_dm[i] = down_move
        else:
            minus_dm[i] = 0

    # 计算ATR
    atr = ewma(tr, period)

    # 计算+DI和-DI
    plus_di = 100 * ewma(plus_dm, period) / atr
    minus_di = 100 * ewma(minus_dm, period) / atr

    # 计算DX
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)

    # 计算ADX
    adx = ewma(dx, period)

    return adx, plus_di, minus_di


def cci(close, high, low, period=20):
    """顺势指标 (Commodity Channel Index)

    Args:
        close: 收盘价数组
        high: 最高价数组
        low: 最低价数组
        period: 周期

    Returns:
        CCI数组
    """
    assert len(close) == len(high) == len(low), "输入数组长度必须相同"

    n = len(close)
    cci = np.zeros(n) * np.nan

    for i in range(period, n):
        # 计算典型价格
        typical_price = (
            high[i - period : i] + low[i - period : i] + close[i - period : i]
        ) / 3

        # 计算简单移动平均
        sma_tp = np.mean(typical_price)

        # 计算平均偏差
        mean_dev = np.mean(np.abs(typical_price - sma_tp))

        if mean_dev == 0:
            cci[i] = 0
        else:
            cci[i] = (typical_price[-1] - sma_tp) / (0.015 * mean_dev)

    return cci


def rvi(close, high, low, period=10):
    """相对活力指标 (Relative Vigor Index)

    Args:
        close: 收盘价数组
        high: 最高价数组
        low: 最低价数组
        period: 周期

    Returns:
        (RVI, Signal) 元组
    """
    assert len(close) == len(high) == len(low), "输入数组长度必须相同"

    # 计算变动
    diff_close = np.diff(close)
    diff_high = np.diff(high)
    diff_low = np.diff(low)

    # 计算分子和分母
    numerator = (
        diff_close[-period:]
        + 2 * diff_close[-period - 1 : -1]
        + 2 * diff_close[-period - 2 : -2]
        + diff_close[-period - 3 : -3]
    ) / 6
    denominator = (
        diff_high[-period:]
        + 2 * diff_high[-period - 1 : -1]
        + 2 * diff_high[-period - 2 : -2]
        + diff_high[-period - 3 : -3]
    ) / 6
    denominator = (
        denominator
        - (
            diff_low[-period:]
            + 2 * diff_low[-period - 1 : -1]
            + 2 * diff_low[-period - 2 : -2]
            + diff_low[-period - 3 : -3]
        )
        / 6
    )

    # 处理除零情况
    denominator[denominator == 0] = 0.0001

    rvi = np.sum(numerator) / np.sum(denominator)

    # 计算信号线
    signal = ewma(np.array([rvi]), period)[0]

    return rvi, signal


def mass_index(high, low, period1=9, period2=25):
    """质量指数 (Mass Index)

    Args:
        high: 最高价数组
        low: 最低价数组
        period1: 短期EMA周期
        period2: 长期EMA周期

    Returns:
        Mass Index数组
    """
    assert len(high) == len(low), "输入数组长度必须相同"

    n = len(high)
    mass = np.zeros(n) * np.nan

    # 计算EMA1
    ema1 = ewma(high - low, period1)

    # 计算EMA2
    ema2 = ewma(ema1, period1)

    # 计算EMA比率
    ema_ratio = ema1 / ema2

    # 计算Mass Index
    for i in range(period2, n):
        mass[i] = np.sum(ema_ratio[i - period2 : i])

    return mass


def chaikin_oscillator(high, low, close, volume, period1=3, period2=10):
    """柴金振荡器 (Chaikin Oscillator)

    Args:
        high: 最高价数组
        low: 最低价数组
        close: 收盘价数组
        volume: 成交量数组
        period1: 短期EMA周期
        period2: 长期EMA周期

    Returns:
        Chaikin Oscillator数组
    """
    assert len(high) == len(low) == len(close) == len(volume), "输入数组长度必须相同"

    n = len(close)

    # 计算资金流量乘数
    mf_multiplier = ((close - low) - (high - close)) / (high - low)
    mf_multiplier[np.isnan(mf_multiplier)] = 0
    mf_multiplier[np.isinf(mf_multiplier)] = 0

    # 计算资金流量
    mf_volume = mf_multiplier * volume

    # 计算累积资金流量
    adl = np.zeros(n)
    adl[0] = mf_volume[0]
    for i in range(1, n):
        adl[i] = adl[i - 1] + mf_volume[i]

    # 计算柴金振荡器
    ema1 = ewma(adl, period1)
    ema2 = ewma(adl, period2)
    chaikin = ema1 - ema2

    return chaikin


def vortex_indicator(high, low, close, period=14):
    """漩涡指标 (Vortex Indicator)

    Args:
        high: 最高价数组
        low: 最低价数组
        close: 收盘价数组
        period: 周期

    Returns:
        (+VI, -VI) 元组
    """
    assert len(high) == len(low) == len(close), "输入数组长度必须相同"

    n = len(close)
    plus_vi = np.zeros(n) * np.nan
    minus_vi = np.zeros(n) * np.nan

    # 计算真实波动幅度
    tr = np.zeros(n)
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr1 = high[i] - low[i]
        tr2 = abs(high[i] - close[i - 1])
        tr3 = abs(low[i] - close[i - 1])
        tr[i] = max(tr1, tr2, tr3)

    # 计算+VM和-VM
    plus_vm = np.zeros(n)
    minus_vm = np.zeros(n)
    for i in range(1, n):
        plus_vm[i] = abs(high[i] - low[i - 1])
        minus_vm[i] = abs(low[i] - high[i - 1])

    # 计算+VI和-VI
    for i in range(period, n):
        sum_tr = np.sum(tr[i - period : i])
        if sum_tr == 0:
            plus_vi[i] = 0
            minus_vi[i] = 0
        else:
            plus_vi[i] = np.sum(plus_vm[i - period : i]) / sum_tr
            minus_vi[i] = np.sum(minus_vm[i - period : i]) / sum_tr

    return plus_vi, minus_vi
