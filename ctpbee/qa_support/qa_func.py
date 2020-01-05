"""
注意此处函数并不是由我编写
但是我并不想在ctpbee里面提供如此庞大的函数导入，
此处仅仅在ctpbee里面复制一些必要的函数

Thanks for QUANTAXIS --> https://github.com/QUANTAXIS/QUANTAXIS

函数我都会保持全名

author: yutiansut (https://github.com/yutiansut)
"""
import time


def QA_util_time_stamp(time_):
    """
    字符串 '2018-01-01 00:00:00'  转变成 float 类型时间 类似 time.time() 返回的类型
    :param time_: 字符串str -- 数据格式 最好是%Y-%m-%d %H:%M:%S 中间要有空格
    :return: 类型float
    """
    if len(str(time_)) == 10:
        # yyyy-mm-dd格式
        return time.mktime(time.strptime(time_, '%Y-%m-%d'))
    elif len(str(time_)) == 16:
        # yyyy-mm-dd hh:mm格式
        return time.mktime(time.strptime(time_, '%Y-%m-%d %H:%M'))
    else:
        timestr = str(time_)[0:19]
        return time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))

