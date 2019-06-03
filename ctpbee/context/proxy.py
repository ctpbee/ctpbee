from threading import get_ident, Lock
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

    def push(self, name, obj):
        """Pushes a new item to the stack"""
        self._local.append(obj)
        self._simple[name] = obj
        return self._local

    def switch(self, name: Text):
        if name in self._simple.keys():
            rv = getattr(self._local, "stack", None)
            index = rv.index(self._simple.get(name))
            rv[index], rv[-1] = rv[-1], rv[index]
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


def _switch_app():
    """将指定app的变量切换到栈顶 方便current_app进行访问"""
    return _app_context_ctx.switch


def _find_app():
    # 返回栈顶的app变量.
    top = _app_context_ctx.top
    if top is None:
        raise ContextError("无app变量")
    return top


current_app = LocalProxy(_find_app)
switch_app = LocalProxy(_switch_app)
