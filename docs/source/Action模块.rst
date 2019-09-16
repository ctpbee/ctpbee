.. _Action模块:

Action模块
=========================


得益于ctpbee的设计(其实是flask的设计了), 我们实现了可扩展的操作模块

基于Action的含义, 里面是封装了大量的操作,

包括**买多**, **卖空**, **平空头**, **平多头**, **撤单**,  **查询持仓**, **查询账户** 等操作

默认实现
------------------

- 买多
    Action. **buy** (self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData, PositionData],
            price_type: OrderType = "LIMIT", stop: bool = False, lock: bool = False, **kwargs)

    解释: 接受price, volume, origin 三个参数和默认的price_type

.. warning::
    stop, lock 参数目前是不被支持.其他下单函数同样也是


- 卖空
    Action. **short** (self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData, PositionData],
              stop: bool = False, lock: bool = False, **kwargs)
      解释: 接受price, volume, origin 三个参数和默认的限价发单


- 平空头
    Action. **sell** (self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData] = None,
             stop: bool = False, lock: bool = False, **kwargs)

    解释: 接受price, volume, origin 三个参数和默认的限价发单


- 平多头
    Action. **cover** (self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData] = None,
             stop: bool = False, lock: bool = False, **kwargs)

    解释: 接受price, volume, origin 三个参数和默认的限价发单


- 撤单
    Action. **cancel** (self, id: Text, origin: [BarData, TickData, TradeData, OrderData, PositionData] = None, **kwargs)
    解释: 传入本地发单id, origin是可选项 ,具体逻辑请参阅源码

- 查持仓
    Action. **query_position** (self)
    解释: 向服务器发起查询持仓请求

- 查账户
    Action. **query_account** (self)
    解释: 向服务器发起查询账户请求


.. note::
    上述模块在策略或者风控中只需要通过self.action 即可拿到操作模块, self参数是不需要传的

扩展
------------------

ctpbee允许你在重写本类, 达到扩展的方法. 在策略中可以随时调用这些你喜欢的方法来优化和你的代码::

    from ctpbee import Action

    class ActionMe(Action):

        def __init__(self, app):
            super().__init__(app)
            """
                还记得我在风控里面提到的绑定操作吗
                你可以在这里简单调用API使用哦
                使用方法 -> self.add_risk_check(func_name)
            """
            # 例如实现对卖空的操作检查
            self.add_risk_check(self.short)




        # 你可以在此处编写你想要的各种办法


然后将ActionMe注入到CtpBee中去, 代码同样非常简单, 请参阅下面一行::

    ``app = CtpBee("ctpbee", __name__, action_class=ActionMe, risk=RiskControl)``

在你想使用实现了一些特殊的风控操作时候,请别忘记将ActionMe和RiskControl一同注入进去 , 他们 应该是一对好伙伴!

.. note::
    发挥你的创造力量, 来构建属于你的个性化方法吧 !


下一章:
    :ref:`回测系统`