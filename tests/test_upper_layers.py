# -*- coding: utf-8 -*-
"""ctpbee 上层功能模拟测试(不依赖 CTP 回调与真实 Redis)。

覆盖: constant 数据对象与 frozen 保护 → helpers.call 分发 → Recorder
全链路(假 app + 隔离的全局信号) → 本地持仓(成交分支/冻结/拆单/今昨
转换) → DDDR/UDDR 序列化往返 → func(Hickey 时段/交易日/请求构造) →
CtpbeeApi 事件分发(route/register/subscribe)。
直接运行: python tests/test_upper_layers.py
"""
import logging
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ctpbee.signals as signal_mod  # noqa: E402
from ctpbee import dumps, loads  # noqa: E402
from ctpbee.config import Config  # noqa: E402
from ctpbee.constant import (  # noqa: E402
    ACTIVE_STATUSES, AccountData, BarData, CancelRequest, ContractData, Direction,
    Event, Exchange, Offset, OrderData, OrderRequest, PositionData, Status,
    TickData, TradeData, ToolRegisterType, EVENT_ACCOUNT, EVENT_BAR, EVENT_CONTRACT,
    EVENT_INIT_FINISHED, EVENT_ORDER, EVENT_POSITION, EVENT_TICK, EVENT_TIMER,
    EVENT_TRADE,
)
from ctpbee.func import Helper, get_current_trade_day, hickey, join_path  # noqa: E402
from ctpbee.level import CtpbeeApi, Tool  # noqa: E402
from ctpbee.record import Recorder  # noqa: E402
from ctpbee.stream import DDDR, UDDR  # noqa: E402

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))


def tick(price=15345.0, symbol="ag2612", exchange=Exchange.SHFE):
    return TickData(symbol=symbol, exchange=exchange, last_price=price,
                    pre_settlement_price=15310.0, gateway_name="ctp")


def order(order_id=1, status=Status.NOTTRADED, symbol="ag2612",
          direction=Direction.LONG, offset=Offset.OPEN, volume=2, price=15345.0):
    return OrderData(symbol=symbol, exchange="SHFE", order_id=order_id,
                     gateway_name="ctp", status=status, direction=direction,
                     offset=offset, volume=volume, price=price)


def trade(order_id=1, tradeid="T1", direction=Direction.LONG,
          offset=Offset.OPEN, volume=2, price=15345.0):
    return TradeData(symbol="ag2612", exchange="SHFE", order_id=order_id,
                     tradeid=tradeid, gateway_name="ctp", direction=direction,
                     offset=offset, volume=volume, price=price)


def contract(symbol="ag2612", size=15.0):
    return ContractData(symbol=symbol, exchange=Exchange.SHFE, size=size,
                        pricetick=1.0, net_position=False, gateway_name="ctp")


# ================================================================== #
# A. constant: 数据对象
# ================================================================== #
t = tick()
check("A1 TickData 派生 local_symbol", t.local_symbol == "ag2612.SHFE")
o = order(order_id=123)
check("A2 OrderData 派生 local_order_id/local_symbol",
      o.local_order_id == "ctp.123" and o.local_symbol == "ag2612.SHFE")
active_status = next(iter(ACTIVE_STATUSES))
# 注意上游约定: OrderData.local_symbol 直接拼 exchange(字符串),
# 而 CancelRequest.__post_init__ 需要 exchange.value(枚举)——
# 撤单请求的构造单独用枚举 exchange 验证
o_enum = OrderData(symbol="ag2612", exchange=Exchange.SHFE, order_id=123,
                   gateway_name="ctp", status=Status.NOTTRADED,
                   direction=Direction.LONG, offset=Offset.OPEN,
                   volume=2, price=1.0)
check("A3 _is_active 按状态判定 + 撤单请求构造",
      order(status=active_status)._is_active() is True
      and order(status=Status.ALLTRADED)._is_active() is False
      and o_enum.create_cancel_request().order_id == 123
      and o_enum.local_symbol == "ag2612.SHFE")  # 枚举路径同样产出纯代码

