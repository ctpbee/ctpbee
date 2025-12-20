接口开发准则 / Interface development criteria

### 中文版本

#### 为了兼顾到接口的稳定性,接口需要实现一些约定俗成的东西

- 需要交易API需要实现下述几项功能

    + 发单接口 ----> send_order(req, **kwargs)
    + 撤单接口 ----> cancel_order(req, **kwargs)
    + 查询账户 ----> query_account()
    + 查询持仓 ----> query_position()
    + 发送初始化信息 ---> EVENT_INIT_FINISHED
    + 登录接口 ----> connect(info)


- 行情API

    + 登录接口 ----> connect(info)
    + 订阅行情 ----> subscribe(symbol)
    + 取消订阅 ----> unsubscribe(symbol)

#### 接口描述

- ctp 期货交易实盘接口
- looper 回测接口, 支持股票和期货以及数字货币
- stock 股票测试接口 ---->

### English version

#### Here are the guidelines for developing interfaces

- Development when realizing function of trade
    + send interface ----> send_order(req, **kwargs)
    + cancel interface ----> cancel_order(req, **kwargs)
    + query account info ----> query_account()
    + query position info ----> query_position()
    + send info of initialization ---> EVENT_INIT_FINISHED
    + login interface ----> connect(info)


- Market Api
    + login interface ---> connect(info)
    + subscribe market ---> subscribe(symbol)
    + unsubscribe market ---> unsubscribe(symbol)
    