# -*- coding: utf-8 -*-
"""回测主循环(looper)热路径优化的等价性回归。

优化点(见 agentic.md changelog 2026-09-22a):
  1. `ctpbee/looper/data.py`: `VessData.last_bar` 每回放一根 bar/tick 就尝试一次
     `from data_api import Tick, Kline`。data_api 是未开源的可选包, 绝大多数部署下
     这个 import 必然失败; 而【失败】的 import 不进 sys.modules, 每次都要把
     PathFinder 的 sys.path 逐条拼接 + stat 走满一遍。改为至多探测一次并缓存结果。
  2. `ctpbee/date.py`: 新增惰性构建的 {日期: 下标} 索引与 is_trade_date /
     trade_date_index 两个 O(1) 原语, get_day_from 同步改用。
  3. `ctpbee/looper/interface.py`: LocalLooper.__call__ 末尾的交易日解析块抽成
     trade_day_of(), 由"每个 tick 线性扫描 trade_dates 1~2 次 + strptime"
     改为 O(1) 定位 + 按 (自然日, 是否夜盘) 记忆化。

本文件把【优化前的实现逐行内联为预言函数】(ref_old_trade_day_of /
ref_old_last_bar), 并做三层验证:
  * 单元层: ① 全部 8800 个交易日 x 5 个时段 ② 2025-01-01~2027-01-04 全部自然日
    x 5 个时段(含周末/节假日, 覆盖 ValueError / IndexError 分支) —— 穷举断言取值
    与异常完全一致;
  * 机制层: 记忆化/探测缓存确实生效(旧实现每根 bar 都重算 —— 该断言在旧实现上
    失败, 即优化存在的证明);
  * 端到端层: 双合约、跨结算、开平仓都有的小回测, 新实现与旧实现跑出来的
    daily_life / 成交流水 / 最终权益逐项相等。
直接运行:
    python tests/test_backtest_hotpath.py
"""
import importlib.util
import json
import os
import sys
import timeit
import types
from datetime import date, datetime, timedelta
from itertools import repeat

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ctpbee.date import (  # noqa: E402
    get_day_from,
    is_trade_date,
    trade_date_index,
    trade_dates,
)
from ctpbee.looper.interface import _TRADE_DAY_MEMO, trade_day_of  # noqa: E402
import ctpbee.looper.interface as looper_mod  # noqa: E402
import ctpbee.looper.data as data_mod  # noqa: E402
from ctpbee.looper.data import VessData, data_api_types  # noqa: E402

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))


# --------------------------------------------------------------------------- #
# 预言函数: 与优化前的 ctpbee 逐行一致
# --------------------------------------------------------------------------- #
def ref_old_trade_day_of(entity_datetime):
    """优化前 ctpbee/looper/interface.py __call__ 末尾的交易日解析块。"""
    if entity_datetime.hour >= 21:
        """if hour > 21, switch to next trade day"""
        index = trade_dates.index(str(entity_datetime.date()))
        return datetime.strptime(trade_dates[index + 1], "%Y-%m-%d").date()
    else:
        if str(entity_datetime.date()) not in trade_dates:
            last_day = entity_datetime + timedelta(days=-1)
            return datetime.strptime(trade_dates[trade_dates.index(str(last_day.date())) + 1],
                                     "%Y-%m-%d").date()
        else:
            return entity_datetime.date()


def ref_old_last_bar(self):
    """优化前 VessData.last_bar: 每根 bar 都尝试一次 data_api 的 import。"""
    ax = min([x.datetime for x in self.the_buffer.values()])
    for key, value in self.the_buffer.items():
        if ax == value.datetime:
            nx = value
            self.the_buffer[key] = next(self.inner_data[key])
            try:
                from data_api import Tick, Kline
                if isinstance(nx, Tick) or isinstance(nx, Kline):
                    return nx.to_bumblebee()
                else:
                    return nx
            except ImportError:
                return nx


def outcome(fn, timing):
    """执行并返回 ('ok', value) 或 ('exc', 异常类型名, 异常消息)。"""
    try:
        return ("ok", fn(timing))
    except Exception as exc:  # noqa: BLE001 - 预言对比需要捕获全部异常
        return ("exc", type(exc).__name__, str(exc))


