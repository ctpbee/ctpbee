"""
Basic data structure used for general trading function in VN Trader.
"""

from dataclasses import dataclass, asdict
from datetime import datetime, date
from enum import Enum
from logging import INFO
from typing import Any


class Missing:
    value = "属性缺失"


class Direction(Enum):
    """
    Direction of order/trade/position.
    """
    LONG = "多"
    SHORT = "空"
    NET = "净"


class Offset(Enum):
    """
    Offset of order/trade.
    """
    NONE = ""
    OPEN = "开"
    CLOSE = "平"
    CLOSETODAY = "平今"
    CLOSEYESTERDAY = "平昨"


class Status(Enum):
    """
    Order status.
    """
    SUBMITTING = "提交中"
    NOTTRADED = "未成交"
    PARTTRADED = "部分成交"
    ALLTRADED = "全部成交"
    CANCELLED = "已撤销"
    REJECTED = "拒单"


class Product(Enum):
    """
    Product class.
    """
    EQUITY = "股票"
    FUTURES = "期货"
    OPTION = "期权"
    INDEX = "指数"
    FOREX = "外汇"
    SPOT = "现货"
    ETF = "ETF"
    BOND = "债券"
    WARRANT = "权证"
    SPREAD = "价差"
    FUND = "基金"


class OrderType(Enum):
    """
    Order type.
    """
    LIMIT = "限价"
    MARKET = "市价"
    STOP = "STOP"
    FAK = "FAK"
    FOK = "FOK"


class OptionType(Enum):
    """
    Option type.
    """
    CALL = "看涨期权"
    PUT = "看跌期权"


class Exchange(Enum):
    """
    Exchange.
    """
    # Chinese
    CFFEX = "CFFEX"
    SHFE = "SHFE"
    CZCE = "CZCE"
    DCE = "DCE"
    INE = "INE"
    SSE = "SSE"
    SZSE = "SZSE"
    SGE = "SGE"
    CTP = "ctp"
    # Global
    SMART = "SMART"
    NYMEX = "NYMEX"
    GLOBEX = "GLOBEX"
    IDEALPRO = "IDEALPRO"
    CME = "CME"
    ICE = "ICE"
    SEHK = "SEHK"
    HKFE = "HKFE"

    # CryptoCurrency
    BITMEX = "BITMEX"
    OKEX = "OKEX"
    HUOBI = "HUOBI"
    BITFINEX = "BITFINEX"


TODAY_EXCHANGE = [Exchange.INE, Exchange.SHFE]
EXCHANGE_MAPPING = {
    "CFFEX": Exchange.CFFEX,
    "SHFE": Exchange.SHFE,
    "CZCE": Exchange.CZCE,
    "DCE": Exchange.DCE,
    "INE": Exchange.INE,
    "SSE": Exchange.SSE,
    "SZSE": Exchange.SZSE,
    "SGE": Exchange.SGE,
    "SMART": Exchange.SMART,
    "NYMEX": Exchange.NYMEX,
    "GLOBEX": Exchange.GLOBEX,
    "IDEALPRO": Exchange.IDEALPRO,
    "CME": Exchange.CME,
    "ICE": Exchange.ICE,
    "SEHK": Exchange.SEHK,
    "HKFE": Exchange.HKFE,
    "BITMEX": Exchange.BITMEX,
    "OKEX": Exchange.OKEX,
    "HUOBI": Exchange.HUOBI,
    "BITFINEX": Exchange.BITFINEX,
    "CTP": Exchange.CTP
}


class Currency(Enum):
    """
    Currency.
    """
    USD = "USD"
    HKD = "HKD"
    CNY = "CNY"


class Interval(Enum):
    """
    Interval of bar data.
    """
    MINUTE = "1m"
    HOUR = "1h"
    DAILY = "d"
    WEEKLY = "w"


enums = [Interval, Currency, Exchange, OptionType, OrderType, Product, Status, Offset, Direction]

ACTIVE_STATUSES = set([Status.NOTTRADED, Status.PARTTRADED])

EVENT_LOG = "log"
EVENT_CONTRACT = "contract"
EVENT_TICK = "tick"
EVENT_BAR = "bar"
EVENT_ERROR = "error"
EVENT_POSITION = "position"
EVENT_TRADE = "trade"
EVENT_ORDER = "order"
EVENT_ACCOUNT = "account"
EVENT_SHARED = "shared"
EVENT_LAST = "last"
EVENT_INIT_FINISHED = "init"
EVENT_WARNING = "warning"