# A7: 字符串 exchange 的 OrderData 也能安全撤单(排掉 CancelRequest 枚举专属的雷)
o_str = order(order_id=456)
creq = o_str.create_cancel_request()
check("A7 字符串 exchange 的撤单请求构造(原本此处 AttributeError)",
      creq.order_id == 456 and creq.local_symbol == "ag2612.SHFE")
try:
    o.last_price = 1.0  # 公开函数名 → frozen 拒绝
    ok = False
except AttributeError:
    ok = True
check("A4 数据对象 frozen 保护(公开函数拒写)", ok)
p = PositionData(symbol="ag2612", exchange=Exchange.SHFE,
                 direction=Direction.LONG, volume=2, yd_volume=1,
                 price=15300.0, pnl=90.0, open_price=15300.0, gateway_name="ctp")
# 怪癖锁存: direction 是 f-string 直拼枚举 → str(enum) 形式
check("A5 PositionData 派生 local_position_id(str(enum) 形式)",
      p.local_position_id == "ag2612.SHFE.Direction.LONG")
ev = Event(type=EVENT_TICK, data=t)
check("A6 Event 构造与 str", "tick" in str(ev))

# ================================================================== #
# B/C. Recorder 全链路(假 app + 隔离信号)
# ================================================================== #
class FakeConfig(dict):
    def get(self, k, d=None):
        return dict.get(self, k, d)


class FakeApp:
    def __init__(self):
        self.config = FakeConfig()
        self.tools = {}
        self._extensions = {}
        self.app_signal = signal_mod.AppSignal("fake_app")
        self.logger = logging.getLogger("test_app")
        self.recorder = None

    def get_contract(self, local_symbol):
        return self.recorder.get_contract(local_symbol)


class CountingApi(CtpbeeApi):
    def __init__(self, name, app=None):
        super().__init__(name, app=app)
        self.ticks = self.orders = self.trades = self.positions = 0
        self.accounts = self.contracts = self.inits = 0

    def on_tick(self, tick):
        self.ticks += 1

    def on_order(self, o):
        self.orders += 1

    def on_trade(self, tr):
        self.trades += 1

    def on_position(self, pos):
        self.positions += 1

    def on_account(self, acc):
        self.accounts += 1

    def on_contract(self, c):
        self.contracts += 1

    def on_init(self, init):
        self.inits += 1


class CountingTool(Tool):
    def __init__(self, name):
        super().__init__(name)
        self.ticks = 0

    def on_tick(self, tick):
        self.ticks += 1
        return tick.last_price


