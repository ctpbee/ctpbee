# coding:utf-8
import json
from vnpy.api.ctp import MdApi, defineDict

from vnpy.trader.language.english.constant import *
from vnpy.trader.vtFunction import getTempPath
from .engine import Event
from vnpy.trader.vtObject import *
from vnpy.trader.gateway.ctpGateway.language.english import text
from vnpy.trader.vtEvent import *

from datetime import time

DAY_START = time(8, 57)  # 日盘启动和停止时间
DAY_END = time(15, 18)
NIGHT_START = time(20, 57)  # 夜盘启动和停止时间
NIGHT_END = time(2, 33)
# 以下为一些VT类型和CTP类型的映射字典
# 价格类型映射
priceTypeMap = {}
priceTypeMap[PRICETYPE_LIMITPRICE] = defineDict["THOST_FTDC_OPT_LimitPrice"]
priceTypeMap[PRICETYPE_MARKETPRICE] = defineDict["THOST_FTDC_OPT_AnyPrice"]
priceTypeMapReverse = {v: k for k, v in priceTypeMap.items()}

# 方向类型映射
directionMap = {}
directionMap[DIRECTION_LONG] = defineDict['THOST_FTDC_D_Buy']
directionMap[DIRECTION_SHORT] = defineDict['THOST_FTDC_D_Sell']
directionMapReverse = {v: k for k, v in directionMap.items()}

# 开平类型映射
offsetMap = {}
offsetMap[OFFSET_OPEN] = defineDict['THOST_FTDC_OF_Open']
offsetMap[OFFSET_CLOSE] = defineDict['THOST_FTDC_OF_Close']
offsetMap[OFFSET_CLOSETODAY] = defineDict['THOST_FTDC_OF_CloseToday']
offsetMap[OFFSET_CLOSEYESTERDAY] = defineDict['THOST_FTDC_OF_CloseYesterday']
offsetMapReverse = {v: k for k, v in offsetMap.items()}

# 交易所类型映射
exchangeMap = {}
exchangeMap[EXCHANGE_CFFEX] = 'CFFEX'
exchangeMap[EXCHANGE_SHFE] = 'SHFE'
exchangeMap[EXCHANGE_CZCE] = 'CZCE'
exchangeMap[EXCHANGE_DCE] = 'DCE'
exchangeMap[EXCHANGE_SSE] = 'SSE'
exchangeMap[EXCHANGE_SZSE] = 'SZSE'
exchangeMap[EXCHANGE_INE] = 'INE'
exchangeMap[EXCHANGE_UNKNOWN] = ''
exchangeMapReverse = {v: k for k, v in exchangeMap.items()}

# 持仓类型映射
posiDirectionMap = {}
posiDirectionMap[DIRECTION_NET] = defineDict["THOST_FTDC_PD_Net"]
posiDirectionMap[DIRECTION_LONG] = defineDict["THOST_FTDC_PD_Long"]
posiDirectionMap[DIRECTION_SHORT] = defineDict["THOST_FTDC_PD_Short"]
posiDirectionMapReverse = {v: k for k, v in posiDirectionMap.items()}

# 产品类型映射
productClassMap = {}
productClassMap[PRODUCT_FUTURES] = defineDict["THOST_FTDC_PC_Futures"]
productClassMap[PRODUCT_OPTION] = defineDict["THOST_FTDC_PC_Options"]
productClassMap[PRODUCT_COMBINATION] = defineDict["THOST_FTDC_PC_Combination"]
productClassMapReverse = {v: k for k, v in productClassMap.items()}
productClassMapReverse[defineDict["THOST_FTDC_PC_ETFOption"]] = PRODUCT_OPTION
productClassMapReverse[defineDict["THOST_FTDC_PC_Stock"]] = PRODUCT_EQUITY

