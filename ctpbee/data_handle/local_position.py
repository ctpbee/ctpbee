"""
Notice : 神兽保佑 ，测试一次通过
//      
//      ┏┛ ┻━━━━━┛ ┻┓
//      ┃　　　　　　 ┃
//      ┃　　　━　　　┃
//      ┃　┳┛　  ┗┳　┃
//      ┃　　　　　　 ┃
//      ┃　　　┻　　　┃
//      ┃　　　　　　 ┃
//      ┗━┓　　　┏━━━┛
//        ┃　　　┃   Author: somewheve
//        ┃　　　┃   Datetime: 2019/7/3 下午8:46  ---> 无知即是罪恶
//        ┃　　　┗━━━━━━━━━┓
//        ┃　　　　　　　    ┣┓
//        ┃　　　　         ┏┛
//        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
//          ┃ ┫ ┫   ┃ ┫ ┫
//          ┗━┻━┛   ┗━┻━┛
//
"""
from typing import Text

""" 本地持仓对象 """
import warnings
from copy import copy

from ctpbee.constant import PositionData, Offset, Direction, OrderRequest, OrderData, \
    Exchange, TickData, EXCHANGE_MAPPING, BarData


class LocalVariable:
    def __init__(self, data):

        if data.get("long") is not None:
            self.long = float(data.get('long'))
        else:
            self.long = 0
        if data.get("short") is not None:
            self.short = float(data.get('short'))
        else:
            self.short = 0


# local position support


