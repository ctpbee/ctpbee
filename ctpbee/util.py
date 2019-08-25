

class RiskLevel:
    def __init__(self, app):
        self.app = app
        # self.app.event_engine.register(EVENT_TIMER, self.realtime_check)

    """ 
    检测到不同的函数操作进来 
    f.__name__ ---> 不同的处理函数 ---> 执行事前检查 ---> f(*args, **kwargs) ---> 事后检查 


    """

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

    def realtime_check(self):
        """ 一直检查 """
        pass

# 风控层 用户自行自定义