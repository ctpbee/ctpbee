from datetime import date, datetime

from ctpbee.constant import *
from ctpbee.event_engine import Event
from ctpbee.signals import common_signals
from .lib import *


class BeeMdApi(MdApi):
    """"""

    def __init__(self, app_signal):
        """Constructor"""
        super(BeeMdApi, self).__init__()

        self.gateway_name = "ctp"

        self.reqid = 0
        self.app_signal = app_signal
        self.connect_status = False
        self.login_status = False
        self.subscribed = set()

        self.userid = ""
        self.password = ""
        self.brokerid = 0

    @property
    def md_status(self):
        return self.login_status

    def on_event(self, type, data):
        if type == EVENT_TICK or type == EVENT_ERROR:
            event = Event(type=type, data=data)
            signal = getattr(common_signals, f"{type}_signal")
            signal.send(event)
        else:
            event = Event(type=type, data=data)
            signal = getattr(self.app_signal, f"{type}_signal")
            signal.send(event)

    def onFrontConnected(self):
        """
        Callback when front server is connected.
        """
        self.connect_status = True
        self.on_event(type=EVENT_LOG, data="行情服务器连接成功")
        self.login()

    def onFrontDisconnected(self, reason: int):
        """
        Callback when front server is disconnected.
        """
        self.connect_status = False
        self.login_status = False
        self.on_event(type=EVENT_LOG, data=f"行情连接断开，原因{reason}")

    def onRspUserLogin(self, data: dict, error: dict, reqid: int, last: bool):
        """
        Callback when user is logged in.
        """
        if not error["ErrorID"]:
            self.login_status = True
            self.on_event(type=EVENT_LOG, data="行情服务器登录成功")

            for symbol in self.subscribed:
                self.subscribeMarketData(symbol)
        else:
            error["detail"] = "行情登录失败"
            self.on_event(type=EVENT_ERROR, data=error)

    def onRspError(self, error: dict, reqid: int, last: bool):
        """
        Callback when error occured.
        """
        error['detail'] = "行情接口报错"
        self.on_event(type=EVENT_ERROR, data=error)

    def onRspSubMarketData(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        if not error or not error["ErrorID"]:
            return
        error['detail'] = "行情订阅失败"
        self.on_event(type=EVENT_ERROR, data=error)

    def onRtnDepthMarketData(self, data: dict):
        """
        Callback of tick data update.
        """
        symbol = data["InstrumentID"]
        exchange = symbol_exchange_map.get(symbol, "")
        if not exchange:
            return

        timestamp = f"{data['ActionDay']} {data['UpdateTime']}.{int(data['UpdateMillisec'] / 100)}"
        try:
            datetimed = datetime.strptime(timestamp, "%Y%m%d %H:%M:%S.%f")
        except ValueError as e:
            datetimed = datetime.strptime(str(date.today()) + " " + timestamp, "%Y-%m-%d %H:%M:%S.%f")

        tick = TickData(
            symbol=symbol,
            exchange=exchange,
            datetime=datetimed,
            name=symbol_name_map[symbol],
            volume=data["Volume"],
            last_price=data["LastPrice"],
            limit_up=data["UpperLimitPrice"],
            limit_down=data["LowerLimitPrice"],
            open_interest=data['OpenInterest'],
            open_price=data["OpenPrice"],
            high_price=data["HighestPrice"],
            low_price=data["LowestPrice"],
            pre_close=data["PreClosePrice"],
            bid_price_1=data["BidPrice1"],
            ask_price_1=data["AskPrice1"],
            bid_volume_1=data["BidVolume1"],
            ask_volume_1=data["AskVolume1"],
            average_price=data['AveragePrice'],
            pre_settlement_price=data['PreSettlementPrice'],
            settlement_price=data['SettlementPrice'],
            pre_open_interest=data['PreOpenInterest'],
            gateway_name=self.gateway_name
        )
        self.on_event(type=EVENT_TICK, data=tick)

    def connect(self, info: dict):
        """
        Start connection to server.
        """
        self.userid = info['userid']
        self.password = info['password']
        self.brokerid = info['brokerid']

        # If not connected, then start connection first.
        if not self.connect_status:
            path = get_folder_path(self.gateway_name.lower() + f"/{self.userid}")
            self.createFtdcMdApi(str(path) + "\\Md")
            self.registerFront(info['md_address'])
            self.init()
        # If already connected, then login immediately.
        elif not self.login_status:
            self.login()

    def login(self):
        """
        Login onto server.
        """
        req = {
            "UserID": self.userid,
            "Password": self.password,
            "BrokerID": self.brokerid
        }

        self.reqid += 1
        self.reqUserLogin(req, self.reqid)

    def subscribe(self, symbol):
        """
        Subscribe to tick data update.
        """
        result = None
        if self.login_status:
            result = self.subscribeMarketData(symbol)
        self.subscribed.add(symbol)
        return result

    def close(self):
        """
        Close the connection.
        """
        if self.connect_status:
            self.exit()


class BeeMdApiApp(MdApiApp):
    """"""

    def __init__(self, event_engine):
        """Constructor"""
        super(BeeMdApiApp, self).__init__()

        self.gateway_name = "ctp"

        self.reqid = 0
        self.event_engine = event_engine
        self.connect_status = False
        self.login_status = False
        self.subscribed = set()

        self.userid = ""
        self.password = ""
        self.brokerid = 0

    @property
    def md_status(self):
        return self.login_status

    def on_event(self, type, data):
        event = Event(type=type, data=data)
        self.event_engine.put(event)

    def onFrontConnected(self):
        """
        Callback when front server is connected.
        """
        self.connect_status = True
        self.on_event(type=EVENT_LOG, data="行情服务器连接成功")
        self.login()

    def onFrontDisconnected(self, reason: int):
        """
        Callback when front server is disconnected.
        """
        self.connect_status = False
        self.login_status = False
        self.on_event(type=EVENT_LOG, data=f"行情连接断开，原因{reason}")

    def onRspUserLogin(self, data: dict, error: dict, reqid: int, last: bool):
        """
        Callback when user is logged in.
        """
        if not error["ErrorID"]:
            self.login_status = True
            self.on_event(type=EVENT_LOG, data="行情服务器登录成功")

            for symbol in self.subscribed:
                self.subscribeMarketData(symbol)
        else:
            error["detail"] = "行情登录失败"
            self.on_event(type=EVENT_ERROR, data=error)

    def onRspError(self, error: dict, reqid: int, last: bool):
        """
        Callback when error occured.
        """
        error['detail'] = "行情接口报错"
        self.on_event(type=EVENT_ERROR, data=error)

    def onRspSubMarketData(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        if not error or not error["ErrorID"]:
            return
        error['detail'] = "行情订阅失败"
        self.on_event(type=EVENT_ERROR, data=error)

    def onRtnDepthMarketData(self, data: dict):
        """
        Callback of tick data update.
        """
        symbol = data["InstrumentID"]
        exchange = symbol_exchange_map.get(symbol, "")
        if not exchange:
            return

        timestamp = f"{data['ActionDay']} {data['UpdateTime']}.{int(data['UpdateMillisec'] / 100)}"
        try:
            datetimed = datetime.strptime(timestamp, "%Y%m%d %H:%M:%S.%f")
        except ValueError as e:
            datetimed = datetime.strptime(str(date.today()) + " " + timestamp, "%Y-%m-%d %H:%M:%S.%f")

        tick = TickData(
            symbol=symbol,
            exchange=exchange,
            datetime=datetimed,
            name=symbol_name_map[symbol],
            volume=data["Volume"],
            last_price=data["LastPrice"],
            limit_up=data["UpperLimitPrice"],
            limit_down=data["LowerLimitPrice"],
            open_interest=data['OpenInterest'],
            open_price=data["OpenPrice"],
            high_price=data["HighestPrice"],
            low_price=data["LowestPrice"],
            pre_close=data["PreClosePrice"],
            bid_price_1=data["BidPrice1"],
            ask_price_1=data["AskPrice1"],
            bid_volume_1=data["BidVolume1"],
            ask_volume_1=data["AskVolume1"],
            average_price=data['AveragePrice'],
            pre_settlement_price=data['PreSettlementPrice'],
            gateway_name=self.gateway_name
        )
        self.on_event(type=EVENT_TICK, data=tick)

    def connect(self, info: dict):
        """
        Start connection to server.
        """
        self.userid = info['userid']
        self.password = info['password']
        self.brokerid = info['brokerid']

        # If not connected, then start connection first.
        if not self.connect_status:
            path = get_folder_path(self.gateway_name.lower() + f"/{self.userid}")
            self.createFtdcMdApi(str(path) + "\\Md")
            self.registerFront(info['md_address'])
            self.init()
        # If already connected, then login immediately.
        elif not self.login_status:
            self.login()

    def login(self):
        """
        Login onto server.
        """
        req = {
            "UserID": self.userid,
            "Password": self.password,
            "BrokerID": self.brokerid
        }

        self.reqid += 1
        self.reqUserLogin(req, self.reqid)

    def subscribe(self, symbol):
        """
        Subscribe to tick data update.
        """
        result = None
        if self.login_status:
            result = self.subscribeMarketData(symbol)
        self.subscribed.add(symbol)
        return result

    def close(self):
        """
        Close the connection.
        """
        if self.connect_status:
            self.exit()
