"""
Here is from https://github.com/yutiansut/QIFIAccount
"""
import uuid
import datetime
from typing import List
from collections import OrderedDict

from qaenv import mongo_ip

from ctpbee.constant import AccountData, OrderData, TradeData

try:
    import QUANTAXIS as QA
except ImportError:
    raise EnvironmentError("请安装ctpbee[QA_SUPPORT]版本，安装详见: https://docs.ctpbee.com/install\n"
                           "please install ctpbee[QA_SUPPORT] version. see the url before")


class QIFI:
    def __init__(self, username, password, model="SIM", broker_name="QAPaperTrading", trade_host=mongo_ip,
                 init_cash=1000000, taskid=str(uuid.uuid4())):
        """Initial
        QIFI Account是一个基于 DIFF/ QIFI/ QAAccount后的一个实盘适用的Account基类
        1. 兼容多持仓组合
        2. 动态计算权益
        使用 model = SIM/ REAL来切换
        """
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
        self.positions = {}
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
            "trades": self.trades,
            "positions": self.positions,
            "orders": self.orders,
            "event": self.event,
            "transfers": self.transfers,
            "banks": self.banks,
            "frozen": self.frozen,
            "settlement": {},
        }

    @property
    def float_profit(self):
        return sum([pos.float_profit for pos in self.positions.values()])

    @property
    def position_profit(self):
        return sum([pos.position_profit for pos in self.positions.values()])

    @property
    def commission(self):
        return sum([pos.commission for pos in self.positions.values()])

    @property
    def frozen_margin(self):
        return sum([item.get('money') for item in self.frozen.values()])

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
            "risk_ratio": 1 - self.available / self.balance
        }


class QIFIManager:
    """
    注意QIFIManager是为了快速快速将数据写入与写出到QA的操作
    并不具备本地结算功能　
    """

    def __init__(self, app):
        """
        """
        self.qpp = app
        try:
            config = app.config.get("QA_SETUP", None)
            if config is None:
                raise TypeError("你已经使用了QIFI参数配置, 请通过设置QA_SETUP传入mongodb配置信息")
            self.qifi_instance = QIFI(app.name, *config)
            result = self.detect_if_exist()
            if result:
                self._reload(app.name)
                self.app.logger.info("账户已经恢复")
        except ImportError:
            raise TypeError("你使用了qifi支持，但是似乎你没有安装qifiaccount, 请执行pip install qifiaccount，然后重新运行")

    def detect_if_exist(self) -> bool:
        return self.qifi_instance.db.account.find_one(
            {'account_cookie': self.qifi_instance.user_id, 'password': self.qifi_instance.password}) is not None

    def _reload(self, name):
        message = self.qifi_instance.db.account.find_one(
            {'account_cookie': self.qifi_instance.user_id, 'password': self.qifi_instance.password})

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
            self.qifi_instance.money = message.get('money')
            self.qifi_instance.source_id = message.get('sourceid')

            self.qifi_instance.pre_balance = accpart.get('pre_balance')
            self.qifi_instance.deposit = accpart.get('deposit')
            self.qifi_instance.withdraw = accpart.get('withdraw')
            self.qifi_instance.withdrawQuota = accpart.get('WithdrawQuota')
            self.qifi_instance.close_profit = accpart.get('close_profit')
            self.qifi_instance.static_balance = accpart.get('static_balance')
            self.qifi_instance.event = message.get('event')
            self.qifi_instance.trades = message.get('trades')
            self.qifi_instance.transfers = message.get('transfers')
            self.qifi_instance.orders = message.get('orders')
            self.qifi_instance.taskid = message.get('taskid', str(uuid.uuid4()))

            positions = message.get('positions')
            for position in positions.values():
                self.qifi_instance.positions[position.get('instrument_id')] = position

            self.banks = message.get('banks')

            self.status = message.get('status')
            self.wsuri = message.get('wsuri')

            if message.get('trading_day', '') == str(self.trading_day):
                # reload
                pass

    def from_(self, account: AccountData, orders: List[OrderData], deals: List[TradeData]):
        """ 从数据中导入 """

    def insert_trade(self, trade):
        """ 插入成交单　"""
        self.qifi_instance.trades[trade.local_trade_id] = trade

    def insert_order(self, order):
        """ 创建order注意需要按照顺序进行插入 """
        self.qifi_instance.orders[order.local_order_id] = order

    def cancel(self, order_id):
        """　撤单　"""
        try:
            self.qifi_instance.orders.pop(order_id)
        except IndexError:
            self.app.logger.warning("撤单不存在,已经被撤或者已经成交ｋ")

    def update(self):
        """更新到mongodb数据库中"""
        self.qifi_instance.db.account.update(
            {'account_cookie': self.qifi_instance.user_id, 'password': self.qifi_instance.password}, {
                '$set': self.qifi_instance.to_dict()}, upsert=True)
        self.qifi_instance.db.hisaccount.insert_one(
            {'updatetime': self.now, 'account_cookie': self.qifi_instance.user_id,
             'accounts': self.qifi_instance.account_msg})

    @property
    def now(self):
        return datetime.datetime.now().replace(".", "_")