# 覆盖日盘 / 夜盘 / 凌晨三段语义, 以及 hour >= 21 边界的两侧
HOURS = [(1, 5), (9, 30), (14, 55), (21, 0), (23, 30)]

# --------------------------------------------------------------------------- #
# A. date.py 的 O(1) 原语 vs 列表线性扫描
# --------------------------------------------------------------------------- #
bad_index = bad_member = 0
for d in trade_dates:
    if trade_date_index(d) != trade_dates.index(d):
        bad_index += 1
    if is_trade_date(d) is not (d in trade_dates):
        bad_member += 1
check("A1 trade_date_index 对全部 8800 个交易日与 list.index 同下标",
      bad_index == 0, f"不一致 {bad_index}")
check("A2 is_trade_date 对全部交易日与 `in list` 一致",
      bad_member == 0, f"不一致 {bad_member}")

# 非交易日: 成员判断为 False, 定位抛 ValueError 且消息与 list.index 完全相同
non_trade = ["1990-12-18", "2026-04-05", "2026-12-31x", "", "2026-13-01"]
bad_exc = 0
for d in non_trade:
    try:
        trade_dates.index(d)
        old = None
    except ValueError as exc:
        old = ("ValueError", str(exc))
    try:
        trade_date_index(d)
        new = None
    except ValueError as exc:
        new = ("ValueError", str(exc))
    if old != new or is_trade_date(d):
        bad_exc += 1
check("A3 非交易日: ValueError 类型+消息与 list.index 一致, 且 is_trade_date 为 False",
      bad_exc == 0, f"不一致 {bad_exc}")

check("A4 trade_dates 元素唯一(字典定位的前提)",
      len(trade_dates) == len(set(trade_dates)), f"{len(trade_dates)} 项")

# --------------------------------------------------------------------------- #
# B. trade_day_of vs 旧实现: 全交易日穷举
# --------------------------------------------------------------------------- #
mismatch = 0
sample_mismatch = None
for d in trade_dates:
    y, m, dd = (int(x) for x in d.split("-"))
    for hh, mm in HOURS:
        t = datetime(y, m, dd, hh, mm)
        if outcome(ref_old_trade_day_of, t) != outcome(trade_day_of, t):
            mismatch += 1
            if sample_mismatch is None:
                sample_mismatch = d
check("B1 全部交易日 x 5 时段: 取值/异常与旧实现完全一致",
      mismatch == 0, f"{len(trade_dates) * len(HOURS)} 例, 不一致 {mismatch}"
      + (f", 首例 {sample_mismatch}" if sample_mismatch else ""))

# --------------------------------------------------------------------------- #
# C. trade_day_of vs 旧实现: 自然日穷举(周末/节假日/边界)
# --------------------------------------------------------------------------- #
mismatch = exc_parity = probed = 0
for offset in range((date(2027, 1, 5) - date(2025, 1, 1)).days):
    day = date(2025, 1, 1) + timedelta(days=offset)
    for hh, mm in HOURS:
        t = datetime(day.year, day.month, day.day, hh, mm)
        old, new = outcome(ref_old_trade_day_of, t), outcome(trade_day_of, t)
        probed += 1
        if old != new:
            mismatch += 1
        if old[0] == "exc":
            exc_parity += 1
check("C1 2025-01-01~2027-01-04 全部自然日 x 5 时段一致",
      mismatch == 0, f"{probed} 例, 不一致 {mismatch}")
check("C2 日历边界外/节假日的 ValueError 与 IndexError 分支保持一致",
      exc_parity > 100, f"异常用例 {exc_parity} 例全部一致")

# 明确锁定两类已知边界(旧实现即如此, 本次不改动行为):
_last = trade_dates[-1]
_ly, _lm, _ld = (int(x) for x in _last.split("-"))
check("C3 最后一个交易日夜盘 -> IndexError(与旧实现相同的既有边界)",
      outcome(trade_day_of, datetime(_ly, _lm, _ld, 21, 0))[0] == "exc"
      and outcome(trade_day_of, datetime(_ly, _lm, _ld, 21, 0))[1] == "IndexError",
      _last)