_orig_common = signal_mod.common_signals
signal_mod.common_signals = signal_mod.CommonSignal()
try:
    app = FakeApp()
    app.recorder = Recorder(app)
    api = CountingApi("counting")
    app._extensions["counting"] = api
    tool = CountingTool("ctool")
    app.tools["ctool"] = tool

    t1, t2 = tick(15345.0), tick(15346.0)
    app.recorder.process_tick_event(Event(type=EVENT_TICK, data=t1))
    app.recorder.process_tick_event(Event(type=EVENT_TICK, data=t2))
    check("B1 tick 分发到 extension 与 tool 双路",
          api.ticks == 2 and tool.ticks == 2)
    check("B2 Recorder 保存最新 tick / 查询接口",
          app.recorder.get_tick("ag2612.SHFE") is t2
          and app.recorder.get_last_price("ag2612.SHFE") == 15346.0)

    oa = order(1, status=Status.NOTTRADED)
    ob = order(1, status=Status.ALLTRADED)
    app.recorder.process_order_event(Event(type=EVENT_ORDER, data=oa))
    check("B3 活动报单入 active_orders(键=local_order_id)",
          "ctp.1" in app.recorder.active_orders and api.orders == 1)
    app.recorder.process_order_event(Event(type=EVENT_ORDER, data=ob))
    check("B4 终态报单移出 active_orders",
          "ctp.1" not in app.recorder.active_orders
          and app.recorder.get_order("ctp.1") is ob
          and app.recorder.order_amount == 1)

    app.recorder.process_trade_event(Event(type=EVENT_TRADE, data=trade()))
    check("B5 成交分发与查询", api.trades == 1
          and app.recorder.get_trade("ctp.T1") is not None)

    # position 走 @call 分发; account/contract 是无装饰的手动遍历——两种殊途同归
    app.recorder.process_position_event(Event(type=EVENT_POSITION, data=p))
    check("B6 持仓事件更新管理器并分发扩展",
          api.positions == 1 and "ag2612.SHFE.Direction.LONG" in app.recorder.positions)

    acc = AccountData(gateway_name="ctp", accountid="001", balance=100.0, available=80.0)
    app.recorder.process_account_event(Event(type=EVENT_ACCOUNT, data=acc))
    check("B7 账户事件分发", api.accounts == 1
          and app.recorder.get_account() is acc)

    c1 = contract()
    app.recorder.process_contract_event(Event(type=EVENT_CONTRACT, data=c1))
    check("B8 合约事件分发与查询", api.contracts == 1
          and app.recorder.get_contract("ag2612.SHFE") is c1)

    # INSTRUMENT_INDEPEND: 只把命中的行情给对应策略
    app.config["INSTRUMENT_INDEPEND"] = True
    api.instrument_set = {"ag2612.SHFE"}
    app.recorder.process_tick_event(Event(type=EVENT_TICK, data=tick()))
    check("B9 INSTRUMENT_INDEPEND 命中订阅集合才分发", api.ticks == 3)
    sn = tick(symbol="sn2609", exchange=Exchange.SHFE)
    app.recorder.process_tick_event(Event(type=EVENT_TICK, data=sn))
    check("B10 未命中订阅集合不分发(但 Recorder 照常存储)",
          api.ticks == 3 and app.recorder.get_tick("sn2609.SHFE") is sn)
    del app.config["INSTRUMENT_INDEPEND"]
    api.instrument_set = set()

    # init 事件只触发一次 on_init
    app.recorder.process_init_event(Event(type=EVENT_INIT_FINISHED, data=True))
    app.recorder.process_init_event(Event(type=EVENT_INIT_FINISHED, data=True))
    check("B11 INIT_FINISHED 只触发一次 on_init", api.inits == 1)

    # timer → on_realtime 经 @call 到 extensions
    api2_ticks = api.ticks
    app.recorder.process_timer_event(Event(type=EVENT_TIMER, data=None))
    check("B12 timer 事件不误伤 tick 计数", api.ticks == api2_ticks)

    # last 事件 → 最新价映射 + 主力合约聚合
    from ctpbee.constant import LastData  # noqa: E402
    ld = LastData(symbol="ag2612", exchange=Exchange.SHFE, last_price=15350.0,
                  open_interest=100, pre_open_interest=90, volume=10,
                  gateway_name="ctp")
    app.recorder.process_last_event(Event(type="last", data=ld))
    # 聚合键 = 去数字后大写("ag2612.SHFE" → "AG.SHFE")
    check("B13 last 事件维护最新价映射",
          app.recorder.get_contract_last_price("ag2612.SHFE") == 15350.0
          and "ag2612.SHFE" in [x.local_symbol for x in
                                app.recorder.main_contract_mapping.get("AG.SHFE", [])])

    check("B14 get_all_ticks 返回列表(每合约一条)", len(app.recorder.get_all_ticks()) == 2)
    app.recorder.clear_all()
    check("B15 clear_all 清空", len(app.recorder.ticks) == 0
          and len(app.recorder.orders) == 0)

    # CtpbeeApi.__call__ 直发
    api3 = CountingApi("direct")
    api3(Event(type=EVENT_TICK, data=tick()))
    api3(Event(type=EVENT_INIT_FINISHED, data=True))
    api3(Event(type=EVENT_INIT_FINISHED, data=True))
    check("C1 __call__ 按事件类型分发且 init 只一次",
          api3.ticks == 1 and api3.inits == 1)

    # route 装饰器
    api4 = CountingApi("routed")
    @api4.route(handler="tick")
    def my_tick(self, tk):
        self.ticks += 100
    api4(Event(type=EVENT_TICK, data=tick()))
    check("C2 route 装饰器覆盖处理器", api4.ticks == 100)

    # register 装饰器绑定方法
    api5 = CountingApi("regd")
    @api5.register()
    def hello(self):
        return "hi"
    check("C3 register 绑定实例方法", api5.hello() == "hi")

    # subscribe 未注册工具(需绑定 app 才能查 tools)
    api_sub = CountingApi("sub_test")
    api_sub.init_app(app)
    try:
        api_sub.subscribe("no_such_tool", lambda x: x, ToolRegisterType.TICK)
        ok = False
    except ValueError:
        ok = True
    check("C4 subscribe 未注册工具显式报错", ok)

    # __repr__ 不抛异常即可(Recorder/Tool 均无自定义 repr)
    check("C5 Recorder/Tool repr 不抛异常",
          isinstance(repr(app.recorder), str) and isinstance(repr(tool), str))