@dataclass(init=False, repr=False)
class BaseData:
    """
    Any data object needs a gateway_name as source
    and should inherit base data.
    """

    gateway_name: str
    local_symbol: str

    def __new__(cls, **kwargs):
        args = super().__new__(cls)
        setattr(args, "__name__", cls.__name__)
        return args

    def __init__(self, **mapping):
        for key, value in mapping.items():
            setattr(self, key, value)
        if hasattr(self, "__post_init__"):
            self.__post_init__()

    def __init_subclass__(cls, **kwargs):
        # ??? excuse me ....
        cls.__dict__['__annotations__']['gateway_name'] = str
        cls.__dict__['__annotations__']['local_symbol'] = str

    def __repr__(self):
        mat = []
        for key in dir(self):
            if key.startswith("_") or key.startswith("create"):
                continue
            mat.append(f" {key}={getattr(self, key, None)}, ")
        return f"{self.__name__}({''.join(mat)})"

    @classmethod
    def _create_class(cls, kwargs: dict):
        """ 根据字典值创建类实例 """
        args = super().__new__(cls)
        args.__init__(**kwargs)
        setattr(args, "__name__", cls.__name__)
        return args

    def _serialize(self, data):
        for key, value in data:
            setattr(self, key, value)

    def _to_dict(self) -> dict:
        """ 转换enum为value的字典 """
        temp = {}
        for x in dir(self):
            if x.startswith("_") or x.startswith("create"):
                continue
            if isinstance(getattr(self, x), Enum):
                temp[x] = getattr(self, x).value
                continue
            temp[x] = getattr(self, x)
        return temp

    def _to_df(self):
        try:
            from pandas import DataFrame
            temp = {}
            for x in dir(self):
                if x.startswith("_") or x.startswith("create"):
                    continue
                if isinstance(getattr(self, x), Enum):
                    temp[x] = getattr(self, x).value
                    continue
                temp[x] = getattr(self, x)
            return DataFrame([temp], columns=list(temp.keys()).remove("datetime")).set_index(['datetime']) if temp.get(
                "datetime", None) is not None else DataFrame([temp], columns=list(temp.keys()))
        except ImportError:
            raise ImportError("请使用pip install pandas 以获取此特性")

    def _asdict(self):
        """ 转换为字典 里面会有enum """
        return asdict(self)


@dataclass(init=False, repr=False)
class BaseRequest:
    """
    Any data object needs a gateway_name as source
    and should inherit base data.
    """

    def __new__(cls, **kwargs):
        args = super().__new__(cls)
        setattr(args, "__name__", cls.__name__)
        return args

    def __init__(self, **mapping):
        for key, value in mapping.items():
            setattr(self, key, value)
        if hasattr(self, "__post_init__"):
            self.__post_init__()

    def __repr__(self):
        mat = []
        for key in dir(self):
            if key.startswith("_") or key.startswith("create"):
                continue
            mat.append(f" {key}={getattr(self, key)}, ")
        return f"{self.__name__}({''.join(mat)})"

    @classmethod
    def _create_class(cls, kwargs: dict):
        """ 根据字典值创建类 """
        args = super().__new__(cls)
        args.__init__(**kwargs)
        setattr(args, "__name__", cls.__name__)
        return args

    def _serialize(self, data):
        for key, value in data:
            setattr(self, key, value)

    def _to_dict(self) -> dict:
        """ 转换enum为value的字典 """
        temp = {}
        for x in dir(self):
            if x.startswith("_") or x.startswith("create"):
                continue
            if isinstance(getattr(self, x), Enum):
                temp[x] = getattr(self, x).value
                continue
            temp[x] = getattr(self, x)
        return temp

    def _asdict(self):
        """ 转换为字典 里面会有enum """
        return asdict(self)