check("C4 节假日后一日(前一日亦非交易日)-> ValueError(与旧实现相同)",
      outcome(ref_old_trade_day_of, datetime(2026, 4, 6, 9, 30))
      == outcome(trade_day_of, datetime(2026, 4, 6, 9, 30))
      and outcome(trade_day_of, datetime(2026, 4, 6, 9, 30))[1] == "ValueError",
      "2026-04-06")

# --------------------------------------------------------------------------- #
# D. 返回值类型与语义抽查
# --------------------------------------------------------------------------- #
check("D1 日盘交易日归当日",
      trade_day_of(datetime(2026, 8, 21, 9, 30)) == date(2026, 8, 21))
check("D2 周五夜盘归下一交易日(周一)",
      trade_day_of(datetime(2026, 8, 21, 21, 0)) == date(2026, 8, 24)
      and isinstance(trade_day_of(datetime(2026, 8, 21, 21, 0)), date))
check("D3 周六凌晨 02:00 归下一交易日(周一)",
      trade_day_of(datetime(2026, 8, 22, 2, 0)) == date(2026, 8, 24))
# setup.py 声明支持 Python 3.6(还给 3.6 额外装 dataclasses 兼容包), 而
# date.fromisoformat 是 3.7 才有的 API —— 它在 3.6 上会让每一根夜盘 bar 抛
# AttributeError。这里用源码守卫锁定这一点(3.6 的 date 是 C 类型, 无法在运行时
# 模拟"没有 fromisoformat")。
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_hot_files = ["ctpbee/looper/interface.py", "ctpbee/looper/data.py", "ctpbee/date.py"]
_with_37_api = [p for p in _hot_files
                if "fromisoformat(" in open(os.path.join(_ROOT, *p.split("/")), encoding="utf-8").read()]
check("D4 回测热路径不使用 3.7+ 才有的 date.fromisoformat(setup.py 支持 3.6)",
      not _with_37_api, ", ".join(_with_37_api))

# --------------------------------------------------------------------------- #
# E. 交易日记忆化确实生效(优化的存在性证明)
# --------------------------------------------------------------------------- #
_real_index = looper_mod.trade_date_index
_real_member = looper_mod.is_trade_date
calls = {"index": 0, "member": 0}


def _counting_index(d):
    calls["index"] += 1
    return _real_index(d)


def _counting_member(d):
    calls["member"] += 1
    return _real_member(d)


def _lookups():
    """一次调用背后真正发生的 trade_dates 定位次数(旧实现每次 tick 至少 1 次)。"""
    return calls["index"] + calls["member"]


night_target = datetime(2026, 8, 21, 21, 0)   # 夜盘: 需要定位下一交易日
day_target = datetime(2026, 8, 21, 9, 30)     # 日盘交易日: 旧实现走一次 `in` 线性扫描
_TRADE_DAY_MEMO.pop((day_target.date(), False), None)
_TRADE_DAY_MEMO.pop((night_target.date(), True), None)

looper_mod.trade_date_index = _counting_index
looper_mod.is_trade_date = _counting_member
try:
    calls.update(index=0, member=0)
    night_first = trade_day_of(night_target)
    night_cold = _lookups()
    for _ in range(5000):
        night_again = trade_day_of(night_target)
    night_warm = _lookups() - night_cold

    base = _lookups()
    day_first = trade_day_of(day_target)
    day_cold = _lookups() - base
    # 09:30 与 14:55 落在同一个 (自然日, 非夜盘) 记忆条目上, 必须零重算
    same_minute = trade_day_of(datetime(2026, 8, 21, 14, 55))
    same_day_cost = _lookups() - base - day_cold
finally:
    looper_mod.trade_date_index = _real_index
    looper_mod.is_trade_date = _real_member

check("E1 夜盘: 冷路径定位 1 次, 5000 次热调用 0 次重算",
      night_cold == 1 and night_warm == 0,
      f"cold={night_cold} warm_after_5000={night_warm}")
check("E2 日盘: 冷路径 1 次, 同日不同时刻(09:30/14:55 同桶)命中记忆 0 次",
      day_cold == 1 and same_day_cost == 0,
      f"cold={day_cold} same_day={same_day_cost}")
check("E3 记忆化不改变取值",
      night_first == night_again == date(2026, 8, 24)
      and day_first == same_minute == date(2026, 8, 21))
