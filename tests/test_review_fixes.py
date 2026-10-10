# -*- coding: utf-8 -*-
"""代码审查修复的回归测试(2026-10-10)。

覆盖以下修复(每项修复前均有可复现的失败):
  F1/F2  suspend_extension / enable_extension 名字改写失效 —— 冻结后事件
         仍被分发(_CtpBee__frozen vs _CtpbeeApi__frozen);
  F3     run_forever 重置的 f_init 属性不存在 —— _reset_init 后 on_init
         重新触发;
  F4     route() 污染同类兄弟实例(类级 map 被改写);
  F5     LocalLooper.cancel_order 直接 order.status = 被 @frozen 拒绝,
         回测撤单抛 AttributeError;
  F6     LocalLooper.cancel_all 迭代 dict key(str), 对其赋属性必崩,
         且不归还冻结保证金/手续费;
  F7     match_deal 只按品种字母过滤 —— ag2412 的挂单被 ag2501 的行情
         价格成交(跨月撮合用错价格);
  F8     Account.close_position_by_amount: dict 结果按属性访问 +
         self.interface.action 不存在 —— 强平路径两处 AttributeError;
  F9     LooperYou.connect 调用数值属性 initial_capital → TypeError;
  F10    Recorder.clear_all 漏清 main_contract_mapping(无界增长)等四项;
  F11    Entity._to_df: list.remove() 返回 None, columns=None 碰巧等价;
  F12    Account.result 内 plt.show() 弹窗阻塞 + finally: return 吞异常;
  F13    CtpBee.get_result 逐字段相减的耗时在跨零点后为负。

直接运行: python tests/test_review_fixes.py
"""
import os
import sys
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import warnings

warnings.simplefilter("ignore")

from ctpbee.constant import (EVENT_INIT_FINISHED, Direction, Exchange, Offset,
                             OrderRequest, OrderType, Status, TickData, Event)

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))


# --------------------------------------------------------------------------- #
# F1/F2: 冻结与解冻真正生效
# --------------------------------------------------------------------------- #
from ctpbee.app import CtpBee
from ctpbee.level import CtpbeeApi

app = CtpBee("frozen_test", __name__)
app.config.from_mapping({"PATTERN": "real", "TD_FUNC": False,
                         "MD_FUNC": False, "LOG_OUTPUT": False})

_received = []


class _TickCounter(CtpbeeApi):
    def on_tick(self, tick):
        _received.append(tick)


_s = _TickCounter("s1")
app.add_extension(_s)

_suspend_ok = app.suspend_extension("s1")
_s(Event(type="tick", data="t1"))
check("F1 冻结后事件不再分发", _suspend_ok and _received == [])

app.enable_extension("s1")
_s(Event(type="tick", data="t2"))
check("F2 解冻后事件恢复分发", _received == ["t2"])

# --------------------------------------------------------------------------- #
# F3: _reset_init 使 on_init 重新触发(此前默认仅一次)
# --------------------------------------------------------------------------- #
_inits = []


class _InitCounter(CtpbeeApi):
    def on_init(self, init):
        _inits.append(init)


_ev_init = Event(type=EVENT_INIT_FINISHED, data=True)
_s2 = _InitCounter("s2")
_s2(_ev_init)
_s2(_ev_init)
check("F3a init 事件默认只触发一次 on_init", len(_inits) == 1)

_s2._reset_init()
_s2(_ev_init)
check("F3b _reset_init 后 on_init 重新触发", len(_inits) == 2)

# --------------------------------------------------------------------------- #
# F4: route() 不再污染同类兄弟实例
# --------------------------------------------------------------------------- #


class _Routed(CtpbeeApi):
    def on_tick(self, tick):
        return "default"


_a, _b = _Routed("a"), _Routed("b")


@_a.route(handler="tick")
def _routed_tick(self, tick):
    return "routed"