finally:
    signal_mod.common_signals = _orig_common

# ================================================================== #
# D. 本地持仓: 成交分支/冻结/拆单/今昨转换
# ================================================================== #
from ctpbee.data_handle.local_position import (  # noqa: E402
    LocalPositionManager, PositionHolding,
)


def holding(symbol="ag2612.SHFE", size=15.0):
    return PositionHolding(symbol, contract=SimpleNamespace(size=size))


_mgr_d = LocalPositionManager(app=None)


def yesterday(h, **kw):
    """今仓转昨仓要经 LocalPositionManager(方法在 Manager 而非 Holding 上)。"""
    _mgr_d[h.local_symbol] = h
    _mgr_d.covert_to_yesterday_holding(**kw)


h = holding()
h.update_trade(trade(volume=2, price=15300.0))            # 多开 2
h.update_trade(trade(volume=3, price=15400.0, direction=Direction.SHORT,
                     offset=Offset.OPEN))                   # 空开 3
check("D1 双向开仓持仓与均价(加权)",
      h.long_pos == 2 and h.short_pos == 3
      and h.long_price == 15300.0 and h.short_price == 15400.0)

# 非上期所 CLOSE 优先平今, td 不够溢出到 yd
h2 = PositionHolding("ma601.DCE", contract=SimpleNamespace(size=10.0))
h2.update_trade(trade(volume=2, price=2500.0, direction=Direction.SHORT, offset=Offset.OPEN))
h2.update_trade(trade(volume=3, price=2500.0, direction=Direction.SHORT, offset=Offset.OPEN))
yesterday(h2)                                              # 5 手全转昨仓
h2.update_trade(trade(volume=4, price=2500.0, direction=Direction.LONG, offset=Offset.CLOSE))
check("D2 非SHFE CLOSE 优先平今并溢出昨仓",
      h2.short_td == 0 and h2.short_yd == 1 and h2.short_pos == 1)

# SHFE CLOSE 等同平昨
h3 = holding()
h3.update_trade(trade(volume=2, price=15300.0, direction=Direction.SHORT, offset=Offset.OPEN))
yesterday(h3)
h3.update_trade(trade(volume=1, price=15300.0, direction=Direction.LONG, offset=Offset.CLOSE))
check("D3 SHFE CLOSE 直接平昨", h3.short_yd == 1 and h3.short_td == 0)

# 活动报单冻结
h4 = holding()
h4.update_trade(trade(volume=2, price=15300.0, direction=Direction.SHORT, offset=Offset.OPEN))
h4.update_trade(trade(volume=3, price=15300.0, direction=Direction.SHORT, offset=Offset.OPEN))
yesterday(h4)
oa = OrderData(symbol="ag2612", exchange="SHFE", order_id=9,
               gateway_name="ctp", status=Status.NOTTRADED,
               direction=Direction.LONG, offset=Offset.CLOSE,
               volume=4, price=1.0, traded=1)
h4.update_order(oa)
check("D4 今仓为 0 时平仓冻结全部落昨仓",
      h4.short_td_frozen == 0 and h4.short_yd_frozen == 3
      and h4.short_pos_frozen == 3)

# SHFE 拆单
h5 = holding()
# 混合今昨仓 td=2/yd=3——转换路径会把今仓清零, 故直写字段构造拆单场景
h5.short_td, h5.short_yd, h5.short_pos = 2, 3, 5
req = OrderRequest(symbol="ag2612", exchange=Exchange.SHFE,
                   direction=Direction.LONG, offset=Offset.CLOSE,
                   volume=3, price=1.0)
