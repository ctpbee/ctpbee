"""
Here is from https://github.com/yutiansut/QIFIAccount
"""
import json
import uuid
import datetime
import warnings
from dataclasses import dataclass, asdict
from typing import List
from collections import OrderedDict

from qaenv import mongo_ip

from ctpbee.center import PositionModel
from ctpbee.constant import AccountData, OrderData, TradeData, PositionData, Direction, Offset

try:
    import QUANTAXIS as QA
except ImportError:
    warnings.warn("请安装ctpbee[QA_SUPPORT]版本，安装详见: https://docs.ctpbee.com/install\n"
                  "please install ctpbee[QA_SUPPORT] version. see the url before")

mongo_ip = "192.168.2.117"


class Basic:
    @classmethod
    def from_dict(cls, dit: dict):
        """ 从字典中载入 """
        data = cls()
        for key, var in dit.values():
            setattr(data, key, var)
        return data

    @classmethod
    def from_json(cls, json_name):
        with open(json_name, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)


@dataclass
class Position(Basic):
    user_id: str = ""
    exchange_id: str = ""
    instrument_id: str = ""
    volume_long_today: float = 0.0
    volume_long_his: float = 0.0
    volume_long: float = 0.0
    volume_long_frozen_today: float = 0.0
    volume_long_frozen_his: float = 0.0
    volume_long_frozen: float = 0.0
    volume_short_today: float = 0.0
    volume_short_his: float = 0.0
    volume_short: float = 0.0
    volume_short_frozen_today: float = 0.0
    volume_short_frozen_his: float = 0.0
    volume_short_frozen: float = 0.0
    volume_long_yd: float = 0.0
    volume_short_yd: float = 0.0
    pos_long_his: float = 0.0
    pos_long_today: float = 0.0
    pos_short_his: float = 0.0
    pos_short_today: float = 0.0
    open_price_long: float = 0.0
    open_price_short: float = 0.0
    open_cost_long: float = 0.0
    open_cost_short: float = 0.0
    position_price_long: float = 0.0
    position_price_short: float = 0.0
    position_cost_long: float = 0.0
    position_cost_short: float = 0.0
    last_price: float = 0.0
    float_profit_long: float = 0.0
    float_profit_short: float = 0.0
    float_profit: float = 0.0
    position_profit_long: float = 0.0
    position_profit_short: float = 0.0
    position_profit: float = 0.0
    margin_long: float = 0.0
    margin_short: float = 0.0
    margin: float = 0.0

    def __getattr__(self, item):
        return self.__dict__.get(item)


@dataclass
class Order(Basic):
    seqno: int = 0
    user_id: str = ""
    order_id: str = ""
    exchange_id: str = ""
    instrument_id: str = ""
    direction: str = Direction.LONG.value
    offset: str = Offset.OPEN.value
    volume_orign: float = 0
    price_type: str = ""
    limit_price: float = 0.0
    time_condition: str = "GFD"
    volume_condition: str = ""
    insert_date_time: int = 0
    exchange_order_id: str = ""
    status: str = ""
    volume_left: int = 0
    last_msg: str = ""


def transform_dt(times):
    if isinstance(times, str):
        tradedt = datetime.datetime.strptime(times, '%Y-%m-%d %H:%M:%S') if len(
            times) == 19 else datetime.datetime.strptime(times.replace('_', '.'), '%Y-%m-%d %H:%M:%S.%f')
        return tradedt.timestamp() * 1000000000
    elif isinstance(times, datetime.datetime):
        return times.timestamp() * 1000000000


@dataclass
class Trade(Basic):
    seqno: int = 0
    user_id: str = ""
    trade_id: str = ""
    exchange_id: str = ""
    instrument_id: str = ""
    order_id: str = ""
    exchange_trade_id: str = ""
    direction: str = Direction.LONG.value
    offset: str = Offset.OPEN.value
    volume: float = 0.0
    price: float = 0.0
    trade_date_time: int = 0
    commission: float = 0


def get_offset(offseted):
    if offseted == Offset.OPEN:
        offset = "OPEN"
    elif offseted == Offset.CLOSETODAY:
        offset = "CLOSETODAY"
    elif offseted == Offset.CLOSEYESTERDAY:
        offset = "CLOSEYESTERDAY"
    else:
        offset = "CLOSE"
    return offset