check("F4a route 生效于本实例", _a.map["tick"] is _routed_tick)
check("F4b route 不污染兄弟实例", _b.map["tick"] is _Routed.on_tick)

# --------------------------------------------------------------------------- #
# F11: _to_df 显式列(datetime 进索引, 其余字段全保留)
# --------------------------------------------------------------------------- #
_t = TickData(gateway_name="s", local_symbol="ag2412.SHFE",
              datetime=datetime(2026, 1, 5, 10, 0), last_price=5000)
_df = _t._to_df()
_df_keys = set(_t._to_dict().keys())
check("F11 _to_df: datetime 进索引不进列, 列覆盖全部其余字段",
      _df.index.name == "datetime" and "datetime" not in _df.columns
      and set(_df.columns) | {"datetime"} == _df_keys)

# --------------------------------------------------------------------------- #
# F12: Account.result 不再触发绘图(装有 matplotlib 时旧实现弹窗阻塞)
# --------------------------------------------------------------------------- #
from ctpbee.looper.account import Account

try:
    import matplotlib.pyplot as _plt
except ImportError:
    _plt = None

_acc = Account(interface=None)
_acc.daily_life[date(2026, 1, 5)] = dict(
    date=date(2026, 1, 5), balance=1_000_000.0, margin=0.0,
    available=1_000_000.0, short_balance=1_000_000.0, long_balance=1_000_000.0,
    commission=0.0, net_pnl=0.0, count=0, turnover=0.0)

_show_calls = [0]
if _plt is not None:
    # 计数而非抛异常: 若未来回归把 plt.show 放回 try/finally: return
    # 结构, 异常会被吞掉而测试静默通过; 调用计数是可靠信号
    _orig_show = _plt.show

    def _count_show(*args, **kwargs):
        _show_calls[0] += 1

    _plt.show = _count_show
try:
    _res = _acc.result
finally:
    if _plt is not None:
        _plt.show = _orig_show
check("F12 result 为纯计算(不弹窗)且可算出指标",
      isinstance(_res, dict) and _res.get("total_days / 交易天数") == 1
      and (not _show_calls or _show_calls[0] == 0),
      f"plt.show called {(_show_calls[0] if _show_calls else 0)}x")

# --------------------------------------------------------------------------- #
# 回测单元: LocalLooper 撤单 / 撤全部 / 逐合约撮合
# --------------------------------------------------------------------------- #
from ctpbee.looper.interface import LocalLooper
from ctpbee.looper.data import Bumblebee
from ctpbee.signals import AppSignal

_COUNTER = [0]


def make_looper():
    class _FakeApp:
        pass

    _COUNTER[0] += 1
    looper = LocalLooper(AppSignal(f"fix_{_COUNTER[0]}"), _FakeApp())
    looper.datetime = datetime(2026, 1, 5, 9, 31)
    looper.account.update_params({
        "initial_capital": 1_000_000.0,
        "size_map": {"ag2412.SHFE": 15, "ag2501.SHFE": 15},
        "margin_ratio": {"ag2412.SHFE": 0.1, "ag2501.SHFE": 0.1},
        "commission_ratio": {
            "ag2412.SHFE": {"close": 0.0001, "close_today": 0.0002},
            "ag2501.SHFE": {"close": 0.0001, "close_today": 0.0002},
        },
    })
    return looper


def buy_req(symbol):
    return OrderRequest(symbol=symbol, exchange=Exchange.SHFE,
                        direction=Direction.LONG, type=OrderType.LIMIT,
                        volume=1, price=5000, offset=Offset.OPEN)


class _CancelReq:
    """cancel_order 只读取 order_id 字段"""

    def __init__(self, order_id):
        self.order_id = order_id


