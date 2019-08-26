import types
from functools import wraps

from ctpbee.constant import EVENT_LOG
from ctpbee.event_engine import Event
from ctpbee.event_engine.engine import EVENT_TIMER


class RiskLevel:
    """
    检测到不同的函数操作进来 
    f.__name__ ---> 不同的处理函数 ---> 执行事前检查 ---> f(*args, **kwargs) ---> 事后检查 

    """
    app = None
    mapping = {}

    def __init__(self, func):
        wraps(func)(self)

    @classmethod
    def update_app(cls, app):
        cls.app = app
        cls.app.event_engine.register(EVENT_TIMER, cls.realtime_check)

    def __call__(self, *args, **kwargs):
        # check before execute
        result = None
        fr_func = getattr(self, f"before_{self.__wrapped__.__name__}", None)
        if fr_func:
            result = fr_func()
        if not result:
            self.log("事前检查失败, 放弃此次操作")
            return
        # execute func
        result = self.__wrapped__(*args, **kwargs)

        # clean the action
        af_func = getattr(self, f"after_{self.__wrapped__.__name__}", None)
        if not af_func:
            return af_func(result)
        else:
            return None

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def log(self, log):
        event = Event(EVENT_LOG, data=log)
        self.app.event_engine.put(event)

    def realtime_check(self):
        """ 一直检查 """
        pass
