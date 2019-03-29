# coding:utf-8
from vnpy.trader.vtGateway import *
from functools import wraps
from constant import PositionDetail
from ctpApi import CtpTdApi
from time import sleep
from .vtEvent import *
from .engine import EventEngine


def wait_one_second(func):
    @wraps(func)
    def wrapper(*args, **kw):
        sleep(0.3)
        u = func(*args, **kw)
        sleep(0.3)
        return u

    return wrapper


def wait(func):
    @wraps(func)
    def wrapper(*args, **kw):
        u = func(*args, **kw)
        time.sleep(0.1)
        return u

    return wrapper


class MainEngine:

    # self.tdPenaltyList = globalSetting['tdPenalty']  # 平今手续费惩罚的产品代码列表

    def __init__(self):
        self.FINISHED_STATUS = [STATUS_ALLTRADED, STATUS_REJECTED, STATUS_CANCELLED]
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
        self.tdApi = CtpTdApi(self.event_engine)
        self.event_engine.register(EVENT_TICK, self.processTickEvent)
        self.event_engine.register(EVENT_CONTRACT, self.processContractEvent)
        self.event_engine.register(EVENT_ORDER, self.processOrderEvent)
        self.event_engine.register(EVENT_TRADE, self.processTradeEvent)
        self.event_engine.register(EVENT_POSITION, self.processPositionEvent)
        self.event_engine.register(EVENT_ACCOUNT, self.processAccountEvent)
        self.event_engine.register(EVENT_LOG, self.processLogEvent)
        self.event_engine.register(EVENT_ERROR, self.processErrorEvent)

    def qry_account(self):
        self.tdApi.qryAccount()

    @wait_one_second
    def qry_positions(self):
        self.tdApi.qryPosition()

    def qry_account_lonely(self):
        self._qryAccount()
        return self.getAllAccounts()

    def query_account_data(self):
        return self.getAllAccounts()

    def query_all_postion_data(self):
        return self.getAllPositions()

    def query_position_detial(self, vtsymbol):
        self.tdApi.qryPosition()
        return self.getPositionDetail(vtsymbol)

    @wait
    def login(self, userID, password, brokerID, tdAddress, authCode=None, userProductInfo=None):
        self.tdApi.connect(userID, password, brokerID, tdAddress, authCode, userProductInfo)

    def get_login_status(self):
        return self.tdApi.loginStatus

    @wait_one_second
    def __send_order(self, order_req):
        return self.tdApi.sendOrder(order_req)

    def qry_action(self):
        self._qryAccount()
        self._qryOrder()
        self._qryPosition()
        self._qryTrade()

    @wait_one_second
    def _qryOrder(self):
        self.tdApi.qryOrder()

    @wait_one_second
    def _qryTrade(self):
        self.tdApi.qryTrade()

    @wait_one_second
    def _qryPosition(self):
        self.tdApi.qryPosition()

    @wait_one_second
    def _qryAccount(self):
        self.qry_account()

    def send_order(self, order_req):
        """
        发单
        :param order_req:  object VtOrderReq
        :return:  list
            """
        # 发单 同时返回成交数据和错误  如果发单错误 那么list[1] ？？
        order_id = self.__send_order(order_req)
        return self.getOrder(vtOrderID=order_id), self.getError()

    @wait_one_second
    def __cancle_order(self, cancle_order_req):
        self.tdApi.cancelOrder(cancelOrderReq=cancle_order_req)

    def cancle_order(self, cancel_order_req):
        """
        撤单
        :param cancel_order_req: object VtCancelOrderReq
        :return: []
                """
        self.__cancle_order(cancel_order_req)
        return self.getOrder(vtOrderID=cancel_order_req.vtOrderID), self.getError()

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

    def processCase(self, event):
        case = event.dict_
        self.orderDict[case.vtOrderID] = case

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

        # ----------------------------------------------------------------------

    def qry_instrument(self):
        self.tdApi.reqInstrument()

    def getPositionDetail(self, vtSymbol):
        """查询持仓细节, 在本地不维护持仓细节"""

        if vtSymbol in self.detailDict:
            detail = self.detailDict[vtSymbol]
        else:
            contract = self.getContract(vtSymbol)
            detail = PositionDetail(vtSymbol, contract)
            self.detailDict[vtSymbol] = detail

            # 设置持仓细节的委托转换模式
            contract = self.getContract(vtSymbol)

            if contract:
                detail.exchange = contract.exchange

                # 上期所合约
                if contract.exchange == EXCHANGE_SHFE:
                    detail.mode = detail.MODE_SHFE

                # # 检查是否有平今惩罚
                # for productID in self.tdPenaltyList:
                #     if str(productID) in contract.symbol:
                #         detail.mode = detail.MODE_TDPENALTY

        return detail

        # ----------------------------------------------------------------------

    def getAllPositionDetails(self):
        """查询所有本地持仓缓存细节"""
        return self.detailDict.values()

        # ----------------------------------------------------------------------

    def updateOrderReq(self, req, vtOrderID):
        """委托请求更新"""
        vtSymbol = req.vtSymbol

        detail = self.getPositionDetail(vtSymbol)
        detail.updateOrderReq(req, vtOrderID)

        # ----------------------------------------------------------------------

    def convertOrderReq(self, req):
        """根据规则转换委托请求"""
        detail = self.detailDict.get(req.vtSymbol, None)
        if not detail:
            return [req]
        else:
            return detail.convertOrderReq(req)

        # ----------------------------------------------------------------------

    def getLog(self):
        """获取日志"""
        return self.logList

        # ----------------------------------------------------------------------

    def getError(self):
        """获取错误"""
        return self.errorList

    def close_connection(self):
        self.tdApi.close()
