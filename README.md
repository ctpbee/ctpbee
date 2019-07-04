# ctpbee 
bee bee .... there is an industrious bee created ~~

ctpbee 提供了一个微小的ctp核心，不会做过多控制流程的事, 也就是说耦合很低很低， 你可以通过这个核心来构建值得信赖的工具， 
当然这需要你的编程功力。 你所需要关心的是如何编程来处理行情和交易信息即可。

# 开始之前 
```bash
# just for linux 
sudo locale-gen zh_CN.GB18030  
```

## 代码下载 

```
git clone https://github.com/somewheve/ctpbee
```

## 起源

- 衍生自 [vnpy](https://github.com/vnpy/vnpy) 和 [flask](https://github.com/pallets/flask)  


## 安装 
```bash
# code install 
git clone https://github.com/somewheve/ctpbee && cd ctpbee && python3 setup.py install  

# pip install
pip3 install ctpbee

```

## 功能
1. k线数据支持
2. 分时图数据支持
3. 交易支持
4. 行情支持 --> 需要自己编写相应的数据库写入代码。
5. 自由自在的发单方式


## 快速开始 
```python
from ctpbee import CtpBee
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
    },
    "TD_FUNC": True,  # 开启交易功能 
}
app.config.from_mapping(info)  # 从dict中载入信息 对于更多配置载入方式, 请参阅文档或者阅读代码
app.start()  

```

## 更多 
> 如果想获得更多信息 , 请参见 [wiki](https://github.com/somewheve/ctpbee/wiki) 或者阅读下面的代码[examples](https://github.com/somewheve/ctpbee/tree/master/examples)


## 等待完成 
- 优化代码
- 创建实例 --> 包括一个 web client
- 维护本地持仓
- 申请穿透式
- 快速下单助手
- 策略层对接CTA
- 单账户 多个策略 ？
- 多账户支持
- 跟单信号 
- 回测系统搭建 


- 暑假之前完不成了.....  再立个flag, 暑假之前一定推出1.0正式版！

## Api支持 

请参阅文档（待上线）


## 最后一句 
如果这个能帮助到你， 请点击star来支持我噢. QAQ
如果你希望贡献代码, 欢迎加群一起讨论和或者提交PR   QQ群号(: 756319143)