# 委托状态映射
statusMap = {}
statusMap[STATUS_ALLTRADED] = defineDict["THOST_FTDC_OST_AllTraded"]
statusMap[STATUS_PARTTRADED] = defineDict["THOST_FTDC_OST_PartTradedQueueing"]
statusMap[STATUS_NOTTRADED] = defineDict["THOST_FTDC_OST_NoTradeQueueing"]
statusMap[STATUS_CANCELLED] = defineDict["THOST_FTDC_OST_Canceled"]
statusMapReverse = {v: k for k, v in statusMap.items()}

# 全局字典, key:symbol, value:exchange
symbolExchangeDict = {"AP903": "SHFE", "rb1905": "SHFE"}

# 夜盘交易时间段分隔判断
NIGHT_TRADING = datetime(1900, 1, 1, 20).time()


class CtpMdApi(MdApi):
    """CTP行情API实现"""

    def __init__(self, event_engine):
        """Constructor"""
        super(CtpMdApi, self).__init__()

        self.event_engine = event_engine
        # self.gateway = gateway  # gateway对象
        self.gatewayName = "CTP"  # gateway对象名称

        self.reqID = EMPTY_INT  # 操作请求编号

        self.connectionStatus = False  # 连接状态
        self.loginStatus = False  # 登录状态
        self.mdConnected = False
        self.subscribedSymbols = set()  # 已订阅合约代码

        self.userID = EMPTY_STRING  # 账号
        self.password = EMPTY_STRING  # 密码
        self.brokerID = EMPTY_STRING  # 经纪商代码
        self.address = EMPTY_STRING  # 服务器地址

    def onFrontConnected(self):
        """服务器连接"""
        self.connectionStatus = True
        self.login()

    def onFrontDisconnected(self, n):
        """服务器断开"""
        self.connectionStatus = False
        self.loginStatus = False
        self.mdConnected = False
        self.writeLog(text.DATA_SERVER_DISCONNECTED)

    def onHeartBeatWarning(self, n):
        """心跳报警"""
        # 因为API的心跳报警比较常被触发，且与API工作关系不大，因此选择忽略
        pass

    def onRspError(self, error, n, last):
        """错误回报"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        event = Event(err, EVENT_ERROR)
        self.event_engine.put(event)

    def onRspUserLogin(self, data, error, n, last):
        """登陆回报"""
        # 如果登录成功，推送日志信息
        if error['ErrorID'] == 0:
            self.loginStatus = True
            self.mdConnected = True

            # 重新订阅之前订阅的合约
            for subscribeReq in self.subscribedSymbols:
                self.subscribe(subscribeReq)

        # 否则，推送错误信息
        else:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            event = Event(err, EVENT_ERROR)
            self.event_engine.put(event)

    def onRspUserLogout(self, data, error, n, last):
        """登出回报"""
        # 如果登出成功，推送日志信息
        if error['ErrorID'] == 0:
            self.loginStatus = False
            self.mdConnected = False
            self.writeLog(text.DATA_SERVER_LOGOUT)

        # 否则，推送错误信息
        else:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            event = Event(err, EVENT_ERROR)
            self.event_engine.put(event)

    def onRspSubMarketData(self, data, error, n, last):
        """订阅合约回报"""
        if 'ErrorID' in error and error['ErrorID']:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            event = Event(err, EVENT_ERROR)
            self.event_engine.put(event)

    def onRspUnSubMarketData(self, data, error, n, last):
        """退订合约回报"""
        # 同上
        pass

    def onRtnDepthMarketData(self, data):
        """行情推送"""
        # 过滤尚未获取合约交易所时的行情推送
        symbol = data['InstrumentID']
        # if symbol not in symbolExchangeDict:
        #     return
        # if int(data['ClosePrice']) > 100000000:
        #     """防止脏数据推送进来"""
        #     return
        # 判断当前处于的时间段
        # 创建对象
        tick = VtTickData()
        tick.gatewayName = self.gatewayName

        tick.symbol = symbol
        tick.exchange = symbolExchangeDict[tick.symbol]
        tick.vtSymbol = tick.symbol  # '.'.join([tick.symbol, tick.exchange])

        tick.lastPrice = data['LastPrice']
        tick.volume = data['Volume']
        tick.openInterest = data['OpenInterest']
        tick.avergePrice = data['AveragePrice']
        tick.time = '.'.join([data['UpdateTime'], str(data['UpdateMillisec'] / 100)])

        # 上期所和郑商所可以直接使用，大商所需要转换
        tick.date = data['ActionDay']

        tick.openPrice = data['OpenPrice']
        tick.highPrice = data['HighestPrice']
        tick.lowPrice = data['LowestPrice']
        tick.preClosePrice = data['PreClosePrice']

        tick.upperLimit = data['UpperLimitPrice']
        tick.lowerLimit = data['LowerLimitPrice']

        # CTP只有一档行情
        tick.bidPrice1 = data['BidPrice1']
        tick.bidVolume1 = data['BidVolume1']
        tick.askPrice1 = data['AskPrice1']
        tick.askVolume1 = data['AskVolume1']

        # 大商所日期转换
        if tick.exchange == EXCHANGE_DCE:
            tick.date = datetime.now().strftime('%Y%m%d')

        # 上交所，SEE，股票期权相关
        if tick.exchange == EXCHANGE_SSE:
            tick.bidPrice2 = data['BidPrice2']
            tick.bidVolume2 = data['BidVolume2']
            tick.askPrice2 = data['AskPrice2']
            tick.askVolume2 = data['AskVolume2']

            tick.bidPrice3 = data['BidPrice3']
            tick.bidVolume3 = data['BidVolume3']
            tick.askPrice3 = data['AskPrice3']
            tick.askVolume3 = data['AskVolume3']

            tick.bidPrice4 = data['BidPrice4']
            tick.bidVolume4 = data['BidVolume4']
            tick.askPrice4 = data['AskPrice4']
            tick.askVolume4 = data['AskVolume4']

            tick.bidPrice5 = data['BidPrice5']
            tick.bidVolume5 = data['BidVolume5']
            tick.askPrice5 = data['AskPrice5']
            tick.askVolume5 = data['AskVolume5']
            tick.date = data['TradingDay']
        event = Event(tick, EVENT_TICK)
        self.event_engine.put(event)

    def onRspSubForQuoteRsp(self, data, error, n, last):
        """订阅期权询价"""
        pass

    def onRspUnSubForQuoteRsp(self, data, error, n, last):
        """退订期权询价"""
        pass

    def onRtnForQuoteRsp(self, data):
        """期权询价推送"""
        pass

    def connect(self, userID, password, brokerID, address):
        """初始化连接"""
        self.userID = userID  # 账号
        self.password = password  # 密码
        self.brokerID = brokerID  # 经纪商代码
        self.address = address  # 服务器地址
        # 如果尚未建立服务器连接，则进行连接
        if not self.connectionStatus:
            # 创建C++环境中的API对象，这里传入的参数是需要用来保存.con文件的文件夹路径
            path = getTempPath(self.gatewayName + '_')
            self.createFtdcMdApi(path)
            # 注册服务器地址
            self.registerFront(self.address)

            # 初始化连接，成功会调用onFrontConnected
            resule = self.init()
        # 若已经连接但尚未登录，则进行登录
        else:
            if not self.loginStatus:
                self.login()


    def subscribe(self, symbol):
        return self.subscribeMarketData(str(symbol))

    def register(self, address):
        a = self.registerFront(address)

    def login(self):
        """登录"""
        # 如果填入了用户名密码等，则登录
        if self.userID and self.password and self.brokerID:
            req = {}
            req['UserID'] = self.userID
            req['Password'] = self.password
            req['BrokerID'] = self.brokerID
            self.reqID += 1
            self.reqUserLogin(req, self.reqID)

    def close(self):
        """关闭"""
        self.exit()

    def writeLog(self, content):
        """发出日志"""
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = content
        event = Event(log, EVENT_LOG)
        self.event_engine.put(event)