def create_trade(trade: TradeData, name: str) -> Trade:
    return Trade(seqno=int(trade.order_id.split("_")[-1]), user_id=name, trade_id=trade.tradeid.lstrip(),
                 volume=trade.volume,
                 order_id=trade.order_id, exchange_trade_id=trade.tradeid.lstrip(), instrument_id=trade.symbol,
                 exchange_id=trade.exchange.value, direction="BUY" if trade.direction == Direction.LONG else "SELL",
                 offset=get_offset(trade.offset),
                 price=trade.price, trade_date_time=int(
            transform_dt(times=str(datetime.datetime.now().date()) + " {}".format(trade.time))))


def create_order(order: OrderData, name: str) -> Order:
    """
    :type order: object
    """
    return Order(seqno=int(order.order_id.split("_")[-1]), user_id=name, order_id=order.order_id,
                 exchange_id=order.exchange.value, instrument_id=order.symbol,
                 direction="BUY" if order.direction == Direction.LONG else "SELL", offset=get_offset(order.offset),
                 volume_orign=order.volume,
                 price_type=order.type.value, limit_price=order.price, exchange_order_id=order.order_id,
                 status=order.status.value,
                 insert_date_time=int(
                     transform_dt(times=str(datetime.datetime.now().date()) + " {}".format(order.time)))
                 )


def create_position(pos: PositionModel, name) -> Position:
    return Position(volume_long=pos.long_volume, volume_long_his=pos.long_yd_volume,
                    volume_long_today=pos.long_volume - pos.long_yd_volume, volume_short=pos.short_volume,
                    volume_short_his=pos.short_yd_volume,
                    volume_short_today=pos.short_volume - pos.short_yd_volume,
                    open_price_long=pos.long_price, open_price_short=pos.short_price,
                    open_cost_long=pos.long_volume * pos.long_price,
                    open_cost_short=pos.short_volume * pos.short_price,
                    float_profit=pos.long_pnl + pos.short_pnl,
                    float_profit_long=pos.long_pnl, float_profit_short=pos.short_pnl,
                    instrument_id=pos.local_symbol.split(".")[0], exchange_id=pos.exchange,
                    user_id=name
                    )