check("E4 旧实现在同样 5000 次调用下每根 bar 都重算",
      sum(1 for _ in range(5000) if outcome(ref_old_trade_day_of, day_target)[0] == "ok")
      == 5000, "预言函数可用, 且不含任何缓存")

# --------------------------------------------------------------------------- #
# F. get_day_from 行为未变
# --------------------------------------------------------------------------- #
check("F1 get_day_from 向后 +1/+2 个交易日",
      get_day_from("2026-08-21") == "2026-08-24"
      and get_day_from("2026-08-21", 2) == "2026-08-25")
check("F2 get_day_from 支持负步长(与原实现同样允许负下标回绕)",
      get_day_from("2026-08-24", -1) == "2026-08-21")
try:
    get_day_from("2026-12-31")
    f3 = False
except IndexError as exc:
    f3 = str(exc) == "参数date不为交易日"
except ValueError:
    f3 = False
else:
    f3 = False
check("F3 越界仍抛 IndexError 且消息为『参数date不为交易日』", f3)
try:
    get_day_from("2026-04-05")
    f4 = False
except ValueError as exc:
    f4 = str(exc) == "'2026-04-05' is not in list"
check("F4 非交易日入参仍抛 ValueError(消息与 list.index 一致)", f4)


# --------------------------------------------------------------------------- #
# G. data_api 探测缓存
# --------------------------------------------------------------------------- #
_MISSING = object()   # "sys.modules 里原本没有 data_api" 的哨兵


def _reset_probe():
    data_mod._DATA_API_TYPES = None


def _row(local_symbol, when, price=100.0):
    return dict(local_symbol=local_symbol, datetime=str(when), open_price=price,
                close_price=price, high_price=price + 1, low_price=price - 1,
                volume=10, turnover=price * 10, open_interest=100)


def _vess(symbols, days):
    """构造一个多源 VessData(与 app.add_data 的入参形状一致)。"""
    per_symbol = []
    for s in symbols:
        rows = [_row(s, datetime(2026, 8, day, 9, minute))
                for day in days for minute in range(0, 60)]
        per_symbol.append(rows)
    return VessData(*per_symbol)


_reset_probe()
check("G1 data_api 不存在时探测结果为空元组(空元组让 isinstance 恒不命中)",
      data_api_types() == () and data_api_types() == data_mod._DATA_API_TYPES)

# G2: last_bar 对普通回放行原样返回 Bumblebee(与旧实现一致)
vess = _vess(["rb2609.SHFE"], [21])
first = vess.last_bar
check("G2 data_api 缺失: last_bar 返回内部 Bumblebee 实体, 字段完整",
      type(first).__name__ == "Bumblebee" and first.local_symbol == "rb2609.SHFE"
      and first.datetime == datetime(2026, 8, 21, 9, 0)
      and first.close_price == 100.0 and first.type == "bar")

# G3: 可选依赖存在时, data_api 实体仍然被转换成 Bumblebee
_reset_probe()
fake = types.ModuleType("data_api")


class FakeTick:
    """模拟 data_api.Tick"""
    def __init__(self, local_symbol, when):
        self.local_symbol = local_symbol
        self.datetime = when

    def to_bumblebee(self):
        return ("converted", self.local_symbol)


fake.Tick = FakeTick
fake.Kline = type("Kline", (FakeTick,), {})
# 注入前先记下现场: 装了真 data_api 的环境里, 无条件 del 会把人家的模块抹掉。
_prev_data_api = sys.modules.get("data_api", _MISSING)
sys.modules["data_api"] = fake
try:
    types_ok = data_api_types()
    vess = _vess(["rb2609.SHFE"], [21])
    tick = FakeTick("rb2609.SHFE", datetime(2026, 8, 21, 9, 0))
    vess.the_buffer["rb2609.SHFE"] = tick
    converted = vess.last_bar
    # 非 data_api 实体在依赖存在时依旧原样返回
    plain = vess.last_bar
finally:
    if _prev_data_api is _MISSING:
        sys.modules.pop("data_api", None)
    else:
        sys.modules["data_api"] = _prev_data_api
    _reset_probe()
check("G3 data_api 存在: 探测到 (Tick, Kline), 实体走 to_bumblebee() 分支",
      len(types_ok) == 2 and converted == ("converted", "rb2609.SHFE"))
