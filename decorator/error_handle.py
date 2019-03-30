#coding:utf-8
from functools import wraps

import sys_signal
from sys_constant import ERROR_LEVEL

def err_collector(func):
    """
    收集错误信息 , 使得程序正常运行 .
    :param func: the func should be decorated
    :return: func
    """
    @wraps(func)
    def wrapper(data):
        try:
            func(data)
        except Exception as e:
            sys_signal.log_signal.send(log_message=e, log_level=ERROR_LEVEL)
        return func
    return wrapper