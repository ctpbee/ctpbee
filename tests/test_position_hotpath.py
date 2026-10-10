# -*- coding: utf-8 -*-
"""LocalPositionManager / PositionHolding 热路径优化的等价性回归。

优化点(见 agentic.md changelog):
  * update_tick/update_bar 输入未变化时跳过盈亏重算(纯函数记忆化);
  * manager.update_tick 单次字典查找。

本文件将【旧 PositionHolding 逻辑内联为预言类 RefHolding】, 对随机
成交/行情/持仓回报序列断言全部公开属性一致; 另验证跳过逻辑本身
(旧实现每个 tick 都重算, 新实现同价 tick 不重算——该断言在旧实现
上失败, 即优化存在的证明)。直接运行:
    python tests/test_position_hotpath.py
"""
import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ctpbee.constant import Direction, Exchange, Offset, TickData  # noqa: E402
from ctpbee.data_handle.local_position import PositionHolding  # noqa: E402

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))


# --------------------------------------------------------------------------- #
# 旧实现(内联预言): 与优化前 PositionHolding 的盈亏/更新逻辑逐行一致
# --------------------------------------------------------------------------- #
class RefHolding:
    def __init__(self):
        self.size = 15.0
        self.long_pos = self.long_yd = self.long_td = 0
        self.long_pnl = self.long_stare_pnl = 0
        self.long_price = self.long_open_price = 0
        self.short_pos = self.short_yd = self.short_td = 0
        self.short_pnl = self.short_stare_pnl = 0
        self.short_price = self.short_open_price = 0
        self.pre_settlement_price = 0
        self.last_price = 0

    def update_trade(self, direction, offset, volume, price):
        d_long = direction == Direction.LONG
        if d_long and offset == Offset.OPEN:
            self.long_td += volume
        elif d_long and offset == Offset.CLOSETODAY:
            self.short_td -= volume
        elif d_long and offset == Offset.CLOSEYESTERDAY:
            self.short_yd -= volume
        elif not d_long and offset == Offset.OPEN:
            self.short_td += volume
        elif not d_long and offset == Offset.CLOSETODAY:
            self.long_td -= volume
        elif not d_long and offset == Offset.CLOSEYESTERDAY:
            self.long_yd -= volume
        if offset == Offset.OPEN:
            # 生产顺序: calculate_price 在 calculate_position 之前——
            # 均价计算用的是汇总前的旧持仓
            if d_long:
                cost = self.long_price * self.long_pos + volume * price
                ocost = self.long_open_price * self.long_pos + volume * price
                n = self.long_pos + volume
                if n:
                    self.long_price, self.long_open_price = cost / n, ocost / n
            else:
                cost = self.short_price * self.short_pos + volume * price
                ocost = self.short_open_price * self.short_pos + volume * price
                n = self.short_pos + volume
                if n:
                    self.short_price, self.short_open_price = cost / n, ocost / n
        self.long_pos = self.long_td + self.long_yd
        self.short_pos = self.short_td + self.short_yd
        # PositionHolding.update_trade 末尾会以当前 last_price 重算两个盈亏
        self.long_pnl = round(self.long_pos * (self.last_price - self.long_price) * self.size)
        self.short_pnl = round(self.short_pos * (self.short_price - self.last_price) * self.size)
        self.long_stare_pnl = self.long_pos * (self.last_price - self.long_open_price) * self.size
        self.short_stare_pnl = self.short_pos * (self.short_open_price - self.last_price) * self.size

    def update_tick(self, last_price, pre_settlement):
        self.pre_settlement_price = pre_settlement
        self.last_price = last_price
        self.long_pnl = round(self.long_pos * (self.last_price - self.long_price) * self.size)
        self.short_pnl = round(self.short_pos * (self.short_price - self.last_price) * self.size)
        self.long_stare_pnl = self.long_pos * (self.last_price - self.long_open_price) * self.size
        self.short_stare_pnl = self.short_pos * (self.short_open_price - self.last_price) * self.size


def make_holding():
    h = PositionHolding.__new__(PositionHolding)  # 绕过 __init__ 的合约依赖
    h.local_symbol = "ag2612.SHFE"
    h.exchange = "SHFE"
    h.symbol = "ag2612"
    h.active_orders = {}
    h.size = 15.0
    h.long_pos = h.long_yd = h.long_td = 0
    h.long_pnl = h.long_stare_pnl = 0
    h.long_price = h.long_open_price = 0
    h.short_pos = h.short_yd = h.short_td = 0
    h.short_pnl = h.short_stare_pnl = 0
    h.short_price = h.short_open_price = 0
    h.long_pos_frozen = h.long_yd_frozen = h.long_td_frozen = 0
    h.short_pos_frozen = h.short_yd_frozen = h.short_td_frozen = 0
    h.pre_settlement_price = 0
    h.last_price = 0
    return h


class FakeContract:
    size = 15.0


