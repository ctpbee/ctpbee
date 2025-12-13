#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨期套利策略运行示例
"""

from ctpbee import CtpBee
from strategy.spread_arbitrage import SpreadArbitrage

from ctpbee_kline import Kline

def run_spread_arbitrage():
    """
    运行跨期套利策略
    """
    # 创建CtpBee应用实例
    kline = Kline()
    app = CtpBee(
        "spread_arbitrage_app",
        __name__,
        refresh=True,
        work_mode="api"
    ).with_tools(kline)
    # 配置回测或实盘参数
    # 注意：这里需要根据实际情况配置，以下是回测模式示例
    app.config.from_json("./config.json")
    # 配置策略参数
    main_contract = "rb2401.SHFE"  # 主合约（螺纹钢2401）
    sub_contract = "rb2402.SHFE"  # 子合约（螺纹钢2402）
    
    # 初始化套利策略
    spread_strategy = SpreadArbitrage(
        name="rb_spread_strategy",
        main_contract=main_contract,
        sub_contract=sub_contract
    )
    
    # 向应用中添加策略
    app.add_extension(spread_strategy)
    

    # 启动应用
    app.start()
    
    print(f"跨期套利策略已启动 - 主合约: {main_contract}, 子合约: {sub_contract}")
    print("策略日志将实时输出到控制台")
    print("按 Ctrl+C 停止策略")
    return app


if __name__ == "__main__":
    # 运行套利策略
    app = run_spread_arbitrage()
    
    # 保持程序运行
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n策略已停止")
        app.release()
