"""
ctpbee里面内置模拟成交网关 ---> 主要调用回测接口进行处理
"""
from ctpbee.looper.interface import LocalLooper


class SimInterface(LocalLooper):
    """
    模拟成交接口网关， 负责向上提供API
    """