# F5: cancel_order 可用且释放冻结
_lo = make_looper()
_sent = _lo.send_order(buy_req("ag2412"))
_oid = next(iter(_lo.pending))
_froze = _lo.account.frozen_margin > 0 and _lo.account.frozen > 0
try:
    _lo.cancel_order(_CancelReq(_oid))
    _cancel_ok = (_oid not in _lo.pending
                  and _lo.account.frozen_margin == 0 and _lo.account.frozen == 0)
except AttributeError:
    _cancel_ok = False
check("F5 回测撤单可用(不再被 frozen 拦截)且归还冻结",
      _sent == 1 and _froze and _cancel_ok)

# F6: cancel_all 可用
_lo = make_looper()
_lo.send_order(buy_req("ag2412"))
_lo.send_order(buy_req("ag2412"))
_orders = list(_lo.pending.values())
_froze = _lo.account.frozen_margin > 0
try:
    _ret = _lo.cancel_all()
    _cancel_all_ok = (_ret == 1 and not _lo.pending
                      and all(o.status == Status.CANCELLED for o in _orders)
                      and _lo.account.frozen_margin == 0 and _lo.account.frozen == 0)
except AttributeError:
    _cancel_all_ok = False
check("F6 cancel_all 撤掉全部报单且归还冻结", _froze and _cancel_all_ok)

# F7: 撮合逐合约判断
_lo = make_looper()
_lo.send_order(buy_req("ag2412"))
_lo.data_entity = Bumblebee(local_symbol="ag2501.SHFE",
                             datetime="2026-01-05 09:31:00",
                             open_price=5100, close_price=5100,
                             high_price=5101, low_price=5099, volume=10)
_lo.match_deal()
_cross_kept = len(_lo.pending) == 1 and not _lo.traded_order_mapping

_lo.data_entity = Bumblebee(local_symbol="ag2412.SHFE",
                             datetime="2026-01-05 09:32:00",
                             open_price=5000, close_price=5000,
                             high_price=5001, low_price=4999, volume=10)
_lo.match_deal()
_same_filled = (not _lo.pending and len(_lo.traded_order_mapping) == 1
                and _lo.traded_order_mapping[next(iter(_lo.traded_order_mapping))].price == 5000)
check("F7 撮合逐合约: 跨月行情不成交, 本合约行情成交",
      _cross_kept and _same_filled)

# --------------------------------------------------------------------------- #
# F9: LooperYou.connect 接受 SIM_PRIMARY_CASH
# --------------------------------------------------------------------------- #
from ctpbee.interface.looper.td_api import LooperYou


class _FakeApp2:
    pass


_td = LooperYou(AppSignal("sim_cash"), _FakeApp2())
try:
    _td.connect({"SIM_PRIMARY_CASH": 123456})
    _cash_ok = (_td.account.initial_capital == 123456
                and _td.account.pre_balance == 123456)
except TypeError:
    _cash_ok = False
check("F9 SIM_PRIMARY_CASH 设置初始资金(不再 TypeError)", _cash_ok)

# --------------------------------------------------------------------------- #
# F10: clear_all 清空无界增长的结构
# --------------------------------------------------------------------------- #
from ctpbee.record import Recorder


class _FakeApp3:
    def __init__(self):
        self.app_signal = AppSignal("rec_fake")
        self.config = {"INSTRUMENT_INDEPEND": False, "LOG_OUTPUT": False}
        self._extensions = {}
        self.tools = {}


_rec = Recorder(_FakeApp3())
_rec.main_contract_mapping["AG.SHFE"].append(object())
_rec.main_contract_mapping["AG.SHFE"].append(object())
_rec.local_contract_price_mapping["ag2412.SHFE"] = 5000.0
_rec.bar["ag2412.SHFE"] = object()
_rec.logs["2026-10-10 09:00:00"] = "msg"
_rec.clear_all()
check("F10 clear_all 清空 main_contract_mapping/昨收价/bar/logs",
      (not _rec.main_contract_mapping and not _rec.local_contract_price_mapping
       and not _rec.bar and not _rec.logs
       and not _rec.ticks and not _rec.orders and not _rec.active_orders))

