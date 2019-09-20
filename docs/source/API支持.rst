.. _API支持:

API支持
======================
在这里探索一些比较有趣的功能

交易日历
-----------------------------------

关于如何使用交易日历， ``ctpbee`` 提供了 ``TradingDay`` 工具类

首先你需要导入它::

    from ctpbee import TradingDay
    from datetime import datetime


判断是否假期::

    day = datetime.now()
    result = TradingDay.is_holiday(day)
    print(result)

当然上传的 ``is_holiday()`` 同时可以传入date类型的参数

判断是否为周末::

    day = datetime.now()
    result = TradingDay.is_weekend(day)
    print(result)

判断是否为交易日::

    day = datetime.now()
    result = TradingDay.is_trading_day(day)
    print(result)


7×24小时无人监管
-----------------------------

感谢 ``@杨腾杰Kage`` 的idea～

为了给ctpbee的用户解决难以无人监管的问题， 特别在ctpbee内置了无人监管模式，同时为了简化使用， 下面是简单使用::

    def create_app():
        app = CtpBee("ctpbee", __name__)
        return app

    from ctpbee import hickey
    # 将ctpbee的创建函数注入到hickey中, 运行返回app 或者[app1, app2, app3] 两种格式
    hickey.start_all(create_app)



异步支持
-----------------------------
基于同步的队列操作可能会带来一些性能上的消耗?， 所以ctpbee开发了异步模式，用于快速解决任务，提高性能。不过这项选择仍然可能会带来 ``风险`` ， 尤其是对于策略的执行
我们不是很推荐这种模式， 但是你仍然可以进行尝试,快速食用::

     app = CtpBee("ctpbee", __name__, engine_method="async")`

同时你不再需要 ``CtpbeeApi`` 而是 ``AsyncApi``::

    from ctpbee import AsyncApi
    class MyStrategy(AsyncApi):
        async def on_contract(self, contract):
            print(contract.name)

如果想获得性能的提升，你的许多函数都需要使用await/async支持哦


自动刷新持仓数据与账户数据
---------------------------
绝大数的情况下, ctpbee会根据你的成交数据来计算你的本地持仓数据等等, 但是你可能仍然想拿到交易所的最新数据 ,我们开发了一个单独的线程以支持当前情况 , 这个选项是可选 ,同时频率也是可以被你自己所控制的
快速使用 ::

    app = CtpBee("ctpbee", __name__, refresh=True)

同时你可以在配置文件中指定 ``EFRESH_INTERVAL`` ,他应该是个整数或者浮点数, 单位为second/秒.
