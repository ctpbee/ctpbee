"""通用工具回调注册原语。

本模块【只依赖标准库】, 其他库可以单独引入使用; ctpbee 自身的
Tool 体系(level.Tool)只是它的内置用户。

用法(任意类, 无需继承任何基类):

    from ctpbee.tool_register import tool_register, register_tool_hook

    class Calc:
        @tool_register("tick")          # 键任意可哈希: 字符串/枚举/None
        def on_tick(self, tick):
            return tick.last_price      # 返回值会被喂给注册的回调

    c = Calc()
    register_tool_hook(c, "tick", print)     # 订阅(按注册序, 去重)
    unregister_tool_hook(c, "tick", print)   # 退订

契约与保证:
  * 回调在被装饰方法【返回之后】触发, 收到的是该方法的返回值;
  * 回调按注册顺序执行; 同一函数重复注册只触发一次;
  * 单个回调异常被隔离并节流告警——既不影响其余回调, 也不会沿宿主
    方法向上传播(宿主可能位于行情热路径);
  * 触发时对回调列表做快照迭代: 回调执行中注册/退订不影响本轮,
    下一轮生效;
  * 从未订阅过的对象零额外成本(一次 getattr 判断)。
"""
import logging
from functools import wraps

logger = logging.getLogger("ctpbee.tool_register")

# 节流告警: 同类告警第 1 次与此后每 N 次输出一行, 故障期间不刷爆日志
_LOG_STATE = {}


def _warn_throttled(key, msg, every=100):
    n = _LOG_STATE.get(key, 0) + 1
    _LOG_STATE[key] = n
    if n == 1 or n % every == 0:
        logger.warning("%s (x%d)", msg, n)


# 宿主对象上的回调表属性名。下划线开头: ctpbee 的 frozen Entity 规则
# 只放行下划线调用方的属性写入, 注册经由本模块的下划线函数完成创建,
# 因此 frozen 子类同样可以作为宿主。
_LINKED_ATTR = "_linked"


def _ensure_linked(obj):
    """取(或惰性创建)对象上的回调表; 属性不可写的对象返回 None。"""
    linked = getattr(obj, _LINKED_ATTR, None)
    if linked is None:
        linked = {}
        try:
            setattr(obj, _LINKED_ATTR, linked)
        except (AttributeError, TypeError):
            return None
    return linked


def register_tool_hook(obj, tool_type, func) -> bool:
    """向 obj 的 tool_type 通道注册回调 func(按注册序, 去重)。

    tool_type 任意可哈希——独立使用时无需 ctpbee 的 ToolRegisterType。
    返回是否注册成功(宿主对象属性不可写时返回 False)。
    """
    linked = _ensure_linked(obj)
    if linked is None:
        return False
    hooks = linked.setdefault(tool_type, [])
    if func not in hooks:
        hooks.append(func)
    return True


def unregister_tool_hook(obj, tool_type, func) -> bool:
    """退订回调; 返回是否确实移除了一个回调。"""
    linked = getattr(obj, _LINKED_ATTR, None)
    if not linked:
        return False
    hooks = linked.get(tool_type)
    if hooks and func in hooks:
        hooks.remove(func)
        return True
    return False


def tool_register(tool_type=None):
    """装饰器: 方法返回后把返回值依次喂给 tool_type 通道的回调。

    兼容既有用法 ``tool_register(ToolRegisterType.TICK)``, 也接受任意
    可哈希键(字符串/None/自定义枚举)——独立使用时无需 ctpbee 的枚举。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            ret = func(self, *args, **kwargs)
            linked = getattr(self, _LINKED_ATTR, None)
            if linked:
                # 快照迭代: 执行中的注册/退订下一轮才生效
                for take in tuple(linked.get(tool_type, ())):
                    try:
                        take(ret)
                    except Exception as e:
                        _warn_throttled(
                            "hook_error",
                            f"tool_register 回调执行失败"
                            f"({getattr(func, '__qualname__', func)}): {e!r}")
            return ret

        return wrapper

    return decorator
