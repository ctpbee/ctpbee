# coding:utf-8
from __future__ import division

from copy import copy
from vnpy.trader.vtGateway import *

# encoding: UTF-8

# 默认空值
EMPTY_STRING = ''
EMPTY_UNICODE = u''
EMPTY_INT = 0
EMPTY_FLOAT = 0.0

# 方向常量
DIRECTION_NONE = u'none'
DIRECTION_LONG = u'long'
DIRECTION_SHORT = u'short'
DIRECTION_UNKNOWN = u'unknown'
DIRECTION_NET = u'net'
DIRECTION_SELL = u'sell'      # IB接口
DIRECTION_COVEREDSHORT = u'covered short'    # 证券期权

# 开平常量
OFFSET_NONE = u'none'
OFFSET_OPEN = u'open'
OFFSET_CLOSE = u'close'
OFFSET_CLOSETODAY = u'close today'
OFFSET_CLOSEYESTERDAY = u'close yesterday'
OFFSET_UNKNOWN = u'unknown'

# 状态常量
STATUS_NOTTRADED = u'pending'
STATUS_PARTTRADED = u'partial filled'
STATUS_ALLTRADED = u'filled'
STATUS_CANCELLED = u'cancelled'
STATUS_REJECTED = u'rejected'
STATUS_UNKNOWN = u'unknown'

# 合约类型常量
PRODUCT_EQUITY = u'equity'
PRODUCT_FUTURES = u'futures'
PRODUCT_OPTION = u'option'
PRODUCT_INDEX = u'index'
PRODUCT_COMBINATION = u'combination'
PRODUCT_FOREX = u'forex'
PRODUCT_UNKNOWN = u'unknown'
PRODUCT_SPOT = u'spot'
PRODUCT_DEFER = u'defer'
PRODUCT_NONE = 'none'

# 价格类型常量
PRICETYPE_LIMITPRICE = u'limit order'
PRICETYPE_MARKETPRICE = u'market order'
PRICETYPE_FAK = u'FAK'
PRICETYPE_FOK = u'FOK'

# 期权类型
OPTION_CALL = u'call'
OPTION_PUT = u'put'

# 交易所类型
EXCHANGE_SSE = 'SSE'       # 上交所
EXCHANGE_SZSE = 'SZSE'     # 深交所
EXCHANGE_CFFEX = 'CFFEX'   # 中金所
EXCHANGE_SHFE = 'SHFE'     # 上期所
EXCHANGE_CZCE = 'CZCE'     # 郑商所
EXCHANGE_DCE = 'DCE'       # 大商所
EXCHANGE_SGE = 'SGE'       # 上金所
EXCHANGE_INE = 'INE'       # 国际能源交易中心
EXCHANGE_UNKNOWN = 'UNKNOWN'# 未知交易所
EXCHANGE_NONE = ''          # 空交易所
EXCHANGE_HKEX = 'HKEX'      # 港交所
EXCHANGE_HKFE = 'HKFE'      # 香港期货交易所

EXCHANGE_SMART = 'SMART'       # IB智能路由（股票、期权）
EXCHANGE_NYMEX = 'NYMEX'       # IB 期货
EXCHANGE_GLOBEX = 'GLOBEX'     # CME电子交易平台
EXCHANGE_IDEALPRO = 'IDEALPRO' # IB外汇ECN

EXCHANGE_CME = 'CME'           # CME交易所
EXCHANGE_ICE = 'ICE'           # ICE交易所
EXCHANGE_LME = 'LME'           # LME交易所

EXCHANGE_FXCM = 'FXCM'         # FXCM外汇做市商

EXCHANGE_OKCOIN = 'OKCOIN'       # OKCOIN比特币交易所
EXCHANGE_HUOBI = 'HUOBI'         # 火币比特币交易所
EXCHANGE_LBANK = 'LBANK'         # LBANK比特币交易所
EXCHANGE_ZB = 'ZB'		 # 比特币中国比特币交易所
EXCHANGE_OKEX = 'OKEX'		 # OKEX比特币交易所
EXCHANGE_OKEXFUTURE = 'OKEXFUTURE'		 # OKEX比特币交易所-期货
EXCHANGE_BINANCE = "BINANCE"     # 币安比特币交易所
EXCHANGE_BITFINEX = "BITFINEX"   # Bitfinex比特币交易所
EXCHANGE_BITMEX = 'BITMEX'       # BitMEX比特币交易所
EXCHANGE_FCOIN = 'FCOIN'         # FCoin比特币交易所
EXCHANGE_BIGONE = 'BIGONE'       # BigOne比特币交易所
EXCHANGE_COINBASE = 'COINBASE'   # Coinbase交易所
EXCHANGE_BITHUMB = 'BITHUMB'   # Bithumb比特币交易所

