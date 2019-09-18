import inspect
from datetime import datetime
from types import MethodType
from typing import Set, List, AnyStr, Text
from warnings import warn

from ctpbee.constant import EVENT_INIT_FINISHED, EVENT_TICK, EVENT_BAR, EVENT_ORDER, EVENT_SHARED, EVENT_TRADE, \
    EVENT_POSITION, EVENT_ACCOUNT, EVENT_CONTRACT, OrderData, SharedData, BarData, TickData, TradeData, \
    PositionData, AccountData, ContractData, Offset, Direction, OrderType, Exchange
from ctpbee.event_engine.engine import EVENT_TIMER, Event
from ctpbee.exceptions import ConfigError
from ctpbee.func import helper
from ctpbee.helpers import check


class Action(object):
    """
    自定义的操作模板
    此动作应该被CtpBee, CtpbeeApi, AsyncAp i, RiskLevel调用
    """

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        setattr(instance, "__name__", cls.__name__)
        return instance

    def __getattr__(self, item):
        message = f"尝试在{self.__name__}中调用一个不存在的属性{item}"
        warn(message)
        return None

    def add_risk_check(self, func):
        """ 添加风控函数 """
        if self.app is None or self.app.risk_decorator is None:
            raise AttributeError("app为None, 不可添加风控函数")
        if inspect.ismethod(func) or inspect.isfunction(func):
            setattr(self, func.__name__, self.app.risk_decorator(func))
            return
        raise ValueError(f"请确保传入的func 类型为函数, 当前传入参数类型为{type(func)}")

    @property
    def action(self):
        return self.app.action

    @property
    def recorder(self):
        return self.app.recorder

    @property
    def logger(self):
        return self.app.logger

    def warning(self, msg, **kwargs):
        self.logger.warning(msg, owner=self.__name__, **kwargs)

    def info(self, msg, **kwargs):
        self.logger.info(msg, owner=self.__name__, **kwargs)

    def error(self, msg, **kwargs):
        self.logger.error(msg, owner=self.__name__, **kwargs)

    def debug(self, msg, **kwargs):
        self.logger.debug(msg, owner=self.__name__, **kwargs)

    def __init__(self, app=None):
        self.app = app

    def buy(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData, PositionData],
            price_type: OrderType = "LIMIT", stop: bool = False, lock: bool = False, **kwargs):
        """
        开仓 多头
        """

        if not isinstance(self.app.config['SLIPPAGE_BUY'], float) and not isinstance(
                self.app.config['SLIPPAGE_BUY'], int):
            raise ConfigError(message="滑点配置应为浮点小数或者整数")
        price = price + self.app.config['SLIPPAGE_BUY']
        req = helper.generate_order_req_by_var(volume=volume, price=price, offset=Offset.OPEN, direction=Direction.LONG,
                                               type=OrderType.LIMIT, exchange=origin.exchange, symbol=origin.symbol)
        return self.send_order(req)

    def short(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData, PositionData],
              stop: bool = False, lock: bool = False, **kwargs):
        """
         开仓 空头
        """

        if not isinstance(self.app.config['SLIPPAGE_SHORT'], float) and not isinstance(
                self.app.config['SLIPPAGE_SHORT'], int):
            raise ConfigError(message="滑点配置应为浮点小数")
        price = price + self.app.config['SLIPPAGE_SHORT']
        req = helper.generate_order_req_by_var(volume=volume, price=price, offset=Offset.OPEN,
                                               direction=Direction.SHORT,
                                               type=OrderType.LIMIT, exchange=origin.exchange, symbol=origin.symbol)
        return self.send_order(req)

    def sell(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData] = None,
             stop: bool = False, lock: bool = False, **kwargs):
        """ 平空头 """
        if not isinstance(self.app.config['SLIPPAGE_SELL'], float) and not isinstance(
                self.app.config['SLIPPAGE_SELL'], int):
            raise ConfigError(message="滑点配置应为浮点小数")
        price = price + self.app.config['SLIPPAGE_SELL']
        req_list = [helper.generate_order_req_by_var(volume=x[1], price=price, offset=x[0], direction=Direction.LONG,
                                                     type=OrderType.LIMIT, exchange=origin.exchange,
                                                     symbol=origin.symbol) for x in
                    self.get_req(origin.local_symbol, Direction.SHORT, volume, self.app)]
        return [self.send_order(req) for req in req_list if req.volume != 0]

    def cover(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData, PositionData],
              stop: bool = False, lock: bool = False, **kwargs):
        """
        平多头
        """
        if not isinstance(self.app.config['SLIPPAGE_COVER'], float) and not isinstance(
                self.app.config['SLIPPAGE_COVER'], int):
            raise ConfigError(message="滑点配置应为浮点小数")
        price = price + self.app.config['SLIPPAGE_COVER']
        req_list = [helper.generate_order_req_by_var(volume=x[1], price=price, offset=x[0], direction=Direction.SHORT,
                                                     type=OrderType.LIMIT, exchange=origin.exchange,
                                                     symbol=origin.symbol) for x in
                    self.get_req(origin.local_symbol, Direction.LONG, volume, self.app)]
        return [self.send_order(req) for req in req_list if req.volume != 0]

    def cancel(self, id: Text, origin: [BarData, TickData, TradeData, OrderData, PositionData] = None, **kwargs):
        if "." in id:
            orderid = id.split(".")[1]
        if origin is None:
            exchange = kwargs.get("exchange")
            if isinstance(exchange, Exchange):
                exchange = exchange.value
            local_symbol = kwargs.get("local_symbol")
        elif origin:
            exchange = origin.exchange.value
            local_symbol = origin.local_symbol

        if origin is None and len(kwargs) == 0:
            """ 如果两个都不传"""
            order = self.app.recorder.get_order(id)
            if not order:
                print("找不到订单啦... 撤不了哦")
                return None
            exchange = order.exchange.value
            local_symbol = order.local_symbol

        req = helper.generate_cancel_req_by_str(order_id=orderid, exchange=exchange, symbol=local_symbol)
        return self.cancel_order(req)

    @staticmethod
    def get_req(local_symbol, direction, volume: int, app) -> List:
        """
        generate the offset and volume
        生成平仓所需要的offset和volume
         """

        def cal_req(position, volume, app) -> List:
            # 判断是否为上期所或者能源交易所 / whether the exchange is SHFE or INE
            if position.exchange.value not in app.config["TODAY_EXCHANGE"]:
                return [[Offset.CLOSE, volume]]

            if app.config["CLOSE_PATTERN"] == "today":
                # 那么先判断今仓数量是否满足volume /
                td_volume = position.volume - position.yd_volume
                if td_volume >= volume:
                    return [[Offset.CLOSETODAY, volume]]
                else:
                    return [[Offset.CLOSETODAY, td_volume],
                            [Offset.CLOSEYESTERDAY, volume - td_volume]] if td_volume != 0 else [
                        [Offset.CLOSEYESTERDAY, volume]]

            elif app.config["CLOSE_PATTERN"] == "yesterday":
                if position.yd_volume >= volume:
                    """如果昨仓数量要大于或者等于需要平仓数目 那么直接平昨"""
                    return [[Offset.CLOSEYESTERDAY, volume]]
                else:
                    """如果昨仓数量要小于需要平仓数目 那么优先平昨再平今"""
                    return [[Offset.CLOSEYESTERDAY, position.yd_volume],
                            [Offset.CLOSETODAY, volume - position.yd_volume]] if position.yd_volume != 0 else [
                        [Offset.CLOSETODAY, volume]]
            else:
                raise ValueError("异常配置, ctpbee只支持today和yesterday两种优先模式")

        position: PositionData = app.recorder.position_manager.get_position_by_ld(local_symbol, direction)
        if not position:
            msg = f"{local_symbol}在{direction.value}上无仓位"
            warn(msg)
            return []
        if position.volume < volume:
            msg = f"{local_symbol}在{direction.value}上仓位不足, 平掉当前 {direction.value} 的所有持仓, 平仓数量: {position.volume}"
            warn(msg)
            return cal_req(position, position.volume, app)
        else:
            return cal_req(position, volume, app)

    # 默认四个提供API的封装, 买多卖空等快速函数应该基于send_order进行封装 / default to provide four function
    @check(type="trader")
    def send_order(self, order, **kwargs):
        return self.app.trader.send_order(order, **kwargs)

    @check(type="trader")
    def cancel_order(self, cancel_req, **kwargs):
        return self.app.trader.cancel_order(cancel_req, **kwargs)

    @check(type="trader")
    def query_position(self):
        return self.app.trader.query_position()

    @check(type="trader")
    def query_account(self):
        return self.app.trader.query_account()

    @check(type="trader")
    def transfer(self, req, type):
        """
        req currency attribute
        ["USD", "HKD", "CNY"]
        :param req:
        :param type:
        :return:
        """
        return self.app.trader.transfer(req, type=type)

    @check(type="trader")
    def query_account_register(self, req):
        self.app.trader.query_account_register(req)

    @check(type="trader")
    def query_bank_account_money(self, req):
        self.app.trader.query_bank_account_money(req)

    @check(type="trader")
    def query_transfer_serial(self, req):
        self.trader.query_transfer_serial(req)

    @check(type="trader")
    def query_bank(self):
        pass

    @check(type="market")
    def subscribe(self, local_symbol: AnyStr):
        """订阅行情"""
        if "." in local_symbol:
            local_symbol = local_symbol.split(".")[0]
        return self.app.market.subscribe(local_symbol)

    def __repr__(self):
        return f"{self.__name__} "


