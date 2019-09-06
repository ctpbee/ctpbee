import types
from functools import wraps
from threading import Thread
from types import MethodType

from ctpbee.constant import EVENT_LOG
from ctpbee.event_engine import Event
from ctpbee.event_engine.engine import EVENT_TIMER
from ctpbee.helpers import end_thread


class ThreadMe(Thread):
    def __init__(self, *args, **kwargs):
        self.count = 0
        super().__init__(*args, **kwargs)


class RiskLevel:
    """
    检测到不同的函数操作进来 
    f.__name__ ---> 不同的处理函数 ---> 执行事前检查 ---> f(*args, **kwargs) ---> 事后检查 

    """
    app = None
    action = None
    thread_pool = []

    def __init__(self, func):
        wraps(func)(self)

    @classmethod
    def update_app(cls, app):
        """ 将app更新到类变量里面"""
        cls.app = app
        cls.action = app.action

        update_list = ["realtime_check", "mimo_thread"]
        for _ in update_list:
            func = getattr(cls, _)
            funcd = MethodType(func, cls)
            cls.app.event_engine.register(EVENT_TIMER, funcd)

    def mimo_thread(self, cur):
        for thread in self.thread_pool:
            # 判断线程的数量是否超过超时数
            if not isinstance(self.app.config['AFTER_TIMEOUT'], int):
                raise AttributeError("请检查你的配置中项 AFTER_TIMEOUT的值是否为整数")
            if thread.count >= self.app.config['AFTER_TIMEOUT']:
                try:
                    end_thread(thread)
                except ValueError:
                    pass
                self.thread_pool.remove(thread)
            thread.count += 1

    def run(self, func, args):
        # 你需要在此处实现超时设置, 避免最后的线程最后无限积累
        p = ThreadMe(target=func, args=(args,))
        p.start()
        self.thread_pool.append(p)

    def __call__(self, *args, **kwargs):
        # check before execute
        result = None
        fr_func = getattr(self, f"before_{self.__wrapped__.__name__}", None)
        if fr_func:
            result, new_args, new_kwargs = fr_func(*args, **kwargs)
        if not result:
            self.log("事前检查失败, 放弃此次操作")
        else:
            # execute func
            result = self.__wrapped__(*new_args, **new_kwargs)
            # clean the action

            af_func = getattr(self, f"after_{self.__wrapped__.__name__}", None)
            self.run(af_func, result)
        return result

    def __get__(self, instance, cls):
        if instance is None:
            res = self
        else:
            res = types.MethodType(self, instance)
        return res

    def log(self, log):
        event = Event(EVENT_LOG, data=log)
        self.app.event_engine.put(event)

    @classmethod
    def realtime_check(self, cur):
        """ 一直检查 """
        pass
