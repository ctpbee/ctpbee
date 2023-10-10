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
import warnings
from typing import Text

""" 本地持仓对象 """
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


class PositionHolding:
    """ 单个合约的持仓 """

    def __init__(self, local_symbol, contract=None):
        """"""
        self.local_symbol = local_symbol
        try:
            self.exchange = local_symbol.split(".")[1]
            self.symbol = local_symbol.split(".")[0]
        except Exception:
            raise ValueError("invalid local_symbol")
        self.active_orders = {}
        from ctpbee.looper.account import Account
        if contract is None:
            warnings.warn("no size passed please check your contract! contract will be fixed to 10")
            self.size = 10
        else:
            self.size = contract.size
        self.long_pos = 0
        self.long_yd = 0
        self.long_td = 0
        self.long_pnl = 0
        self.long_stare_pnl = 0
        self.long_price = 0
        self.long_open_price = 0

        self.short_pos = 0
        self.short_yd = 0
        self.short_td = 0
        self.short_pnl = 0
        self.short_stare_pnl = 0
        self.short_price = 0
        self.short_open_price = 0

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
        return self.long_pos - self.long_pos_frozen

    @property
    def short_available(self):
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
            self.long_open_price = position.open_price

        elif position.direction == Direction.SHORT:
            self.short_pos = position.volume
            self.short_yd = position.yd_volume
            self.short_td = self.short_pos - self.short_yd
            self.short_pnl = position.pnl
            self.short_price = position.price
            self.short_open_price = position.open_price

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
        """ 行情更新 """
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
            self.long_stare_pnl = self.long_pos * (self.last_price - self.long_open_price) * self.size
        except ZeroDivisionError:
            self.long_stare_pnl = 0
        except AttributeError:
            self.long_stare_pnl = 0
        except OverflowError:
            self.long_stare_pnl = 0
        try:
            self.short_stare_pnl = self.short_pos * (self.short_open_price - self.last_price) * self.size
        except ZeroDivisionError:
            self.short_stare_pnl = 0
        except AttributeError:
            self.short_stare_pnl = 0
        except OverflowError:
            self.short_stare_pnl = 0

    def calculate_price(self, trade):
        """计算持仓均价（基于成交数据）"""
        # 只有开仓会影响持仓均价
        if trade.offset == Offset.OPEN:
            if trade.direction == Direction.LONG:
                cost = self.long_price * self.long_pos + trade.volume * trade.price
                open_cost = self.long_open_price * self.long_pos + trade.volume * trade.price
                new_pos = self.long_pos + trade.volume
                if new_pos:
                    self.long_price = cost / new_pos
                    self.long_open_price = open_cost / new_pos
                else:
                    self.long_price = 0
                    self.long_open_price = 0
            else:
                cost = self.short_price * self.short_pos + trade.volume * trade.price
                open_cost = self.short_open_price * self.short_pos + trade.volume * trade.price
                new_pos = self.short_pos + trade.volume
                if new_pos:
                    self.short_price = cost / new_pos
                    self.short_open_price = open_cost / new_pos
                else:
                    self.short_price = 0
                    self.short_open_price = 0

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
                open_price=self.long_open_price,
                yd_volume=self.long_yd,
                float_pnl=self.long_stare_pnl,
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
                yd_volume=self.short_yd,
                float_pnl=self.short_stare_pnl,
                open_price=self.short_open_price,
            )
        return None

    def __repr__(self):
        return f"Pos<local_symbol:{self.local_symbol} long_direction: {self.long_pos}---{self.long_price} pnl: {self.long_pnl}    short_direction: {self.short_pos}---{self.short_price} pnl:{self.short_pnl}>"


