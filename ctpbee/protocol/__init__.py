class Protocol:

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
