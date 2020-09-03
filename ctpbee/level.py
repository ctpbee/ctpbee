import inspect
import os
import sys
import types
from functools import partial
from types import MethodType
from typing import Set, List, AnyStr, Text
from warnings import warn

from ctpbee.constant import EVENT_INIT_FINISHED, EVENT_TICK, EVENT_BAR, EVENT_ORDER, EVENT_SHARED, EVENT_TRADE, \
    EVENT_POSITION, EVENT_ACCOUNT, EVENT_CONTRACT, OrderData, SharedData, BarData, TickData, TradeData, \
    PositionData, AccountData, ContractData, Offset, Direction, OrderType, Exchange
from ctpbee.data_handle.level_position import ApiPositionManager
from ctpbee.constant import EVENT_TIMER, Event
from ctpbee.exceptions import ConfigError
from ctpbee.func import helper, get_ctpbee_path
from ctpbee.helpers import check, exec_intercept


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
    def center(self):
        return self.app.center

    @property
    def recorder(self):
        return self.app.recorder

    @property
    def logger(self):
        return self.app.logger

    def warning(self, msg, **kwargs):
        kwargs.update(dict(owner=self.__name__))
        self.logger.warning(msg, **kwargs)

    def info(self, msg, **kwargs):
        kwargs.update(dict(owner=self.__name__))
        self.logger.info(msg, **kwargs)

    def error(self, msg, **kwargs):
        kwargs.update(dict(owner=self.__name__))
        self.logger.error(msg, **kwargs)

    def debug(self, msg, **kwargs):
        kwargs.update(dict(owner=self.__name__))
        self.logger.debug(msg, **kwargs)

    def __init__(self, app=None):
        self.app = app

    def cancel_all(self):
        """ 撤掉所有的报单信息 """
        for order in self.app.center.active_orders:
            self.cancel(order.order_id, order)

    def close_all(self):
        """ 平全部仓位
        API 需要进行一个大的ct
        """
        raise ValueError("此API 暂时未被启用， 将在1.3.1启用")

    def buy(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData, PositionData],
            price_type: OrderType = OrderType.LIMIT, stop: bool = False, lock: bool = False, **kwargs):
        """
        开仓 多头
        """

        if not isinstance(self.app.config['SLIPPAGE_BUY'], float) and not isinstance(
                self.app.config['SLIPPAGE_BUY'], int):
            raise ConfigError(message="滑点配置应为浮点小数或者整数")
        price = price + self.app.config['SLIPPAGE_BUY']
        req = helper.generate_order_req_by_var(volume=volume, price=price, offset=Offset.OPEN, direction=Direction.LONG,
                                               type=price_type, exchange=origin.exchange, symbol=origin.symbol)
        return self.send_order(req)

    def short(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData, PositionData],
              price_type: OrderType = OrderType.LIMIT, stop: bool = False, lock: bool = False, **kwargs):
        """
         开仓 空头
        """

        if not isinstance(self.app.config['SLIPPAGE_SHORT'], float) and not isinstance(
                self.app.config['SLIPPAGE_SHORT'], int):
            raise ConfigError(message="滑点配置应为浮点小数")
        price = price - self.app.config['SLIPPAGE_SHORT']
        req = helper.generate_order_req_by_var(volume=volume, price=price, offset=Offset.OPEN,
                                               direction=Direction.SHORT,
                                               type=price_type, exchange=origin.exchange, symbol=origin.symbol)
        return self.send_order(req)

    def sell(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData] = None,
             price_type: OrderType = OrderType.LIMIT, stop: bool = False, lock: bool = False, **kwargs):
        """
        平空头
        """
        if not isinstance(self.app.config['SLIPPAGE_SELL'], float) and not isinstance(
                self.app.config['SLIPPAGE_SELL'], int):
            raise ConfigError(message="滑点配置应为浮点小数")
        price = price + self.app.config['SLIPPAGE_SELL']
        req_list = [helper.generate_order_req_by_var(volume=x[1], price=price, offset=x[0], direction=Direction.LONG,
                                                     type=price_type, exchange=origin.exchange,
                                                     symbol=origin.symbol) for x in
                    self.get_req(origin.local_symbol, Direction.SHORT, volume, self.app)]
        return [self.send_order(req) for req in req_list if req.volume != 0]

    def cover(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData, PositionData],
              price_type: OrderType = OrderType.LIMIT, stop: bool = False, lock: bool = False, **kwargs):
        """
        平多头
        """
        if not isinstance(self.app.config['SLIPPAGE_COVER'], float) and not isinstance(
                self.app.config['SLIPPAGE_COVER'], int):
            raise ConfigError(message="滑点配置应为浮点小数")
        price = price - self.app.config['SLIPPAGE_COVER']
        req_list = [helper.generate_order_req_by_var(volume=x[1], price=price, offset=x[0], direction=Direction.SHORT,
                                                     type=price_type, exchange=origin.exchange,
                                                     symbol=origin.symbol) for x in
                    self.get_req(origin.local_symbol, Direction.LONG, volume, self.app)]
        return [self.send_order(req) for req in req_list if req.volume != 0]

    def cancel(self, id: Text, origin: [BarData, TickData, TradeData, OrderData, PositionData] = None, **kwargs):
        if "." in id:
            orderid = id.split(".")[1]
        else:
            orderid = id
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
            try:
                exchange = order.exchange.value
            except AttributeError:
                exchange = order.exchange
            local_symbol = order.local_symbol
        req = helper.generate_cancel_req_by_str(order_id=orderid, exchange=exchange, symbol=local_symbol)
        return self.cancel_order(req)

    @staticmethod
    def get_req(local_symbol, direction, volume, app) -> List:
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
                raise ValueError("bad config, ctpbee just on support today and yesterday")

        position: PositionData = app.recorder.position_manager.get_position_by_ld(local_symbol, direction)
        if not position:
            msg = f"{local_symbol}在{direction.value}上无仓位"
            warn(msg)
            return []
        if position.volume < volume:
            msg = f"{local_symbol} position at {direction.value} is not enough, close all the {direction.value} position, close count: {position.volume}"
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