class PositionHolding:
    """ 单个合约的持仓 """

    def __init__(self, local_symbol, app):
        """"""
        self.local_symbol = local_symbol
        try:
            self.exchange = local_symbol.split(".")[1]
            self.symbol = local_symbol.split(".")[0]
        except Exception:
            raise ValueError("invalid local_symbol")
        self.active_orders = {}
        self.size = 1
        from ctpbee.looper.account import Account
        if isinstance(app, Account):
            # if app.balance
            pass
        else:
            if app.recorder.get_contract(self.local_symbol) is not None:
                self.size = app.recorder.get_contract(self.local_symbol).size
            elif getattr(app.trader, "account", None) is not None:
                self.size = app.trader.account.get_size_from_map(local_symbol=local_symbol)
            else:
                raise ValueError("获取合约信息失败, 持仓盈亏计算失败")
        self.long_pos = 0
        self.long_yd = 0
        self.long_td = 0
        self.long_pnl = 0
        self.long_stare_pnl = 0
        self.long_price = 0

        self.short_pos = 0
        self.short_yd = 0
        self.short_td = 0
        self.short_pnl = 0
        self.short_stare_pnl = 0
        self.short_price = 0

        self.long_pos_frozen = 0
        self.long_yd_frozen = 0
        self.long_td_frozen = 0

        self.short_pos_frozen = 0
        self.short_yd_frozen = 0
        self.short_td_frozen = 0

        self.pre_settlement_price = 0
        self.last_price = 0

    @property
    def long_available(self):
        print(self.long_pos, self.long_pos_frozen)
        return self.long_pos - self.long_pos_frozen

    @property
    def short_available(self):
        print(self.short_pos, self.short_pos_frozen)
        return self.short_pos - self.short_pos_frozen

    def update_trade(self, trade):
        """成交更新"""
        # 多头
        if trade.direction == Direction.LONG:
            # 开仓
            if trade.offset == Offset.OPEN:
                self.long_td += trade.volume
            # 平今
            elif trade.offset == Offset.CLOSETODAY:
                self.short_td -= trade.volume
            # 平昨
            elif trade.offset == Offset.CLOSEYESTERDAY:
                self.short_yd -= trade.volume
            # 平仓
            elif trade.offset == Offset.CLOSE:
                # 上期所等同于平昨
                if self.exchange == Exchange.SHFE:
                    self.short_yd -= trade.volume
                # 非上期所，优先平今
                else:
                    self.short_td -= trade.volume
                    if self.short_td < 0:
                        self.short_yd += self.short_td
                        self.short_td = 0

        # 空头 {'OI001.CZCE': 1590.0},

        elif trade.direction == Direction.SHORT:
            # 开仓

            if trade.offset == Offset.OPEN:
                self.short_td += trade.volume
            # 平今
            elif trade.offset == Offset.CLOSETODAY:
                self.long_td -= trade.volume
            # 平昨
            elif trade.offset == Offset.CLOSEYESTERDAY:
                self.long_yd -= trade.volume
            # 平仓
            elif trade.offset == Offset.CLOSE:
                # 上期所等同于平昨
                if self.exchange == Exchange.SHFE:
                    self.long_yd -= trade.volume
                # 非上期所，优先平今
                else:
                    self.long_td -= trade.volume

                    if self.long_td < 0:
                        self.long_yd += self.long_td
                        self.long_td = 0
        # self.long_pos = self.long_td + self.long_yd
        # self.short_pos = self.short_yd + self.short_td
        # 汇总
        self.calculate_price(trade)
        self.calculate_position()
        self.calculate_pnl()
        self.calculate_stare_pnl()

    def calculate_position(self):
        """计算持仓情况"""
        self.long_pos = self.long_td + self.long_yd
        self.short_pos = self.short_td + self.short_yd

    def update_position(self, position: PositionData):
        """"""
        if position.direction == Direction.LONG:
            self.long_pos = position.volume
            self.long_yd = position.yd_volume
            self.long_td = self.long_pos - self.long_yd
            self.long_pnl = position.pnl
            self.long_price = position.price

        elif position.direction == Direction.SHORT:
            self.short_pos = position.volume
            self.short_yd = position.yd_volume
            self.short_td = self.short_pos - self.short_yd
            self.short_pnl = position.pnl
            self.short_price = position.price

    def update_order(self, order: OrderData):
        """"""
        if order._is_active():
            self.active_orders[order.local_order_id] = order
        else:
            if order.local_order_id in self.active_orders:
                self.active_orders.pop(order.local_order_id)

        self.calculate_frozen()

    def update_order_request(self, req: OrderRequest, local_order_id: str):
        """"""
        gateway_name, orderid = local_order_id.split(".")

        order = req._create_order_data(orderid, gateway_name)
        self.update_order(order)

    def update_tick(self, tick, pre_settlement_price):
        """行情更新"""
        self.pre_settlement_price = pre_settlement_price
        self.last_price = tick.last_price
        self.calculate_pnl()
        self.calculate_stare_pnl()

    def update_bar(self, bar, pre_close):
        self.pre_settlement_price = pre_close
        self.last_price = bar.close_price
        self.calculate_pnl()
        self.calculate_stare_pnl()

    def calculate_frozen(self):
        """"""
        self.long_pos_frozen = 0
        self.long_yd_frozen = 0
        self.long_td_frozen = 0

        self.short_pos_frozen = 0
        self.short_yd_frozen = 0
        self.short_td_frozen = 0

        for order in self.active_orders.values():
            # Ignore position open orders
            if order.offset == Offset.OPEN:
                continue

            frozen = order.volume - order.traded

            if order.direction == Direction.LONG:
                if order.offset == Offset.CLOSETODAY:
                    self.short_td_frozen += frozen
                elif order.offset == Offset.CLOSEYESTERDAY:
                    self.short_yd_frozen += frozen
                elif order.offset == Offset.CLOSE:
                    self.short_td_frozen += frozen

                    if self.short_td_frozen > self.short_td:
                        self.short_yd_frozen += (self.short_td_frozen
                                                 - self.short_td)
                        self.short_td_frozen = self.short_td
            elif order.direction == Direction.SHORT:
                if order.offset == Offset.CLOSETODAY:
                    self.long_td_frozen += frozen
                elif order.offset == Offset.CLOSEYESTERDAY:
                    self.long_yd_frozen += frozen
                elif order.offset == Offset.CLOSE:
                    self.long_td_frozen += frozen

                    if self.long_td_frozen > self.long_td:
                        self.long_yd_frozen += (self.long_td_frozen
                                                - self.long_td)
                        self.long_td_frozen = self.long_td

            self.long_pos_frozen = self.long_td_frozen + self.long_yd_frozen
            self.short_pos_frozen = self.short_td_frozen + self.short_yd_frozen

    def convert_order_request_shfe(self, req: OrderRequest):
        """"""
        if req.offset == Offset.OPEN:
            return [req]

        if req.direction == Direction.LONG:
            pos_available = self.short_pos - self.short_pos_frozen
            td_available = self.short_td - self.short_td_frozen
        else:
            pos_available = self.long_pos - self.long_pos_frozen
            td_available = self.long_td - self.long_td_frozen

        if req.volume > pos_available:
            return []
        elif req.volume <= td_available:
            req_td = copy(req)
            req_td.offset = Offset.CLOSETODAY
            return [req_td]
        else:
            req_list = []
            if td_available > 0:
                req_td = copy(req)
                req_td.offset = Offset.CLOSETODAY
                req_td.volume = td_available
                req_list.append(req_td)

            req_yd = copy(req)
            req_yd.offset = Offset.CLOSEYESTERDAY
            req_yd.volume = req.volume - td_available
            req_list.append(req_yd)

            return req_list

    def convert_order_request_lock(self, req: OrderRequest):
        """"""
        if req.direction == Direction.LONG:
            td_volume = self.short_td
            yd_available = self.short_yd - self.short_yd_frozen
        else:
            td_volume = self.long_td
            yd_available = self.long_yd - self.long_yd_frozen

        # If there is td_volume, we can only lock position
        if td_volume:
            req_open = copy(req)
            req_open.offset = Offset.OPEN
            return [req_open]
        # If no td_volume, we close opposite yd position first
        # then open new position
        else:
            open_volume = max(0, req.volume - yd_available)
            req_list = []

            if yd_available:
                req_yd = copy(req)
                if self.exchange == Exchange.SHFE:
                    req_yd.offset = Offset.CLOSEYESTERDAY
                else:
                    req_yd.offset = Offset.CLOSE
                req_list.append(req_yd)

            if open_volume:
                req_open = copy(req)
                req_open.offset = Offset.OPEN
                req_open.volume = open_volume
                req_list.append(req_open)

            return req_list

    def calculate_pnl(self):
        """ 计算浮动盈亏 """
        try:
            self.long_pnl = round(self.long_pos * (self.last_price - self.long_price) * self.size)
        except ZeroDivisionError:
            self.long_pnl = 0
        except AttributeError:
            self.long_pnl = 0
        try:
            self.short_pnl = round(self.short_pos * (self.short_price - self.last_price) * self.size)
        except ZeroDivisionError:
            self.short_pnl = 0
        except AttributeError:
            self.short_pnl = 0

    def calculate_stare_pnl(self):
        """计算盯市盈亏"""
        try:
            self.long_stare_pnl = self.long_pos * (self.long_price - self.pre_settlement_price) * self.size
        except ZeroDivisionError:
            self.long_pnl = 0
        except AttributeError:
            self.long_pnl = 0
        try:
            self.short_stare_pnl = self.short_pos * (self.pre_settlement_price - self.short_price) * self.size
        except ZeroDivisionError:
            self.short_pnl = 0
        except AttributeError:
            self.short_pnl = 0

    def calculate_price(self, trade):
        """计算持仓均价（基于成交数据）"""
        # 只有开仓会影响持仓均价
        if trade.offset == Offset.OPEN:
            if trade.direction == Direction.LONG:
                cost = self.long_price * self.long_pos
                cost += trade.volume * trade.price
                new_pos = self.long_pos + trade.volume
                if new_pos:
                    self.long_price = cost / new_pos
                else:
                    self.long_price = 0
            else:
                cost = self.short_price * self.short_pos
                cost += trade.volume * trade.price
                new_pos = self.short_pos + trade.volume
                if new_pos:
                    self.short_price = cost / new_pos
                else:
                    self.short_price = 0

    def get_position_by_direction(self, direction):
        if direction == Direction.LONG:
            return PositionData(
                symbol=self.symbol,
                volume=self.long_pos,
                exchange=EXCHANGE_MAPPING[self.exchange],
                direction=direction,
                pnl=self.long_pnl,
                price=self.long_price,
                frozen=self.long_pos_frozen,
                yd_volume=self.long_yd
            )
        elif direction == Direction.SHORT:
            return PositionData(
                symbol=self.symbol,
                volume=self.short_pos,
                exchange=EXCHANGE_MAPPING[self.exchange],
                direction=direction,
                pnl=self.short_pnl,
                price=self.short_price,
                frozen=self.short_pos_frozen,
                yd_volume=self.short_yd
            )
        return None


