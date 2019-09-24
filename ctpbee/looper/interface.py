import collections
import random
import uuid

from ctpbee.constant import OrderRequest, Offset, Direction, OrderType, OrderData, CancelRequest, TradeData, BarData, \
    TickData, PositionData
from ctpbee.jsond import dumps
from ctpbee.looper.account import Account
from ctpbee.looper.data import Bumblebee


class Action:
    def __init__(self, looper):
        """ 将action这边报单 """
        self.looper = looper

    def buy(self, price, volume, origin, price_type: OrderType = OrderType.LIMIT, **kwargs):
        req = OrderRequest(price=price, volume=volume, exchange=origin.exchange, offset=Offset.OPEN,
                           direction=Direction.LONG, type=price_type)
        return self.looper.send_order(req)

    def short(self, price, volume, origin, price_type: OrderType = OrderType.LIMIT, **kwargs):
        req = OrderRequest(price=price, volume=volume, exchange=origin.exchange, offset=Offset.OPEN,
                           direction=Direction.SHORT, type=price_type)
        return self.looper.send_order(req)

    @property
    def position(self):
        return self.looper.account.positions

    def sell(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData] = None,
             price_type: OrderType = OrderType.LIMIT, stop: bool = False, lock: bool = False, **kwargs):
        pass

    def cover(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData, PositionData],
              price_type: OrderType = OrderType.LIMIT, stop: bool = False, lock: bool = False, **kwargs):
        pass


