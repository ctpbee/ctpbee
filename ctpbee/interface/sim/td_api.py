"""
ctpbee里面内置模拟成交网关 ---> 主要调用回测接口进行处理
"""
from ctpbee.constant import Event, EVENT_POSITION
from ctpbee.looper.interface import LocalLooper


class SimInterface(LocalLooper):
    """
    模拟成交接口网关， 负责向上提供API
    """

    def __init__(self, app_signal):
        self.app_signal = app_signal
        self.gateway_name = "ctp"
        # 此处的logger需要设置为空，在外部必须被强写掉
        super().__init__(logger=None, risk=None)

    def query_account(self):
        pass

    @property
    def td_status(self):
        return True

    def on_event(self, type, data):
        event = Event(type=type, data=data)
        signal = getattr(self.app_signal, f"{type}_signal")
        signal.send(event)

    def query_positions(self):
        """
        当查询持仓的时候立即向队列报送持仓单子
        """
        [self.on_event(EVENT_POSITION, x) for x in self.account.position_manager.get_all_positions()]
        return 1