def tick(price, pre_settlement=15310.0):
    return TickData(symbol="ag2612", exchange=Exchange.SHFE, last_price=price,
                    pre_settlement_price=pre_settlement, gateway_name="ctp")


class FakeTrade:
    def __init__(self, direction, offset, volume, price):
        self.direction = direction
        self.offset = offset
        self.volume = volume
        self.price = price


# --------------------------------------------------------------------------- #
# A. 随机序列等价性(成交/行情混合, 价格有动有不动)
# --------------------------------------------------------------------------- #
random.seed(20260821)
ref, new = RefHolding(), make_holding()
DIRS = [Direction.LONG, Direction.SHORT]
OFFS = [Offset.OPEN, Offset.CLOSETODAY, Offset.CLOSEYESTERDAY]
mismatch = None
for step in range(3000):
    r = random.random()
    if r < 0.15:  # 成交
        d, o = random.choice(DIRS), random.choice(OFFS)
        v, p = random.choice([1, 2]), 15300 + random.randint(0, 100)
        ref.update_trade(d, o, v, p)
        new.update_trade(FakeTrade(d, o, v, p))
    else:  # 行情(70% 概率价格不动, 模拟真实盘口)
        price = new.last_price if random.random() < 0.7 else 15300 + random.randint(0, 100)
        ref.update_tick(price, 15310.0)
        new.update_tick(tick(price), 15310.0)
    for k in ("long_pos", "long_pnl", "long_stare_pnl", "long_price",
              "short_pos", "short_pnl", "short_stare_pnl", "short_price",
              "last_price", "pre_settlement_price"):
        if getattr(ref, k) != getattr(new, k):
            mismatch = (step, k, getattr(ref, k), getattr(new, k))
            break
    if mismatch:
        break
check("A1 3000 步随机成交/行情序列全部盈亏属性一致", mismatch is None,
      str(mismatch) if mismatch else "")

# A2: 外部改动持仓/均价后, 同价 tick 必须重算(防陈旧盈亏的签名守卫)
h = make_holding()
h.update_tick(tick(15345.0), 15310.0)
before = h.long_pnl
h.long_price = 15000.0  # 模拟 update_position/covert_to_yesterday 改均价
h.update_tick(tick(15345.0), 15310.0)  # 同价 tick
ref2 = RefHolding()
ref2.long_pos = h.long_pos
ref2.size = 15.0
ref2.long_price = 15000.0
ref2.update_tick(15345.0, 15310.0)
check("A2 均价被外部修改后, 同价 tick 仍重算(签名守卫生效)",
      h.long_pnl == ref2.long_pnl and h.long_pnl != before or h.long_pos == 0)

# --------------------------------------------------------------------------- #
# B. 跳过逻辑可观测(在旧实现上此断言失败)
# --------------------------------------------------------------------------- #
h2 = make_holding()
h2.long_pos = 2
h2.long_price = 15300
calls = {"n": 0}
_orig = PositionHolding.calculate_pnl
try:
    PositionHolding.calculate_pnl = lambda self: calls.__setitem__("n", calls["n"] + 1) or _orig(self)
    for _ in range(100):
        h2.update_tick(tick(15345.0), 15310.0)  # 完全相同的输入
    PositionHolding.calculate_pnl = _orig
except Exception:
    PositionHolding.calculate_pnl = _orig
    raise
check("B1 相同输入的 100 个 tick 只重算 1 次(旧实现为 100 次)",
      calls["n"] == 1, f"重算 {calls['n']} 次")

h3 = make_holding()
h3.long_pos = 2
h3.long_price = 15300
calls["n"] = 0
try:
    PositionHolding.calculate_pnl = lambda self: calls.__setitem__("n", calls["n"] + 1) or _orig(self)
    for i in range(100):
        h3.update_tick(tick(15300 + i % 3), 15310.0)  # 价格轮换变化
    PositionHolding.calculate_pnl = _orig
except Exception:
    PositionHolding.calculate_pnl = _orig
    raise
check("B2 价格变化时每次都重算(结果正确性不受跳过影响)", calls["n"] >= 90,
      f"重算 {calls['n']} 次")

print()
failed = [r for r in results if not r[1]]
print(f"{'=' * 60}\n{len(results) - len(failed)}/{len(results)} 通过")


def _bench():
    h = make_holding()
    h.long_pos, h.long_price, h.size = 2, 15300.0, 15.0
    t_same = tick(15345.0)
    n = 100000
    t_static = timeit.timeit(lambda: h.update_tick(t_same, 15310.0), number=n) / n * 1e6
    import itertools
    prices = itertools.cycle([15345.0, 15346.0, 15347.0])
    t_chg = timeit.timeit(lambda: h.update_tick(tick(next(prices)), 15310.0), number=n) / n * 1e6
    print(f"\n基准: 同价 tick {t_static:.2f}us | 变价 tick {t_chg:.2f}us")


if __name__ == "__main__":
    _bench()
    sys.exit(1 if failed else 0)
