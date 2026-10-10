# ctpbee

![avatar](source/ctpbee.png)
[![PyPI Latest Release](https://img.shields.io/pypi/v/ctpbee.svg)](https://pypi.org/project/ctpbee/)
[![Build Status](https://app.travis-ci.com/ctpbee/ctpbee.svg?branch=master)](https://app.travis-ci.com/ctpbee/ctpbee)
[![PyPI Downloads](https://img.shields.io/pypi/dm/ctpbee.svg?label=PyPI%20downloads)](
https://pypi.org/project/ctpbee/)
[![License - MIT](https://img.shields.io/pypi/l/ctpbee.svg)](https://github.com/ctpbee/ctpbee/blob/master/LICENSE)

bee bee .... for developer's trading ~
> tiny but strong

`ctpbee` provide a micro core of trading, you can make trade and backtest in it.

## 🤖 AI 协作指引 / For AI Agents

> **如果你是 AI（Coding Agent），被要求阅读或修改本项目，请先阅读 [agentic.md](agentic.md)，再动任何代码。**
>
> 该文件是本仓库的工作笔记：架构图与数据流、热路径规范（`@frozen` 规则 / 每 tick
> 禁止的可选依赖导入等）、已知边界（交易日历期限、DCE 时间戳口径等）、测试约定
> （每次改动必须带全部通过的测试）以及完整变更历史。
>
> **忽略这些约定会静默损坏行情数据或破坏热路径吞吐。**

If you are an AI coding agent working on this repository, read
[agentic.md](agentic.md) **before touching any code** — it documents the
architecture map, hot-path conventions, known edges, the standing rule that
every change lands with passing tests, and the changelog. Violating those
conventions silently corrupts tick data or breaks hot-path throughput.

## 环境设置

```bash
#  linux用户快速生成中文支持/ windows用户无须设置 
## for root 
bee init-locale 
## for user, xxx为你的用户密码, 注意你当前用户需要拥有sudo权限 
bee init-locale --password xxxxx 

```

## 灵感起源

使用来自于[vnpy](https://github.com/vnpy/vnpy)的交易接口, 重新提供上层封装API, 简化安装流程, 提供快速实现交易功能.

## 快速安装

> `mac`用户注意， `ctpbee_api`目前仅仅提供源码安装方式，
> 需要你预先安装ctpbee_api, [安装参见](https://github.com/ctpbee/ctpbee_api)

```bash


# python version: 3.6+


# 源码安装 
git clone https://github.com/ctpbee/ctpbee && cd ctpbee && python3 setup.py install  

# pip源安装
pip3 install ctpbee
```

### 支持系统

- [x] Linux
- [x] Windows
- [x] MacOS

## 文档

📖 **在线文档地址**: https://ctpbee.github.io/ctpbee/ （GitHub Pages 自动部署，master 分支 docs/ 变更后自动更新）

  - 本地浏览完整版: [docs/index.html](docs/index.html) —— 快速开始 · 配置 · 数据结构 · 策略 API · 下单接口 · Tool 用法 · 回测 · 注意事项
   
## 快速开始

```python
from ctpbee import CtpBee
from ctpbee import CtpbeeApi
from ctpbee.constant import *


class CTA(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)

    def on_init(self, init: bool) -> None:  # 初始化完成回调 
        self.info("init successful")

    def on_tick(self, tick: TickData) -> None:
        print(tick.datetime, tick.last_price)  # 打印tick时间戳以及最新价格 

        # 买开
        self.action.buy_open(tick.last_price, 1, tick)
        # 买平
        self.action.buy_close(tick.last_price, 1, tick)
        # 卖开
        self.action.sell_open(tick.last_price, 1, tick)
        # 卖平 
        self.action.sell_close(tick.last_price, 1, tick)

        # 获取合约的仓位
        position = self.center.get_position(tick.local_symbol)
        print(position)

    def on_contract(self, contract: ContractData) -> None:
        if contract.local_symbol == "rb2205.SHFE":
            self.action.subscribe(contract.local_symbol)  # 订阅行情 
            print("合约乘数: ", contract.size)


if __name__ == '__main__':
    app = CtpBee('ctp', __name__)
    info = {
        "CONNECT_INFO": {
            "userid": "",
            "password": "",
            "brokerid": "",
            "md_address": "",
            "td_address": "",
            "appid": "",
            "auth_code": "",
            "product_info": ""
        },
        "INTERFACE": "ctp",
        "TD_FUNC": True,  # Open trading feature
    }
    app.config.from_mapping(info)  # loading config from dict object
    cta = CTA("cta")
    app.add_extension(cta)
    app.start() 
```

## 功能支持

- [x] 简单易用的下单功能
- [x] 仓位盈亏计算
- [x] 多周期多合约回测
- [x] 实时行情
- [x] k线生成
- [x] 回测报告生成
- [x] 自动运维
- [x] 插件系统的支持
- [x] 多交易接口支持
    - `ctp`
    - `ctp_mini`
    - `rohon`
    - `open_ctp`

更多相关信息, 请参阅[文档](http://docs.ctpbee.com)

## 简单策略示例
- [atr](examples/strategy/atr_strategy.py)
- [bollinger](examples/strategy/bollinger_strategy.py)
- [double_ma](examples/strategy/double_ma.py)
- [macd](examples/strategy/macd_strategy.py)
- [rsi](examples/strategy/rsi_strategy.py)


## 命令行运行效果

![avatar](source/运行.png)

## 回测截图

支持多周期多合约回测, 回测参考`example/backtest`示例
![avatar](source/回测.png)

## 模拟交易测试

本项目推荐使用[openctp](https://github.com/openctp/openctp) 或者[simnow](https://www.simnow.com.cn/)做模拟交易测试

> 关于如何对接`openctp`,请参阅此教程[click here](source/openctp.md)


`DEMO`: 推荐参阅[openctp分发实现](examples/openctp)

## 遇到问题?

请提交`issue`或者于`issue`搜索关键字, 或者查阅[此处](http://docs.ctpbee.com/error.html)

## 历史数据支持

> 对于本地数据自动运维方案, 请👉 [Hive](https://github.com/ctpbee/hive)
> 本项目不提供直接的历史数据访问服务.

## 插件支持

`ctpbee`提供了一个`ToolRegister`机制以支持访问数据触发机制, 可以实现交易各类插件.

欢迎各位大佬参与开发进来. 实现相关生态功能.
如果有相关疑惑, 可以发送邮件到`somewheve@gmail.com`寻求技术支持.
下面是提供的插件列表

- [ctpbee_kline](https://github.com/ctpbee/ckline) k线支持插件

## 还在苦恼ctpbee没有界面?
- [ctpbee_frontend](https://github.com/ctpbee/ctpbee_frontend)  通过`work_mode=Mode.DISPATCHER`进行工作 (通过deepseek生成)

--- 

![avatar](source/client.png)



## 免责声明

本项目维护时间不定期, 开源仅作爱好, 请谨慎使用. 本人不对代码产生的任何使用后果负责.
推荐使用`vnpy | wondertrader | quantaxis | openctp | tqsdk ` 

## License

- MIT
