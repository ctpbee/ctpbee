# ctpbee

bee bee .... for developer's trading ~
> tiny but strong

`ctpbee` provide a micro core of trading, you can make trade and backtest in it.

## 环境设置

```bash
#  linux用户快速生成中文支持/ windows用户无须设置 
sudo ctpbee -auto generate
```

## 灵感起源

使用来自于[vnpy](https://github.com/vnpy/vnpy)的交易接口, 重新提供上层封装API, 简化安装流程, 提供快速实现交易功能.

## 快速安装

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

## 文档与交流

[文档地址](http://docs.ctpbee.com)

[论坛地址](http://forum.ctpbee.com)

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
- [x] 多交易接口支持 
  - `ctp`
  - `ctp_mini`
  - `rohon`

更多相关信息, 请参阅[文档](http://docs.ctpbee.com)

## 命令行运行效果

![avatar](source/运行.png)

## 回测截图

支持多周期多合约回测

![avatar](source/回测.png)

## PR支持

Only Accept [PR](https://github.com/ctpbee/ctpbee/compare) code to `dev` branch, please remember that !


> 对于高频解决方案, 请 👉 [FlashFunk](https://github.com/HFQR/FlashFunk)

> 对于本地数据自动运维方案, 请👉 [Hive](https://github.com/ctpbee/hive)

## 免责声明

本项目长期维护, 开源仅作爱好，本人不对代码产生的任何使用后果负责. 功能尽可能会保持稳定,
但是为了你的实盘账户着想，请先用`simnow`账户测试完善再上实盘!

如有问题, 请提issue, 会在1-2个工作日进行回复.

## License

- MIT
