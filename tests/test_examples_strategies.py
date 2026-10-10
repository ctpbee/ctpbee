# -*- coding: utf-8 -*-
"""examples 策略的中危修复回归。

覆盖三项:
  A. ATRStrategy.instrument_set 自动补全 local_symbol 形式
     (INSTRUMENT_INDEPEND 过滤比较的是 local_symbol, 裸合约名会全部漏掉);
  S. SpreadArbitrage 价差增量化——每对齐分钟恰好一条, 同分钟不重复,
     两腿长度不匹配不产出(旧实现每根 K 线重放整个窗口);
  O. openctp 客户端发单门控——限频 + 本地持仓跟踪
     (旧实现基本每 tick 发 FOK 单且无持仓管理)。
直接运行: python tests/test_examples_strategies.py
"""
import logging
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ctpbee.constant import (  # noqa: E402
    BarData, ContractData, Direction, Exchange, Offset, TickData, TradeData,
)

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))


class FakeApp:
    """只为 logger/debug 提供 app 身份, 不启动任何引擎。"""
    logger = logging.getLogger("test_examples")
    _extensions = {}

    def __init__(self):
        self.config = {}


def contract_of(symbol="ag2612", exchange=Exchange.SHFE):
    return ContractData(symbol=symbol, exchange=exchange, size=15.0,
                        pricetick=1.0, gateway_name="ctp")


def bar_of(symbol, exchange, minute, close):
    return BarData(symbol=symbol, exchange=exchange,
                   datetime=datetime(2026, 8, 21, 9, minute),
                   open_price=close, high_price=close, low_price=close,
                   close_price=close, volume=1, gateway_name="ctp")


# ------------------------------------------------------------------ #
# A. ATRStrategy.instrument_set 补全 local_symbol
# ------------------------------------------------------------------ #
from examples.strategy.atr_strategy import ATRStrategy  # noqa: E402

atr = ATRStrategy("t_atr", "ag2612")
check("A1 初始为裸合约名", "ag2612" in atr.instrument_set)
atr.on_contract(contract_of())
check("A2 合约回报后补全 local_symbol 形式",
      "ag2612.SHFE" in atr.instrument_set
      and "ag2612" in atr.instrument_set)
atr.on_contract(contract_of(symbol="sn2609"))
check("A3 非目标合约不污染集合", "sn2609.SHFE" not in atr.instrument_set)

# ------------------------------------------------------------------ #
# S. SpreadArbitrage 价差增量化
# ------------------------------------------------------------------ #
from examples.strategy.spread_arbitrage import SpreadArbitrage  # noqa: E402

app = FakeApp()
sa = SpreadArbitrage("t_spread", "rb2601.SHFE", "rb2605.SHFE")
sa.init_app(app)
# 缩短预热门槛(缺省 20): length 同时决定预热(12 根)与价差上限(24 条)
# ——22 分钟产出 11 条不被裁剪; 且 11 < 24 使 execute_arbitrage 的
# 门槛(>= length*2)不满足, 测试不依赖任何下单路径
sa.length = 12

MAIN, SUB = "rb2601", "rb2605"
for m in range(1, 23):  # 22 个对齐分钟: 主 3700+m, 子 3500+m
    sa.on_bar(bar_of(MAIN, Exchange.SHFE, m, 3700 + m))
    sa.on_bar(bar_of(SUB, Exchange.SHFE, m, 3500 + m))
check("S1 预热后每对齐分钟恰好一条价差(旧实现每根K线重放整个窗口)",
      len(sa.spreads) == 11, f"len={len(sa.spreads)}")
check("S2 最新价差值正确", sa.spreads[-1] == (3700 + 22) - (3500 + 22))

# 同分钟两腿重复触发 → 不重复累计
sa.on_bar(bar_of(MAIN, Exchange.SHFE, 22, 3799))
sa.on_bar(bar_of(SUB, Exchange.SHFE, 22, 3599))
check("S3 同分钟重复触发不累计", len(sa.spreads) == 11)

# 两腿长度不匹配 → 不产出
sa.on_bar(bar_of(MAIN, Exchange.SHFE, 23, 3723))
check("S4 两腿长度不匹配不产出", len(sa.spreads) == 11)
sa.on_bar(bar_of(SUB, Exchange.SHFE, 23, 3523))
check("S5 补齐后腿恢复产出", len(sa.spreads) == 12
      and sa.spreads[-1] == (3700 + 23) - (3500 + 23))

# ------------------------------------------------------------------ #
# O. openctp 客户端发单门控
# ------------------------------------------------------------------ #
from examples.openctp.openctp_client import Main  # noqa: E402

m = Main("t_openctp")
acts = [m._tick_action() for _ in range(40)]
check("O1 限频: 40 个 tick 只产生 2 次动作", acts.count("open") + acts.count("close") == 2,
      f"动作序列末尾={acts[-3:]}")
check("O2 无持仓时动作均为开仓", set(a for a in acts if a) == {"open"})
m.pos = 1
fired = [m._tick_action() for _ in range(20)]
check("O2b 有持仓时动作切换为平仓", "close" in fired)

m2 = Main("t_openctp2")
m2._tick_action()  # 推进 count


def fake_trade(direction, offset):
    return TradeData(symbol="rb2310", exchange="SHFE", order_id=1,
                     tradeid="T1", gateway_name="ctp", direction=direction,
                     offset=offset, volume=1, price=3700.0)


m2.on_trade(fake_trade(Direction.LONG, Offset.OPEN))
check("O3 开多成交 → 持仓 +1", m2.pos == 1)
m2.on_trade(fake_trade(Direction.LONG, Offset.CLOSE))
check("O4 平多成交 → 持仓归零", m2.pos == 0)
m2.on_trade(fake_trade(Direction.SHORT, Offset.OPEN))
check("O5 开空成交 → 持仓 -1", m2.pos == -1)
m2.on_trade(fake_trade(Direction.SHORT, Offset.CLOSE))
check("O6 平空成交 → 持仓归零", m2.pos == 0)

print()
failed = [r for r in results if not r[1]]
print(f"{'=' * 60}\n{len(results) - len(failed)}/{len(results)} 通过")
sys.exit(1 if failed else 0)
