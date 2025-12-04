"""
Here code was used to check module can be imported normally
Hope have a good result  ^_^
"""

# 测试所有主要模块是否能正常导入
def test_imports():
    """测试所有主要模块是否能正常导入"""
    # 测试核心模块
    import ctpbee
    from ctpbee import (
        CtpBee, Mode, current_app, switch_app, get_app, del_app,
        LocalPositionManager, get_day_from, send_order, cancel_order,
        subscribe, query_func, helper, hickey, get_ctpbee_path,
        get_current_trade_day, tool_register, dynamic_loading_api,
        auth_time, dumps, loads, CtpbeeApi, Action, Tool, VLogger
    )
    
    # 测试子模块
    from ctpbee.constant import (
        Direction, Exchange, Offset, OrderType, Product, Status, Interval,
        OrderRequest, CancelRequest, TradeData, OrderData, PositionData,
        AccountData, TickData, BarData, ContractData, LogData, LastData,
        SubscribeRequest, QueryContract, AccountRegisterRequest, AccountBanlanceRequest,
        TransferRequest, TransferSerialRequest, MarketDataRequest, SharedData, Event, Msg
    )
    
    from ctpbee.data_handle import LocalPositionManager
    from ctpbee.date import trade_dates
    from ctpbee.exceptions import DatabaseError, ConfigError, ContextError, TraderError, MarketError, DataError
    from ctpbee.indicator import Indicator
    from ctpbee.jsond import dumps, loads
    from ctpbee.level import CtpbeeApi, Action, Tool
    from ctpbee.log import VLogger
    from ctpbee.stream import UDDR, DDDR, Dispatcher
    
    # 测试接口模块
    from ctpbee.interface import Interface
    from ctpbee.interface.ctp import BeeMdApi, BeeTdApi
    from ctpbee.interface.ctp_mini import MMdApi, MTdApi
    
    # 测试回测模块
    from ctpbee.looper.account import Account
    from ctpbee.looper.interface import LocalLooper
    
    print("✓ 所有模块导入成功")
    return True

if __name__ == "__main__":
    try:
        test_imports()
        print("\n🎉 所有模块测试通过！")
    except Exception as e:
        print(f"\n❌ 模块测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
