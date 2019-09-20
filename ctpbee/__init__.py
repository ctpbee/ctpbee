"""
    for the future of  life
"""

__version__ = '0.31.1'
__status__ = '0.31修复版本1'

from ctpbee.app import CtpBee
from ctpbee.context import current_app, switch_app, get_app, del_app
from ctpbee.func import cancel_order, send_order, subscribe, query_func, auth_time, helper
from ctpbee.helpers import dynamic_loading_api
from ctpbee.jsond import dumps, loads
from ctpbee.level import CtpbeeApi, AsyncApi, Action
from ctpbee.log import VLogger
from ctpbee.signals import send_monitor, cancel_monitor
from ctpbee.trade_time import TradingDay
from ctpbee.util import RiskLevel
from ctpbee.func import hickey
