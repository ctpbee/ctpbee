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

from ctpbee.constant import (
    PositionData,
    Offset,
    Direction,
    OrderRequest,
    OrderData,
    Exchange,
    TickData,
    EXCHANGE_MAPPING,
    BarData,
)


class PositionModel:
    """单个合约的持仓模型"""

    def __init__(self, local_symbol, contract=None):
        """初始化持仓对象"""
        self.local_symbol = local_symbol
        try:
            self.exchange = local_symbol.split(".")[1]
            self.symbol = local_symbol.split(".")[0]
        except Exception:
            raise ValueError("invalid local_symbol")
        # 使用字典存储活跃订单，减少属性数量
        self.active_orders = {}
        # 合约大小
        if contract is None:
            warnings.warn(
                "no size passed please check your contract! contract will be fixed to 10"
            )
            self.size = 10
        else:
            self.size = contract.size

        # 持仓数据存储 - 使用更紧凑的结构
        self.long = {
            "pos": 0,  # 总持仓
            "yd": 0,  # 昨仓
            "td": 0,  # 今仓
            "price": 0,  # 持仓均价
            "open_price": 0,  # 开仓均价
            "pnl": 0,  # 盈亏
            "float_pnl": 0,  # 浮动盈亏
            "frozen": 0,  # 冻结数量
            "yd_frozen": 0,  # 昨仓冻结
            "td_frozen": 0,  # 今仓冻结
        }

        self.short = {
            "pos": 0,  # 总持仓
            "yd": 0,  # 昨仓
            "td": 0,  # 今仓
            "price": 0,  # 持仓均价
            "open_price": 0,  # 开仓均价
            "pnl": 0,  # 盈亏
            "float_pnl": 0,  # 浮动盈亏
            "frozen": 0,  # 冻结数量
            "yd_frozen": 0,  # 昨仓冻结
            "td_frozen": 0,  # 今仓冻结
        }

        # 行情数据
        self.last_price = 0
        self.pre_settlement_price = 0

        # 缓存计算结果
        self._cached_long_available = 0
        self._cached_short_available = 0
        self._cache_valid = False

    @property
    def long_pos(self):
        return self.long["pos"]

    @property
    def short_pos(self):
        return self.short["pos"]

    @property
    def long_pos_frozen(self):
        return self.long["frozen"]

    @property
    def short_pos_frozen(self):
        return self.short["frozen"]

    @property
    def long_td(self):
        return self.long["td"]

    @property
    def short_td(self):
        return self.short["td"]

    @property
    def long_yd(self):
        return self.long["yd"]

    @property
    def short_yd(self):
        return self.short["yd"]

    @property
    def long_available(self):
        if not self._cache_valid:
            self._update_cache()
        return self._cached_long_available

    @property
    def short_available(self):
        if not self._cache_valid:
            self._update_cache()
        return self._cached_short_available

    @property
    def long_open_price(self):
        return self.long["open_price"]

    @property
    def long_hold_price(self):
        return self.long["price"]

    @property
    def short_open_price(self):
        return self.short["open_price"]

    @property
    def short_hold_price(self):
        return self.short["price"]

    def __repr__(self) -> str:
        return str(self.to_dict())

    def __str__(self) -> str:
        return str(self.to_dict())

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "exchange": self.exchange,
            "long_pos": self.long_pos,
            "long_pos_frozen": self.long_pos_frozen,
            "long_td": self.long_td,
            "long_yd": self.long_yd,
            "long_available": self.long_available,
            "long_open_price": self.long_open_price,
            "long_hold_price": self.long_hold_price,
            "long_pnl": self.long["pnl"],
            "short_pos": self.short_pos,
            "short_pos_frozen": self.short_pos_frozen,
            "short_td": self.short_td,
            "short_yd": self.short_yd,
            "short_available": self.short_available,
            "short_open_price": self.short_open_price,
            "short_hold_price": self.short_hold_price,
            "short_pnl": self.short["pnl"],
        }

    def _update_cache(self):
        """更新缓存"""
        self._cached_long_available = self.long["pos"] - self.long["frozen"]
        self._cached_short_available = self.short["pos"] - self.short["frozen"]
        self._cache_valid = True

    def _calculate_position(self):
        """计算总持仓"""
        self.long["pos"] = self.long["td"] + self.long["yd"]
        self.short["pos"] = self.short["td"] + self.short["yd"]
        self._cache_valid = False

    def _calculate_frozen(self):
        """计算冻结数量"""
        # 重置冻结数量
        self.long["frozen"] = 0
        self.long["yd_frozen"] = 0
        self.long["td_frozen"] = 0
        self.short["frozen"] = 0
        self.short["yd_frozen"] = 0
        self.short["td_frozen"] = 0

        # 遍历活跃订单计算冻结数量
        for order in self.active_orders.values():
            if order.offset == Offset.OPEN:
                continue

            frozen = order.volume - order.traded

            if order.direction == Direction.LONG:
                # 多头平仓，冻结空头仓位
                if order.offset == Offset.CLOSETODAY:
                    self.short["td_frozen"] += frozen
                elif order.offset == Offset.CLOSEYESTERDAY:
                    self.short["yd_frozen"] += frozen
                elif order.offset == Offset.CLOSE:
                    # 优先平今
                    self.short["td_frozen"] += frozen
                    if self.short["td_frozen"] > self.short["td"]:
                        excess = self.short["td_frozen"] - self.short["td"]
                        self.short["yd_frozen"] += excess
                        self.short["td_frozen"] = self.short["td"]
            else:
                # 空头平仓，冻结多头仓位
                if order.offset == Offset.CLOSETODAY:
                    self.long["td_frozen"] += frozen
                elif order.offset == Offset.CLOSEYESTERDAY:
                    self.long["yd_frozen"] += frozen
                elif order.offset == Offset.CLOSE:
                    # 优先平今
                    self.long["td_frozen"] += frozen
                    if self.long["td_frozen"] > self.long["td"]:
                        excess = self.long["td_frozen"] - self.long["td"]
                        self.long["yd_frozen"] += excess
                        self.long["td_frozen"] = self.long["td"]

        # 更新总冻结数量
        self.long["frozen"] = self.long["td_frozen"] + self.long["yd_frozen"]
        self.short["frozen"] = self.short["td_frozen"] + self.short["yd_frozen"]
        self._cache_valid = False

    def _calculate_pnl(self):
        """计算浮动盈亏"""
        # 多头盈亏
        if self.long["pos"] > 0:
            self.long["pnl"] = round(
                self.long["pos"] * (self.last_price - self.long["price"]) * self.size
            )
        else:
            self.long["pnl"] = 0

        # 空头盈亏
        if self.short["pos"] > 0:
            self.short["pnl"] = round(
                self.short["pos"] * (self.short["price"] - self.last_price) * self.size
            )
        else:
            self.short["pnl"] = 0

    def _calculate_float_pnl(self):
        """计算浮动盈亏"""
        # 多头浮动盈亏
        if self.long["pos"] > 0:
            self.long["float_pnl"] = (
                self.long["pos"]
                * (self.last_price - self.long["open_price"])
                * self.size
            )
        else:
            self.long["float_pnl"] = 0

        # 空头浮动盈亏
        if self.short["pos"] > 0:
            self.short["float_pnl"] = (
                self.short["pos"]
                * (self.short["open_price"] - self.last_price)
                * self.size
            )
        else:
            self.short["float_pnl"] = 0

    def _calculate_price(self, trade):
        """计算持仓均价"""
        if trade.offset != Offset.OPEN:
            return

        if trade.direction == Direction.LONG:
            pos = self.long
            current_pos = self.long["pos"]
        else:
            pos = self.short
            current_pos = self.short["pos"]

        # 计算新的持仓均价和开仓均价
        new_pos = current_pos + trade.volume
        if new_pos > 0:
            pos["price"] = (
                pos["price"] * current_pos + trade.volume * trade.price
            ) / new_pos
            pos["open_price"] = (
                pos["open_price"] * current_pos + trade.volume * trade.price
            ) / new_pos
        else:
            pos["price"] = 0
            pos["open_price"] = 0

    def _update_trade(self, trade):
        """成交更新"""
        # 处理多头交易
        if trade.direction == Direction.LONG:
            if trade.offset == Offset.OPEN:
                # 多头开仓
                self.long["td"] += trade.volume
            elif trade.offset == Offset.CLOSETODAY:
                # 平今空头
                self.short["td"] -= trade.volume
            elif trade.offset == Offset.CLOSEYESTERDAY:
                # 平昨空头
                self.short["yd"] -= trade.volume
            elif trade.offset == Offset.CLOSE:
                # 平仓
                if self.exchange == Exchange.SHFE:
                    # 上期所平昨
                    self.short["yd"] -= trade.volume
                else:
                    # 其他交易所优先平今
                    self.short["td"] -= trade.volume
                    if self.short["td"] < 0:
                        excess = self.short["td"]
                        self.short["yd"] += excess
                        self.short["td"] = 0
        # 处理空头交易
        else:
            if trade.offset == Offset.OPEN:
                # 空头开仓
                self.short["td"] += trade.volume
            elif trade.offset == Offset.CLOSETODAY:
                # 平今多头
                self.long["td"] -= trade.volume
            elif trade.offset == Offset.CLOSEYESTERDAY:
                # 平昨多头
                self.long["yd"] -= trade.volume
            elif trade.offset == Offset.CLOSE:
                # 平仓
                if self.exchange == Exchange.SHFE:
                    # 上期所平昨
                    self.long["yd"] -= trade.volume
                else:
                    # 其他交易所优先平今
                    self.long["td"] -= trade.volume
                    if self.long["td"] < 0:
                        excess = self.long["td"]
                        self.long["yd"] += excess
                        self.long["td"] = 0

        # 计算总持仓
        self._calculate_position()
        # 更新持仓均价
        self._calculate_price(trade)
        # 更新盈亏
        self._calculate_pnl()
        self._calculate_float_pnl()

    def _update_position(self, position: PositionData):
        """持仓更新"""
        if position.direction == Direction.LONG:
            pos = self.long
            pos["pos"] = position.volume
            pos["yd"] = position.yd_volume
            pos["td"] = pos["pos"] - pos["yd"]
            pos["pnl"] = position.pnl
            pos["price"] = position.price
            pos["open_price"] = position.open_price
        elif position.direction == Direction.SHORT:
            pos = self.short
            pos["pos"] = position.volume
            pos["yd"] = position.yd_volume
            pos["td"] = pos["pos"] - pos["yd"]
            pos["pnl"] = position.pnl
            pos["price"] = position.price
            pos["open_price"] = position.open_price

        self._cache_valid = False

    def _update_order(self, order: OrderData):
        """订单更新"""
        if order._is_active():
            self.active_orders[order.local_order_id] = order
        else:
            self.active_orders.pop(order.local_order_id, None)

        # 重新计算冻结数量
        self._calculate_frozen()

    def _update_order_request(self, req: OrderRequest, local_order_id: str):
        """订单请求更新"""
        gateway_name, orderid = local_order_id.split(".")
        order = req._create_order_data(orderid, gateway_name)
        self._update_order(order)

    def _update_tick(self, tick, pre_settlement_price):
        """行情更新"""
        self.last_price = tick.last_price
        self.pre_settlement_price = pre_settlement_price

        # 更新盈亏
        self._calculate_pnl()
        self._calculate_float_pnl()

    def _update_bar(self, bar, pre_close):
        """K线更新"""
        self.last_price = bar.close_price
        self.pre_settlement_price = pre_close

        # 更新盈亏
        self._calculate_pnl()
        self._calculate_float_pnl()

    def _convert_order_request_shfe(self, req: OrderRequest):
        """上期所订单转换"""
        if req.offset == Offset.OPEN:
            return [req]

        if req.direction == Direction.LONG:
            pos_available = self.short_available
            td_available = self.short["td"] - self.short["td_frozen"]
        else:
            pos_available = self.long_available
            td_available = self.long["td"] - self.long["td_frozen"]

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

    def _convert_order_request_lock(self, req: OrderRequest):
        """锁仓订单转换"""
        if req.direction == Direction.LONG:
            td_volume = self.short["td"]
            yd_available = self.short["yd"] - self.short["yd_frozen"]
        else:
            td_volume = self.long["td"]
            yd_available = self.long["yd"] - self.long["yd_frozen"]

        # 如果有今仓，只能锁仓
        if td_volume:
            req_open = copy(req)
            req_open.offset = Offset.OPEN
            return [req_open]
        # 否则先平昨仓，再开新仓
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

    def _get_position_by_direction(self, direction):
        """根据方向获取持仓数据"""
        if direction == Direction.LONG:
            return self._to_position_data(self.long, direction)
        elif direction == Direction.SHORT:
            return self._to_position_data(self.short, direction)
        return None

    def _to_position_data(self, pos_dict, direction):
        """将持仓字典快速转换为PositionData对象"""
        return PositionData(
            symbol=self.symbol,
            volume=pos_dict["pos"],
            exchange=EXCHANGE_MAPPING[self.exchange],
            direction=direction,
            pnl=pos_dict["pnl"],
            price=pos_dict["price"],
            frozen=pos_dict["frozen"],
            open_price=pos_dict["open_price"],
            yd_volume=pos_dict["yd"],
            float_pnl=pos_dict["float_pnl"],
        )

    def to_position_data(self, direction=None):
        """
        快速将持仓转换为PositionData对象
        如果未指定direction，则返回包含多空方向的持仓列表
        """
        if direction is None:
            result = []
            if self.long["pos"] > 0:
                result.append(self._to_position_data(self.long, Direction.LONG))
            if self.short["pos"] > 0:
                result.append(self._to_position_data(self.short, Direction.SHORT))
            return result
        else:
            return self._get_position_by_direction(direction)


