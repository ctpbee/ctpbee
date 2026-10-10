# -*- coding: utf-8 -*-
"""Dispatcher(Mode.DISPATCHER 的 Redis 中继)增强的回归测试。

增强点(见 agentic.md changelog): 行情异步入队、_publish 失败不抛、
上行监听单条隔离 + 断线重连骨架、order_key_map LRU 有界、send_order
空返回不入映射、UDDR 坏消息不炸。

不依赖真实 Redis: 用 FakeRedis 注入, Dispatcher 经 __new__ 构造。
直接运行: python tests/test_dispatcher.py
"""
import json
import os
import queue
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ctpbee.constant import Direction, Exchange, Offset, OrderRequest, TickData  # noqa: E402
from ctpbee.stream import DDDR, Dispatcher, UDDR  # noqa: E402

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))


class FakeRedis:
    def __init__(self):
        self.published = []
        self.fail = False

    def publish(self, channel, payload):
        if self.fail:
            raise RuntimeError("redis down")
        self.published.append((channel, payload))


class FakeAction:
    def __init__(self, result="oid_1", raise_=False):
        self.result, self.raise_ = result, raise_
        self.sent = []

    def send_order(self, order, **kw):
        self.sent.append(order)
        if self.raise_:
            raise RuntimeError("not logged in")
        return self.result

    def cancel_order(self, req, **kw):
        return 1


def make_dispatcher(tick_queue_max=4):
    d = object.__new__(Dispatcher)
    d.rd_client = FakeRedis()
    d.order_key_map = OrderedDict()
    d._tick_queue = queue.Queue(maxsize=tick_queue_max)
    d._tick_dropped = 0
    d._closed = False
    d._ORDER_MAP_MAX = 3
    d.order_up_kernel = "up"
    d.tick_kernel = "tick_kernel"
    d.order_down_kernel = "down_kernel"
    return d


def tick(price):
    return TickData(symbol="ag2612", exchange=Exchange.SHFE, last_price=price,
                    gateway_name="ctp")


def uddr_payload(obj, index=7):
    return UDDR(obj, index=index, parse=False).encode()


# ------------------------------------------------------------------ #
d = make_dispatcher()
t1 = tick(15345.0)
d.on_tick(t1)
check("T1 on_tick 只入队不碰 Redis(热路径隔离)",
      d._tick_queue.qsize() == 1 and d.rd_client.published == [])

ok = d._publish_tick(d._tick_queue.get())
rec = d.rd_client.published
check("T2 _publish_tick 发布到行情通道且载荷可解",
      ok and len(rec) == 1 and rec[0][0] == "tick_kernel"
      and "ag2612" in rec[0][1] and json.loads(rec[0][1])["index"] is None)

d.rd_client.fail = True
check("T3 _publish Redis 故障不抛(返回 False)",
      d._publish("any", "x") is False)
d.rd_client.fail = False
check("T4 Redis 恢复后发布成功", d._publish("any", "x") is True)

# ------------------------------------------------------------------ #
# action 是 CtpbeeApi 的只读 property——在子类上临时屏蔽继承以注入假对象
Dispatcher.action = None
try:
    d2 = make_dispatcher()
    d2.action = FakeAction()
    d2._handle_upstream({"data": uddr_payload(OrderRequest(
        symbol="ag2612", exchange=Exchange.SHFE, direction=Direction.LONG,
        offset=Offset.OPEN, volume=1, price=15345.0), index=7)})
    check("T5 OrderRequest 上行 → 发单并记录索引映射",
          len(d2.action.sent) == 1 and d2.order_key_map.get("oid_1") == 7)

    d3 = make_dispatcher()
    d3.action = FakeAction(raise_=True)
    try:
        d3._handle_upstream({"data": uddr_payload(OrderRequest(
            symbol="ag2612", exchange=Exchange.SHFE, direction=Direction.LONG,
            offset=Offset.OPEN, volume=1, price=1.0), index=9)})
        ok = True
    except Exception:
        ok = False
    check("T6 单条消息处理失败不向上抛(监听线程存活)", ok and not d3.order_key_map)

    d4 = make_dispatcher()
    d4.action = FakeAction(result=None)
    d4._handle_upstream({"data": uddr_payload(OrderRequest(
        symbol="ag2612", exchange=Exchange.SHFE, direction=Direction.LONG,
        offset=Offset.OPEN, volume=1, price=1.0), index=5)})
    check("T7 send_order 返回空值不污染映射", None not in d4.order_key_map
          and len(d4.order_key_map) == 0)
finally:
    del Dispatcher.action  # 恢复继承的 property

d5 = make_dispatcher()
for i in range(5):
    d5._remember_order(f"oid{i}", i)
check("T8 order_key_map LRU 有界(容量 3, 保留最新)",
      len(d5.order_key_map) == 3
      and list(d5.order_key_map) == ["oid2", "oid3", "oid4"])

# ------------------------------------------------------------------ #
d6 = make_dispatcher(tick_queue_max=4)
for p in (1.0, 2.0, 3.0, 4.0, 5.0):
    d6.on_tick(tick(p))
head = d6._tick_queue.queue[0]
check("T9 队列满丢最旧纳最新(累计计数)",
      d6._tick_queue.qsize() == 4 and head.last_price == 2.0
      and d6._tick_dropped == 1)

check("T10 UDDR 坏 JSON → obj None 且不抛",
      UDDR("not-json", parse=True).obj is None)

d7 = make_dispatcher()
d7.close()
check("T11 close 置停止位并入队哨兵",
      d7._closed and d7._tick_queue.get() is None)

print()
failed = [r for r in results if not r[1]]
print(f"{'=' * 60}\n{len(results) - len(failed)}/{len(results)} 通过")
sys.exit(1 if failed else 0)
