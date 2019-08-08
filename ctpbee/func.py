"""

面向用户的函数 ,提供极其便捷的体验

"""
from datetime import time
from typing import Text

from ctpbee.constant import \
    (OrderRequest, CancelRequest, EVENT_TRADE, EVENT_SHARED, EVENT_ORDER,
     OrderData, TradeData, PositionData, AccountData, TickData, SharedData,
     BarData, EVENT_POSITION, EVENT_ACCOUNT, EVENT_TICK, EVENT_BAR, EVENT_CONTRACT, ContractData, Direction, Exchange,
     Offset, OrderType, AccountRegisterRequest, AccountBanlanceRequest, TransferRequest, TransferSerialRequest, LogData,
     EVENT_LOG)
from ctpbee.context import current_app
from ctpbee.context import get_app
from ctpbee.event_engine import Event
from ctpbee.exceptions import TraderError, MarketError
from ctpbee.signals import send_monitor, cancle_monitor


def send_order(order_req: OrderRequest, app_name: str = "current_app"):
    """ 发单 """
    if app_name == "current_app":
        app = current_app
    else:
        app = get_app(app_name)
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    send_monitor.send(order_req)
    return app.trader.send_order(order_req)


def cancle_order(cancle_req: CancelRequest, app_name: str = "current_app"):
    """ 撤单 """
    if app_name == "current_app":
        app = current_app
    else:
        app = get_app(app_name)
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    cancle_monitor.send(cancle_req)
    app.trader.cancel_order(cancle_req)


def subscribe(symbol: Text, app_name: str = "current_app") -> None:
    """订阅"""
    if app_name == "current_app":
        app = current_app
    else:
        app = get_app(app_name)
    if not app.config.get("MD_FUNC"):
        raise MarketError(message="行情功能未开启, 无法进行订阅")
    app.market.subscribe(symbol)


def query_func(type: Text, app_name: str = "current_app") -> None:
    """查询持仓 or 账户"""
    if app_name == "current_app":
        app = current_app
    else:
        app = get_app(app_name)
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    if type == "position":
        app.trader.query_position()
    if type == "account":
        app.trader.query_account()


class CtpbeeApi(object):
    """
    数据模块
    策略模块
        如果你要开发上述插件需要继承此抽象demo
        usage:
        ## coding:
            class Processor(ApiAbstract):
                ...

            data_processor = Processor("data_processor", app)
                        or
            data_processor = Processor("data_processor")
            data_processor.init_app(app)
    """

    def __init__(self, extension_name, app=None):
        """
        init function
        :param name: extension name , 插件名字
        :param app: CtpBee 实例
        :param api_type 针对几种API实行不同的优化措施
        """
        self.extension_name = extension_name
        self.app = app
        if self.app is not None:
            self.init_app(self.app)
        # 是否冻结
        self.fronzen = False

    def on_order(self, order: OrderData) -> None:
        raise NotImplemented

    def on_shared(self, shared: SharedData) -> None:
        raise NotImplemented

    def on_bar(self, bar: BarData) -> None:
        raise NotImplemented

    def on_tick(self, tick: TickData) -> None:
        raise NotImplemented

    def on_trade(self, trade: TradeData) -> None:
        raise NotImplemented

    def on_position(self, position: PositionData) -> None:
        raise NotImplemented

    def on_account(self, account: AccountData) -> None:
        raise NotImplemented

    def on_contract(self, contract: ContractData):
        raise NotImplemented

    def on_log(self, log: LogData):
        raise NotImplemented

    def init_app(self, app):
        if app is not None:
            self.app = app
            self.app.extensions[self.extension_name] = self

    def __call__(self, event: Event):
        func = self.map[event.type]
        if not self.fronzen:
            func(self, event.data)

    def __init_subclass__(cls, **kwargs):
        map = {
            EVENT_TICK: cls.on_tick,
            EVENT_BAR: cls.on_bar,
            EVENT_ORDER: cls.on_order,
            EVENT_SHARED: cls.on_shared,
            EVENT_TRADE: cls.on_trade,
            EVENT_POSITION: cls.on_position,
            EVENT_ACCOUNT: cls.on_account,
            EVENT_CONTRACT: cls.on_contract,
            EVENT_LOG: cls.on_log

        }
        parmeter = {
            EVENT_POSITION: EVENT_POSITION,
            EVENT_TRADE: EVENT_TRADE,
            EVENT_BAR: EVENT_BAR,
            EVENT_TICK: EVENT_TICK,
            EVENT_ORDER: EVENT_ORDER,
            EVENT_SHARED: EVENT_SHARED,
            EVENT_ACCOUNT: EVENT_ACCOUNT,
            EVENT_CONTRACT: EVENT_CONTRACT,
            EVENT_LOG: EVENT_LOG
        }
        setattr(cls, "map", map)
        setattr(cls, "parmeter", parmeter)


