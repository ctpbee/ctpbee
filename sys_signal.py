# coding:utf-8
from __future__ import absolute_import
from datetime import datetime
from uuid import uuid1
import handle
from blinker import signal
from vnpy.trader.vtEvent import EVENT_TICK
from database import client
from event_engine import event_engine
from sys_constant import LOG_FORMAT, ERROR_FORMAT, \
    ERROR_LEVEL
from sys_constant import LOG_LEVEL
from setting import XMIN, TICK_DB, XMIN_MAP
from sys_constant import EVENT_BAR
from decorator import err_collector

bar = {}
stop_signal = signal("stop")
log_signal = signal(name="logger")


def get_local_time():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@err_collector
def on_bar(event):
    """
    bar handle function
    event.dict_['db'] : bar type , 1 ,3,5,7... etc
    event.dict_['bar'] : vtBar
    :param event: bar event
    :return: None
    """
    data = event.dict_
    db = data['db']
    doc_name = XMIN_MAP.get(db)
    if data["db"] == "1":
        doc_name = "min_1"
    bar = data['bar'].__dict__
    bar['_id'] = uuid1()
    client[doc_name][bar['symbol']].insert(bar)


@err_collector
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
        bar[symbol] = handle.BarGenerator()
    client[TICK_DB][tick.symbol].insert(tick.__dict__)


def log(sender, **kwargs):
    """
    log handle function
    :param sender: ...
    :param kwargs:  send parameter
    :return: None
    """
    if kwargs.get("log_level") is None:
        level = LOG_LEVEL
    if kwargs.get("log_level") is not None:
        level = ERROR_LEVEL
    log = (LOG_FORMAT if level == LOG_LEVEL else ERROR_FORMAT).format(get_local_time(), level, "SYSTEM",
                                                                      kwargs['log_message'], chr(254))
    with open("debug.log", "a") as f:
        f.write(log + "\n")
    print(log)


# register function
event_engine.register(EVENT_TICK, on_tick)
event_engine.register(EVENT_BAR, on_bar)
log_signal.connect(log)
# stop_signal.connect(handle.BarGenerator.generate)