class LocalPositionManager(dict):
    """ 用于管理持仓信息 只提供向外的接口 """

    def __init__(self, app):
        super().__init__({})
        self.app = app
        self.size_map = {}

    def update_tick(self, tick: TickData, pre_close):
        """
        更新tick信息更新本地持仓盈亏等数据
        """
        """ 更新tick  """
        if tick.local_symbol not in self:
            return
        self.get(tick.local_symbol).update_tick(tick, pre_close)

    def update_bar(self, bar: BarData, pre_close):
        """
        根据k线信息更新本地持仓盈亏
        """
        if bar.local_symbol not in self:
            return
        self.get(bar.local_symbol).update_bar(bar, pre_close)

    def is_convert_required(self, local_symbol: str):
        """
        Check if the contract needs offset convert.
        """
        contract = self.get_contract(local_symbol)

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
            self[req.local_symbol] = PositionHolding(req.local_symbol,
                                                     self.get_contract(req.local_symbol))
        self[req.local_symbol].update_order_request(req, local_orderid)

    def convert_order_request(self, req: OrderRequest, lock: bool):
        """"""
        if not self.is_convert_required(req.local_symbol):
            return [req]

        holding = self.get(req.local_symbol, None)
        if not holding:
            self[req.local_symbol] = PositionHolding(req.local_symbol,
                                                     self.get_contract(req.local_symbol)
                                                     )
        if lock:
            return self[req.local_symbol].convert_order_request_lock(req)
        elif req.exchange == Exchange.SHFE:
            return self[req.local_symbol].convert_order_request_shfe(req)
        else:
            return [req]

    def update_order(self, order):
        """ 更新order """
        if order.local_symbol not in self:

            self[order.local_symbol] = PositionHolding(order.local_symbol,
                                                       self.get_contract(order.local_symbol))
        else:
            self.get(order.local_symbol).update_order(order)

    def get_contract(self, local_symbol):
        from ctpbee.app import CtpBee
        if type(self.app) == CtpBee:
            return self.app.recorder.get_contract(local_symbol)
        else:
            return self.app.get_contract(local_symbol)

    def update_trade(self, trade):
        """ 更新成交  """
        if trade.local_symbol not in self:
            self[trade.local_symbol] = PositionHolding(trade.local_symbol,
                                                       self.get_contract(trade.local_symbol))
            self[trade.local_symbol].update_trade(trade)
        else:
            self.get(trade.local_symbol).update_trade(trade)

    def update_position(self, position):
        """ 更新持仓 """
        if position.local_symbol not in self.keys():
            self[position.local_symbol] = PositionHolding(position.local_symbol,
                                                          self.get_contract(position.local_symbol))
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
            pos = self.get(key, None)
            if pos is not None:
                if pos.long_pos != 0:
                    self[key].long_price = value
                    self[key].long_pnl = 0
                else:
                    self[key].long_price = 0
                    self[key].long_pnl = 0
                if pos.short_pos != 0:
                    self[key].short_price = value
                    self[key].short_pnl = 0
                else:
                    self[key].short_price = 0
                    self[key].short_pnl = 0

    def clear_frozen(self):
        for x in self.values():
            x.active_orders.clear()
            x.calculate_frozen()

    def get_all_position_objects(self):
        """ 返回PositionData格式的持仓数据 """
        pos = []
        for x in self.values():
            if len(x.local_symbol) == 0:
                continue
            if x.long_pos != 0:
                p = PositionData(
                    symbol=x.symbol,
                    exchange=x.exchange,
                    direction=Direction.LONG,
                    volume=x.long_pos,
                    frozen=x.long_pos_frozen,
                    price=x.long_price,
                    pnl=x.long_pnl,
                    yd_volume=x.long_yd,
                    float_pnl=x.long_stare_pnl,
                    open_price=x.long_open_price,
                )
                pos.append(p)
            if x.short_pos != 0:
                p = PositionData(
                    symbol=x.symbol,
                    exchange=x.exchange,
                    direction=Direction.SHORT,
                    volume=x.short_pos,
                    frozen=x.short_pos_frozen,
                    price=x.short_price,
                    pnl=x.short_pnl,
                    yd_volume=x.short_yd,
                    open_price=x.short_open_price,
                    float_pnl=x.short_stare_pnl,
                )
                pos.append(p)
        return pos

    def get_all_positions(self, obj=False):
        """ 返回所有的持仓信息 """
        if obj:
            return self.get_all_position_objects()
        else:
            position_list = []
            for x in self.values():
                if x.local_symbol == "":
                    continue
                if x.long_pos != 0:
                    temp = {'exchange': x.exchange, 'direction': "long", 'position_profit': x.long_pnl,
                            'symbol': x.local_symbol, 'local_symbol': x.local_symbol, 'price': x.long_price,
                            'volume': x.long_pos, 'yd_volume': x.long_yd, "frozen": x.long_pos_frozen,
                            "available": x.long_pos - x.long_pos_frozen, 'float_pnl': x.long_stare_pnl}
                    if x.long_pos == x.long_yd:
                        temp['position_date'] = 2
                    elif x.long_pos != x.long_yd:
                        temp['position_date'] = 1
                    position_list.append(temp)
                if x.short_pos != 0:
                    temp = {'exchange': x.exchange, 'direction': "short", 'position_profit': x.short_pnl,
                            'symbol': x.local_symbol, 'local_symbol': x.local_symbol, 'price': x.short_price,
                            'volume': x.short_pos, 'yd_volume': x.short_yd, "frozen": x.short_pos_frozen,
                            "available": x.short_pos - x.short_pos_frozen, 'float_pnl': x.short_stare_pnl}
                    if x.short_pos == x.short_yd:
                        temp['position_date'] = 2
                    elif x.short_pos != x.short_yd:
                        temp['position_date'] = 1
                    position_list.append(temp)
            return position_list

    @property
    def length(self):
        return len(self)

    def len(self):
        return len(self)