class CtpbeeApi(object):
    """
    数据模块/策略模块 都是基于此实现的
        如果你要开发上述插件需要继承此抽象demo
        usage:
        ## coding:
            class Processor(CtpbeeApi):
                ...

            data_processor = Processor("data_processor", app)
                        or
            data_processor = Processor("data_processor")
            data_processor.init_app(app)
                        or
            app.add_extension(Process("data_processor"))
    """

    def __new__(cls, *args, **kwargs):
        map = {
            EVENT_TIMER: cls.on_realtime,
            EVENT_INIT_FINISHED: cls.on_init,
            EVENT_TICK: cls.on_tick,
            EVENT_BAR: cls.on_bar,
            EVENT_ORDER: cls.on_order,
            EVENT_SHARED: cls.on_shared,
            EVENT_TRADE: cls.on_trade,
            EVENT_POSITION: cls.on_position,
            EVENT_ACCOUNT: cls.on_account,
            EVENT_CONTRACT: cls.on_contract,
        }
        parmeter = {
            EVENT_TIMER: EVENT_TIMER,
            EVENT_INIT_FINISHED: EVENT_INIT_FINISHED,
            EVENT_POSITION: EVENT_POSITION,
            EVENT_TRADE: EVENT_TRADE,
            EVENT_BAR: EVENT_BAR,
            EVENT_TICK: EVENT_TICK,
            EVENT_ORDER: EVENT_ORDER,
            EVENT_SHARED: EVENT_SHARED,
            EVENT_ACCOUNT: EVENT_ACCOUNT,
            EVENT_CONTRACT: EVENT_CONTRACT,
        }
        setattr(cls, "map", map)
        setattr(cls, "parmeter", parmeter)
        return super().__new__(cls)

    def __init__(self, extension_name, app=None):
        """
        init function
        :param name: extension name , 插件名字
        :param app: CtpBee 实例
        """
        self.instrument_set: List or Set = set()
        self.extension_name = extension_name
        self.app = app
        if self.app is not None:
            self.init_app(self.app)
        # 是否冻结
        self.frozen = False

    @property
    def action(self) -> Action:
        if self.app is None:
            raise ValueError("没有载入CtpBee，请尝试通过init_app载入app")
        return self.app.action

    @property
    def logger(self):
        return self.app.logger

    def warning(self, msg, **kwargs):
        self.logger.warning(msg, owner="API: " + self.extension_name, **kwargs)

    def info(self, msg, **kwargs):
        self.logger.info(msg, owner="API: " + self.extension_name, **kwargs)

    def error(self, msg, **kwargs):
        self.logger.error(msg, owner="API: " + self.extension_name, **kwargs)

    def debug(self, msg, **kwargs):
        self.logger.debug(msg, owner="API: " + self.extension_name, **kwargs)

    @property
    def recorder(self):
        if self.app is None:
            raise ValueError("没有载入CtpBee，请尝试通过init_app载入app")
        return self.app.recorder

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

    def on_init(self, init: bool):
        pass

    def on_realtime(self):
        pass

    def init_app(self, app):
        if app is not None:
            self.app = app
            self.app.extensions[self.extension_name] = self

    def route(self, handler):
        """ """
        if handler not in self.map:
            raise TypeError(f"呀， ctpbee暂不支持此函数类型 {handler}, 当前仅支持 {self.map.keys()}")

        def converter(func):
            self.map[handler] = func
            return func

        return converter

    def register(self):
        """ 用于注册函数 """

        def attribute(func):
            funcd = MethodType(func, self)
            setattr(self, func.__name__, funcd)
            return funcd

        return attribute

    def __call__(self, event: Event = None):
        if not event:
            if not self.frozen:
                self.map[EVENT_TIMER](self)
        else:
            func = self.map[event.type]
            if not self.frozen:
                func(self, event.data)


