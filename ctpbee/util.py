import types
from functools import wraps
from threading import Thread
from ctpbee.helpers import end_thread

from ctpbee.signals import common_signals


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
    logger = None
    action = None
    recorder = None
    thread_pool = []

    def __init__(self, func):
        wraps(func)(self)

    @classmethod
    def update_app(cls, app):
        """ 将app更新到类变量里面"""
        cls.app = app
        cls.action = app.action
        cls.logger = app.logger
        cls.recorder = app.recorder
        cls.center = app.center

        def connect_mimo(event):
            cls.mimo_thread()

        def connect_realtime(event):
            classmethod(getattr(cls, "realtime_check")).__func__(self=cls)

        common_signals.timer_signal.connect(connect_mimo, weak=False)

        common_signals.timer_signal.connect(connect_realtime, weak=False)

    @classmethod
    def warning(cls, msg, **kwargs):
        cls.logger.warning(msg, owner="Risk", **kwargs)

    @classmethod
    def info(cls, msg, **kwargs):
        cls.logger.info(msg, owner="Risk", **kwargs)

    @classmethod
    def error(cls, msg, **kwargs):
        cls.logger.error(msg, owner="Risk", **kwargs)

    @classmethod
    def debug(cls, msg, **kwargs):
        cls.logger.debug(msg, owner="Risk", **kwargs)

    @classmethod
    def mimo_thread(cls):
        for thread in cls.thread_pool:
            # 判断线程的数量是否超过超时数
            if not isinstance(cls.app.config['AFTER_TIMEOUT'], int):
                raise AttributeError("请检查你的配置中项 AFTER_TIMEOUT的值是否为整数")
            if thread.count >= cls.app.config['AFTER_TIMEOUT']:
                try:
                    end_thread(thread)
                except ValueError:
                    pass
                cls.thread_pool.remove(thread)
            thread.count += 1

    def run(self, func, args):
        # 你需要在此处实现超时设置, 避免最后的线程最后无限积累
        p = ThreadMe(target=func, args=(args,))
        p.start()
        self.thread_pool.append(p)

    def __call__(self, *args, **kwargs):

        result = None
        fr_func = getattr(self, f"before_{self.__wrapped__.__name__}", None)
        if fr_func:
            result, new_args, new_kwargs = fr_func(*args, **kwargs)
        if not result:
            self.error("事前检查失败, 放弃此次操作")
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

    def realtime_check(self):
        """ 一直检查 """
