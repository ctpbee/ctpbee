import random
import uuid
from copy import deepcopy
from datetime import timedelta, datetime

from ctpbee.constant import (
    OrderRequest,
    Direction,
    OrderData,
    CancelRequest,
    TradeData,
    BarData,
    TickData,
    Status,
    Event,
    EVENT_ORDER,
    EVENT_TRADE,
    EVENT_LOG,
    EVENT_ERROR,
    EVENT_INIT_FINISHED,
    EVENT_BAR,
    EVENT_TICK,
)
from ctpbee.date import trade_dates
from ctpbee.looper.account import Account


class LocalLooper:
    message_box = {-1: "超出下单限制", -2: "超出涨跌价格", -3: "未成交", -4: "资金不足"}

    def __init__(self, app_signal, app):
        """ 需要构建完整的成交回报以及发单报告,
        在account里面需要存储大量的存储
         在我们此处实现过程也通过调用事件引擎来进行调用\
         """
        self.app = app
        # 活跃报单数量
        self.change_month_record = {}
        self.pending = {}

        self.sessionid = random.randint(1000, 10000)
        self.frontid = random.randint(10001, 500000)

        # 日志输出器
        self.app_signal = app_signal
        # 策略池子
        self.strategy_mapping = dict()
        # 覆盖里面的action和logger属性
        # 涨跌停价格
        self.upper_price = 99999
        self.drop_price = 0

        # 风控/risk control todo:完善
        self.params = dict(
            deal_pattern="match",
            single_order_limit=10,
            single_day_limit=100,
            today_exchange=["INE", "SHFE"],
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

        self.pre_close_price = dict()
        # 所有的报单数量
        self.order_buffer = dict()

        self.date = None
        # 行情
        self.data_entity = None
        self.if_next_day = False
        self.data_type = "bar"

        self.price_mapping = dict()
        # 仓位详细
        self.position_detail = dict()

        self.ask_price_mapping = dict()
        self.bid_price_mapping = dict()

    def get_trades(self):
        return list(self.traded_order_mapping.values())

    def on_event(self, type, data):
        event = Event(type=type, data=data)
        if type == EVENT_BAR or type == EVENT_TICK:
            import ctpbee.signals as signals

            signal = getattr(signals.common_signals, f"{type}_signal")
        else:
            signal = getattr(self.app_signal, f"{type}_signal")
        signal.send(event)

    def enable_extension(self, name):
        if name in self.strategy_mapping.keys():
            self.strategy_mapping.get(name).active = True
        else:
            return

    def suspend_extension(self, name):
        if name in self.strategy_mapping.keys():
            self.strategy_mapping.get(name).active = False
        else:
            return

    def update_risk(self, risk):
        self.risk = risk

    def _generate_order_data_from_req(self, req: OrderRequest):
        """将发单请求转换为发单数据"""
        self.order_ref += 1
        order_id = f"{self.frontid}-{self.sessionid}-{self.order_ref}"
        return deepcopy(req)._create_order_data(
            gateway_name="looper", order_id=order_id, time=self.datetime
        )

    def _generate_trade_data_from_order(self, order_data: OrderData):
        """将orderdata转换成成交单"""
        p = TradeData(
            price=order_data.price,
            istraded=order_data.volume,
            volume=order_data.volume,
            tradeid=str(uuid.uuid1()),
            offset=order_data.offset,
            direction=order_data.direction,
            gateway_name=order_data.gateway_name,
            order_time=order_data.time,
            time=self.datetime,
            order_id=order_data.order_id,
            symbol=order_data.symbol,
            exchange=order_data.exchange,
        )
        return p

    def send_order(self, order_req: OrderRequest):
        """发单的操作"""
        if order_req.volume == 0:
            return 0
        return self.intercept_gateway(order_req)

    def _cancel(self, cancel_req):
        """撤单机制"""
        self.intercept_gateway(cancel_req)

    def cancel_order(self, cancel_req: CancelRequest, **kwargs):
        if cancel_req.order_id in self.pending.keys():
            order = self.pending[cancel_req.order_id]
            order.status = Status.CANCELLED
            # 移除掉冻结 使得成为可能
            self.account.pop_order(order)
            self.account.position_manager.update_order(order)
            self.on_event(EVENT_ORDER, order)
            self.pending.pop(cancel_req.order_id)

    def cancel_all(self):
        for x in self.pending:
            x.status = Status.CANCELLED
            self.on_event(EVENT_ORDER, x)
        self.pending.clear()
        return 1

    def intercept_gateway(self, data):
        """拦截网关 同时这里应该返回相应的水平"""
        if isinstance(data, OrderRequest):
            """发单请求处理"""
            order_data = self._generate_order_data_from_req(data)
            result, reason = self.account.is_traded(order=order_data)
            if result:
                order_data.__set_hole__("status", Status.NOTTRADED)
                self.pending[order_data.order_id] = deepcopy(order_data)
                self.on_event(EVENT_ORDER, order_data)
                self.account.update_account_from_order(order_data)
                return 1
            else:
                self.on_event(
                    EVENT_ERROR,
                    f"账户报单可用不足, 报单基础信息: "
                    f"{order_data.local_symbol} volume: {order_data.volume}"
                    f" price: {order_data.price}  {order_data.offset.value}{order_data.direction.value}"
                    f" 出现原因: {reason} 当前报单队列存在 {len(self.pending)} 仓位占用保证金: {self.account.margin} 当前仓位构成: {self.account.position_manager}",
                )
                return 0
        else:
            pass

    def match_deal(self):
        """撮合成交
        维护一个返回状态
        -1: 超出下单限制
        -2: 超出涨跌价格
        -3: 未成交
        -4: 资金不足
        p : 成交回报

        """
        ARC = []
        for active_order in self.pending.values():
            px = "".join(filter(str.isalpha, active_order.local_symbol))
            nx = "".join(filter(str.isalpha, self.data_entity.local_symbol))
            if nx != px:  # 针对多品种，实现拆分。 更新当前的价格，确保多个
                continue
            code = active_order.local_symbol
            if self.params.get("deal_pattern") == "match":
                """撮合成交"""
                # todo: 是否可以模拟一定量的市场冲击响应？ 以靠近更加逼真的回测效果 ？？？？

                """ 调用API生成成交单 """
                # 同时这里需要处理是否要进行
                trade = self._generate_trade_data_from_order(active_order)
                """ 这里按照市价进行匹配成交 """

                price = self.data_entity.last_price
                if price is None:
                    price = self.data_entity.close_price
                if price is None:
                    raise ValueError(
                        f"错误的数据:{self.data_entity} 请检查数据格式",
                    )
                trade.__set_hole__("price", price)
                self.on_event(
                    EVENT_LOG,
                    f"--> {trade.local_symbol} 成交时间: {str(trade.time)}, 成交价格{str(trade.price)}, 成交笔数: {str(trade.volume)},"
                    f" 成交方向: {str(trade.direction.value)}，行为: {str(trade.offset.value)}",
                )
                self.account.update_trade(trade)
                """ 调用strategy的on_trade """
                ARC.append(active_order.order_id)
                self.traded_order_mapping[trade.order_id] = trade
                self.today_volume += active_order.volume
                continue
            elif self.params.get("deal_pattern") == "umatch":
                """撮合成交"""
                # todo: 是否可以模拟一定量的市场冲击响应？ 以靠近更加逼真的回测效果 ？？？？

                """ 调用API生成成交单 """
                # 同时这里需要处理是否要进行
                trade = self._generate_trade_data_from_order(order_data=active_order)
                """ 这里按照市价进行匹配成交 """
                self.on_event(
                    EVENT_LOG,
                    f"--> {trade.local_symbol} 成交时间: {str(trade.time)}, 成交价格{str(trade.price)}, 成交笔数: {str(trade.volume)},"
                    f" 成交方向: {str(trade.direction.value)}，行为: {str(trade.offset.value)}",
                )
                self.account.update_trade(trade)
                """ 调用strategy的on_trade """
                ARC.append(active_order.order_id)
                self.traded_order_mapping[trade.order_id] = trade
                self.today_volume += active_order.volume
                continue
            elif self.params.get("deal_pattern") == "simnow":
                can_trade = False
                # 此处Tick级别回测以对价做撮合
                if (
                    active_order.direction == Direction.LONG
                    and self.price_mapping[code] < active_order.price
                ):
                    can_trade = True
                    if self.data_entity.type == "tick":
                        price = self.data_entity.ask_price_1
                    else:
                        price = self.data_entity.close_price

                if (
                    active_order.direction == Direction.SHORT
                    and self.price_mapping[code] > active_order.price
                ):
                    can_trade = True
                    if self.data_entity.type == "tick":
                        price = self.data_entity.bid_price_1
                    else:
                        price = self.data_entity.close_price
                if can_trade:
                    trade = self._generate_trade_data_from_order(
                        order_data=active_order
                    )
                    trade.__set_hole__("price", price)
                    """ 这里按照市价进行匹配成交 """
                    self.on_event(
                        EVENT_LOG,
                        f"--> {trade.local_symbol} 成交时间: {str(trade.time)}, 成交价格{str(trade.price)}, 成交笔数: {str(trade.volume)},"
                        f" 成交方向: {str(trade.direction.value)}，行为: {str(trade.offset.value)}",
                    )
                    self.account.update_trade(trade)
                    ARC.append(active_order.order_id)
                    self.traded_order_mapping[trade.order_id] = trade
                    self.today_volume += active_order.volume
            elif self.params.get("deal_pattern") == "price":
                """限价成交"""
                # 先判断价格和手数是否满足限制条件
                # 进行成交判断
                long_c = (
                    self.data_entity.low_price
                    if self.data_type == "bar"
                    else self.data_entity.ask_price_1
                )
                short_c = (
                    self.data_entity.high_price
                    if self.data_type == "bar"
                    else self.data_entity.bid_price_1
                )
                long_cross = (
                    active_order.direction == Direction.LONG
                    and 0 < long_c <= active_order.price
                )
                short_cross = (
                    active_order.direction == Direction.SHORT
                    and active_order.price <= short_c
                    and short_c > 0
                )
                if long_cross:
                    """判断账户资金是否足以支撑成交"""
                    # 同时这里需要处理是否要进行
                    trade = self._generate_trade_data_from_order(active_order)
                    self.on_event(
                        EVENT_LOG,
                        data=f"成交时间: {str(trade.time)}, 成交价格{str(trade.price)}, 成交笔数: {str(trade.volume)},"
                        f" 成交方向: {str(trade.direction.value)}，行为: {str(trade.offset.value)}",
                    )
                    """ 调用strategy的on_trade """
                    ARC.append(active_order.order_id)
                    self.account.update_trade(trade)
                    self.traded_order_mapping[trade.order_id] = trade
                    self.today_volume += active_order.volume
                    continue
                elif short_cross:
                    """调用API生成成交单"""
                    # 同时这里需要处理是否要进行
                    trade = self._generate_trade_data_from_order(active_order)
                    self.on_event(
                        EVENT_LOG,
                        data=f"成交时间: {str(trade.time)}, 成交价格{str(trade.price)}, 成交笔数: {str(trade.volume)},"
                        f" 成交方向: {str(trade.direction.value)}，行为: {str(trade.offset.value)}",
                    )
                    """ 调用strategy的on_trade """
                    ARC.append(active_order.order_id)
                    self.account.update_trade(trade)
                    self.traded_order_mapping[trade.order_id] = trade
                    self.today_volume += active_order.volume
                    continue
                continue
            else:
                raise TypeError("未支持的成交机制")
        for key in ARC:
            active_order = self.pending[key]
            active_order.__set_hole__("status", Status.ALLTRADED)
            self.on_event(EVENT_ORDER, data=active_order)
            self.on_event(EVENT_TRADE, data=self.traded_order_mapping[key])
            self.pending.pop(key)

    def _init_params(self, params):
        """回测参数设置"""
        self.params.update(params)
        """ 更新接口参数设置 """
        self.params.update(params)
        """ 更新账户策略参数 """

        self.account.update_params(params)

    def init_params(self, params):
        """初始化参数设置"""
        if not isinstance(params, dict):
            raise AttributeError("回测参数类型错误，请检查是否为字典")
        self._init_params(params.get("LOOPER"))

    @staticmethod
    def auth_time(time):
        if 15 < time.hour < 20 or 3 <= time.hour < 8:
            return False
        else:
            return True

    def __call__(self, *args, **kwargs):
        """回测周期"""
        entity = args[0]
        # 日期不相等时,　更新前日结算价格
        if self.account.date is None:
            self.account.date = self.date
        if self.date is None:
            self.date = entity.datetime.date()
        if not self.auth_time(entity.datetime):
            return
        if entity.type == "bar" and entity.close_price <= 0:
            return
        elif entity.type == "tick" and entity.last_price <= 0:
            return

        self.data_type = entity.type
        # 回测的时候自动更新策略的日期
        try:
            seconds = (entity.datetime - self.datetime).seconds
            if seconds >= 60 * 60 * 4 and (
                (entity.datetime.hour >= 20)
                or (
                    (14 <= self.datetime.hour <= 15)
                    and entity.datetime.date() != self.datetime.date()
                )
                and entity.datetime.hour >= 8
            ):  # 换天
                self.account.settle(entity.datetime.date())
                # 针对于账户的实现 我们需要将昨仓转换为今仓
                self.app.recorder.position_manager.covert_to_yesterday_holding()
                for local_symbol, price in self.price_mapping.items():
                    self.pre_close_price[local_symbol] = price
                #  结算完触发初始化函数
                self.on_event(EVENT_INIT_FINISHED, True)
        except KeyError:
            pass
        except AttributeError:
            pass
        self.data_entity = entity
        self.change_month_record[
            "".join(filter(str.isalpha, entity.local_symbol.split(".")[0]))
        ] = entity
        # 维护一个最新的价格
        self.price_mapping[self.data_entity.local_symbol] = (
            self.data_entity.close_price
            if entity.type == "bar"
            else self.data_entity.last_price
        )
        if self.pre_close_price.get(self.data_entity.local_symbol) is None:
            self.pre_close_price[self.data_entity.local_symbol] = (
                self.data_entity.last_price
                if entity.type == "tick"
                else self.data_entity.close_price
            )

        self.match_deal()

        if entity.type == "tick":
            self.account.position_manager.update_tick(
                self.data_entity, self.pre_close_price[self.data_entity.local_symbol]
            )
            self.app.recorder.position_manager.update_tick(
                self.data_entity, self.pre_close_price[self.data_entity.local_symbol]
            )
            self.on_event(EVENT_TICK, TickData(**entity))

        if entity.type == "bar":
            self.account.position_manager.update_bar(
                self.data_entity, self.pre_close_price[self.data_entity.local_symbol]
            )
            self.app.recorder.position_manager.update_bar(
                self.data_entity, self.pre_close_price[self.data_entity.local_symbol]
            )
            self.on_event(EVENT_BAR, BarData(**entity))

        if entity.datetime.hour >= 21:
            """if hour > 21, switch to next trade day"""
            index = trade_dates.index(str(entity.datetime.date()))
            self.date = datetime.strptime(trade_dates[index + 1], "%Y-%m-%d").date()
        else:
            if str(entity.datetime.date()) not in trade_dates:
                last_day = entity.datetime + timedelta(days=-1)
                self.date = datetime.strptime(
                    trade_dates[trade_dates.index(str(last_day.date())) + 1], "%Y-%m-%d"
                ).date()
            else:
                self.date = entity.datetime.date()
        # 穿过接口日期检查
        self.account.via_aisle()
        self.datetime = entity.datetime

    def get_entity_from_alpha(self, alpha):
        return self.change_month_record.get(alpha)
