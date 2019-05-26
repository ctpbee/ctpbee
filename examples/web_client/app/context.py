from functools import partial
from werkzeug.local import LocalStack, LocalProxy


def get_app(name):
    top = app_context.top
    if top is None: raise RuntimeError("当前无app")
    return getattr(top, name)


app_context = LocalStack()

current_app = LocalProxy(partial(get_app, 'current_app'))
