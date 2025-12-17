from blinker import NamedSignal

import ctpbee.signals
from .lib import *
from ..func import get_folder_path


class MMdApi(MiniMdApi):

    def __init__(self, app_signal):
        """Constructor"""
        super(MMdApi, self).__init__()

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
            self.on_event(EVENT_LOG, "行情服务重新订阅")
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
        exchange = symbol_exchange_map.get(symbol, None)
        if not exchange:
            exchange = Exchange.CTP

        if exchange == Exchange.DCE:
            datetimed = datetime.strptime(
                str(date.today())
                + " "
                + f"{data['UpdateTime']}.{int(data['UpdateMillisec'] / 100)}",
                "%Y-%m-%d %H:%M:%S.%f",
            )
        else:
            # 正常情况下tick的处理
            timestamp = f"{data['ActionDay']} {data['UpdateTime']}.{int(data['UpdateMillisec'] / 100)}"
            try:
                datetimed = datetime.strptime(timestamp, "%Y%m%d %H:%M:%S.%f")
            except ValueError as e:
                datetimed = datetime.strptime(
                    str(date.today()) + " " + timestamp, "%Y-%m-%d %H:%M:%S.%f"
                )

        tick = TickData(
            symbol=symbol,
            exchange=exchange,
            datetime=datetimed,
            name=symbol_name_map.get(symbol, "None"),
            volume=data["Volume"],
            last_price=data["LastPrice"],
            limit_up=data["UpperLimitPrice"],
            limit_down=data["LowerLimitPrice"],
            open_interest=data["OpenInterest"],
            open_price=data["OpenPrice"],
            high_price=data["HighestPrice"],
            low_price=data["LowestPrice"],
            pre_close=data["PreClosePrice"],
            turnover=data["Turnover"],
            bid_price_1=data.get("BidPrice1", 0),
            bid_price_2=data.get("BidPrice2", 0),
            bid_price_3=data.get("BidPrice3", 0),
            bid_price_4=data.get("BidPrice4", 0),
            bid_price_5=data.get("BidPrice5", 0),
            ask_price_1=data.get("AskPrice1", 0),
            ask_price_2=data.get("AskPrice2", 0),
            ask_price_3=data.get("AskPrice3", 0),
            ask_price_4=data.get("AskPrice4", 0),
            ask_price_5=data.get("AskPrice5", 0),
            bid_volume_1=data.get("BidVolume1", 0),
            bid_volume_2=data.get("BidVolume2", 0),
            bid_volume_3=data.get("BidVolume3", 0),
            bid_volume_4=data.get("BidVolume4", 0),
            bid_volume_5=data.get("BidVolume5", 0),
            ask_volume_1=data.get("AskVolume1", 0),
            ask_volume_2=data.get("AskVolume2", 0),
            ask_volume_3=data.get("AskVolume3", 0),
            ask_volume_4=data.get("AskVolume4", 0),
            ask_volume_5=data.get("AskVolume5", 0),
            average_price=data["AveragePrice"],
            pre_settlement_price=data["PreSettlementPrice"],
            settlement_price=data["SettlementPrice"],
            pre_open_interest=data["PreOpenInterest"],
            gateway_name=self.gateway_name,
        )
        self.on_event(type=EVENT_TICK, data=tick)

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
            path = get_folder_path(self.gateway_name.lower() + f"/{self.userid}")
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
            "BrokerID": self.brokerid,
        }

        self.reqid += 1
        self.reqUserLogin(req, self.reqid)

    def subscribe(self, symbol):
        """
        Subscribe to tick data update.
        """
        result = None
        if self.login_status and symbol not in self.subscribed:
            result = self.subscribeMarketData(symbol)
        self.subscribed.add(symbol)
        return result

    def close(self):
        """
        Close the connection.
        """
        if self.connect_status:
            self.exit()