class ActionProxy:
    def __init__(self, action, api):
        self.action = action
        self.api = api

    def __getattr__(self, item):
        callable_func = exec_intercept(self=self, func=getattr(self.action, item))
        return callable_func


class BeeApi(object):
    def resolve_callback(self, item, result):
        """
        处理回调函数
        * item: 操作项
        * result: 执行结果
        """
        pass


class CtpbeeApi(BeeApi):
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

    def __call__(self, event: Event = None):
        # 特别处理两种情况

        if event and event.type == EVENT_ORDER:
            if event.data.local_order_id in self.order_id_mapping:
                self.level_position_manager.on_order(event.data)
        if event and event.type == EVENT_TRADE:
            """如果发现单号是已经存进来的"""
            if event.data.local_order_id in self.order_id_mapping:
                self.level_position_manager.on_trade(event.data)

        if not event:
            if not self.frozen:
                self.map[EVENT_TIMER](self)
        else:
            if event and not self.frozen and (event.type == EVENT_TICK or event.type == EVENT_BAR) and len(
                    self.func) != 0:
                args = list(self.func[0][2])
                if event.type == self.func[0][1]:
                    """ 如果数据类型"""
                    args.insert(0, event.data)
                    result = self.func[0][0](*args)
                    if result == self.complete:
                        self.func.clear()
                    return None
            func = self.map[event.type]
            if not self.frozen:
                func(self, event.data)

    @property
    def complete(self):
        """ 结束当前任务 """
        return "end"

    def run_until_complete(self, target=None, *args, typed=EVENT_TICK):
        """ 越过函数检查， 进行循环判断,  目前只支持单步队列
        """
        self.func.clear()
        if not isinstance(target, types.MethodType) and not isinstance(target, types.FunctionType):
            raise TypeError("target参数类型应该为一个函数")
        self.func.append((target, typed, *args))

    def __init__(self, extension_name, app=None, **kwargs):
        """
        init function
        :param name: extension name , 插件名字
        :param app: CtpBee 实例
        """
        self.instrument_set: List or Set = set()
        self.extension_name = extension_name
        self.app = app
        self.func = []
        init = False
        if self.app is not None:
            self.init_app(self.app)
        # 是否冻结
        self.frozen = False
        if "cache_path" in kwargs:
            self.path = kwargs.get("cache_path")
            if not os.path.isdir(self.path):
                raise ValueError("请填写正确的缓存绝对路径")
        else:
            self.path = get_ctpbee_path()
        init = kwargs.get("init_position")
        if init and not isinstance(init, bool):
            raise TypeError(f"init参数应该设置为True或者False，而不是{type(init)}")

        # 单号如
        self.order_id_mapping = {}

        self.api_path = self.get_dir(self.path)
        self.level_position_manager = ApiPositionManager(self.extension_name, self.api_path, init)

    def resolve_callback(self, item, result):
        """
        处理回调函数
        * item: 操作项
        * result: 执行结果
        """

        # 买多卖空
        if item == "buy" or item == "short":
            self.order_id_mapping.setdefault(result, False)
        # 平多平空
        elif item == "sell" or item == "cover":
            for i in result:
                self.order_id_mapping.setdefault(i, False)

    @staticmethod
    def get_dir(path):
        """
        获取API专属的文件夹的路径
        如果不存在就创建
        """
        path = os.path.join(path, "api")
        if not os.path.isdir(path):
            os.mkdir(path)
        return path

    @property
    def action(self):
        if self.app is None:
            raise ValueError("没有载入CtpBee，请尝试通过init_app载入app")
        return ActionProxy(self.app.action, self)

    @property
    def center(self):
        if self.app is None:
            raise ValueError("没有载入CtpBee，请尝试通过init_app载入app")
        return self.app.center

    @property
    def logger(self):
        return self.app.logger

    def warning(self, msg, **kwargs):
        kwargs['owner'] = "API: " + self.extension_name
        self.logger.warning(msg, **kwargs)

    def info(self, msg, **kwargs):
        kwargs['owner'] = "API: " + self.extension_name
        self.logger.info(msg, **kwargs)

    def error(self, msg, **kwargs):
        kwargs['owner'] = "API: " + self.extension_name
        self.logger.error(msg, **kwargs)

    def debug(self, msg, **kwargs):
        kwargs['owner'] = "API: " + self.extension_name
        self.logger.debug(msg, **kwargs)

    @property
    def recorder(self):
        if self.app is None:
            raise ValueError("没有载入CtpBee，请尝试通过init_app载入app")
        return self.app.recorder

    def get_strategy(self, strategy_name):
        return self.app.get_extension(strategy_name)

    def on_order(self, order: OrderData) -> None:
        pass

    def on_bar(self, bar: BarData) -> None:
        raise NotImplemented

    def on_tick(self, tick: TickData) -> None:
        raise NotImplemented

    def on_trade(self, trade: TradeData) -> None:
        pass

    def on_position(self, position: PositionData) -> None:
        pass

    def on_account(self, account: AccountData) -> None:
        pass

    def on_contract(self, contract: ContractData):
        pass

    def on_init(self, init: bool):
        pass

    def on_realtime(self):
        pass

    def init_app(self, app):
        if app is not None:
            self.app = app
            self.app._extensions[self.extension_name] = self

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
