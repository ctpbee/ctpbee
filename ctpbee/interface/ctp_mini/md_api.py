from blinker import NamedSignal

import ctpbee.signals
from .lib import *
from ..func import get_folder_path


class MiniMdApi(MdApi):

    def __init__(self, app_signal):
        """Constructor"""
        super(MiniMdApi, self).__init__()

        self.gateway_name = "ctp_mini"
        self.reqid = 0
        self.app_signal = app_signal
        self.connect_status = False
        self.login_status = False
        self.subscribed = set()

        self.userid = ""
        self.password = ""
        self.brokerid = ""

    @property
    def md_status(self):
        return self.login_status

    def on_event(self, type, data):
        if type == EVENT_TICK:
            event = Event(type=type, data=data)
            signal = getattr(ctpbee.signals.common_signals, f"{type}_signal")
            signal.send(event)
        else:
            event = Event(type=type, data=data)
            signal: NamedSignal = getattr(self.app_signal, f"{type}_signal")
            signal.send(event)

    def onFrontConnected(self):
        """
        Callback when front server is connected.
        """
        self.on_event(EVENT_LOG, "行情服务器连接成功")
        self.login()

    def onFrontDisconnected(self, reason: int):
        """
        Callback when front server is disconnected.
        """
        self.login_status = False
        self.on_event(EVENT_LOG, f"行情服务器连接断开，原因{reason}")

    def onRspUserLogin(self, data: dict, error: dict, reqid: int, last: bool):
        """
        Callback when user is logged in.
        """
        if not error["ErrorID"]:
            self.login_status = True
            self.on_event(EVENT_LOG, "行情服务器登录成功")

            for symbol in self.subscribed:
                self.subscribeMarketData(symbol)
        else:
            self.on_event(EVENT_ERROR, f"行情服务器登录失败: {error}")

    def onRspError(self, error: dict, reqid: int, last: bool):
        """
        Callback when error occured.
        """
        self.on_event(EVENT_ERROR, f"行情接口报错 {error}")

    def onRspSubMarketData(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        if not error or not error["ErrorID"]:
            return

        self.on_event(EVENT_ERROR, f"行情订阅失败: {error}")

    def onRtnDepthMarketData(self, data: dict):
        """
        Callback of tick data update.
        """
        symbol = data["InstrumentID"]
        exchange = symbol_exchange_map.get(symbol, "")
        if not exchange:
            return

        timestamp = f"{data['ActionDay']} {data['UpdateTime']}.{int(data['UpdateMillisec'] / 100)}"
        dt = datetime.strptime(timestamp, "%Y%m%d %H:%M:%S.%f")
        dt = CHINA_TZ.localize(dt)

        tick = TickData(
            symbol=symbol,
            exchange=exchange,
            datetime=dt,
            name=symbol_name_map[symbol],
            volume=data["Volume"],
            open_interest=data["OpenInterest"],
            last_price=data["LastPrice"],
            limit_up=data["UpperLimitPrice"],
            limit_down=data["LowerLimitPrice"],
            open_price=data["OpenPrice"],
            high_price=data["HighestPrice"],
            low_price=data["LowestPrice"],
            pre_close=data["PreClosePrice"],
            bid_price_1=data["BidPrice1"],
            ask_price_1=data["AskPrice1"],
            bid_volume_1=data["BidVolume1"],
            ask_volume_1=data["AskVolume1"],
            gateway_name=self.gateway_name
        )

        if data["BidPrice2"]:
            tick.bid_price_2 = data["BidPrice2"]
            tick.bid_price_3 = data["BidPrice3"]
            tick.bid_price_4 = data["BidPrice4"]
            tick.bid_price_5 = data["BidPrice5"]

            tick.ask_price_2 = data["AskPrice2"]
            tick.ask_price_3 = data["AskPrice3"]
            tick.ask_price_4 = data["AskPrice4"]
            tick.ask_price_5 = data["AskPrice5"]

            tick.bid_volume_2 = data["BidVolume2"]
            tick.bid_volume_3 = data["BidVolume3"]
            tick.bid_volume_4 = data["BidVolume4"]
            tick.bid_volume_5 = data["BidVolume5"]

            tick.ask_volume_2 = data["AskVolume2"]
            tick.ask_volume_3 = data["AskVolume3"]
            tick.ask_volume_4 = data["AskVolume4"]
            tick.ask_volume_5 = data["AskVolume5"]

        self.on_event(EVENT_TICK, tick)

    def connect(self, info):
        """
        Start connection to server.
        """
        address = info["md_address"]
        self.userid = info["userid"]
        self.password = info["password"]
        self.brokerid = info["brokerid"]

        # If not connected, then start connection first.
        if not self.connect_status:
            path = get_folder_path(self.gateway_name.lower())
            self.createFtdcMdApi(str(path) + "\\Md")

            self.registerFront(address)
            self.init()

            self.connect_status = True
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

    def subscribe(self, req: SubscribeRequest):
        """
        Subscribe to tick data update.
        """
        if self.login_status:
            self.subscribeMarketData(req.symbol)
        self.subscribed.add(req.symbol)

    def close(self):
        """
        Close the connection.
        """
        if self.connect_status:
            self.exit()