# 货币类型
CURRENCY_USD = 'USD'            # 美元
CURRENCY_CNY = 'CNY'            # 人民币
CURRENCY_HKD = 'HKD'            # 港币
CURRENCY_UNKNOWN = 'UNKNOWN'    # 未知货币
CURRENCY_NONE = ''              # 空货币




########################################################################
class PositionDetail(object):
    """本地维护的持仓信息"""
    WORKING_STATUS = [STATUS_UNKNOWN, STATUS_NOTTRADED, STATUS_PARTTRADED]

    MODE_NORMAL = 'normal'  # 普通模式
    MODE_SHFE = 'shfe'  # 上期所今昨分别平仓
    MODE_TDPENALTY = 'tdpenalty'  # 平今惩罚

    # ----------------------------------------------------------------------
    def __init__(self, vtSymbol, contract=None):
        """Constructor"""
        self.vtSymbol = vtSymbol
        self.symbol = EMPTY_STRING
        self.exchange = EMPTY_STRING
        self.name = EMPTY_UNICODE
        self.size = 1

        if contract:
            self.symbol = contract.symbol
            self.exchange = contract.exchange
            self.name = contract.name
            self.size = contract.size

        self.longPos = EMPTY_INT
        self.longYd = EMPTY_INT
        self.longTd = EMPTY_INT
        self.longPosFrozen = EMPTY_INT
        self.longYdFrozen = EMPTY_INT
        self.longTdFrozen = EMPTY_INT
        self.longPnl = EMPTY_FLOAT
        self.longPrice = EMPTY_FLOAT

        self.shortPos = EMPTY_INT
        self.shortYd = EMPTY_INT
        self.shortTd = EMPTY_INT
        self.shortPosFrozen = EMPTY_INT
        self.shortYdFrozen = EMPTY_INT
        self.shortTdFrozen = EMPTY_INT
        self.shortPnl = EMPTY_FLOAT
        self.shortPrice = EMPTY_FLOAT

        self.lastPrice = EMPTY_FLOAT

        self.mode = self.MODE_NORMAL
        self.exchange = EMPTY_STRING

        self.workingOrderDict = {}

    # ----------------------------------------------------------------------
    def updateTrade(self, trade):
        """成交更新"""
        # 多头
        if trade.direction is DIRECTION_LONG:
            # 开仓
            if trade.offset is OFFSET_OPEN:
                self.longTd += trade.volume
            # 平今
            elif trade.offset is OFFSET_CLOSETODAY:
                self.shortTd -= trade.volume
            # 平昨
            elif trade.offset is OFFSET_CLOSEYESTERDAY:
                self.shortYd -= trade.volume
            # 平仓
            elif trade.offset is OFFSET_CLOSE:
                # 上期所等同于平昨
                if self.exchange is EXCHANGE_SHFE:
                    self.shortYd -= trade.volume
                # 非上期所，优先平今
                else:
                    self.shortTd -= trade.volume

                    if self.shortTd < 0:
                        self.shortYd += self.shortTd
                        self.shortTd = 0
                        # 空头
        elif trade.direction is DIRECTION_SHORT:
            # 开仓
            if trade.offset is OFFSET_OPEN:
                self.shortTd += trade.volume
            # 平今
            elif trade.offset is OFFSET_CLOSETODAY:
                self.longTd -= trade.volume
            # 平昨
            elif trade.offset is OFFSET_CLOSEYESTERDAY:
                self.longYd -= trade.volume
            # 平仓
            elif trade.offset is OFFSET_CLOSE:
                # 上期所等同于平昨
                if self.exchange is EXCHANGE_SHFE:
                    self.longYd -= trade.volume
                # 非上期所，优先平今
                else:
                    self.longTd -= trade.volume

                    if self.longTd < 0:
                        self.longYd += self.longTd
                        self.longTd = 0

        # 汇总
        self.calculatePrice(trade)
        self.calculatePosition()
        self.calculatePnl()

    # ----------------------------------------------------------------------
    def updateOrder(self, order):
        """委托更新"""
        # 将活动委托缓存下来
        if order.status in self.WORKING_STATUS:
            self.workingOrderDict[order.vtOrderID] = order

        # 移除缓存中已经完成的委托
        else:
            if order.vtOrderID in self.workingOrderDict:
                del self.workingOrderDict[order.vtOrderID]

        # 计算冻结
        self.calculateFrozen()

    # ----------------------------------------------------------------------
    def updatePosition(self, pos):
        """持仓更新"""
        if pos.direction is DIRECTION_LONG:
            self.longPos = pos.position
            self.longYd = pos.ydPosition
            self.longTd = self.longPos - self.longYd
            self.longPnl = pos.positionProfit
            self.longPrice = pos.price
        elif pos.direction is DIRECTION_SHORT:
            self.shortPos = pos.position
            self.shortYd = pos.ydPosition
            self.shortTd = self.shortPos - self.shortYd
            self.shortPnl = pos.positionProfit
            self.shortPrice = pos.price

    # ----------------------------------------------------------------------
    def updateOrderReq(self, req, vtOrderID):
        """发单更新"""
        vtSymbol = req.vtSymbol

        # 基于请求生成委托对象
        order = VtOrderData()
        order.vtSymbol = vtSymbol
        order.symbol = req.symbol
        order.exchange = req.exchange
        order.offset = req.offset
        order.direction = req.direction
        order.totalVolume = req.volume
        order.status = STATUS_UNKNOWN

        # 缓存到字典中
        self.workingOrderDict[vtOrderID] = order

        # 计算冻结量
        self.calculateFrozen()

    # ----------------------------------------------------------------------
    def updateTick(self, tick):
        """行情更新"""
        self.lastPrice = tick.lastPrice
        self.calculatePnl()

    # ----------------------------------------------------------------------
    def calculatePnl(self):
        """计算持仓盈亏"""
        self.longPnl = self.longPos * (self.lastPrice - self.longPrice) * self.size
        self.shortPnl = self.shortPos * (self.shortPrice - self.lastPrice) * self.size

    # ----------------------------------------------------------------------
    def calculatePrice(self, trade):
        """计算持仓均价（基于成交数据）"""
        # 只有开仓会影响持仓均价
        if trade.offset == OFFSET_OPEN:
            if trade.direction == DIRECTION_LONG:
                cost = self.longPrice * self.longPos
                cost += trade.volume * trade.price
                newPos = self.longPos + trade.volume
                if newPos:
                    self.longPrice = cost / newPos
                else:
                    self.longPrice = 0
            else:
                cost = self.shortPrice * self.shortPos
                cost += trade.volume * trade.price
                newPos = self.shortPos + trade.volume
                if newPos:
                    self.shortPrice = cost / newPos
                else:
                    self.shortPrice = 0

    # ----------------------------------------------------------------------
    def calculatePosition(self):
        """计算持仓情况"""
        self.longPos = self.longTd + self.longYd
        self.shortPos = self.shortTd + self.shortYd

        # ----------------------------------------------------------------------

    def calculateFrozen(self):
        """计算冻结情况"""
        # 清空冻结数据
        self.longPosFrozen = EMPTY_INT
        self.longYdFrozen = EMPTY_INT
        self.longTdFrozen = EMPTY_INT
        self.shortPosFrozen = EMPTY_INT
        self.shortYdFrozen = EMPTY_INT
        self.shortTdFrozen = EMPTY_INT

        # 遍历统计
        for order in self.workingOrderDict.values():
            # 计算剩余冻结量
            frozenVolume = order.totalVolume - order.tradedVolume

            # 多头委托
            if order.direction is DIRECTION_LONG:
                # 平今
                if order.offset is OFFSET_CLOSETODAY:
                    self.shortTdFrozen += frozenVolume
                # 平昨
                elif order.offset is OFFSET_CLOSEYESTERDAY:
                    self.shortYdFrozen += frozenVolume
                # 平仓
                elif order.offset is OFFSET_CLOSE:
                    self.shortTdFrozen += frozenVolume

                    if self.shortTdFrozen > self.shortTd:
                        self.shortYdFrozen += (self.shortTdFrozen - self.shortTd)
                        self.shortTdFrozen = self.shortTd
            # 空头委托
            elif order.direction is DIRECTION_SHORT:
                # 平今
                if order.offset is OFFSET_CLOSETODAY:
                    self.longTdFrozen += frozenVolume
                # 平昨
                elif order.offset is OFFSET_CLOSEYESTERDAY:
                    self.longYdFrozen += frozenVolume
                # 平仓
                elif order.offset is OFFSET_CLOSE:
                    self.longTdFrozen += frozenVolume

                    if self.longTdFrozen > self.longTd:
                        self.longYdFrozen += (self.longTdFrozen - self.longTd)
                        self.longTdFrozen = self.longTd

            # 汇总今昨冻结
            self.longPosFrozen = self.longYdFrozen + self.longTdFrozen
            self.shortPosFrozen = self.shortYdFrozen + self.shortTdFrozen

    # ----------------------------------------------------------------------
    def convertOrderReq(self, req):
        """转换委托请求"""
        # 普通模式无需转换
        if self.mode is self.MODE_NORMAL:
            return [req]

        # 上期所模式拆分今昨，优先平今
        elif self.mode is self.MODE_SHFE:
            # 开仓无需转换
            if req.offset is OFFSET_OPEN:
                return [req]

            # 多头
            if req.direction is DIRECTION_LONG:
                posAvailable = self.shortPos - self.shortPosFrozen
                tdAvailable = self.shortTd - self.shortTdFrozen
                ydAvailable = self.shortYd - self.shortYdFrozen
                # 空头
            else:
                posAvailable = self.longPos - self.longPosFrozen
                tdAvailable = self.longTd - self.longTdFrozen
                ydAvailable = self.longYd - self.longYdFrozen

            # 平仓量超过总可用，拒绝，返回空列表
            if req.volume > posAvailable:
                return []
            # 平仓量小于今可用，全部平今
            elif req.volume <= tdAvailable:
                req.offset = OFFSET_CLOSETODAY
                return [req]
            # 平仓量大于今可用，平今再平昨
            else:
                l = []

                if tdAvailable > 0:
                    reqTd = copy(req)
                    reqTd.offset = OFFSET_CLOSETODAY
                    reqTd.volume = tdAvailable
                    l.append(reqTd)

                reqYd = copy(req)
                reqYd.offset = OFFSET_CLOSEYESTERDAY
                reqYd.volume = req.volume - tdAvailable
                l.append(reqYd)

                return l

        # 平今惩罚模式，没有今仓则平昨，否则锁仓
        elif self.mode is self.MODE_TDPENALTY:
            # 多头
            if req.direction is DIRECTION_LONG:
                td = self.shortTd
                ydAvailable = self.shortYd - self.shortYdFrozen
            # 空头
            else:
                td = self.longTd
                ydAvailable = self.longYd - self.longYdFrozen

            # 这里针对开仓和平仓委托均使用一套逻辑

            # 如果有今仓，则只能开仓（或锁仓）
            if td:
                req.offset = OFFSET_OPEN
                return [req]
            # 如果平仓量小于昨可用，全部平昨
            elif req.volume <= ydAvailable:
                if self.exchange is EXCHANGE_SHFE:
                    req.offset = OFFSET_CLOSEYESTERDAY
                else:
                    req.offset = OFFSET_CLOSE
                return [req]
            # 平仓量大于昨可用，平仓再反向开仓
            else:
                l = []

                if ydAvailable > 0:
                    reqClose = copy(req)
                    if self.exchange is EXCHANGE_SHFE:
                        reqClose.offset = OFFSET_CLOSEYESTERDAY
                    else:
                        reqClose.offset = OFFSET_CLOSE
                    reqClose.volume = ydAvailable

                    l.append(reqClose)

                reqOpen = copy(req)
                reqOpen.offset = OFFSET_OPEN
                reqOpen.volume = req.volume - ydAvailable
                l.append(reqOpen)

                return l

        # 其他情况则直接返回空
        return []