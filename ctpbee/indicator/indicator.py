"""
纯numpy实现指标计算方法

注:大部分来自于网上
"""

import numpy as np


def rolling(data, window):
    shape = data.shape[:-1] + (data.shape[-1] - window + 1, window)
    strides = data.strides + (data.strides[-1],)
    return np.lib.stride_tricks.as_strided(data, shape=shape, strides=strides)


def std(data):
    """
    计算方差
    """
    return np.std(data, ddof=1)


def ma(data, n):
    """移动平均线"""
    mv = np.convolve(data, np.ones(n) / n, mode='valid')
    return np.concatenate(([np.NaN for k in range(n - 1)], mv))


def ewma(data, period, row_size=None, dtype=None, order='C', out=None):
    """
    copy from https://blog.csdn.net/Shepherdppz/article/details/104120689

    Reshapes data before calculating EWMA, then iterates once over the rows
    to calculate the offset without precision issues
    :param data: Input data, will be flattened.
    :param alpha: scalar float in range (0,1)
        The alpha parameter for the moving average.
    :param row_size: int, optional
        The row size to use in the computation. High row sizes need higher precision,
        low values will impact performance. The optimal value depends on the
        platform and the alpha being used. Higher alpha values require lower
        row size. Default depends on dtype.
    :param dtype: optional
        Data type used for calculations. Defaults to float64 unless
        data.dtype is float32, then it will use float32.
    :param order: {'C', 'F', 'A'}, optional
        Order to use when flattening the data. Defaults to 'C'.
    :param out: ndarray, or None, optional
        A location into which the result is stored. If provided, it must have
        the same shape as the desired output. If not provided or `None`,
        a freshly-allocated array is returned.
    :return: The flattened result.
    """
    data = np.array(data, copy=False)
    alpha = 1.0 - 2.0 / (1.0 + period)

    if dtype is None:
        if data.dtype == np.float32:
            dtype = np.float32
        else:
            dtype = np.float
    else:
        dtype = np.dtype(dtype)

    if row_size is not None:
        row_size = int(row_size)
    else:
        row_size = get_max_row_size(alpha, dtype)

    if data.size <= row_size:
        # The normal function can handle this input, use that
        return ewma_vectorized(data, alpha, dtype=dtype, order=order, out=out)

    if data.ndim > 1:
        # flatten input
        data = np.reshape(data, -1, order=order)

    if out is None:
        out = np.empty_like(data, dtype=dtype)
    else:
        assert out.shape == data.shape
        assert out.dtype == dtype

    row_n = int(data.size // row_size)  # the number of rows to use
    trailing_n = int(data.size % row_size)  # the amount of data leftover
    first_offset = data[0]

    if trailing_n > 0:
        # set temporary results to slice view of out parameter
        out_main_view = np.reshape(out[:-trailing_n], (row_n, row_size))
        data_main_view = np.reshape(data[:-trailing_n], (row_n, row_size))
    else:
        out_main_view = out
        data_main_view = data

    # get all the scaled cumulative sums with 0 offset
    ewma_vectorized_2d(data_main_view, alpha, axis=1, offset=0, dtype=dtype,
                       order='C', out=out_main_view)

    scaling_factors = (1 - alpha) ** np.arange(1, row_size + 1)
    last_scaling_factor = scaling_factors[-1]

    # create offset array
    offsets = np.empty(out_main_view.shape[0], dtype=dtype)
    offsets[0] = first_offset
    # iteratively calculate offset for each row
    for i in range(1, out_main_view.shape[0]):
        offsets[i] = offsets[i - 1] * last_scaling_factor + out_main_view[i - 1, -1]

    # add the offsets to the result
    out_main_view += offsets[:, np.newaxis] * scaling_factors[np.newaxis, :]

    if trailing_n > 0:
        # process trailing data in the 2nd slice of the out parameter
        ewma_vectorized(data[-trailing_n:], alpha, offset=out_main_view[-1, -1],
                        dtype=dtype, order='C', out=out[-trailing_n:])
    return out


def get_max_row_size(alpha, dtype=float):
    assert 0. <= alpha < 1.
    # This will return the maximum row size possible on
    # your platform for the given dtype. I can find no impact on accuracy
    # at this value on my machine.
    # Might not be the optimal value for speed, which is hard to predict
    # due to numpy's optimizations
    # Use np.finfo(dtype).eps if you  are worried about accuracy
    # and want to be extra safe.
    epsilon = np.finfo(dtype).tiny
    # If this produces an OverflowError, make epsilon larger
    return int(np.log(epsilon) / np.log(1 - alpha)) + 1


def ewma_vectorized(data, alpha, offset=None, dtype=None, order='C', out=None):
    """
    Calculates the exponential moving average over a vector.
    Will fail for large inputs.
    :param data: Input data
    :param alpha: scalar float in range (0,1)
        The alpha parameter for the moving average.
    :param offset: optional
        The offset for the moving average, scalar. Defaults to data[0].
    :param dtype: optional
        Data type used for calculations. Defaults to float64 unless
        data.dtype is float32, then it will use float32.
    :param order: {'C', 'F', 'A'}, optional
        Order to use when flattening the data. Defaults to 'C'.
    :param out: ndarray, or None, optional
        A location into which the result is stored. If provided, it must have
        the same shape as the input. If not provided or `None`,
        a freshly-allocated array is returned.
    """
    data = np.array(data, copy=False)

    if dtype is None:
        if data.dtype == np.float32:
            dtype = np.float32
        else:
            dtype = np.float64
    else:
        dtype = np.dtype(dtype)

    if data.ndim > 1:
        # flatten input
        data = data.reshape(-1, order)

    if out is None:
        out = np.empty_like(data, dtype=dtype)
    else:
        assert out.shape == data.shape
        assert out.dtype == dtype

    if data.size < 1:
        # empty input, return empty array
        return out

    if offset is None:
        offset = data[0]

    alpha = np.array(alpha, copy=False).astype(dtype, copy=False)

    # scaling_factors -> 0 as len(data) gets large
    # this leads to divide-by-zeros below
    scaling_factors = np.power(1. - alpha, np.arange(data.size + 1, dtype=dtype),
                               dtype=dtype)
    # create cumulative sum array
    np.multiply(data, (alpha * scaling_factors[-2]) / scaling_factors[:-1],
                dtype=dtype, out=out)
    np.cumsum(out, dtype=dtype, out=out)

    # cumsums / scaling
    out /= scaling_factors[-2::-1]

    if offset != 0:
        offset = np.array(offset, copy=False).astype(dtype, copy=False)
        # add offsets
        out += offset * scaling_factors[1:]

    return out


def ewma_vectorized_2d(data, alpha, axis=None, offset=None, dtype=None, order='C', out=None):
    """
    Calculates the exponential moving average over a given axis.
    :param data: Input data, must be 1D or 2D array.
    :param alpha: scalar float in range (0,1)
        The alpha parameter for the moving average.
    :param axis: The axis to apply the moving average on.
        If axis==None, the data is flattened.
    :param offset: optional
        The offset for the moving average. Must be scalar or a
        vector with one element for each row of data. If set to None,
        defaults to the first value of each row.
    :param dtype: optional
        Data type used for calculations. Defaults to float64 unless
        data.dtype is float32, then it will use float32.
    :param order: {'C', 'F', 'A'}, optional
        Order to use when flattening the data. Ignored if axis is not None.
    :param out: ndarray, or None, optional
        A location into which the result is stored. If provided, it must have
        the same shape as the desired output. If not provided or `None`,
        a freshly-allocated array is returned.
    """
    data = np.array(data, copy=False)

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
        # empty input, return empty array
        return out

    if axis is None or data.ndim < 2:
        # use 1D version
        if isinstance(offset, np.ndarray):
            offset = offset[0]
        return ewma_vectorized(data, alpha, offset, dtype=dtype, order=order,
                               out=out)

    assert -data.ndim <= axis < data.ndim

    # create reshaped data views
    out_view = out
    if axis < 0:
        axis = data.ndim - int(axis)

    if axis == 0:
        # transpose data views so columns are treated as rows
        data = data.T
        out_view = out_view.T

    if offset is None:
        # use the first element of each row as the offset
        offset = np.copy(data[:, 0])
    elif np.size(offset) == 1:
        offset = np.reshape(offset, (1,))

    alpha = np.array(alpha, copy=False).astype(dtype, copy=False)

    # calculate the moving average
    row_size = data.shape[1]
    row_n = data.shape[0]
    scaling_factors = np.power(1. - alpha, np.arange(row_size + 1, dtype=dtype),
                               dtype=dtype)
    # create a scaled cumulative sum array
    np.multiply(
        data,
        np.multiply(alpha * scaling_factors[-2], np.ones((row_n, 1), dtype=dtype),
                    dtype=dtype)
        / scaling_factors[np.newaxis, :-1],
        dtype=dtype, out=out_view
    )
    np.cumsum(out_view, axis=1, dtype=dtype, out=out_view)
    out_view /= scaling_factors[np.newaxis, -2::-1]

    if not (np.size(offset) == 1 and offset == 0):
        offset = offset.astype(dtype, copy=False)
        # add the offsets to the scaled cumulative sums
        out_view += offset[:, np.newaxis] * scaling_factors[np.newaxis, 1:]

    return out


def wma(values, window):
    weights = np.arange(window, 0, -1.0)
    weights /= (window * (window + 1) / 2)
    weighted_moving_averages = np.empty(window - 1)
    weighted_moving_averages[:] = np.NAN
    weighted_moving_averages = np.append(weighted_moving_averages, np.convolve(values, weights, 'valid'))
    return weighted_moving_averages


def std_dev(data, period):
    mean_squared = ma(pow(np.array(data), 2), period)
    mead_data = ma(data, period)
    squared_mean = pow(mead_data, 2)
    return pow(np.array(mean_squared) - np.array(squared_mean), 0.5)


def macd(data, period_me1=12, period_me2=26, period_signal=9):
    """
    移动平均趋同/偏离(异同移动平均线) MACDHisto
    Formula:
        - macd = ema(data, me1_period) - ema(data, me2_period)
        - signal = ema(macd, signal_period)
        - histo = macd - signal
    """
    me1 = ewma(data, period=period_me1)
    me2 = ewma(data, period=period_me2)
    macd = np.array(me1) - np.array(me2)
    signal = ewma(macd, period=period_signal)
    histo = np.array(macd) - np.array(signal)
    return macd, signal, histo


def rsi(data, period=5):
    diff = np.diff(data)
    up = np.where(diff > 0.0, 0.0)
    diff_rev = diff * -1
    down = np.where(diff_rev, 0.0)
    ma_up = ewma(up, period=period)
    ma_down = ewma(down, period=period)
    rs = np.array(ma_up) / np.array(ma_down)
    return 100.0 - 100.0 / (1.0 + rs)


def kd(data: np.array, period, period_df_ast=3):
    diff = np.diff(data)
    rolling_array = rolling(diff, period)
    lowest = np.array(list(map(np.min, rolling_array)))
    highest = np.array(list(map(np.max, rolling_array)))
    k_num = np.array(data) - lowest
    k_den = np.array(highest) - np.array(lowest)
    k = 100 * (k_num / k_den)
    d = ma(k, period_df_ast)
    perc = ma(d, period_df_ast)
    return k, perc


def kdj(close, high, low, n=9, m1=3, m2=3):
    """
    :param close: ndarray, close price
    :param high: ndarray, high price
    :param low: ndarray, low price
    :param n: int, the length of KDJ indicator
    :param m1: int, the weight of K value
    :param m2: int, the weight of D value
    :return: tuple, (K, D, J)
    """
    RSV = (close - np.minimum(low, np.roll(close, n))) / (
            np.maximum(high, np.roll(close, n)) - np.minimum(low, np.roll(close, n))) * 100
    K = np.zeros_like(RSV)
    K[:n] = 50
    K = np.convolve(K, np.ones(m1) / m1, mode='same')[n - 1:]
    K = np.convolve(K, np.ones(m2) / m2, mode='same')[m2 - 1:]
    D = np.convolve(K, np.ones(m2) / m2, mode='same')
    J = 3 * K - 2 * D
    return K, D, J


def bollinger_bands(close, window_size, num_of_std):
    rolling_mean = np.mean(close[-window_size:])
    rolling_std = np.std(close[-window_size:])
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return upper_band, lower_band


def sma(data, window):
    weights = np.repeat(1.0, window) / window
    sma = np.convolve(data, weights, 'valid')
    return sma
