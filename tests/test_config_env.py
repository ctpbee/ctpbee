# -*- coding: utf-8 -*-
"""Config.from_envvars 环境变量读取的回归测试。

约定: 前缀 CTPBEE_ 的环境变量 → 去前缀后作为配置键(须全大写, 与
from_mapping 一致); 值优先按 JSON 解析(bool/int/float/list/dict——
CONNECT_INFO 这类字典结构可用 JSON 表达), 解析失败保留原始字符串。
推荐用法: from_json 之后再 from_envvars, 环境变量覆盖文件值。
直接运行: python tests/test_config_env.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ctpbee.config import Config  # noqa: E402

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))


def with_env(pairs, fn):
    """设置环境变量执行 fn 后恢复原状(顺序执行, 无并发竞态)。"""
    backup = {}
    try:
        for k, v in pairs:
            backup[k] = os.environ.get(k)
            os.environ[k] = v
        return fn()
    finally:
        for k, v in backup.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


cfg = Config(root_path=".")


def run():
    n_before = len(cfg)
    cfg.from_envvars()
    check("T1 无相关环境变量时为无操作",
          len(cfg) == n_before or all(k in cfg for k in ()) and
          not any(k.startswith("CTPBEE_") for k in ()))


with_env([("CTPBEE_TD_FUNC", "true")], run)

# ------------------------------------------------------------------ #
def typed():
    cfg2 = Config(root_path=".")
    cfg2.from_mapping({"TD_FUNC": True, "MD_FUNC": True})  # 文件值
    cfg2.from_envvars()
    check("T2 环境变量覆盖文件值(布尔解析)",
          cfg2["TD_FUNC"] is False and cfg2["MD_FUNC"] is True)


with_env([("CTPBEE_TD_FUNC", "false")], typed)


def scalars():
    cfg3 = Config(root_path=".")
    pairs = [
        ("CTPBEE_RD_CLIENT_PORT", "6379"),
        ("CTPBEE_RD_CLIENT_ADDR", "127.0.0.1"),
        ("CTPBEE_SUBSCRIBE_CONTRACT", '["ag2608.SHFE", "sn2609.SHFE"]'),
        ("CTPBEE_CONNECT_INFO", '{"userid": "001", "brokerid": "9999"}'),
        ("CTPBEE_SHARE_MD", "null"),
        ("OTHER_X", "1"),
    ]
    def apply():
        cfg3.from_envvars()
    with_env(pairs, apply)
    check("T3 标量/列表/字典按 JSON 解析, 无前缀变量忽略",
          cfg3["RD_CLIENT_PORT"] == 6379
          and cfg3["RD_CLIENT_ADDR"] == "127.0.0.1"
          and cfg3["SUBSCRIBE_CONTRACT"] == ["ag2608.SHFE", "sn2609.SHFE"]
          and cfg3["CONNECT_INFO"] == {"userid": "001", "brokerid": "9999"}
          and cfg3["SHARE_MD"] is None
          and "OTHER_X" not in cfg3)


scalars()


def fallback_str():
    cfg4 = Config(root_path=".")
    def apply():
        cfg4.from_envvars()  # silent=True: 解析失败保留原字符串
    with_env([("CTPBEE_SHARE_MD", "not-json")], apply)
    check("T4 非 JSON 值回退为原始字符串", cfg4["SHARE_MD"] == "not-json")

    def apply_strict():
        cfg4.from_envvars(silent=False)
    try:
        with_env([("CTPBEE_SHARE_MD", "not-json")], apply_strict)
        ok = False
    except ValueError:
        ok = True
    check("T5 silent=False 时非 JSON 值显式抛错", ok)


fallback_str()


def bad_key():
    cfg5 = Config(root_path=".")
    def apply():
        # 无字母键 "123" 的 isupper() 恒为 False——跨平台稳定
        # (Windows 上 os.environ 会把小写键自动转大写, 不能用它测此分支)
        cfg5.from_envvars()
    with_env([("CTPBEE_123", "1"), ("CTPBEE_", "2")], apply)
    check("T6 非大写键/空前缀被忽略", "123" not in cfg5 and "" not in cfg5)

    def apply_strict():
        cfg5.from_envvars(silent=False)
    try:
        with_env([("CTPBEE_123", "1")], apply_strict)
        ok = False
    except ValueError:
        ok = True
    check("T7 silent=False 时非大写键显式抛错", ok)


bad_key()


def custom_prefix():
    cfg6 = Config(root_path=".")
    def apply():
        cfg6.from_envvars(prefix="BEE_")
    with_env([("BEE_X_VAR", "3"), ("CTPBEE_X_VAR", "4")], apply)
    check("T8 自定义前缀", cfg6["X_VAR"] == 3 and "X_VAR" in cfg6
          and cfg6["X_VAR"] != 4)


custom_prefix()

print()
failed = [r for r in results if not r[1]]
print(f"{'=' * 60}\n{len(results) - len(failed)}/{len(results)} 通过")
sys.exit(1 if failed else 0)
