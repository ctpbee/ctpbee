from ctpbee.exceptions import ContextError
from ctpbee.context.proxy import proxy

def current_app():
    """

    :return:当前app对象
    """
    if len(proxy) == 0:
        raise ContextError
    return proxy.get_app()
