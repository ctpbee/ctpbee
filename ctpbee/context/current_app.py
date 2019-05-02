from ctpbee.exceptions import ContextError
from ctpbee.context.proxy import proxy


def current_app():
    if len(proxy) == 0:
        raise ContextError
    return proxy.get_app()
