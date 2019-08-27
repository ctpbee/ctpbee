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

    app = CtpBee("ctpbee", __name__, work_mode="forever")`

你只需要在CtpBee里面显式传入 ``work_mode="forever"`` 参数即可，这样你就可以享用到无人监管的快感了，当然你需要知道的是， ctpbee默认指定的是 ``work_mode="limit_time"`` ，


异步支持
-----------------------------
基于同步的队列操作可能会带来一些性能上的消耗?， 所以ctpbee开发了异步模式，用于快速解决任务，提高性能。不过这项选择仍然可能会带来 ``风险`` ， 尤其是对于策略的执行
我们不是很推荐这种模式， 但是你仍然可以进行尝试,快速食用::

     app = CtpBee("ctpbee", __name__, engine_method="forever")`

同时你不再需要 ``CtpbeeApi`` 而是 ``AsyncApi``::

    from ctpbee import AsyncApi
    class MyStrategy(AsyncApi):
        async def on_contract(self, contract):
            print(contract.name)

如果想获得性能的提升，你的许多函数都需要使用await/async支持哦

