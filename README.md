# ctpbee 
bee bee .... there is an industrious bee created ~~

ctpbee 提供了一个微小的核心，不会做过多控制流程的事, 也就是说耦合很低很低， 你可以通过这个核心来构建值得信赖的工具， 
当然这需要你的编程功力。 你所需要关心的是如何编程来处理行情和交易信息即可。

>  使用旧版接口
# 开始之前 
```bash
sudo locale-gen zh_CN.GB18030
```

## 代码下载 

```
git clone https://github.com/somewheve/ctpbee
```

## 起源

- 衍生自[vnpy](https://github.com/vnpy/vnpy) 


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

## 快速开始 
```python
from ctpbee import CtpBee
app = CtpBee("hello", __name__)
info = {
    "CONNECT_INFO": {
        "userid": "",
        "password": "",
        "brokerid": "9999",
        "md_address": "tcp://180.168.146.187:10011",
        "td_address": "tcp://180.168.146.187:10000",
        "appid": "",
        "auth_code": "",
    }
}
app.config.from_mapping(info)
app.start()
```

## 更多 
> 如果想获得更多信息 , 请参见 [wiki](https://github.com/somewheve/ctpbee/wiki) 或者阅读下面的代码[examples](https://github.com/somewheve/ctpbee/tree/master/examples)


## 等待完成 
- 优化代码
- 创建实例 --> 包括一个 web client 和一个data_recorder
- 维护本地持仓

## 最后一句 
如果这个能帮助到你， 请点击star来支持我噢. QAQ

ctpbee 是专做ctp的交易插件,当前主要由我一人开发维护,如果你对这个项目感兴趣, 欢迎加群一起讨论和或者贡献代码哦 群号(: 756319143)



