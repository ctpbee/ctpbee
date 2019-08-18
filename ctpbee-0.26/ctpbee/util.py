class RiskLevel:
    def __init__(self, app):
        self.app = app

    def __call__(self, *args, **kwargs):
        """ 将事件传输进来 """
        pass

    def before_send(self):
        raise NotImplemented

    def after_send(self):
        raise NotImplemented

    def before_cancle(self):
        raise NotImplemented

    def after_cancel(self):
        raise NotImplemented

    def checking(self):
        """这个函数会一直被触发 用于检查你的信息"""
        raise NotImplemented