# --------------------------------------------------------------------------- #
# F8 + F13: 端到端小回测 —— 强平路径可用 & 耗时非负
# --------------------------------------------------------------------------- #
from ctpbee.constant import BarData, ContractData
from ctpbee.signals import common_signals

_CODE, _SIZE = "ag2412.SHFE", 15
common_signals.bar_signal.receivers.clear()
common_signals.tick_signal.receivers.clear()

_rows = []
_p = 5000.0
for _i in range(30):
    _p += 0.5
    _t = datetime(2026, 1, 5, 9, 0) + timedelta(minutes=_i)
    _rows.append(dict(local_symbol=_CODE,
                      datetime=_t.strftime("%Y-%m-%d %H:%M:%S"),
                      open_price=_p, close_price=_p, high_price=_p + 1,
                      low_price=_p - 1, volume=100,
                      turnover=_p * 100 * _SIZE, open_interest=1000))


class _Holder(CtpbeeApi):
    def on_bar(self, bar: BarData) -> None:
        self.i = getattr(self, "i", -1) + 1
        if self.i == 10:
            self.action.buy_open(bar.close_price, 2, origin=bar)


_bt = CtpBee("cpa_test", "ctpbee")
_bt.config.from_mapping({
    "PATTERN": "looper",
    "LOG_OUTPUT": False,
    "LOOPER": {
        "initial_capital": 1_000_000,
        "margin_ratio": {_CODE: 0.1},
        "commission_ratio": {_CODE: {"close": 0.0001, "close_today": 0.0002}},
        "size_map": {_CODE: _SIZE},
    },
})
_bt.add_local_contract(ContractData(local_symbol=_CODE, exchange=Exchange.SHFE,
                                    symbol="ag2412", size=_SIZE, pricetick=1))
_bt.add_extension(_Holder("holder"))
_bt.add_data(_rows)
_trader = _bt.start()

_positions = _trader.account.position_manager.get_all_positions(obj=True)
check("F8a 回测结束后产生多头持仓", len(_positions) > 0
      and _positions[0].direction == Direction.LONG)

_amount = _trader.account.margin * 0.5
try:
    _trader.account.close_position_by_amount(_amount, _trader.price_mapping)
    _close_orders = list(_trader.pending.values())
    _cpa_ok = (len(_close_orders) >= 1
               and all(o.direction == Direction.SHORT for o in _close_orders)
               and all(o.offset in (Offset.CLOSE, Offset.CLOSETODAY,
                                    Offset.CLOSEYESTERDAY)
                       for o in _close_orders))
except Exception as e:  # noqa: BLE001 —— 旧实现在此 AttributeError
    _cpa_ok = False
    print(f"    close_position_by_amount raised: {e!r}")
check("F8b 强平路径可下发平仓单(不再 AttributeError)", _cpa_ok)

# F13: 跨零点耗时不为负 —— 强制 start_datetime 晚于当前时间
import ctpbee.app as _app_mod

_bt.start_datetime = datetime.now() + timedelta(hours=25)
_captured = {}
_real_render = _app_mod.render_result


def _fake_render(result, **kwargs):
    _captured.update(kwargs)
    return "fake_path"


_app_mod.render_result = _fake_render
try:
    _bt.get_result(report=True)
finally:
    _app_mod.render_result = _real_render
check("F13 get_result 耗时跨零点不为负",
      _captured.get("cost_time") == "0h 0m 0s",
      f"cost_time={_captured.get('cost_time')!r}")

_bt.release()

# --------------------------------------------------------------------------- #
failed = [r for r in results if not r[1]]
print()
print("=" * 60)
print(f"{len(results) - len(failed)}/{len(results)} 通过")
if failed:
    for name, _, detail in failed:
        print(f"  FAIL: {name} {detail}")
sys.exit(1 if failed else 0)