class AsyncApi(object):
    """
    数据模块
    策略模块
        如果你要开发上述插件需要继承此抽象demo
    AsyncApi ---> 性能优化
    """

    def __new__(cls, *args, **kwargs):
        map = {
            EVENT_TIMER: cls.on_realtime,
            EVENT_INIT_FINISHED: cls.on_init,
            EVENT_TICK: cls.on_tick,
            EVENT_BAR: cls.on_bar,
            EVENT_ORDER: cls.on_order,
            EVENT_SHARED: cls.on_shared,
            EVENT_TRADE: cls.on_trade,
            EVENT_POSITION: cls.on_position,
            EVENT_ACCOUNT: cls.on_account,
            EVENT_CONTRACT: cls.on_contract,
        }
        parmeter = {
            EVENT_TIMER: EVENT_TIMER,
            EVENT_INIT_FINISHED: EVENT_INIT_FINISHED,
            EVENT_POSITION: EVENT_POSITION,
            EVENT_TRADE: EVENT_TRADE,
            EVENT_BAR: EVENT_BAR,
            EVENT_TICK: EVENT_TICK,
            EVENT_ORDER: EVENT_ORDER,
            EVENT_SHARED: EVENT_SHARED,
            EVENT_ACCOUNT: EVENT_ACCOUNT,
            EVENT_CONTRACT: EVENT_CONTRACT,
        }
        setattr(cls, "map", map)
        setattr(cls, "parmeter", parmeter)
        return super().__new__(cls)

    def __init__(self, extension_name, app=None):
        """
        init function
        :param name: extension name , 插件名字
        :param app: CtpBee 实例
        :param api_type 针对几种API实行不同的优化措施
        """
        self.extension_name = extension_name
        self.instrument_set: List or Set = set()
        self.app = app
        if self.app is not None:
            self.init_app(self.app)
        # 是否冻结
        self.fronzen = False

    @property
    def action(self):
        if self.app is None:
            raise ValueError("没有载入CtpBee，请尝试通过init_app载入app")
        return self.app.action

    @property
    def recorder(self):
        if self.app is None:
            raise ValueError("没有载入CtpBee，请尝试通过init_app载入app")
        return self.app.recorder

    @property
    def logger(self):
        if self.app is None:
            raise ValueError("没有载入CtpBee，请尝试通过init_app载入app")
        return self.app.logger

    def warning(self, msg, **kwargs):
        self.logger.warning(msg, owner="API: " + self.extension_name, **kwargs)

    def info(self, msg, **kwargs):
        self.logger.info(msg, owner="API: " + self.extension_name, **kwargs)

    def error(self, msg, **kwargs):
        self.logger.error(msg, owner="API: " + self.extension_name, **kwargs)

    def debug(self, msg, **kwargs):
        self.logger.debug(msg, owner="API: " + self.extension_name, **kwargs)

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

    async def on_init(self, init: bool):
        pass

    async def on_realtime(self, timed: datetime):
        pass

    def route(self, handler):
        """ """
        if handler not in self.map:
            raise TypeError(f"呀， ctpbee暂不支持此函数类型 {handler}")

        def converter(func):
            self.map[handler] = func
            return func

        return converter

    def register(self):
        """ 用于注册函数 """

        def attribute(func):
            funcd = MethodType(func, self)
            setattr(self, func.__name__, funcd)
            return funcd

        return attribute

    def init_app(self, app):
        if app is not None:
            self.app = app
            self.app.extensions[self.extension_name] = self

    async def __call__(self, event: Event):
        if not event:
            if not self.frozen:
                await self.map[EVENT_TIMER](self)
        else:
            func = self.map[event.type]
            if not self.frozen:
                await func(self, event.data)
