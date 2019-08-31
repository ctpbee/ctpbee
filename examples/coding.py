"""
这个是我用来测试代码的文件， 你们直接忽略就好了
"""
from warnings import warn


class Action(object):
    """
    自定义的Action动作模板
    此动作应该被CtpBee, CtpbeeApi, AsyncApi, RiskLevel调用
    """

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        setattr(instance, "__name__", cls.__name__)
        return instance

    def __getattr__(self, item):
        message = f"尝试在{self.__name__}中调用一个不存在的属性{item}"
        warn(message)
        return None

    # 默认四个提供API的封装, 买多卖空等快速函数应该基于send_order进行封装
    def send_order(self, order, **kwargs):
        return self.app.trader.send_order(order, **kwargs)

    def cancel_order(self, cancel_req, **kwargs):
        return self.app.trader.cancel_order(cancel_req, **kwargs)

    def query_position(self):
        return self.app.trader.query_position()

    def query_account(self):
        return self.app.trader.query_accont()

    def __repr__(self):
        return f"{self.__name__} "