split = h5.convert_order_request_shfe(req)
check("D5 SHFE 平仓拆单: 今2昨1",
      len(split) == 2
      and [(r.offset, r.volume) for r in split] ==
      [(Offset.CLOSETODAY, 2), (Offset.CLOSEYESTERDAY, 1)])
req_all_today = OrderRequest(symbol="ag2612", exchange=Exchange.SHFE,
                             direction=Direction.LONG, offset=Offset.CLOSE,
                             volume=2, price=1.0)
check("D6 SHFE 平仓全为今仓时不拆",
      [r.offset for r in h5.convert_order_request_shfe(req_all_today)] == [Offset.CLOSETODAY])
req_over = OrderRequest(symbol="ag2612", exchange=Exchange.SHFE,
                        direction=Direction.LONG, offset=Offset.CLOSE,
                        volume=9, price=1.0)
check("D7 超出可用持仓拒单(空列表)", h5.convert_order_request_shfe(req_over) == [])

# 锁仓转换: 有今仓 → 直接开仓
h6 = holding()
h6.update_trade(trade(volume=1, price=1.0, direction=Direction.SHORT, offset=Offset.OPEN))
req_lock = OrderRequest(symbol="ag2612", exchange=Exchange.SHFE,
                        direction=Direction.LONG, offset=Offset.CLOSE,
                        volume=2, price=1.0)
check("D8 锁仓转换: 存在今仓时直接开仓",
      [r.offset for r in h6.convert_order_request_lock(req_lock)] == [Offset.OPEN])

# 今昨转换 + 均价重置
h7 = holding()
h7.update_trade(trade(volume=2, price=15300.0, direction=Direction.LONG, offset=Offset.OPEN))
h7.update_trade(trade(volume=3, price=15400.0, direction=Direction.LONG, offset=Offset.OPEN))
yesterday(h7, **{"ag2612.SHFE": 15310.0})
check("D9 今仓转昨仓 + 结算价重置均价",
      h7.long_yd == 5 and h7.long_td == 0 and h7.long_price == 15310.0
      and h7.long_pnl == 0)

# PositionData 视图
h8 = holding()
h8.update_trade(trade(volume=2, price=15300.0, direction=Direction.LONG, offset=Offset.OPEN))
h8.update_tick(tick(15345.0), 15310.0)
pd_long = h8.get_position_by_direction(Direction.LONG)
check("D10 持仓视图(PositionData)字段",
      pd_long.volume == 2 and pd_long.pnl == round(2 * 45 * 15)
      and pd_long.float_pnl == 2 * 45 * 15)
mgr = LocalPositionManager(app=None)
mgr["ag2612.SHFE"] = h8
positions = mgr.get_all_positions()
check("D11 get_all_positions 字典视图与 position_date",
      len(positions) == 1 and positions[0]["volume"] == 2
      and positions[0]["position_date"] == 1)

# ================================================================== #
# E. DDDR/UDDR 序列化往返
# ================================================================== #
# 注意上游怪癖(stream.py fixme 注释自认): loads 直接还原对象而非 dict,
# 因此 DDDR.encode→DDDR(parse=True) 不自洽——parse 分支嗅探需要纯 dict
# 载荷, 以下用手工构造的 dict 载荷锁存各嗅探分支行为。
import json as _json  # noqa: E402


def dddr_parse(data_dict, index=1):
    return DDDR(_json.dumps({"data": _json.dumps(data_dict), "index": index}),
                parse=True)


for obj, name in [(tick(), "TickData"), (order(), "OrderData"),
                  (trade(), "TradeData"), (contract(), "ContractData")]:
    payload = UDDR(obj, index=3, parse=False).encode()
    back = UDDR(payload, parse=True)
    check(f"E1 {name} UDDR 往返(类型+索引)",
          type(back.obj).__name__ == name and back.index == 3)

dr = DDDR(obj=tick(), index=5)
outer = _json.loads(dr.encode())
check("E2 DDDR encode 结构(index 保留, data 为序列化产物)",
      outer["index"] == 5 and "data" in outer)

po = dddr_parse({"order_id": 1, "symbol": "ag2612", "exchange": "SHFE",
                 "gateway_name": "ctp"})
check("E3 DDDR order 嗅探分支", type(po.order).__name__ == "OrderData"
      and po.order.order_id == 1)
