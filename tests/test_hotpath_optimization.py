# -*- coding: utf-8 -*-
"""热路径优化的等价性回归(datetime 构造 + frozen setattr + Entity 批量初始化)。

背景: onRtnDepthMarketData 每 tick 走 strptime(~4us) + TickData 40 次
setattr(每次经 frozen 的 inspect.getframeinfo ~14us, 合计 ~400us)。
优化后: 直接构造 datetime(~0.3us) + 批量 __dict__ 初始化 + 快速帧名检查。

本文件把【旧实现内联为基准预言】, 逐 case 断言新实现结果完全一致;
另覆盖 frozen 保护语义与 TickData 行为不变。直接运行:
    python tests/test_hotpath_optimization.py
"""
import os
import sys
import timeit
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))


# --------------------------------------------------------------------------- #
# 旧实现(内联, 作为等价性预言)
# --------------------------------------------------------------------------- #
def old_parse_normal(action_day, update_time, millisec):
    timestamp = f"{action_day} {update_time}.{int(millisec / 100)}"
    return datetime.strptime(timestamp, "%Y%m%d %H:%M:%S.%f")


def old_parse_dce(update_time, millisec):
    return datetime.strptime(
        str(date.today()) + " " + f"{update_time}.{int(millisec / 100)}",
        "%Y-%m-%d %H:%M:%S.%f")


# --------------------------------------------------------------------------- #
# A. build_tick_datetime 等价性
# --------------------------------------------------------------------------- #
from ctpbee.helpers import build_tick_datetime  # noqa: E402

CASES = [
    ("20260821", "09:30:00", 0),
    ("20260821", "21:59:59", 1),
    ("20260821", "00:00:00", 49),      # 量化: <100ms → ".0"
    ("20260819", "10:15:30", 50),
    ("20260819", "23:59:59", 99),      # 量化: 99ms → ".0"
    ("20260819", "13:31:22", 100),
    ("20260819", "13:31:22", 149),
    ("20260819", "13:31:23", 550),     # 量化: 550ms → ".5" = 500ms
    ("20260820", "02:29:59", 999),
]
ok = True
for ad, ut, ms in CASES:
    want = old_parse_normal(ad, ut, ms)
    got = build_tick_datetime(ad, ut, ms)
    if want != got:
        ok = False
        print(f"  不一致: {ad} {ut} {ms}ms → 旧 {want} 新 {got}")
check("A1 ActionDay/时刻/毫秒矩阵与旧 strptime 完全一致(含 100ms 量化)", ok)

ok = True
for ut, ms in [("21:00:01", 550), ("09:00:00", 0), ("23:59:59", 999)]:
    if build_tick_datetime(None, ut, ms, use_today=True) != old_parse_dce(ut, ms):
        ok = False
check("A2 DCE 分支(use_today)与旧 date.today() 分支一致", ok)

d = date.today()
got = build_tick_datetime("", "21:00:01", 500)
check("A3 ActionDay 缺失回退今天(旧实现此处抛 ValueError, 新实现可用)",
      (got.year, got.month, got.day) == (d.year, d.month, d.day)
      and got.hour == 21 and got.microsecond == 500000)

# 缓存正确性: 不同日期不串
a = build_tick_datetime("20260831", "09:00:00", 0)
b = build_tick_datetime("20260901", "09:00:00", 0)
check("A4 日期缓存按 ActionDay 隔离", a.day == 31 and b.day == 1)

# --------------------------------------------------------------------------- #
# B. frozen 保护语义不变
# --------------------------------------------------------------------------- #
from ctpbee.constant import Exchange, TickData  # noqa: E402

KW = dict(symbol="ag2612", exchange=Exchange.SHFE, datetime=datetime.now(),
          name="x", volume=100.0, last_price=15345.0, gateway_name="ctp")


def mutate_from_public(t):
    t.last_price = 1.0  # 公开函数名 → 必须被 frozen 拒绝


def _mutate_from_private(t):
    t.last_price = 2.0  # 下划线函数名 → 允许(与旧版规则一致)


t = TickData(**KW)
try:
    mutate_from_public(t)
    check("B1 公开函数 setattr 被 frozen 拒绝", False)
except AttributeError as e:
    check("B1 公开函数 setattr 被 frozen 拒绝",
          "protected" in str(e) and "mutate_from_public" in str(e))

_mutate_from_private(t)
check("B2 下划线函数 setattr 放行", t.last_price == 2.0)

# --------------------------------------------------------------------------- #
# C. TickData 构造行为不变(批量初始化 + __post_init__)
# --------------------------------------------------------------------------- #
full = dict(
    symbol="ag2612", exchange=Exchange.SHFE, datetime=datetime(2026, 8, 21, 21, 0, 1),
    name="x", volume=100.0, last_price=15345.0, limit_up=16000.0, limit_down=15000.0,
    open_interest=1000, open_price=15300.0, high_price=15400.0, low_price=15200.0,
    pre_close=15300.0, turnover=1e9, average_price=15320.0,
    settlement_price=0.0, pre_settlement_price=15310.0, pre_open_interest=990,
    **{f"{s}_price_{i}": 15340.0 + i for s in ("bid", "ask") for i in range(1, 6)},
    **{f"{s}_volume_{i}": 10 + i for s in ("bid", "ask") for i in range(1, 6)},
    gateway_name="ctp")
t2 = TickData(**full)
check("C1 全部 40 字段落位",
      all(getattr(t2, k) == v for k, v in full.items()))
check("C2 __post_init__ 的 local_symbol 照常生成", t2.local_symbol == "ag2612.SHFE")
td = t2._to_dict()
check("C3 _to_dict 可用且含关键字段",
      td["symbol"] == "ag2612" and "last_price" in td)
check("C4 repr 可用", "ag2612" in repr(t2))

print()
failed = [r for r in results if not r[1]]
print(f"{'=' * 60}\n{len(results) - len(failed)}/{len(results)} 通过")


# --------------------------------------------------------------------------- #
# 基准(仅打印, 不断言): 旧 vs 新
# --------------------------------------------------------------------------- #
def _bench():
    n = 20000
    t_old_dt = timeit.timeit(lambda: old_parse_normal("20260821", "21:00:01", 550), number=n) / n * 1e6
    t_new_dt = timeit.timeit(lambda: build_tick_datetime("20260821", "21:00:01", 550), number=n) / n * 1e6
    t_ctor = timeit.timeit(lambda: TickData(**full), number=2000) / 2000 * 1e6
    print(f"\n基准: 时间解析 旧 {t_old_dt:.1f}us → 新 {t_new_dt:.1f}us ({t_old_dt / max(t_new_dt, 1e-9):.0f}x)"
          f" | TickData 构造(优化后) {t_ctor:.1f}us (原 ~408us)")


if __name__ == "__main__":
    _bench()
    sys.exit(1 if failed else 0)
