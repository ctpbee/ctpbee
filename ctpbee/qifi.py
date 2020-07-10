"""
qifi Support

此镜像写入的qifi可以被QA

"""
from typing import List

from ctpbee.constant import AccountData, OrderData, TradeData


class QIFI:
    pass


class QIFIManager:
    def __init__(self, app):
        """
        """
        self.qifi = QIFI()
        from ctpbee.qa_support.qa_app import QADataSupport

        config = app.config.get("QA_SETUP", None)
        if config is None:
            raise TypeError("你已经使用了QIFI参数配置, 请通过设置QA_SETUP传入mongodb配置信息")
        self.client = QADataSupport(**config)
        self._reload(app.name)

    def _reload(self, app_name):
        self.qifi = self.client.get_qifi_value(app_name)

    def from_(self, account: AccountData, orders: List[OrderData], deals: List[TradeData]):
        """ 从数据中导入 """

    def update(self):
        """更新到mongodb数据库中"""
        pass
