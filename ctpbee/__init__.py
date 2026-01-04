"""
for the future of  life
"""

__version__ = "1.7.2"

# Here are pre import
from ctpbee.app import CtpBee
from ctpbee.constant import Mode
from ctpbee.context import current_app, del_app, get_app, switch_app
from ctpbee.data_handle import LocalPositionManager
from ctpbee.date import get_day_from
from ctpbee.func import (
    cancel_order,
    get_ctpbee_path,
    get_current_trade_day,
    helper,
    hickey,
    query_func,
    send_order,
    subscribe,
    tool_register,
)
from ctpbee.helpers import auth_time, dynamic_loading_api
from ctpbee.jsond import dumps, loads
from ctpbee.level import Action, CtpbeeApi, Tool
from ctpbee.log import VLogger
