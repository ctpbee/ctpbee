#coding=utf8
import logging
import sys
from logging.handlers import RotatingFileHandler

import pandas as pd


def set_display():

    # 显示所有列(参数设置为None代表显示所有行，也可以自行设置数字)
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置数据的显示长度，默认为50
    pd.set_option('max_colwidth', 200)
    # 禁止自动换行(设置为Flase不自动换行，True反之)
    pd.set_option('expand_frame_repr', False)


__all__ = ["mylogger", "cleanlogs", "myalert", "logging", "formatter"]
"""
增加日志文件只需在这里添加"""
"""--------------------------------------------"""
log_debug = r"logs/debug.log"
log_info = r"./logs/info.log"
log_warning = r"./logs/warning.log"
log_error = r"./logs/error.log"
# logging.basicConfig(stream=sys.stdout)

logfiles = [log_debug, log_info, log_error, log_warning]
"""-------------------------------------------"""

mylogger = logging.getLogger(__name__)
mylogger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s ||[%(threadName)s|%(filename)s:%(lineno)d]|| - %(levelname)s -\n %(message)s'
)

for lf in logfiles:
    fh = RotatingFileHandler(lf,
                             mode='a',
                             maxBytes=10 * 1024 * 1024,
                             backupCount=2,
                             encoding='utf-8')
    lv = lf.rsplit("/")[-1][:-4].upper()
    fh.setLevel(getattr(logging, lv))
    fh.setFormatter(formatter)
    mylogger.addHandler(fh)


def cleanlogs():
    global logfiles
    for f in logfiles:
        with open(f, "w") as f1:
            f1.close()
    mylogger.debug("日志清除成功\r\n")
