from typing import Text
from ctpbee.exceptions import ContextError
from werkzeug.local import LocalProxy


class LocalStack(object):
    def __init__(self):
        self._local = list()
        self._simple = dict()

    def __call__(self):
        def _lookup():
            rv = self.top
            if rv is None:
                raise RuntimeError("object unbound")
            return rv

        return LocalProxy(_lookup)

    def get_app(self, name):
        return self._simple.get(name, None)

    def push(self, name, obj):
        """Pushes a new item to the stack"""
        self._local.append(obj)
        self._simple[name] = obj
        return self._local

    def switch(self, name: Text):
        if name in self._simple.keys():
            index = self._local.index(self._simple.get(name))
            self._local[index], self._local[-1] = self._local[-1], self._local[index]
            return True
        return False

    def pop(self):
        """Removes the topmost item from the stack, will return the
        old value or `None` if the stack was already empty.
        """
        if self._local is None:
            return None
        elif len(self._local) == 1:
            return self._local[-1]
        else:
            return self._local.pop()

    @property
    def top(self):
        """The topmost item on the stack.  If the stack is empty,
        `None` is returned.
        """
        try:
            return self._local[-1]
        except (AttributeError, IndexError):
            return None


_app_context_ctx = LocalStack()



def _find_app():
    # 返回栈顶的app变量.
    top = _app_context_ctx.top
    if top is None:
        raise ContextError("无app变量")
    return top


def _get_app(name):
    """ 根据CtpBee的名字找到CtpBee 对象 """
    return _app_context_ctx.get_app(name)


current_app = LocalProxy(_find_app)
switch_app = _app_context_ctx.switch

get_app = _app_context_ctx.get_app
