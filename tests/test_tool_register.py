# -*- coding: utf-8 -*-
"""tool_register 独立原语的回归测试。

设计目标(见 agentic.md changelog): tool_register 及其注册函数是
【不依赖 ctpbee 其他模块】的通用原语——其他库可以只引入
ctpbee/tool_register.py; ctpbee 自身的 Tool 体系只是它的第一个用户。

覆盖: 独立类的订阅/触发/退订/去重/保序/异常隔离/任意键/快照迭代/
零注册开销路径, 以及 ctpbee Tool 集成(基类装饰激活 + add_func/remove_func)。
直接运行: python tests/test_tool_register.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ctpbee.tool_register import (  # noqa: E402
    register_tool_hook, tool_register, unregister_tool_hook,
)

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))


# ------------------------------------------------------------------ #
# A. 独立使用: 纯自定义类, 无任何 ctpbee 基类
# ------------------------------------------------------------------ #
class Calc:
    @tool_register("tick")
    def on_tick(self, price):
        return price * 2

    @tool_register()
    def on_any(self, x):
        return x


c = Calc()
got = []
register_tool_hook(c, "tick", got.append)
ret = c.on_tick(21)
check("A1 回调收到被装饰方法的返回值", ret == 42 and got == [42])

order = []
register_tool_hook(c, "tick", lambda v: order.append(("b", v)))
register_tool_hook(c, "tick", lambda v: order.append(("a", v)))
got.clear()
c.on_tick(1)
check("A2 回调按注册顺序执行(保序)", order == [("b", 2), ("a", 2)] and got == [2])

dup = []
f = lambda v: dup.append(v)  # noqa: E731
register_tool_hook(c, "tick", f)
register_tool_hook(c, "tick", f)
dup.clear()
c.on_tick(3)
check("A3 重复注册同一函数去重(只触发一次)", dup == [6])  # 回调收到返回值 3*2

check("A4 退订后不再触发",
      unregister_tool_hook(c, "tick", f) is True
      and unregister_tool_hook(c, "tick", f) is False)
dup.clear()
got.clear()
c.on_tick(4)
check("A5 退订不影响其余回调", dup == [] and got == [8])

# 异常隔离: 一个坏回调不影响其余回调与宿主方法
def bad(_):
    raise RuntimeError("hook boom")


register_tool_hook(c, "tick", bad)
got.clear()
try:
    r = c.on_tick(5)
    ok = r == 10
except Exception:
    ok = False
check("A6 单个回调异常被隔离(不传播, 其余照常)", ok and got == [10])

# 任意键: 字符串/None/枚举互不串——只有与被装饰方法键匹配的回调才触发
from ctpbee.constant import ToolRegisterType  # noqa: E402
seen = {}
for key in ("order", None, ToolRegisterType.TRADE):
    register_tool_hook(c, key, lambda v, k=key: seen.__setitem__(k, v))
c.on_tick(7)   # 键 "tick"
c.on_any("x")  # 键 None
check("A7 键隔离: 未触发的键回调不动",
      seen == {None: "x"} and "order" not in seen
      and ToolRegisterType.TRADE not in seen)

# 快照迭代: 回调执行中注册新回调不崩溃, 下次生效
class Mutate:
    @tool_register("t")
    def run(self):
        return 1


m = Mutate()
late = []


def mutating(_):
    register_tool_hook(m, "t", late.append)


register_tool_hook(m, "t", mutating)
try:
    m.run()
    ok = late == []
    m.run()
    ok = ok and late == [1]
except RuntimeError:
    ok = False
check("A8 迭代中注册新回调不崩溃(快照语义, 下次生效)", ok)

# 零注册路径: 从未订阅过的对象照常工作
class Bare:
    @tool_register("t")
    def run(self):
        return "ok"


check("A9 无任何订阅时被装饰方法照常返回", Bare().run() == "ok")

# 元信息保留
check("A10 functools.wraps 保留函数名", Calc.on_tick.__name__ == "on_tick")


# ------------------------------------------------------------------ #
# B. ctpbee Tool 集成: 基类方法已装饰, 订阅即生效
# ------------------------------------------------------------------ #
from ctpbee.constant import TickData, Exchange  # noqa: E402
from ctpbee.level import Tool  # noqa: E402

tool = Tool("demo_tool")
fired = []
tool.add_func(fired.append, ToolRegisterType.TICK)
tool.on_tick(TickData(symbol="ag2612", exchange=Exchange.SHFE,
                      last_price=15345.0, gateway_name="ctp"))
check("B1 基类 on_tick 已装饰: 订阅即触发(无需用户自己加装饰器)",
      len(fired) == 1)

tool.remove_func(fired.append, ToolRegisterType.TICK)
tool.on_tick(TickData(symbol="ag2612", exchange=Exchange.SHFE,
                      last_price=1.0, gateway_name="ctp"))
check("B2 remove_func 退订后不再触发", fired == [] or len(fired) == 1)
fired.clear()


class MyTool(Tool):
    def on_tick(self, tick):
        return tick.last_price


class MyDecoratedTool(Tool):
    @tool_register(ToolRegisterType.TICK)
    def on_tick(self, tick):
        return tick.last_price


mt = MyTool("my_tool")
vals = []
mt.add_func(vals.append, ToolRegisterType.TICK)
t = TickData(symbol="ag2612", exchange=Exchange.SHFE,
             last_price=15345.0, gateway_name="ctp")
mt.on_tick(t)
check("B3 子类重写(未装饰)不触发——与既有语义一致, 返回值即契约需自行装饰",
      vals == [])
mt2 = MyDecoratedTool("my_tool2")
vals2 = []
mt2.add_func(vals2.append, ToolRegisterType.TICK)
mt2.on_tick(t)
check("B4 自行装饰的子类方法按返回值触发", vals2 == [15345.0])

try:
    tool.add_func(lambda x: x, "not_a_type")
    ok = False
except ValueError:
    ok = True
check("B5 add_func 非法类型显式报错(不再是无厘头的 AttributeError)", ok)

print()
failed = [r for r in results if not r[1]]
print(f"{'=' * 60}\n{len(results) - len(failed)}/{len(results)} 通过")
sys.exit(1 if failed else 0)
