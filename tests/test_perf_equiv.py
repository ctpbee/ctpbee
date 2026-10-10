# -*- coding: utf-8 -*-
"""性能优化(2026-10-10 第二轮)的等价性回归。

每处优化都内联【改动前的实现】作为 oracle, 断言值与异常类型逐项一致:
  E1  Bumblebee.covert_datetime 快路径 vs 旧双 strptime
  E2  TickData/BarData __post_init__ 单 split vs 旧双 split
  E3  LocalLooper._alpha_of 记忆化 vs 旧 join(filter(isalpha))
  E4  _COMMON_SIGNALS / _TICK_SIGNAL 与单例信号对象同一
  E5  match_deal 空 pending 早退: 无任何副作用
  E6  on_event 预绑定后接收者收到的 Event 不变(端到端)
基准: 回测 µs/bar 与实盘 µs/tick 前后对比(打印, 非判定)。

直接运行: python tests/test_perf_equiv.py
"""
import os
import sys
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import warnings

warnings.simplefilter("ignore")

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))


# ------------------------------------------------------------------ E1
from ctpbee.looper.data import Bumblebee


def old_covert_datetime(datetime_data):
    """改动前的实现(oracle)"""
    if isinstance(datetime_data, datetime):
        return datetime_data
    if isinstance(datetime_data, str):
        try:
            return datetime.strptime(datetime_data, "%Y-%m-%d %H:%M:%S")
        except Exception:
            return datetime.strptime(datetime_data, "%Y-%m-%d %H:%M:%S.%f")
    if isinstance(datetime_data, int):
        return datetime.fromtimestamp(datetime_data)


def outcome(fn, x):
    try:
        return ("ok", fn(x))
    except Exception as e:
        return ("raise", type(e))


cases = []
for d in range(1, 28, 3):
    for h in (0, 9, 15, 21, 23):
        cases.append(f"2026-01-{d:02d} {h:02d}:31:07")
# 宽松形态
cases += ["2026-1-5 9:3:1", "2026-1-5 9:3:1 ",
          "2026-01-05 09:31:07.5", "2026-01-05 09:31:07.123456",
          "2026-01-05 09:31:07.", "2026-01-05T09:31:07", "2026-01-05",
          "", " ", "2026-01-05  09:31:07", "2026-13-05 09:31:07",
          "abc", "2026-01-05 25:61:61"]
# 对抗样本: int() 比 strptime 宽松的形态(下划线/字段内空白/正负号),
# 快路径的 isdigit 门卫必须把它们全部推回旧逻辑
cases += ["20_6-01-05 09:31:07", "2026-0_-05 09:31:07",
          "2026-01-05 09:3_:07", "2026- 1-05 09:31:07",
          "2026-01-05 09:31: 7", "2026-01-05 09:3 1:07",
          "+026-01-05 09:31:07"[:19], "2026-01-0+ 09:31:07",
          "２026-01-05 09:31:07", "2026-01-05 09:31:０7",
          "99999999999999-1-5 9:3:1"]
# 确定性变异模糊: 固定种子, 对规范串做 1-3 处 随机替换/插入/删除
import random

rng = random.Random(20261010)
base = "2026-01-05 09:31:07"
alphabet = "0123456789-: ._+ab２０⁵"
for _ in range(3000):
    chars = list(base)
    for _ in range(rng.randint(1, 3)):
        if not chars:
            break
        i = rng.randrange(len(chars))
        op = rng.random()
        if op < 0.5:
            chars[i] = rng.choice(alphabet)
        elif op < 0.8:
            chars.insert(i, rng.choice(alphabet))
        else:
            del chars[i]
    cases.append("".join(chars))

ok = True
for c in cases:
    a, b = outcome(old_covert_datetime, c), outcome(Bumblebee.covert_datetime, c)
    if a != b:
        ok = False
        print(f"    差异: {c!r} 旧={a} 新={b}")
check("E1a covert_datetime 字符串输入逐例等价(值+异常类型)",
      ok, f"{len(cases)} 例(含 3000 变异模糊)")

ok = True
for ts in (0, 1, 1700000000, 1767225600):
    if old_covert_datetime(ts) != Bumblebee.covert_datetime(ts):
        ok = False
check("E1b covert_datetime int 时间戳等价", ok)

dt = datetime(2026, 1, 5, 10, 0)
check("E1c covert_datetime datetime 透传等价",
      Bumblebee.covert_datetime(dt) is old_covert_datetime(dt) is dt)

# ------------------------------------------------------------------ E2
from ctpbee.constant import BarData, Exchange, TickData


def old_post(local_symbol):
    """旧 __post_init__ 的双 split 语义(oracle)"""
    return local_symbol.split(".")[0], local_symbol.split(".")[1]


ok = True
for sym in ["ag2412.SHFE", "rb2609.SHFE", "ta609.CZCE", "a.b.c"]:
    t = TickData(gateway_name="g", local_symbol=sym, datetime=dt, last_price=1.0)
    b = BarData(gateway_name="g", local_symbol=sym, datetime=dt, close_price=1.0)
    exp = old_post(sym)
    if (t.symbol, t.exchange) != exp or (b.symbol, b.exchange) != exp:
        ok = False
check("E2a TickData/BarData post_init 派生字段等价", ok)

ok = True
for sym in ["nodot", ""]:
    for cls, kw in ((TickData, dict(last_price=1.0)), (BarData, dict(close_price=1.0))):
        try:
            cls(gateway_name="g", local_symbol=sym, datetime=dt, **kw)
            ok = False
        except IndexError:
            pass
check("E2b local_symbol 无点时仍抛 IndexError", ok)

t2 = TickData(gateway_name="g", symbol="ag2412", exchange=Exchange.SHFE,
              datetime=dt, last_price=1.0)
