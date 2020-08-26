"""
ctpbee里面内置模拟成交网关 ---> 主要调用回测接口进行处理
"""
from ctpbee.constant import Event, EVENT_POSITION, AccountData, EVENT_ACCOUNT
from ctpbee.looper.interface import LocalLooper


class LooperYou(LocalLooper):
    """
    模拟成交接口网关， 负责向上提供API
    三点之后发起结算
    """

    def __init__(self, app_signal, app):
        super().__init__(app_signal, app)
        self.gateway_name = "ctp"

    def query_account(self):
        """ 查询账户信息API"""
        self.on_event(EVENT_ACCOUNT, self.account.to_object())
        return 1

    @property
    def td_status(self):
        return True

    def query_positions(self):
        """
        当查询持仓的时候立即向队列报送持仓单子
        """
        [self.on_event(EVENT_POSITION, x) for x in self.account.position_manager.get_all_positions()]
        return 1

    def connect(self, info: dict):
        print("模拟器已经载入， 正在初始化历史资金数据")
        if info.get("SIM_PRIMARY_CASH"):
            self.account.initial_capital(info.get("SIM_PRIMARY_CASH"))
