# coding:utf-8
from vnpy.trader.vtGateway import *
from .mdApi import CtpMdApi
from vnpy.trader.vtEvent import *
from .engine import EventEngine


class MarketEngine():
    # self.tdPenaltyList = globalSetting['tdPenalty']  # 平今手续费惩罚的产品代码列表
    def __init__(self):
        # self.FINISHED_STATUS = [STATUS_ALLTRADED, STATUS_REJECTED, STATUS_CANCELLED]
        self.tickDict = {}
        self.contractDict = {}
        self.orderDict = {}
        self.workingOrderDict = {}  # 可撤销委托
        self.tradeDict = {}
        self.accountDict = {}
        self.positionDict = {}
        self.logList = []
        self.errorList = []
        self.detailDict = {}  # vtSymbol:PositionDetail
        self.event_engine = EventEngine()
        self.mdApi = CtpMdApi(self.event_engine)

        self.event_engine.register(EVENT_TICK, self.processTickEvent)
        self.event_engine.register(EVENT_CONTRACT, self.processContractEvent)
        self.event_engine.register(EVENT_ORDER, self.processOrderEvent)
        self.event_engine.register(EVENT_TRADE, self.processTradeEvent)
        self.event_engine.register(EVENT_POSITION, self.processPositionEvent)
        self.event_engine.register(EVENT_ACCOUNT, self.processAccountEvent)
        self.event_engine.register(EVENT_LOG, self.processLogEvent)
        self.event_engine.register(EVENT_ERROR, self.processErrorEvent)

    def processTickEvent(self, event):
        """处理成交事件"""
        tick = event.dict_
        self.tickDict[tick.vtSymbol] = tick

        # ----------------------------------------------------------------------

    def processContractEvent(self, event):
        """处理合约事件"""
        contract = event.dict_
        self.contractDict[contract.vtSymbol] = contract
        self.contractDict[contract.symbol] = contract  # 使用常规代码（不包括交易所）可能导致重复

        # ----------------------------------------------------------------------

    def processOrderEvent(self, event):
        """处理委托事件"""
        order = event.dict_
        self.orderDict[order.vtOrderID] = order

        # 如果订单的状态是全部成交或者撤销，则需要从workingOrderDict中移除
        if order.status in self.FINISHED_STATUS:
            if order.vtOrderID in self.workingOrderDict:
                del self.workingOrderDict[order.vtOrderID]
        # 否则则更新字典中的数据
        else:
            self.workingOrderDict[order.vtOrderID] = order

        # 更新到持仓细节中
        detail = self.getPositionDetail(order.vtSymbol)
        detail.updateOrder(order)

        # ----------------------------------------------------------------------

    def processTradeEvent(self, event):
        """处理成交事件"""
        trade = event.dict_
        self.tradeDict[trade.vtTradeID] = trade
        # 更新到持仓细节中
        detail = self.getPositionDetail(trade.vtSymbol)
        detail.updateTrade(trade)

        # ----------------------------------------------------------------------

    def processPositionEvent(self, event):
        """处理持仓事件"""
        pos = event.dict_

        self.positionDict[pos.vtPositionName] = pos

        # 更新到持仓细节中
        detail = self.getPositionDetail(pos.vtSymbol)
        detail.updatePosition(pos)

        # ----------------------------------------------------------------------

    def processAccountEvent(self, event):
        """处理账户事件"""
        account = event.dict_
        self.accountDict[account.vtAccountID] = account

        # ----------------------------------------------------------------------

    def processLogEvent(self, event):
        """处理日志事件"""
        log = event.dict_
        self.logList.append(log)

        # ----------------------------------------------------------------------

    def processErrorEvent(self, event):
        """处理错误事件"""
        error = event.dict_
        self.errorList.append(error)

        # ----------------------------------------------------------------------

    def getTick(self, vtSymbol):
        """查询行情对象"""
        try:
            return self.tickDict[vtSymbol]
        except KeyError:
            return None
            # ----------------------------------------------------------------------

    def getAllTick(self):
        try:
            return self.tickDict.values()
        except KeyError:
            return None

    def getContract(self, vtSymbol):
        """查询合约对象"""
        try:
            return self.contractDict[vtSymbol]
        except KeyError:
            return None

        # ----------------------------------------------------------------------

    def getAllContracts(self):
        """查询所有合约对象（返回列表）"""
        return self.contractDict.values()

        # ----------------------------------------------------------------------

    def getOrder(self, vtOrderID):
        """查询委托"""
        try:
            return self.orderDict[vtOrderID]
        except KeyError:
            return None

        # ----------------------------------------------------------------------

    def getAllWorkingOrders(self):
        """查询所有活动委托（返回列表）"""
        return self.workingOrderDict.values()

        # ----------------------------------------------------------------------

    def getAllOrders(self):
        """获取所有委托"""
        return self.orderDict.values()

        # ----------------------------------------------------------------------

    def getAllTrades(self):
        """获取所有成交"""
        return self.tradeDict.values()

        # ----------------------------------------------------------------------

    def getAllPositions(self):
        """获取所有持仓"""
        return self.positionDict.values()

        # ----------------------------------------------------------------------

    def getAllAccounts(self):
        """获取所有资金"""
        return self.accountDict.values()

        # ---------------------------------------------------------------------

    def getAllPositionDetails(self):
        """查询所有本地持仓缓存细节"""
        return self.detailDict.values()

        # ----------------------------------------------------------------------

    def subscribe(self, req):
        self.mdApi.subscribe(req)

    def connect(self, userID="089131", password="350888", BrokeID="9999", mdAddress="tcp://180.168.146.187:10011"):
        self.mdApi.connect(userID, password, BrokeID, mdAddress)

    def get_login_status(self):
        return self.mdApi.loginStatus
