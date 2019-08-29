import collections
import random
from copy import deepcopy
from functools import lru_cache

from ctpbee.constant import OrderRequest, CancelRequest, EVENT_TICK, TickData, EVENT_ORDER, EVENT_TRADE, \
    OrderData, Status, TradeData, EVENT_INIT_FINISHED
from ctpbee.event_engine import Event
from ctpbee.interface.looper.me import Account


class AliasDayResult:
    """
    每天的结果
    """

    def __init__(self, **kwargs):
        """ 实例化进行调用 """
        for i, v in kwargs:
            setattr(self, i, v)


class LocalLooperApi():
    """
    本地化回测的服务端 ---> this will be a very interesting thing!
    尽量模拟交易所成交

    -----> 应该推出在线回测与本地回测两种模式
    在线: tick和bar的接收应该与协议保持一致----> 对接开源的looper_me服务器
    本地 : 读取本地数据库的数据进行回测
    """

    def __init__(self, event_engine, app):
        super().__init__()

        # 接入事件引擎
        self.event_engine = event_engine
        self.pending = collections.deque()
        self.account = Account()

        self.sessionid = random.randint(1000, 10000)
        self.frontid = random.randint(10001, 500000)

        # 发单的ref集合
        self.order_ref_set = set()
        # 已经order_id ---- 成交单
        self.traded_order_mapping = {}
        # 已经order_id --- 报单
        self.order_id_pending_mapping = {}

        # 当前tick
        self.current_tick: TickData = None

        # 独立回测
        self.p = collections.defaultdict(collections.deque)
        self._ocos = dict()
        self._ocol = collections.defaultdict(list)

        # 根据外部配置覆盖配置
        self.init_config(app)
        self.account.update_attr(app.config['LOOPER_SETTING'])
        self.event_engine.register(EVENT_TICK, self._process_tick)

    def _push_order(self, order: OrderData):
        """
        将订单回报推送到策略层，这个地方将order请求转换为order数据， 从而简化代码
        :param order:
        :return:
        """
        event = Event(EVENT_ORDER, deepcopy(order))
        self.event_engine.put(event)

    def _push_trade(self, trade):
        """  将成交回报推送到策略层 """
        event = Event(EVENT_TRADE, deepcopy(trade))
        self.event_engine.put(event)

    def _push_order_callback(self, order: OrderData, is_traded: bool):
        """
        推送order回策略层，
        如果已经成交， 那么找到成交单数据并推送回去，
        如果没有成交 ，那么将order的状态推荐为正在提交中
        :param order_data: 报单
        :param is_traded: 是否成交
        :return:
        """
        if is_traded:
            """ 如果成交了那么同时推送"""
            trade = self.traded_order_mapping[order.order_id]
            order.status = Status.ALLTRADED
            self._push_order()
            self._push_trade(trade)
        else:
            order.status = Status.SUBMITTING
            self.order_id_pending_mapping[order.order_id] = order
            self._push_order(order)
            self.pending.appendleft(order)

    def _process_tick(self, event):
        """
        处理tick数据， 对服务器的单子 进行成交
        :param event: tick数据事件
        :return:
        """
        # 先更新当前tick
        self.current_tick = event.data

        # 然后立即处理未成交的单子或者部分成交的单子
        for _ in self.pending:
            # 行情能够发生成交
            result = self._cal_whether_traded(_, event.data)
            if result:
                # 判断当前成交单是否能由账户支撑起
                if self.account.is_traded(result):
                    # 如果账户能够进行交易 那么更新账户数据
                    self._update_trading(result)
                else:
                    # 无法交易 直接进行下一个的成交
                    continue
                self.traded_order_mapping[_.order_id] = result
                self._push_order_callback(_, is_traded=False)
                self.pending.remove(_)
            else:
                continue

    @lru_cache(maxsize=100000)
    def _cal_whether_traded(self, order: OrderData, tick: TickData) -> TradeData or None:
        """
        计算是否进行成交， 这个地方需要用到lru缓存来提升计算性能
        :param order:报单
        :param tick:当前行情
        :return: 成交单或者空
        """
        if tick.ask_price_1 and tick.bid_price_1:
            pass
        if tick.ask_price_1 >= tick.bid_price_1:
            # 撮合成交
            return TradeData(
                direction=order.direction,
                price=order.price,
                symbol=order.symbol,
                offset=order.offset,
                type=order.type,
                time=order.time,
            )
            pass
        else:
            return None

    def _convert_req_to_data(self, order: OrderRequest):
        # 随机生成一个order_ref
        while True:
            ref = random.randint(1, 100000)
            if ref not in self.order_ref_set:
                self.order_ref_set.add(ref)
                break
        order_id = f"{self.frontid}_{self.sessionid}_{ref}"

        return order._create_order_data(order_id=order_id, gateway_name="looper")

    def __accept_order(self, order: OrderRequest):
        """

        :param order:报单
        :return:
        """
        order = self._convert_req_to_data(order)
        if self._auth_order_price(order):
            #  如果单子满足 那么立即进行撮合成交
            self._brokered_transactions(order)

    def _auth_order_price(self, order: OrderData):
        """
        检查报单价格是否超过涨跌停
        :param order: 报单
        :return:
        """
        if order.price > self.current_tick.limit_up or order.price < self.current_tick.limit_down:
            self.log("价格超过涨跌停， 拒单")
            order.status = Status.REJECTED
            self._push_order(order)
            return False
        return True

    def _brokered_transactions(self, order):
        """
        计算是否成交， 如果成交那么就 推送成交回报并将报单推送回去
        :param order:保单数据
        :return:
        """
        result = self._cal_whether_traded(order, self.current_tick)
        if result:
            # 判断当前成交单是否能由账户支撑起
            if self.account.is_traded(result):
                # 如果账户能够进行交易 那么更新账户数据
                self._update_trading(result)
            else:
                # 无法交易 直接推出并过滤此次成交
                # todo： 是否此处应该将order添加为未成交
                return
            self.traded_order_mapping[order.order_id] = result
            self._push_order_callback(order, is_traded=False)

    def _update_trading(self, trade):
        """ 根据成交单进行系统更新 """
        self.account.trading(trade)

    def set_attribute(self, **attr):
        """ 通过外部设置参数 """
        for i, v in attr:
            setattr(self, i, v)

    def init_config(self, app):
        """ 初始化设置 """
        {setattr(self, idx, value) for idx, value in app.config['LOOPER'] if hasattr(self, idx)}

    def send_order(self, order: OrderRequest):
        """ 发单, 可以被外部进行调用
        """
        self._accept_order(order)

    def cancel_order(self, cancel_req: CancelRequest):
        """
        根据撤单请求找到order，然后在
        可以被外部进行调用
        :param cancel_req:
        :return:
        """
        if cancel_req.order_id in self.order_id_pending_mapping:
            """ 在pending中进行移除"""

            order = self.order_id_pending_mapping[cancel_req.order_id]
            # 在挂单中移除order
            self.pending.remove(order)

            # 将撤单推送回去
            order.status = Status.CANCELLED
            self._push_order(order)
            # 删除挂单映射
            # todo 回撤单是否可以存起来 ？
            del self.order_id_pending_mapping[order.order_id]
            self.log(f"撤单, 单号:{order.order_id}")
            return 0
        return -1

    def log(self, log):
        from datetime import datetime
        print(f"{str(datetime.now())}    交易所   {log}")

    def query_position(self):
        return 0

    def query_account(self):
        return 0

    def request_market_data(self):
        """ 请求市场行情 """
        return True

    def connect(self, info):
        self.userid = info.get("userid")
        # 初始化策略
        event = Event(EVENT_INIT_FINISHED, True)
        self.event_engine.put(event)