class LocalPositionManager(dict):
    """ 用于管理持仓信息 只提供向外的接口 """

    def __init__(self, app):
        super().__init__({})
        self.app = app
        self.size_map = {}

    def update_tick(self, tick: TickData, pre_close):
        """ 更新tick  """
        if tick.local_symbol not in self:
            return
        self.get(tick.local_symbol).update_tick(tick, pre_close)

    def update_bar(self, bar: BarData, pre_close):
        if bar.local_symbol not in self:
            return
        self.get(bar.local_symbol).update_bar(bar, pre_close)

    def is_convert_required(self, local_symbol: str):
        """
        Check if the contract needs offset convert.
        """
        contract = self.app.recorder.get_contract(local_symbol)

        # Only contracts with long-short position mode requires convert
        if not contract:
            return False
        elif contract.net_position:
            return False
        else:
            return True

    def update_order_request(self, req: OrderRequest, local_orderid: str):
        """"""
        if not self.is_convert_required(req.local_symbol):
            return

        holding = self.get(req.local_symbol, None)
        if not holding:
            self[req.local_symbol] = PositionHolding(req.local_symbol, self.app)
        self[req.local_symbol].update_order_request(req, local_orderid)

    def convert_order_request(self, req: OrderRequest, lock: bool):
        """"""
        if not self.is_convert_required(req.local_symbol):
            return [req]

        holding = self.get(req.local_symbol, None)
        if not holding:
            self[req.local_symbol] = PositionHolding(req.local_symbol, self.app)
        if lock:
            return self[req.local_symbol].convert_order_request_lock(req)
        elif req.exchange == Exchange.SHFE:
            return self[req.local_symbol].convert_order_request_shfe(req)
        else:
            return [req]

    def update_order(self, order):
        """ 更新order """
        if order.local_symbol not in self:
            self[order.local_symbol] = PositionHolding(order.local_symbol, self.app)
        else:
            self.get(order.local_symbol).update_order(order)

    def update_trade(self, trade):
        """ 更新成交  """
        if trade.local_symbol not in self:
            self[trade.local_symbol] = PositionHolding(trade.local_symbol, self.app)
            self[trade.local_symbol].update_trade(trade)
        else:
            self.get(trade.local_symbol).update_trade(trade)

    def update_position(self, position):
        """ 更新持仓 """
        if position.local_symbol not in self.keys():
            self[position.local_symbol] = PositionHolding(position.local_symbol, self.app)
            self[position.local_symbol].update_position(position)
        else:
            self.get(position.local_symbol).update_position(position)

    def get_position(self, local_symbol):
        """ 根据local_symbol 获取持仓信息 """
        return self.get(local_symbol, None)

    def update_size_map(self, params):
        self.size_map = params.get("size_map")

    def get_position_by_ld(self, local_symbol: Text, direction: Direction) -> PositionData:
        """
        ld means local_symbol and direction
        ld意味着local_symbol和direction
        """
        if local_symbol not in self:
            return None
        return self[local_symbol].get_position_by_direction(direction)

    def covert_to_yesterday_holding(self, **kwargs):
        """ 将今日持仓转换为昨日持仓 """
        for holding in self.values():
            if holding.long_td != 0:
                holding.long_yd += holding.long_td
                holding.long_td = 0

            if holding.short_td != 0:
                holding.short_yd += holding.short_td
                holding.short_td = 0
        for key, value in kwargs.items():
            pos = self.get(key)
            if pos:
                pos.long_price = value
                pos.short_price = value

    def clear_frozen(self):
        for x in self.values():
            x.active_orders.clear()
            x.calculate_frozen()

    def get_all_positions(self):
        """ 返回所有的持仓信息 """
        position_list = []
        for x in self.values():
            if x.local_symbol == "":
                continue
            if x.long_pos != 0:
                temp = {}
                temp['exchange'] = x.exchange
                temp['direction'] = "long"
                temp['position_profit'] = x.long_pnl
                temp['symbol'] = x.local_symbol
                temp['local_symbol'] = x.local_symbol
                temp['price'] = x.long_price
                temp['volume'] = x.long_pos
                temp['yd_volume'] = x.long_yd
                temp["frozen"] = x.long_pos_frozen
                temp["available"] = x.long_pos - x.long_pos_frozen
                temp['stare_position_profit'] = x.long_stare_pnl
                if x.long_pos == x.long_yd:
                    temp['position_date'] = 2
                elif x.long_pos != x.long_yd:
                    temp['position_date'] = 1
                position_list.append(temp)
            if x.short_pos != 0:
                temp = {}
                temp['exchange'] = x.exchange
                temp['direction'] = "short"
                temp['position_profit'] = x.short_pnl
                temp['symbol'] = x.local_symbol
                temp['local_symbol'] = x.local_symbol
                temp['price'] = x.short_price
                temp['volume'] = x.short_pos
                temp['yd_volume'] = x.short_yd
                temp["frozen"] = x.short_pos_frozen
                temp["available"] = x.short_pos - x.short_pos_frozen
                temp['stare_position_profit'] = x.short_stare_pnl
                if x.short_pos == x.short_yd:
                    temp['position_date'] = 2
                elif x.short_pos != x.short_yd:
                    temp['position_date'] = 1
                position_list.append(temp)
        return position_list

    @property
    def length(self):
        return len(self)