check("G4 data_api 存在与否, 普通回放行的返回值一致",
      type(plain).__name__ == "Bumblebee" and plain.datetime == datetime(2026, 8, 21, 9, 1))

# G5: 失败的 import 只发生一次(旧实现每根 bar 一次)
class _SearchCounter:
    """meta_path 上的计数器: 记录针对 data_api 的基于 sys.path 的搜索尝试。"""

    def __init__(self):
        self.n = 0

    def find_spec(self, fullname, path=None, target=None):
        if fullname == "data_api":
            self.n += 1
        return None


_reset_probe()
counter = _SearchCounter()
old_property = VessData.last_bar
sys.meta_path.insert(0, counter)
try:
    rows = [_row("rb2609.SHFE", datetime(2026, 8, 21) + timedelta(seconds=i))
            for i in range(1, 5002)]

    def _replay(vess, n):
        """把 VessData 的缓冲/生成器复位 n 次, 只测 last_bar 里 data_api 探测的开销。"""
        fresh = data_mod.Bumblebee(**rows[0])
        for _ in range(n):
            vess.the_buffer["rb2609.SHFE"] = fresh
            vess.inner_data["rb2609.SHFE"] = repeat(fresh)
            vess.last_bar

    vess_new = VessData(rows)
    counter.n = 0
    _replay(vess_new, 5000)
    searched_new = counter.n

    VessData.last_bar = property(ref_old_last_bar)
    try:
        vess_old = VessData(rows)
        counter.n = 0
        _replay(vess_old, 200)
        searched_old = counter.n
    finally:
        VessData.last_bar = old_property
finally:
    sys.meta_path.remove(counter)
    _reset_probe()
check("G5 5000 次回放只探测 1 次; 旧实现 200 次回放即搜索 200 次",
      searched_new == 1 and searched_old == 200,
      f"new={searched_new} old={searched_old}")

# G6/G7: 非 ImportError 的错误不被吞掉, 也不会被当成"data_api 不可用"缓存下来
class _BoomFinder:
    """模拟 data_api 自身代码在 import 阶段抛错(非 ImportError)。"""

    def find_spec(self, fullname, path=None, target=None):
        if fullname == "data_api":
            raise RuntimeError("data_api 内部炸了")
        return None


_reset_probe()
boomer = _BoomFinder()
sys.meta_path.insert(0, boomer)
old_property = VessData.last_bar
try:
    VessData.last_bar = property(ref_old_last_bar)
    try:
        try:
            _vess(["rb2609.SHFE"], [21]).last_bar
            old_propagated = False
        except RuntimeError:
            old_propagated = True
    finally:
        VessData.last_bar = old_property
    _reset_probe()
    try:
        data_api_types()
        new_propagated = False
    except RuntimeError:
        new_propagated = True
    # 抛错之后缓存仍为"未探测", 下一次调用依旧重新尝试(与旧实现一致)
    again = False
    try:
        data_api_types()
    except RuntimeError:
        again = True
finally:
    sys.meta_path.remove(boomer)
    VessData.last_bar = old_property
    _reset_probe()
check("G6 data_api import 抛非 ImportError 时新旧实现都向调用方传播",
      new_propagated and old_propagated)
check("G7 该错误不会被静默缓存成『data_api 不可用』, 下次调用仍会尝试", again)


# --------------------------------------------------------------------------- #
# H. 端到端回测差分: 新实现 vs 旧实现
# --------------------------------------------------------------------------- #
VOLATILE = {"local_order_id", "local_trade_id", "tradeid", "order_id", "trade_id",
            "gateway_name", "ids"}


def _e2e_rows():
    """两个合约在同一时间轴上回放(覆盖多源归并 + 平今平昨 + 跨结算)。"""
    from ctpbee.constant import Exchange
    codes = [("rb2609.SHFE", Exchange.SHFE, 10), ("ta2609.CZCE", Exchange.CZCE, 5)]
    days = [d for d in trade_dates if "2026-01-05" <= d <= "2026-12-20"][:6]
    out = []
    for code, _, size in codes:
        rows = []
        price = 3600.0 if code.startswith("rb") else 6100.0
        for d in days:
            day = datetime.strptime(d, "%Y-%m-%d")
            stamps = [day.replace(hour=9) + timedelta(minutes=m) for m in range(0, 240)]
            stamps += [day.replace(hour=21) + timedelta(minutes=m) for m in range(0, 120)]
            for i, t in enumerate(stamps):
                price += (i % 9) * 0.5 - 0.25
                p = round(price, 1)
                rows.append(dict(local_symbol=code,
                                 datetime=t.strftime("%Y-%m-%d %H:%M:%S"),
                                 open_price=p, close_price=p, high_price=p + 1,
                                 low_price=p - 1, volume=100,
                                 turnover=p * 100 * size, open_interest=1000))
        out.append((code, size, rows))
    return codes, out


