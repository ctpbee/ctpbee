from datetime import datetime
from typing import Set, List

from ctpbee.constant import EVENT_INIT_FINISHED, EVENT_TICK, EVENT_BAR, EVENT_ORDER, EVENT_SHARED, EVENT_TRADE, \
    EVENT_POSITION, EVENT_ACCOUNT, EVENT_CONTRACT, EVENT_LOG, OrderData, SharedData, BarData, TickData, TradeData, \
    PositionData, AccountData, ContractData, LogData

from ctpbee.event_engine.engine import EVENT_TIMER, Event


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
        self.instrument_set: List or Set = set()
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

    def on_init(self, init: bool):
        raise NotImplemented

    def on_realtime(self, timed: datetime):
        pass

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
            EVENT_LOG: cls.on_log

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
        self.instrument_set: List or Set = set()
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

    async def on_init(self, init: bool):
        raise NotImplemented

    async def on_realtime(self, timed: datetime):
        pass

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
            EVENT_LOG: cls.on_log

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
            EVENT_LOG: EVENT_LOG
        }
        setattr(cls, "map", map)
        setattr(cls, "parmeter", parmeter)


class Action:
    """
    自定义的Action动作模板
    此动作应该被ctpbee
    """

    print("")