class AsyncApi(object):
    """
    数据模块
    策略模块
        如果你要开发上述插件需要继承此抽象demo
    AsyncApi ---> 性能优化
    """

    def __init__(self, extension_name, app=None):
        """
        init function
        :param name: extension name , 插件名字
        :param app: CtpBee 实例
        :param api_type 针对几种API实行不同的优化措施
        """
        self.extension_name = extension_name
        self.app = app
        if self.app is not None:
            self.init_app(self.app)
        # 是否冻结
        self.fronzen = False

    async def on_order(self, order: OrderData) -> None:
        raise NotImplemented

    async def on_shared(self, shared: SharedData) -> None:
        raise NotImplemented

    async def on_bar(self, bar: BarData) -> None:
        raise NotImplemented

    async def on_tick(self, tick: TickData) -> None:
        raise NotImplemented

    async def on_trade(self, trade: TradeData) -> None:
        raise NotImplemented

    async def on_position(self, position: PositionData) -> None:
        raise NotImplemented

    async def on_account(self, account: AccountData) -> None:
        raise NotImplemented

    async def on_contract(self, contract: ContractData):
        raise NotImplemented

    async def on_log(self, log: LogData):
        raise NotImplemented

    def init_app(self, app):
        if app is not None:
            self.app = app
            self.app.extensions[self.extension_name] = self

    async def __call__(self, event: Event):
        func = self.map[event.type]
        if not self.fronzen:
            await func(self, event.data)

    def __init_subclass__(cls, **kwargs):
        map = {
            EVENT_TICK: cls.on_tick,
            EVENT_BAR: cls.on_bar,
            EVENT_ORDER: cls.on_order,
            EVENT_SHARED: cls.on_shared,
            EVENT_TRADE: cls.on_trade,
            EVENT_POSITION: cls.on_position,
            EVENT_ACCOUNT: cls.on_account,
            EVENT_CONTRACT: cls.on_contract,
            EVENT_LOG: cls.on_log

        }
        parmeter = {
            EVENT_POSITION: EVENT_POSITION,
            EVENT_TRADE: EVENT_TRADE,
            EVENT_BAR: EVENT_BAR,
            EVENT_TICK: EVENT_TICK,
            EVENT_ORDER: EVENT_ORDER,
            EVENT_SHARED: EVENT_SHARED,
            EVENT_ACCOUNT: EVENT_ACCOUNT,
            EVENT_CONTRACT: EVENT_CONTRACT,
            EVENT_LOG: EVENT_LOG
        }
        setattr(cls, "map", map)
        setattr(cls, "parmeter", parmeter)


class Helper():
    """ 工具函数 帮助你快速构建查询请求 """
    direction_map = {
        "LONG": Direction.LONG,
        "SHORT": Direction.SHORT,
    }
    exchange_map = {
        "SHFE": Exchange.SHFE,
        "INE": Exchange.INE,
        "CZCE": Exchange.CZCE,
        "CFFEX": Exchange.CFFEX,
        "DCE": Exchange.DCE,
    }

    offset_map = {
        "CLOSE": Offset.CLOSE,
        "OPEN": Offset.OPEN,
        "CLOSETODAY": Offset.CLOSETODAY,
        "CLOSEYESTERDAY": Offset.CLOSEYESTERDAY
    }

    price_type_map = {
        "MARKET": OrderType.MARKET,
        "STOP": OrderType.STOP,
        "FAK": OrderType.FAK,
        "LIMIT": OrderType.LIMIT,
        "FOK": OrderType.FOK
    }

    @classmethod
    def generate_order_req_by_str(cls, symbol: str, exchange: str, direction: str, offset: str, type: str, volume,
                                  price):
        """ 手动构造发单请求"""
        if "." in symbol:
            symbol = symbol.split(".")[1]

        return OrderRequest(exchange=cls.exchange_map.get(exchange.upper()), symbol=symbol,
                            direction=cls.direction_map.get(direction.upper()),
                            offset=cls.offset_map.get(offset.upper()), type=cls.price_type_map.get(type.upper()),
                            volume=volume, price=price)

    @classmethod
    def generate_order_req_by_var(cls, symbol: str, exchange: Exchange, direction: Direction, offset: Offset,
                                  type: OrderType, volume, price):
        if "." in symbol:
            symbol = symbol.split(".")[1]
        return OrderRequest(symbol=symbol, exchange=exchange, direction=direction, offset=offset, type=type,
                            volume=volume, price=price)

    @classmethod
    def generate_cancle_req_by_str(cls, symbol: str, exchange: str, order_id: str):
        if "." in symbol:
            symbol = symbol.split(".")[1]
        return CancelRequest(symbol=symbol, exchange=cls.exchange_map.get(exchange), order_id=order_id)

    @classmethod
    def generate_cancle_req_by_var(cls, symbol: str, exchange: Exchange, order_id: str):
        if "." in symbol:
            symbol = symbol.split(".")[1]
        return CancelRequest(symbol=symbol, exchange=exchange, order_id=order_id)

    @classmethod
    def generate_ac_register_req(cls, bank_id, currency_id="CNY"):

        return AccountRegisterRequest(bank_id=bank_id, currency_id=currency_id)

    @classmethod
    def generate_ac_banlance_req(cls, bank_id, bank_account, bank_password,
                                 currency_id="CNY"):
        return AccountBanlanceRequest(bank_id=bank_id, bank_account=bank_account, bank_password=bank_password,
                                      currency_id=currency_id)

    @classmethod
    def generate_transfer_request(cls, bank_id, bank_account, bank_password,
                                  trade_account, currency_id="CNY"):
        return TransferRequest(bank_id=bank_id, bank_account=bank_account, band_password=bank_password,
                               currency_id=currency_id,
                               trade_account=trade_account)

    @classmethod
    def generate_transfer_serial_req(cls, bank_id, currency_id="CNY"):
        return TransferSerialRequest(bank_id=bank_id, currency_id=currency_id)


helper = Helper()


def auth_time(data_time: time):
    """
    校验时间tick或者bar的时间合不合法
    for example:
        data_time = tick.datetime.time()
    """
    if not isinstance(data_time, time):
        raise TypeError("参数类型错误, 期望为datatime.time}")
    DAY_START = time(9, 0)  # 日盘启动和停止时间
    DAY_END = time(15, 0)
    NIGHT_START = time(21, 0)  # 夜盘启动和停止时间
    NIGHT_END = time(2, 30)
    if data_time <= DAY_END and data_time >= DAY_START:
        return True
    if data_time >= NIGHT_START:
        return True
    if data_time <= NIGHT_END:
        return True
    return False
