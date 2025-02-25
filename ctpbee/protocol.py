"""
ctpbee目前采用qifi协议 使得成为QUANTAXIS交易底层成为可能, 同时使得ctpbee用户能同时使用来自QA的界面端
"""


class Protocol:
    def __init__(self):
        pass

    def update_account(self, account):
        raise NotImplementedError

    def update_order(self, order):
        raise NotImplementedError

    def update_trade(self, trade):
        raise NotImplementedError

    def save(self):
        """
        此函数实现保存在本地数据与缓存协议的同步
        """
        raise NotImplementedError