class LocalPositionManager(dict):
    """用于管理持仓信息 只提供向外的接口"""

    def __init__(self, app):
        super().__init__({})
        self.app = app
        self.size_map = {}

    def update_tick(self, tick: TickData, pre_close):
        """
        更新tick信息更新本地持仓盈亏等数据
        """
        """ 更新tick  """
        holding = self.get(tick.local_symbol)
        if holding:
            holding._update_tick(tick, pre_close)

    def update_bar(self, bar: BarData, pre_close):
        """
        根据k线信息更新本地持仓盈亏
        """
        holding = self.get(bar.local_symbol)
        if holding:
            holding._update_bar(bar, pre_close)

    def is_convert_required(self, local_symbol: str):
        """
        Check if the contract needs offset convert.
        """
        contract = self.get_contract(local_symbol)

        # Only contracts with long-short position mode requires convert
        if not contract:
            return False
        return not getattr(contract, 'net_position', True)

    def update_order_request(self, req: OrderRequest, local_orderid: str):
        """"""
        if not self.is_convert_required(req.local_symbol):
            return

        holding = self.get(req.local_symbol)
        if not holding:
            self[req.local_symbol] = PositionModel(
                req.local_symbol, self.get_contract(req.local_symbol)
            )
            holding = self[req.local_symbol]
        holding._update_order_request(req, local_orderid)

    def convert_order_request(self, req: OrderRequest, lock: bool):
        """"""
        if not self.is_convert_required(req.local_symbol):
            return [req]

        holding = self.get(req.local_symbol)
        if not holding:
            self[req.local_symbol] = PositionModel(
                req.local_symbol, self.get_contract(req.local_symbol)
            )
            holding = self[req.local_symbol]

        if lock:
            return holding._convert_order_request_lock(req)
        elif req.exchange == Exchange.SHFE:
            return holding._convert_order_request_shfe(req)
        else:
            return [req]

    def get_contract(self, local_symbol):
        """获取合约信息"""
        from ctpbee.app import CtpBee

        if self.app is None:
            return None
        elif isinstance(self.app, CtpBee):
            return self.app.recorder.get_contract(local_symbol)
        else:
            return self.app.get_contract(local_symbol)

    def update_order(self, order):
        """更新order"""
        local_symbol = order.local_symbol
        self.setdefault(
            local_symbol, PositionModel(local_symbol, self.get_contract(local_symbol))
        )._update_order(order)

    def update_trade(self, trade):
        """更新成交"""
        local_symbol = trade.local_symbol
        self.setdefault(
            local_symbol, PositionModel(local_symbol, self.get_contract(local_symbol))
        )._update_trade(trade)

    def update_position(self, position):
        """更新持仓"""
        local_symbol = position.local_symbol
        self.setdefault(
            local_symbol, PositionModel(local_symbol, self.get_contract(local_symbol))
        )._update_position(position)

    def update_size_map(self, params):
        """更新size_map"""
        self.size_map = params.get("size_map")

    def covert_to_yesterday_holding(self, **kwargs):
        """将今日持仓转换为昨日持仓"""
        for holding in self.values():
            # 将今仓转为昨仓
            if holding.long["td"] > 0:
                holding.long["yd"] += holding.long["td"]
                holding.long["td"] = 0

            if holding.short["td"] > 0:
                holding.short["yd"] += holding.short["td"]
                holding.short["td"] = 0

            # 重新计算总持仓
            holding._calculate_position()

        # 更新价格和盈亏
        for key, value in kwargs.items():
            holding = self.get(key)
            if not holding:
                continue

            if holding.long["pos"] > 0:
                holding.long["price"] = value
                holding.long["pnl"] = 0
            else:
                holding.long["price"] = 0
                holding.long["pnl"] = 0

            if holding.short["pos"] > 0:
                holding.short["price"] = value
                holding.short["pnl"] = 0
            else:
                holding.short["price"] = 0
                holding.short["pnl"] = 0

    def clear_frozen(self):
        """清空冻结数量"""
        for holding in self.values():
            holding.active_orders.clear()
            holding._calculate_frozen()

    def get_all_position_objects(self):
        """返回PositionData格式的持仓数据"""
        pos_list = []
        for holding in self.values():
            if not holding.local_symbol:
                continue
            # 使用to_position_data方法快速转换
            pos_list.extend(holding.to_position_data())
        return pos_list

    def get_position_by_ld(
        self, local_symbol: str, direction: Direction
    ) -> PositionData:
        """
        ld means local_symbol and direction
        ld意味着local_symbol和direction
        """
        holding: PositionModel = self.get(local_symbol)
        if not holding:
            return None
        return holding._get_position_by_direction(direction)

    def get_position(self, local_symbol):
        """根据local_symbol 获取持仓信息"""
        # holding = self.get(tick.local_symbol)
        model = self.get(local_symbol, None)
        return model

    def get_all_positions(self):
        """返回所有的持仓信息"""
        return [holding for holding in self.values() if holding.local_symbol]

    @property
    def length(self):
        """返回持仓数量"""
        return len(self)

    def len(self):
        """返回持仓数量"""
        return len(self)
