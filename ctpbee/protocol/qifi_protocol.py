"""
ctpbee目前采用qifi协议 使得成为QUANTAXIS交易底层成为可能, 同时使得ctpbee用户能同时使用来自QA的界面端
"""
from dataclasses import dataclass

from ctpbee.protocol import Protocol


@dataclass
class QifiAccount:
    user_id = ""
    currenty: str = ""
    pre_balance: float = ""
    deposit: float = 0.0
    withdraw: float = 0.0
    WithdrawQuota: float = 0.0
    close_profit: float = 0.0
    commision: float = 0.0
    premium: float = 0.0
    static_balance: float = 0.0
    float_profit: float = 0.0
    balance: float = 0.0
    margin: float = 0.0
    frozen_margin: float = 0.0
    frozen_premium: float = 0.0
    available: float = 0.0
    risk_ratio: float = 0.0


@dataclass
class QifiBankDetail:
    id: str = ""
    name: str = ""
    bank_ccount: str = ""
    fetch_amount: float = 0
    qry_count: int = 0


@dataclass
class QifiOrder:
    seqno: int = 0
    user_id: str = ""
    order_id: str = ""
    exchange_id: str = ""
    instrument_id: str = ""
    direction: str = ""
    offset: str = ""
    volume_orign: float = 0
    price_type: str = ""
    limit_price: float = 0
    time_condition: str = ""
    volume_condition: str = ""
    insert_date_time: int = 0
    exchange_order_id: str = ""
    status: str = ""
    volume_left: float = 0
    last_msg: float = 0


@dataclass
class Position:
    user_id: str = ""
    exchange_id: str = ""
    instrument_id: str = ""
    volume_long_today: float = 0
    volume_long_his: float = 0
    volume_long: float = 0
    volume_long_frozen_today: float = 0
    volume_long_frozen_his: float = 0
    volume_long_frozen: float = 0

    volume_short_today: float = 0
    volume_short_his: float = 0
    volume_short: float = 0
    volume_short_frozen_today: float = 0
    volume_short_frozen_his: float = 0
    volume_short_frozen: float = 0
    volume_long_yd: float = 0
    volume_short_yd: float = 0

    pos_long_his: float = 0
    pos_long_today: float = 0

    pos_short_his: float = 0
    pos_short_today: float = 0
    open_price_long: float = 0
    open_price_short: float = 0
    open_cost_long: float = 0
    open_cost_short: float = 0
    position_price_long: float = 0
    position_price_short: float = 0
    position_cost_long: float = 0
    position_cost_short: float = 0
    last_price: float = 0
    float_profit_long: float = 0
    float_profit_long: float = 0
    float_profit: float = 0
    margin_long: float = 0
    margin_short: float = 0
    margin: float


@dataclass
class QifiTrade:
    seqno: int = 0
    user_id: str = ""
    trade_id: str = ""
    exchange_id: str = ""
    instrument_id: str = ""
    order_id: str = ""
    exchange_trade_id: str = ""
    direction: str = ""
    offset: str = ""
    volume: float = 0
    price: float = 0
    trade_date_time: int = 0
    commission: float = 0


@dataclass
class QifiTransfer:
    datetime: int = 0
    currency: str = ""
    amount: float = 0
    error_id: int = 0
    error_msg: str = ""


class QifiProtocol(Protocol):
    def __init__(self, **kwargs):
        self.databaseip: str = "127.0.0.1"
        self.account_cookie: str = "ctpbee"
        self.password: str = "123456"
        self.portfolio: str = ""
        self.broker_name: str = ""
        self.capital_password: str = ""
        self.bank_password: str = ""
        self.bankid: str = ""
        self.investor_name: str = ""
        self.money: float = 0
        self.pub_host = "127.0.0.1"
        self.settlement: dict = {}
        self.taskid: str = ""
        self.trade_host: str = "127.0.0.1"
        self.updatetime: str = 0
        self.wsuri: str = ""
        self.bankname: str = ""
        self.trading_day: str = ""
        self.status: str = ""
        self.accounts: QifiAccount = QifiAccount()
        self.banks = dict()
        self.event: dict = dict()
        self.orders = OrderedDict()
        self.positions = OrderedDict()
        self.trades = OrderedDict()
        self.transfers = OrderedDict()
        self.ping_gap = 0
        self.eventmq_ip: str = "127.0.0.1"