def _run_e2e(tag):
    """跑一遍小回测, 返回可比较的规范化结果。"""
    from ctpbee.app import CtpBee
    from ctpbee.constant import ContractData, BarData
    from ctpbee.jsond import dumps
    from ctpbee.level import CtpbeeApi
    from ctpbee.signals import common_signals

    codes, built = _e2e_rows()

    class _T(CtpbeeApi):
        def on_bar(self, bar: BarData) -> None:
            self.i = getattr(self, "i", -1) + 1
            i = self.i
            # 第一根 bar 上发单会撞上 LocalLooper.datetime 尚未赋值的既有边界,
            # 因此留出若干根 bar 再开始交易(与本次优化无关)
            if i < 300:
                return
            if i % 300 == 0:
                self.action.buy_open(bar.close_price, 2, origin=bar)
            elif i % 300 == 137:
                self.action.sell_open(bar.close_price, 1, origin=bar)
            elif i % 300 == 211:
                self.action.cover(bar.close_price, 2, origin=bar)
            elif i % 300 == 271:
                self.action.sell(bar.close_price, 1, origin=bar)

    # bar/tick 走全局信号, 同进程内多个 app 会互相串扰 -> 每次跑前摘干净
    common_signals.bar_signal.receivers.clear()
    common_signals.tick_signal.receivers.clear()

    app = CtpBee(f"ht_{tag}", "ctpbee")
    app.config.from_mapping({
        "PATTERN": "looper",
        "LOG_OUTPUT": False,
        "LOOPER": {
            "initial_capital": 1_000_000,
            "margin_ratio": {c: 0.1 for c, _, _ in codes},
            "commission_ratio": {c: {"close": 0.0001, "close_today": 0.0002}
                                 for c, _, _ in codes},
            "size_map": {c: s for c, _, s in codes},
        },
    })
    for code, exchange, size in codes:
        app.add_local_contract(ContractData(local_symbol=code, exchange=exchange,
                                            symbol=code.split(".")[0], size=size,
                                            pricetick=1))
    app.add_extension(_T(f"t_{tag}"))
    app.add_data(*[rows for _, _, rows in built])
    trader = app.start()

    def _strip(obj):
        if isinstance(obj, dict):
            return {k: _strip(v) for k, v in obj.items() if k not in VOLATILE}
        if isinstance(obj, list):
            return [_strip(v) for v in obj]
        return obj

    trades = sorted((_strip(json.loads(dumps(t))) for t in trader.traded_order_mapping.values()),
                    key=lambda x: json.dumps(x, sort_keys=True, default=str))
    payload = {
        "trader_date": str(trader.date),
        "account_date": str(trader.account.date),
        "pre_close_price": {k: v for k, v in sorted(trader.pre_close_price.items())},
        "price_mapping": {k: v for k, v in sorted(trader.price_mapping.items())},
        "daily_life": _strip({str(k): v for k, v in sorted(trader.account.daily_life.items(),
                                                          key=lambda kv: str(kv[0]))}),
        "trades": trades,
        "final_balance": trader.account.balance,
    }
    app.release()
    return payload


_reset_probe()
_TRADE_DAY_MEMO.clear()
new_run = _run_e2e("new")

# 把两处实现换回优化前的版本再跑一遍(相同输入, 相同预期)
_reset_probe()
_TRADE_DAY_MEMO.clear()
_real_trade_day_of = looper_mod.trade_day_of
_real_last_bar = VessData.last_bar
looper_mod.trade_day_of = ref_old_trade_day_of
VessData.last_bar = property(ref_old_last_bar)
try:
    old_run = _run_e2e("old")
