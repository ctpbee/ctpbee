from ctpbee.exceptions import ContextError
from ctpbee.context.proxy import proxy

def current_app():
    """
    :return:当前环境中运行的app对象
    :return: CtpBee
    """
    if len(proxy) == 0:
        raise ContextError
    return proxy.get_app()