class TickData(BaseData):
    """
    Tick data contains information about:
        * last trade in market
        * orderbook snapshot
        * intraday market statistics.
    """
    symbol: str
    exchange: Any
    datetime: datetime
    name: str = ""
    volume: float = 0
    last_price: float = 0
    last_volume: float = 0
    limit_up: float = 0
    limit_down: float = 0
    open_interest: int = 0
    average_price: float = 0
    settlement_price: float = 0
    pre_settlement_price: float = 0
    pre_open_interest: int = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    pre_close: float = 0
    turnover: float = 0

    bid_price_1: float = 0
    bid_price_2: float = 0
    bid_price_3: float = 0
    bid_price_4: float = 0
    bid_price_5: float = 0

    ask_price_1: float = 0
    ask_price_2: float = 0
    ask_price_3: float = 0
    ask_price_4: float = 0
    ask_price_5: float = 0

    bid_volume_1: float = 0
    bid_volume_2: float = 0
    bid_volume_3: float = 0
    bid_volume_4: float = 0
    bid_volume_5: float = 0

    ask_volume_1: float = 0
    ask_volume_2: float = 0
    ask_volume_3: float = 0
    ask_volume_4: float = 0
    ask_volume_5: float = 0

    def __post_init__(self):
        """"""
        l = getattr(self, "local_symbol", None)
        if l is not None:
            setattr(self, "symbol", l.split(".")[0])
            setattr(self, "exchange", l.split(".")[1])
        else:
            self.local_symbol = f"{self.symbol}.{self.exchange.value}"


class BarData(BaseData):
    """
    Candlestick bar data of a certain trading period.
    """
    symbol: str
    exchange: Exchange
    datetime: datetime

    interval: Interval = None
    volume: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0
    is_next: bool = False
    is_last: bool = False

    def __post_init__(self):
        """"""
        l = getattr(self, "local_symbol", None)
        if l is not None:
            setattr(self, "symbol", l.split(".")[0])
            setattr(self, "exchange", l.split(".")[1])
        else:
            try:
                self.local_symbol = f"{self.symbol}.{self.exchange.value}"
            except AttributeError:
                self.local_symbol = f"{self.symbol}.{self.exchange}"

class OrderData(BaseData):
    """
    Order data contains information for tracking lastest status
    of a specific order.
    """
    local_order_id: str = ""
    symbol: str
    exchange: Exchange
    order_id: str

    type: OrderType = OrderType.LIMIT
    direction: Direction = ""
    offset: Offset = Offset.NONE
    price: float = 0
    volume: float = 0
    traded: float = 0
    status: Status = Status.SUBMITTING
    time: str = ""

    def __post_init__(self):
        """"""
        try:
            self.local_symbol = f"{self.symbol}.{self.exchange.value}"
        except AttributeError as e:
            self.local_symbol = f"{self.symbol}.{self.exchange}"
        self.local_order_id = f"{self.gateway_name}.{self.order_id}"

    def _is_active(self):
        """
        Check if the order is active.
        """
        if self.status in ACTIVE_STATUSES:
            return True
        else:
            return False

    def create_cancel_request(self):
        """
        Create cancel request object from order.
        """
        req = CancelRequest(
            order_id=self.order_id, symbol=self.symbol, exchange=self.exchange
        )
        return req


class TradeData(BaseData):
    """
    Trade data contains information of a fill of an order. One order
    can have several trade fills.
    """
    local_order_id: str = ""
    local_trade_id: str = ""
    symbol: str
    exchange: Exchange
    order_id: str
    tradeid: str
    direction: Direction = ""

    offset: Offset = Offset.NONE
    price: float = 0
    volume: float = 0
    time: str = ""
    order_time: str = ""

    def __post_init__(self):
        """"""
        try:
            self.local_symbol = f"{self.symbol}.{self.exchange.value}"
        except AttributeError:
            self.local_symbol = f"{self.symbol}.{self.exchange}"
        self.local_order_id = f"{self.gateway_name}.{self.order_id}"
        self.local_trade_id = f"{self.gateway_name}.{self.tradeid}"


class PositionData(BaseData):
    """
    Positon data is used for tracking each individual position holding.
    """
    local_position_id: str = ""
    symbol: str
    exchange: Exchange
    direction: Direction

    volume: float = 0
    frozen: float = 0
    price: float = 0
    pnl: float = 0
    yd_volume: float = 0

    def __post_init__(self):
        """"""
        self.local_symbol = f"{self.symbol}.{self.exchange.value}"
        self.local_position_id = f"{self.local_symbol}.{self.direction}"


class AccountData(BaseData):
    """
    Account data contains information about balance, frozen and
    available.
    """
    local_account_id: str = ""
    accountid: str

    balance: float = 0
    frozen: float = 0

    def __post_init__(self):
        """"""
        self.available = self.balance - self.frozen
        self.local_account_id = f"{self.gateway_name}.{self.accountid}"


class LogData(BaseData):
    """
    Log data is used for recording log messages on GUI or in log files.
    """
    time: datetime = None
    msg: str
    level: int = INFO

    def __post_init__(self):
        """"""
        self.time = datetime.now()