class QIFI:
    def __init__(self, username, password, model="SIM", broker_name="QAPaperTrading", trade_host=mongo_ip,
                 init_cash=1000000, taskid=str(uuid.uuid4())):
        try:
            import pymongo
        except Exception as e:
            raise ValueError(
                "请尝试安装pymongo以使用mongodb功能"
            )
        self.user_id = username
        self.username = username
        self.password = password
        self.source_id = "QIFI_Account"  # 识别号
        # 指的是 Account所属的账户编组(实时的时候的账户观察组)
        self.portfolio = "QAPaperTrade"
        self.model = model
        self.broker_name = broker_name  # 所属期货公司/ 模拟的组
        self.investor_name = ""  # 账户所属人(实盘的开户人姓名)
        self.bank_password = ""
        self.capital_password = ""
        self.wsuri = ""

        self.bank_id = "QASIM"
        self.bankname = "QASIMBank"

        self.trade_host = trade_host
        self.db = pymongo.MongoClient(trade_host).QAREALTIME

        self.pub_host = ""
        self.trade_host = ""
        self.last_updatetime = ""
        self.status = 200
        self.trading_day = ""
        self.init_cash = init_cash
        self.pre_balance = 0

        self.static_balance = 0

        self.deposit = 0  # 入金
        self.withdraw = 0  # 出金
        self.withdrawQuota = 0  # 可取金额
        self.close_profit = 0
        self.premium = 0  # 本交易日内交纳的期权权利金
        self.event_id = 0
        self.taskid = taskid
        self.money = 0
        self.transfers = {}

        self.banks = {}

        self.frozen = {}

        self.event = {}
        self.positions = OrderedDict()
        self.trades = OrderedDict()
        self.orders = OrderedDict()

    def to_dict(self):
        return {
            # // 账户号(兼容QUANTAXIS QAAccount)// 实盘的时候是 账户id
            "account_cookie": self.user_id,
            "password": self.password,
            "databaseip": self.trade_host,
            "model": self.model,
            "ping_gap": 5,
            "portfolio": self.portfolio,
            "broker_name": self.broker_name,  # // 接入商名称
            "capital_password": self.capital_password,  # // 资金密码 (实盘用)
            "bank_password": self.bank_password,  # // 银行密码(实盘用)
            "bankid": self.bank_id,  # // 银行id
            "investor_name": self.investor_name,  # // 开户人名称
            "money": self.money,  # // 当前可用现金
            "pub_host": self.pub_host,
            "trade_host": self.trade_host,
            "taskid": self.taskid,
            "sourceid": self.source_id,
            "updatetime": str(self.last_updatetime),
            "wsuri": self.wsuri,
            "bankname": self.bankname,
            "trading_day": str(self.trading_day),
            "status": self.status,
            "accounts": self.account_msg,
            "trades": {key: asdict(value) for key, value in self.trades.items()},
            "positions": {key: asdict(value) for key, value in self.positions.items()},
            "orders": {key: asdict(value) for key, value in self.orders.items()},
            "event": self.event,
            "transfers": self.transfers,
            "banks": self.banks,
            "frozen": self.frozen,
            "settlement": {},
        }

    @property
    def float_profit(self):
        """  """
        return sum([pos.float_profit for pos in self.positions.values()])

    @property
    def position_profit(self):
        return sum([pos.position_profit for pos in self.positions.values()])

    @property
    def commission(self):
        return 0

    @property
    def frozen_margin(self):
        # return sum([item.get('money') for item in self.frozen.values()])
        return self.frozen

    @property
    def balance(self):
        """动态权益
        Arguments:
            self {[type]} -- [description]
        """

        return self.static_balance + self.deposit - self.withdraw + self.float_profit + self.close_profit

    @property
    def available(self):
        """ 可用余额　"""
        return self.money

    @property
    def margin(self):
        """保证金
        """
        return sum([position.margin for position in self.positions.values()])

    @property
    def account_msg(self):
        return {
            "user_id": self.user_id,
            "currency": "CNY",
            "pre_balance": self.pre_balance,
            "deposit": self.deposit,
            "withdraw": self.withdraw,
            "WithdrawQuota": self.withdrawQuota,
            "close_profit": self.close_profit,
            "commission": self.commission,
            "premium": self.premium,
            "static_balance": self.static_balance,
            "position_profit": self.position_profit,
            "float_profit": self.float_profit,
            "balance": self.balance,
            "margin": self.margin,
            "frozen_margin": self.frozen_margin,
            "frozen_commission": 0.0,
            "frozen_premium": 0.0,
            "available": self.available,
            "risk_ratio": 1 - self.available / self.balance if self.balance != 0 else 0
        }


