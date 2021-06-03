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

- using ctp interface from [vnpy](https://github.com/vnpy/vnpy)

## 快速安装

```bash
# 源码安装 
git clone https://github.com/ctpbee/ctpbee && cd ctpbee && python3 setup.py install  

# pip源安装
pip3 install ctpbee
```

## 文档信息

点击阅读 [document address](http://docs.ctpbee.com)

## 快速开始

```python
from ctpbee import CtpBee
from ctpbee import CtpbeeApi

sta = CtpbeeApi("hello world")


@sta.route(handler="tick")
def on_tick(context, tick):
    print(tick)


@sta.route(handler="bar")
def on_tick(context, bar):
    print(bar)


app = CtpBee("ctpbee", __name__)
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
app.add_extension(sta)
app.start() 
```

更多功能 请阅读[document address](http://docs.ctpbee.com)

## 命令行运行截图

![avatar](source/运行.png)

## 回测截图

支持多周期多合约回测

![avatar](source/回测.png)

## PR支持

Only Accept [PR](https://github.com/ctpbee/ctpbee/compare) code to `dev` branch, please remember that !

## 高性能版本

对于更高性能和速度要求（PS: 别再优化Python了） 请 👉 [FlashFunk](https://github.com/HFQR/FlashFunk)，

## IM

Due to the laziness of the main developer, fans have spontaneously formed a QQ group`521545606`.

You can join the group by search `ctpbee` or `521545606` in QQ and contact with them.

If you have any confusion about developing, please send email to me.

Email: `somewheve@gmail.com`

At last, have a good luck.

## License

- MIT