pt = dddr_parse({"order_id": 1, "tradeid": "T1", "symbol": "ag2612",
                 "exchange": "SHFE", "gateway_name": "ctp"})
check("E4 DDDR trade 嗅探分支(order_id+tradeid 优先于 order)",
      type(pt.order).__name__ == "TradeData" and pt.order.tradeid == "T1")
pc = dddr_parse({"pricetick": 1.0, "size": 15.0, "symbol": "ag2612",
                 "exchange": "SHFE", "gateway_name": "ctp"})
check("E5 DDDR contract 嗅探分支(pricetick+size)", pc.order.size == 15.0)
check("E6 DDDR 未知形状 → None", dddr_parse({"foo": 1}).order is None)
check("E7 jsond dumps/loads 直接往返", loads(dumps(tick())).symbol == "ag2612")
check("E8 UDDR 坏消息不抛", UDDR("{bad", parse=True).obj is None)

# E9: encode→parse 自洽(loads 还原实体对象时直接采用, 不再要求 dict)
for obj, key, want in [(tick(), "last_price", 15345.0), (order(), "order_id", 1),
                       (trade(), "tradeid", "T1"), (contract(), "size", 15.0)]:
    back = DDDR(DDDR(obj=obj, index=11).encode(), parse=True)
    check(f"E9 {type(obj).__name__} DDDR encode→parse 往返",
          type(back.order).__name__ == type(obj).__name__
          and getattr(back.order, key) == want and back.index == 11)

# ================================================================== #
# F. func: Hickey 时段 / 交易日 / 请求构造
# ================================================================== #
from datetime import datetime as dt  # noqa: E402


def at(day, h, m):
    return dt(2026, 8, day, h, m) if day else dt(2026, 8, day, h, m)


FRI, SAT = 21, 22  # 2026-08-21 周五(交易日), 08-22 周六
check("F1 auth_time 交易日白盘", hickey.auth_time(at(FRI, 10, 0)) is True)
check("F2 auth_time 交易日夜盘", hickey.auth_time(at(FRI, 21, 30)) is True)
check("F3 auth_time 周六凌晨(周五夜延续)", hickey.auth_time(at(SAT, 1, 0)) is True)
check("F4 auth_time 周六白天(休市)", hickey.auth_time(at(SAT, 10, 0)) is False)
check("F5 auth_time 交易日 03:00(休市间隙)", hickey.auth_time(at(FRI, 3, 0)) is False)

check("F6 get_current_trade_day 白盘归当日",
      get_current_trade_day(at(FRI, 10, 0)) == "2026-08-21")
check("F7 收盘后归下一交易日",
      get_current_trade_day(at(FRI, 15, 30)) == "2026-08-24")
check("F8 周六凌晨归下一交易日",
      get_current_trade_day(at(SAT, 1, 0)) == "2026-08-24")

req = Helper.generate_order_req_by_str(
    "ag2612", "SHFE", "long", "open", "limit", 2, 15345.0)
check("F9 Helper 生成发单请求",
      req.symbol == "ag2612" and req.exchange == Exchange.SHFE
      and req.direction == Direction.LONG and req.offset == Offset.OPEN)
creq = Helper.generate_cancel_req_by_str("ag2612", "SHFE", "123")
check("F10 Helper 生成撤单请求", creq.order_id == "123")
check("F11 join_path", join_path("a", "b", "c").endswith(os.path.join("b", "c")))

# ================================================================== #
# G. Config 其他导入方式
# ================================================================== #
cfg = Config(root_path=".")


class Defaults:
    TD_FUNC = True
    SHARE_MD = False


cfg.from_object(Defaults())
cfg.from_mapping({"MD_FUNC": True})
check("G1 from_object/from_mapping", cfg["TD_FUNC"] is True
      and cfg["SHARE_MD"] is False and cfg["MD_FUNC"] is True)
check("G2 from_mapping 过滤非大写键", cfg.from_mapping({"x": 1}) is True
      and "x" not in cfg)

print()
failed = [r for r in results if not r[1]]
print(f"{'=' * 60}\n{len(results) - len(failed)}/{len(results)} 通过")
sys.exit(1 if failed else 0)