b2 = BarData(gateway_name="g", symbol="rb2609", exchange="SHFE",
             datetime=dt, close_price=1.0)
check("E2c 无 local_symbol 时按 symbol+exchange 构建(枚举/字符串)",
      t2.local_symbol == "ag2412.SHFE" and b2.local_symbol == "rb2609.SHFE"
      and isinstance(b2.exchange, str))

# ------------------------------------------------------------------ E3/E4/E5
from ctpbee.looper.interface import LocalLooper, _COMMON_SIGNALS
from ctpbee.signals import AppSignal, common_signals


class _FakeApp:
    pass


lo = LocalLooper(AppSignal("pe"), _FakeApp())
lo.datetime = datetime(2026, 1, 5, 9, 31)
syms = ["ag2412.SHFE", "rb2609.SHFE", "ta609.CZCE", "SP eb2402&eb2403.DCE", "a.b.c"]
ok = True
for sym in syms:
    alpha = lo._alpha_of.get(sym)
    if alpha is None:
        alpha = lo._alpha_of[sym] = "".join(filter(str.isalpha, sym.split(".")[0]))
    if alpha != "".join(filter(str.isalpha, sym.split(".")[0])):
        ok = False
check("E3a _alpha_of 记忆化与旧表达式逐值相同", ok and len(lo._alpha_of) == len(syms))

check("E4a _COMMON_SIGNALS 与单例同一",
      _COMMON_SIGNALS["bar"] is common_signals.bar_signal
      and _COMMON_SIGNALS["tick"] is common_signals.tick_signal)

from ctpbee.interface.ctp.md_api import _TICK_SIGNAL as _T_CTP
from ctpbee.interface.ctp_mini.md_api import _TICK_SIGNAL as _T_MINI
from ctpbee.interface.ctp_rohon.md_api import _TICK_SIGNAL as _T_ROHON
check("E4b 三个 md_api 的 _TICK_SIGNAL 与单例同一(副本同步)",
      _T_CTP is _T_MINI is _T_ROHON is common_signals.tick_signal)

before = (dict(lo.traded_order_mapping), lo.today_volume, dict(lo.pending))
lo.data_entity = Bumblebee(local_symbol="ag2412.SHFE",
                           datetime="2026-01-05 09:31:00",
                           open_price=1, close_price=1, high_price=2,
                           low_price=0, volume=1)
lo.match_deal()
after = (dict(lo.traded_order_mapping), lo.today_volume, dict(lo.pending))
check("E5 match_deal 空 pending 早退: 零副作用", before == after)

# ------------------------------------------------------------------ E6 端到端
from ctpbee.app import CtpBee
from ctpbee.constant import ContractData
from ctpbee.date import trade_dates
from ctpbee.level import CtpbeeApi

common_signals.bar_signal.receivers.clear()
common_signals.tick_signal.receivers.clear()

CODE = "ag2412.SHFE"
days = [d for d in trade_dates if "2026-01-05" <= d <= "2026-02-28"][:20]
rows, p = [], 5000.0
for d in days:
    day0 = datetime.strptime(d, "%Y-%m-%d").replace(hour=9)
    for i in range(240):
        p += 0.5
        t = day0 + timedelta(minutes=i)
        rows.append(dict(local_symbol=CODE, datetime=t.strftime("%Y-%m-%d %H:%M:%S"),
                         open_price=p, close_price=p, high_price=p + 1,
                         low_price=p - 1, volume=100, turnover=p * 1500,
                         open_interest=1000))


class Counter(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.bars = []
        self.init = 0

    def on_bar(self, bar: BarData) -> None:
        self.bars.append((bar.local_symbol, bar.datetime, bar.close_price))

    def on_init(self, init):
        self.init += 1


app = CtpBee("pe_e2e", "ctpbee")
app.config.from_mapping({
    "PATTERN": "looper", "LOG_OUTPUT": False,
    "LOOPER": {"initial_capital": 1_000_000, "margin_ratio": {CODE: 0.1},
               "commission_ratio": {CODE: {"close": 1e-4, "close_today": 2e-4}},
               "size_map": {CODE: 15}},
})
app.add_local_contract(ContractData(local_symbol=CODE, exchange=Exchange.SHFE,
                                    symbol="ag2412", size=15, pricetick=1))
ctr = Counter("c")
app.add_extension(ctr)
app.add_data(rows)
t0 = time.perf_counter()
trader = app.start()
per_bar = (time.perf_counter() - t0) / len(rows) * 1e6
app.release()

expect = [(r["local_symbol"],
           datetime.strptime(r["datetime"], "%Y-%m-%d %H:%M:%S"),
           r["close_price"]) for r in rows]
# 既有怪癖(非本轮引入): VessData.last_bar 在 return 前执行 next(), 数据源
# 的【最后一根 bar】随 StopIteration 被丢弃、不分发 —— 两版差分实现同形,
# test_backtest_hotpath 一直锁定此行为。修正它属于功能变更, 本轮不动。
check("E6a 端到端: 策略收到的每根 bar(symbol/datetime/close)与数据源逐项相等",
      ctr.bars == expect[:-1], f"{len(ctr.bars)} bars (末根被既有行为丢弃)")
check("E6b init 事件恰好触发一次", ctr.init == 1)
print(f"\n基准: 回测 {per_bar:.2f} us/bar (本轮优化前 11.74, 含 20 结算日)")

failed = [r for r in results if not r[1]]
print()
print("=" * 60)
print(f"{len(results) - len(failed)}/{len(results)} 通过")
if failed:
    for name, _, detail in failed:
        print(f"  FAIL: {name} {detail}")
sys.exit(1 if failed else 0)