class LastData(BaseData):
    symbol: str
    exchange: Exchange
    pre_open_interest: float
    open_interest: float
    volume: int
    last_price: float

    def __post_init__(self):
        self.local_symbol = f"{self.symbol}.{self.exchange.value}"


class ContractData(BaseData):
    """
    Contract data contains basic information about each contract traded.
    """

    symbol: str
    exchange: Exchange
    name: str
    product: Product
    size: int
    pricetick: float

    min_volume: float = 1
    stop_supported: bool = False
    net_position: bool = False

    option_strike: float = 0
    option_underlying: str = ""
    option_type: OptionType = None
    option_expiry: datetime = None

    create_date: date
    open_date: date
    expire_date: date
    start_delivery_date: date
    end_delivery_date: date

    inst_life_phase: str
    is_trading: bool

    position_type: str
    position_date_type: str
    long_margin_ratio: float
    short_margin_ratio: float
    max_margin_side_algorithm: bool

    def __post_init__(self):
        """"""
        self.local_symbol = f"{self.symbol}.{self.exchange.value}"


class SubscribeRequest(BaseRequest):
    """
    Request sending to specific gateway for subscribing tick data update.
    """
    local_symbol: str = ""
    symbol: str
    exchange: Exchange

    def __post_init__(self):
        """"""
        self.local_symbol = f"{self.symbol}.{self.exchange.value}"


class OrderRequest(BaseRequest):
    """
    Request sending to specific gateway for creating a new order.
    """
    local_symbol: str = ""
    symbol: str
    exchange: Exchange
    direction: Direction
    type: OrderType
    volume: float
    price: float = 0
    offset: Offset = Offset.NONE

    def __post_init__(self):
        """"""
        try:
            self.local_symbol = f"{self.symbol}.{self.exchange.value}"
        except AttributeError:
            self.local_symbol = f"{self.symbol}.{self.exchange}"

    def _create_order_data(self, order_id: str, gateway_name: str, time=None):
        """
        Create order data from request.
        """
        order = OrderData(
            symbol=self.symbol,
            exchange=self.exchange,
            order_id=order_id,
            type=self.type,
            direction=self.direction,
            offset=self.offset,
            price=self.price,
            volume=self.volume,
            gateway_name=gateway_name,
            time=time
        )
        return order


class CancelRequest(BaseRequest):
    """
    Request sending to specific gateway for canceling an existing order.
    """
    local_symbol: str = ""
    order_id: str
    symbol: str
    exchange: Exchange

    def __post_init__(self):
        """"""
        self.local_symbol = f"{self.symbol}.{self.exchange.value}"


class SharedData(BaseData):
    local_symbol: str
    datetime: datetime

    open_interest: int = 0
    volume: float = 0
    last_price: float = 0
    average_price: float = 0


# type check
# https://www.jianshu.com/p/36bfc4a927a4

# 查询银行账号
class AccountRegisterRequest(BaseRequest):
    bank_id: str = ""
    # bank_branch_id: str = ""
    currency_id: str = "CNY"


# 查询银行余额
class AccountBanlanceRequest(BaseRequest):
    bank_id: str
    # bank_branch_id: str
    # broker_branch_id: str
    bank_account: str
    bank_password: str
    currency_id: str = "CNY"


# 证券与银行互转请求
class TransferRequest(BaseRequest):
    bank_id: str
    # bank_branch_id: str

    # broker_branch_id: str
    # 银行
    bank_account: str
    band_password: str
    # 币
    trade_account: int
    currency_id: str = "CNY"


class TransferSerialRequest(BaseRequest):
    """ 查询转账流水 """
    bank_id: str
    currency_id: str = "CNY"


class MarketDataRequest(BaseRequest):
    """ 请求市场数据 """
    symbol: str
    exchange: Exchange


EVENT_TIMER = "timer"


class Event:
    """
    Event object consists of a type string which is used
    by event engine for distributing event, and a data
    object which contains the real data.
    """

    def __init__(self, type: str, data: Any = None):
        """"""
        self.type = type
        self.data = data

    def __str__(self):
        return "Event(type={})".format(self.type)


data_class = [TickData, BarData, OrderData, TradeData, PositionData, AccountData, LogData, ContractData, SharedData]
request_class = [SubscribeRequest, OrderRequest, CancelRequest, AccountRegisterRequest, AccountBanlanceRequest,
                 TransferRequest, TransferSerialRequest]