class LocalLooper():
    def __init__(self, logger, strategy=None, risk=None):
        """ 需要构建完整的成交回报以及发单报告,在account里面需要存储大量的存储 """

        # 活跃报单数量
        self.pending = collections.deque()

        self.sessionid = random.randint(1000, 10000)
        self.frontid = random.randint(10001, 500000)

        # 日志输出器
        self.logger = logger

        self.strategy = strategy
        # 覆盖里面的action和logger属性
        # 涨跌停价格
        self.upper_price = 9999
        self.drop_price = 0

        # 风控/risk control todo:完善
        self.risk = risk
        self.params = dict(
            deal_pattern="match",
            single_order_limit=10,
            single_day_limit=100,
        )
        # 账户属性
        self.account = Account(self)
        self.order_ref = 0

        # 发单的ref集合
        self.order_ref_set = set()
        # 已经order_id ---- 成交单
        self.traded_order_mapping = {}
        # 已经order_id --- 报单
        self.order_id_pending_mapping = {}

        # 当日成交笔数, 需要如果是第二天的数据，那么需要被清空
        self.today_volume = 0

        # 所有的报单数量
        self.order_buffer = dict()

        # 行情
        self.price = None

    def update_strategy(self, strategy):
        self.strategy = strategy
        setattr(self.strategy, "action", Action(self))
        setattr(self.strategy, "logger", self.logger)
        setattr(self.strategy, "info", self.logger.info)
        setattr(self.strategy, "debug", self.logger.debug)
        setattr(self.strategy, "error", self.logger.error)
        setattr(self.strategy, "warning", self.logger.warning)

    def update_risk(self, risk):
        self.risk = risk

    def _generate_order_data_from_req(self, req: OrderRequest):
        """ 将发单请求转换为发单数据 """
        self.order_ref += 1
        order_id = f"{self.frontid}-{self.sessionid}-{self.order_ref}"
        return req._create_order_data(gateway_name="looper", order_id=order_id)

    def _generate_trade_data_from_order(self, order_data: OrderData):
        """ 将orderdata转换成成交单 """
        p = TradeData(price=order_data.price, istraded=order_data.volume, volume=order_data.volume,
                      trade_id=uuid.uuid1(),
                      gateway_name=order_data.gateway_name, time=order_data.time,
                      order_id=order_data.order_id)
        return p

    def send_order(self, order_req):
        """ 发单的操作"""
        self.intercept_gateway(order_req)

    def cancel(self, cancel_req):
        """ 撤单机制 """
        self.intercept_gateway(cancel_req)

    def intercept_gateway(self, data):
        """ 拦截网关 同时这里应该返回相应的水平"""
        if isinstance(data, OrderRequest):
            """ 发单请求处理 """
            result = self.match_deal(self._generate_order_data_from_req(data))
            if result:
                """ 将成交单通过日志接口暴露出去"""
                self.logger.info(dumps(result))
        if isinstance(data, CancelRequest):
            """ 撤单请求处理 """
            # todo: 处理日志接口

    def match_deal(self, data: OrderData):
        """ 撮合成交 """
        if self.params.get("deal_pattern") == "match":
            """ 撮合成交 """
            # todo: 是否可以模拟一定量的市场冲击响应？ 以靠近更加逼真的回测效果 ？？？？

        elif self.params.get("deal_pattern") == "price":
            """ 见价成交 """
            # 先判断价格和手数是否满足限制条件
            if data.volume > self.params.get("single_order_limit") or self.today_volume > self.params.get(
                    "single_day_limit"):
                """ 超出限制 直接返回不允许成交 """
                return None
            if data.price < self.drop_price or data.price > self.upper_price:
                """ 超出涨跌价格 """
                return None

            # if self.mode == BacktestingMode.BAR:
            #     long_cross_price = self.bar.low_price
            #     short_cross_price = self.bar.high_price
            #     long_best_price = self.bar.open_price
            #     short_best_price = self.bar.open_price
            # else:
            #     long_cross_price = self.tick.ask_price_1
            #     short_cross_price = self.tick.bid_price_1
            #     long_best_price = long_cross_price
            #     short_best_price = short_cross_price

            long_c = self.price.low_price if self.price.low_price is not None else self.price.ask_price_1
            short_c = self.price.high_price if self.price.low_price is not None else self.price.bid_price_1
            long_b = self.price.open_price if self.price.low_price is not None else long_c
            short_b = self.price.open_price if self.price.low_price is not None else short_c
            long_cross = data.direction == Direction.LONG and data.price >= long_c > 0
            short_cross = data.direction == Direction.SHORT and data.price <= short_c and short_c > 0

            for order in self.pending:
                long_cross = data.direction == Direction.LONG and order.price >= long_c > 0
                short_cross = data.direction == Direction.SHORT and order.price <= short_c and short_c > 0
                if not long_cross and not short_cross:
                    """ 不成交 """
                    continue
                if long_cross:
                    order.price = min(order.price, long_b)
                else:
                    order.price = max(order.price, short_b)
                trade = self._generate_trade_data_from_order(order)
                self.strategy.on_trade(trade)

            if not long_cross and not short_cross:
                # 未成交单, 提交到pending里面去
                self.pending.append(data)

            """ 判断账户资金是否足以支撑成交 """
            if self.account.is_traded(data):
                """ 调用API生成成交单 """
                # 同时这里需要处理是否要进行
                p = self._generate_trade_data_from_order(data)
                self.account.update_trade(p)
                """ 调用strategy的on_trade """
                self.strategy.on_trade(p)
                self.today_volume += data.volume
                return p
            else:
                """ 当前账户不足以支撑成交 """
                self.logger.error("资金不足啦!")
                return None
        else:
            raise TypeError("未支持的成交机制")

    def init_params(self, params):
        """ 回测参数设置 """
        # todo: 本地设置回测参数

        self.params.update(params)

    def __init_params(self, params):
        """ 初始化参数设置  """
        if not isinstance(params, dict):
            raise AttributeError("回测参数类型错误，请检查是否为字典")
        self.strategy.init_params(params.get("strategy"))
        self.init_params(params.get("looper"))

    def __call__(self, *args, **kwargs):
        """ 回测周期 """
        p_data: Bumblebee = args[0]
        params = args[1]

        self.price = p_data
        self.__init_params(params)
        if p_data.type == "tick":
            self.strategy.on_tick(tick=p_data.to_tick())

        if p_data.type == "bar":
            self.strategy.on_bar(tick=p_data.to_bar())
