# coding:utf-8
from __future__ import absolute_import
from datetime import datetime
from functools import wraps
from uuid import uuid1
import handle.bar_generator
from blinker import signal
from vnpy.trader.vtEvent import EVENT_TICK
from database import client
from event_engine import event_engine
from sys_constant import LOG_FORMAT, ERROR_FORMAT, \
    ERROR_LEVEL
from sys_constant import LOG_LEVEL
from setting import XMIN, TICK_DB, XMIN_MAP
from sys_constant import EVENT_BAR

bar = {}
stop_signal = signal("stop")
log_signal = signal(name="logger")


def get_local_time():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def err_collector(func):
    @wraps(func)
    def wrapper(data):
        try:
            func(data)
        except Exception as e:
            log_signal.send(log_message=e, log_level=ERROR_LEVEL)
        return func

    return wrapper


@err_collector
def on_bar(event):
    data = event.dict_
    db = data['db']
    doc_name = XMIN_MAP.get(db)
    if data["db"] == "1":
        doc_name = "min_1"
    bar = data['bar'].__dict__
    bar['_id'] = uuid1()
    client[doc_name][bar['symbol']].insert(bar)


def log(sender, **kwargs):
    if kwargs.get("log_level") is None:
        level = LOG_LEVEL
    if kwargs.get("log_level") is not None:
        level = ERROR_LEVEL
    log = (LOG_FORMAT if level == LOG_LEVEL else ERROR_FORMAT).format(get_local_time(), level, "SYSTEM",
                                                                      kwargs['log_message'], chr(254))
    print(log)


# @err_collector
def on_tick(data):
    """solve tick data function in here"""
    tick = data.dict_
    symbol = tick.symbol
    # 生成datetime对象
    if not tick.datetime:
        if '.' in tick.time:
            tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S.%f')
        else:
            tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S')

    bm = bar.get(symbol, None)
    if bm:
        bm.updateTick(tick)
    if not bm:
        bar[symbol] = handle.bar_generator.BarGenerator()
    client[TICK_DB][tick.symbol].insert(tick.__dict__)


# tick register function
event_engine.register(EVENT_TICK, on_tick)
event_engine.register(EVENT_BAR, on_bar)
log_signal.connect(log)
stop_signal.connect(handle.bar_generator.BarGenerator.generate)