finally:
    looper_mod.trade_day_of = _real_trade_day_of
    VessData.last_bar = _real_last_bar
    _reset_probe()

same_keys = new_run["daily_life"].keys() == old_run["daily_life"].keys()
check("H1 端到端回测: 逐日结算记录 daily_life 完全一致",
      same_keys and new_run["daily_life"] == old_run["daily_life"],
      f"{len(new_run['daily_life'])} 个结算日")
check("H2 端到端回测: 成交流水(去掉 uuid 单号)完全一致",
      new_run["trades"] == old_run["trades"], f"{len(new_run['trades'])} 笔成交")
check("H3 端到端回测: 交易日/昨收价/最新价/最终权益一致",
      new_run["trader_date"] == old_run["trader_date"]
      and new_run["account_date"] == old_run["account_date"]
      and new_run["pre_close_price"] == old_run["pre_close_price"]
      and new_run["price_mapping"] == old_run["price_mapping"]
      and new_run["final_balance"] == old_run["final_balance"],
      f"date={new_run['trader_date']} balance={new_run['final_balance']:.2f}")
check("H4 端到端回测确实交易过、确实结算过(差分不是空跑)",
      len(new_run["trades"]) > 30 and len(new_run["daily_life"]) >= 5
      and new_run["final_balance"] != 1_000_000,
      f"{len(new_run['trades'])} 笔成交 / {len(new_run['daily_life'])} 个结算日")

print()
failed = [r for r in results if not r[1]]
print(f"{'=' * 60}\n{len(results) - len(failed)}/{len(results)} 通过")


# --------------------------------------------------------------------------- #
# 基准(仅打印, 不断言): 旧 vs 新
# --------------------------------------------------------------------------- #
def _bench():
    n = 20000
    day_t = datetime(2026, 8, 21, 9, 30)      # 日盘, 交易日
    night_t = datetime(2026, 8, 21, 21, 0)    # 夜盘 -> 定位 + 解析
    _TRADE_DAY_MEMO.clear()
    t_old_day = timeit.timeit(lambda: ref_old_trade_day_of(day_t), number=n) / n * 1e6
    t_old_night = timeit.timeit(lambda: ref_old_trade_day_of(night_t), number=n) / n * 1e6
    t_new = timeit.timeit(lambda: trade_day_of(day_t), number=n) / n * 1e6
    t_new_night = timeit.timeit(lambda: trade_day_of(night_t), number=n) / n * 1e6
    print(f"\n基准: 交易日解析 日盘 旧 {t_old_day:6.1f}us -> 新 {t_new:5.2f}us"
          f" ({t_old_day / t_new:.0f}x) | 夜盘 旧 {t_old_night:6.1f}us -> 新 {t_new_night:5.2f}us"
          f" ({t_old_night / t_new_night:.0f}x)")

    # data_api: 每根 bar 的 import 开销 vs 命中缓存
    # 只有 data_api 确实不可用时, "每根 bar 一次失败的 import" 才是真实场景;
    # 装了真 data_api 的机器上跳过这一项, 免得量出来一个不存在的路径。
    if importlib.util.find_spec("data_api") is not None:
        print("      data_api 本机可导入: 跳过【失败 import】基准(旧实现在这里不会反复扫 sys.path)")
    else:
        _reset_probe()
        t_old_import = timeit.timeit(
            "try:\n"
            "    from data_api import Tick, Kline\n"
            "except ImportError:\n"
            "    pass",
            setup="import sys; sys.modules.pop('data_api', None)",
            number=300) / 300 * 1e6
        _reset_probe()
        data_api_types()                      # 先让缓存热起来
        t_new_import = timeit.timeit(lambda: data_api_types(), number=200000) / 200000 * 1e6
        print(f"      data_api 探测 旧 {t_old_import:8.1f}us/根 -> 新 {t_new_import:5.3f}us/根"
              f" ({t_old_import / t_new_import:,.0f}x), 新实现全生命周期至多探测 1 次")
    print(f"      trade_dates {len(trade_dates)} 项; 交易日记忆表条目数 "
          f"{len(_TRADE_DAY_MEMO)} (≈ 覆盖天数 x 2)")


if __name__ == "__main__":
    _bench()
    sys.exit(1 if failed else 0)
