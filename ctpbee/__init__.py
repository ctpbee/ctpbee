"""
for the future of  life
"""

__version__ = "1.7.2"

# Here are pre import
from ctpbee.app import CtpBee
from ctpbee.constant import Mode
from ctpbee.context import current_app, switch_app, get_app, del_app
from ctpbee.data_handle import LocalPositionManager
from ctpbee.date import get_day_from
from ctpbee.func import (
    cancel_order,
    send_order,
    subscribe,
    query_func,
    helper,
    hickey,
    get_ctpbee_path,
    get_current_trade_day,
    tool_register,
)
from ctpbee.helpers import dynamic_loading_api, auth_time
from ctpbee.jsond import dumps, loads
from ctpbee.level import CtpbeeApi, Action, Tool
from ctpbee.log import VLogger
