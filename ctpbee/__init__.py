"""
    for the future of  life
"""
__version__ = '1.5.5'
__status__ = 'dev level'

# Here are pre import
from ctpbee.app import CtpBee
from ctpbee.array import Array, LArray
from ctpbee.context import current_app, switch_app, get_app, del_app
from ctpbee.data_handle.generator import HighKlineSupporter
from ctpbee.date import get_day_from
from ctpbee.func import cancel_order, send_order, subscribe, query_func, auth_time, helper
from ctpbee.func import hickey, get_ctpbee_path, get_current_trade_day
from ctpbee.helpers import dynamic_loading_api
from ctpbee.jsond import dumps, loads
from ctpbee.level import CtpbeeApi, Action
from ctpbee.log import VLogger
from ctpbee.message import Mail
from ctpbee.signals import common_signals
from ctpbee.signals import send_monitor, cancel_monitor