class QIFIManager:
    """
    注意QIFIManager是为了快速快速将数据写入与写出到QA的操作
    并不具备本地结算功能　
    """

    def __init__(self, app):
        """
        """
        self.app = app
        try:
            config = app.config.get("QA_SETUP", None)
            if config is None:
                raise TypeError("你已经使用了QIFI参数配置, 请通过设置QA_SETUP传入mongodb配置信息")
            self.instance = QIFI(app.name, *config)
            result = self.detect_if_exist()
            if result:
                self._reload(app.name)
                self.app.logger.info(f"QIFIAccount: {app.name} 账户已经恢复")
        except ImportError:
            raise TypeError("你使用了qifi支持，但是似乎你没有安装qifiaccount, 请执行pip install qifiaccount，然后重新运行")

    def detect_if_exist(self) -> bool:
        return self.instance.db.account.find_one(
            {'account_cookie': self.instance.user_id, 'password': self.instance.password}) is not None

    def _reload(self, name):
        message = self.instance.db.account.find_one(
            {'account_cookie': self.instance.user_id, 'password': self.instance.password})

        time = datetime.datetime.now()
        # resume/settle

        if time.hour <= 15:
            self.trading_day = time.date()
        else:
            if time.weekday() in [0, 1, 2, 3]:
                self.trading_day = time.date() + datetime.timedelta(days=1)
            elif time.weekday() in [4, 5, 6]:
                self.trading_day = time.date() + datetime.timedelta(days=(7 - time.weekday()))
        if message is not None:
            accpart = message.get('accounts')
            self.instance.money = message.get('money')
            self.instance.source_id = message.get('sourceid')

            self.instance.pre_balance = accpart.get('pre_balance')
            self.instance.deposit = accpart.get('deposit')
            self.instance.withdraw = accpart.get('withdraw')
            self.instance.withdrawQuota = accpart.get('WithdrawQuota')
            self.instance.close_profit = accpart.get('close_profit')
            self.instance.static_balance = accpart.get('static_balance')
            self.instance.event = message.get('event')
            self.instance.transfers = message.get('transfers')
            try:
                self.instance.trades.update(
                    {sig.get("exchange_trade_id"): Order.from_dict(sig) for sig in message.get('trades')})
                self.instance.orders.update(
                    {sig.get("order_id"): Order.from_dict(sig) for sig in message.get('orders')})
                self.instance.taskid = message.get('taskid', str(uuid.uuid4()))

                self.instance.positions.update(
                    {sig.get("instrument_id"): Position.from_dict(sig) for sig in message.get('positions')})
            except AttributeError:
                self.app.logger.warning("从QAREALTIME账户中恢复数据失败")

            self.banks = message.get('banks')
            self.status = message.get('status')
            self.wsuri = message.get('wsuri')

            if message.get('trading_day', '') == str(self.trading_day):
                # reload
                pass

    def from_app(self):
        """ 从数据中导入 读取App里面的核心数据
        todo: 注意目前是单账户级别的 并没有做策略层级的优化
        """
        if self.app.center.account:
            self.instance.static_balance = self.app.center.account.balance
            self.instance.frozen = self.app.center.account.frozen
            self.instance.money = self.app.center.account.available
        local_symbols = list(set([x["local_symbol"] for x in self.app.center.positions]))
        for local_symbol in local_symbols:
            pos = self.app.center.get_position(local_symbol)
            if pos:
                local = create_position(pos, self.app.name)
                key = "{}_{}".format(pos.exchange, pos.local_symbol.split(".")[0])
                self.instance.positions[key] = local
        for order in self.app.center.active_orders:
            covert_order = create_order(order, self.app.name)
            self.instance.orders[order.order_id] = covert_order

        for trade in self.app.center.trades:
            self.instance.trades[trade.tradeid.lstrip()] = create_trade(trade, self.app.name)

    def insert_trade(self, trade):
        """ 插入成交单　"""
        self.instance.trades[trade.local_trade_id] = trade
        self.update()

    def insert_order(self, order):
        """ 创建order注意需要 按照顺序进行插入 """
        self.instance.orders[order.local_order_id] = order
        self.update()

    def cancel(self, order_id):
        """　撤单　"""
        try:
            self.instance.orders.pop(order_id)
            self.update()
        except IndexError:
            self.app.logger.warning("撤单不存在,已经被撤或者已经成交ｋ")

    def update(self):
        """ 更新到mongodb数据库中 """
        self.instance.db.account.update(
            {'account_cookie': self.instance.user_id, 'password': self.instance.password}, {
                '$set': self.instance.to_dict()}, upsert=True)
        self.instance.db.hisaccount.insert_one(
            {'updatetime': self.now, 'account_cookie': self.instance.user_id,
             'accounts': self.instance.account_msg})

    @property
    def now(self):
        """ 返回最新的时间 """
        return str(datetime.datetime.now()).replace(".", "_")


if __name__ == '__main__':
    from ctpbee import CtpBee

    info = {
        "CONNECT_INFO": {
            "userid": "089131",
            "password": "350888",
            "brokerid": "9999",
            "md_address": "tcp://218.202.237.33:10112",
            "td_address": "tcp://218.202.237.33:10102",
            "product_info": "",
            "appid": "simnow_client_test",
            "auth_code": "0000000000000000"
        },
        "INTERFACE": "ctp",  # 接口声明
        "TD_FUNC": True,  # 开启交易功能
        "MD_FUNC": True,
        "QA_SETUP": {"password": "somex"}
    }
    app = CtpBee("some", "", refresh=True)
    app.config.from_mapping(info)
    app.start()
    manager = QIFIManager(app)
    import time

    time.sleep(3)
    while True:
        app.action.query_position()
        manager.from_app()
        manager.update()
        time.sleep(1)
