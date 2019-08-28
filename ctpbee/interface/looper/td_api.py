import collections
import random
from copy import deepcopy
from functools import lru_cache
from typing import Dict

from ctpbee.constant import OrderRequest, CancelRequest, EVENT_TICK, TickData, EVENT_ORDER, EVENT_TRADE, \
    OrderData, Status, TradeData
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
            result = self._cal_whether_traded(_, event.data)
            if result:
                self._update_trading(result)
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
        return

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

        :param order:
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
            self._update_trading(result)
            self.traded_order_mapping[order.order_id] = result
            self._push_order_callback(order, is_traded=False)

    def _update_trading(self, trade):
        """ 根据成交单进行系统更新 """

        # todo  需要更新本地持仓 ？

        pass

    def set_attribute(self, **attr):
        """ 通过外部设置参数 """
        for i, v in attr:
            setattr(self, i, v)

    def init_config(self, app):
        """ 初始化设置 """
        for idx, value in app.config['LOOPER']:
            setattr(self, idx, value)

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

    def update_account(self):
        """ 更新账户资金信息 """
        # todo 更新账户资金信息到账户

    def calculate_result(self) -> Dict:
        """ 计算每日结果输出信息 """
        result = dict()
        return result
