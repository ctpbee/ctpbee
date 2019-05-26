from ctpbee.exceptions import ContextError

from werkzeug.local import LocalProxy, LocalStack
from functools import partial

_app_context_ctx = LocalStack()


# 根据 app名字获取到 app实例.
def get_app(name):
    top = _app_context_ctx.top
    if top is None: raise ContextError("无app变量")
    return getattr(top, name)

# 当前栈顶的app变量.
def _find_app():
    top = _app_context_ctx.top
    if top is None:
        raise ContextError("无app变量")
    return top


current_app = LocalProxy(_find_app)
