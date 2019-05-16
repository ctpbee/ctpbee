# ctpbee

bee bee .... there is an industrious bee created ~~

ctpbee 提供了一个微小的核心，不会做过多控制流程的事。 你所需要关心的是如何编程来处理行情和交易信息即可。

## 下载 

```
git clone https://github.com/somewheve/ctpbee
```

## 起源

- 衍生自[vnpy](https://github.com/vnpy/vnpy) 


## 安装 
```bash
python3 setup.py install
```

## 功能
1. k线数据支持
2. 分时图数据支持
3. 交易支持
4. 行情支持 --> 需要自己编写相应的数据库写入代码。

## 快速开始 
```python
from ctpbee import CtpBee
app = CtpBee(__name__)
info = {
    "CONNECT_INFO": {
        "userid": "",
        "password": "",
        "brokerid": "9999",
        "md_address": "tcp://180.168.146.187:10011",
        "td_address": "tcp://180.168.146.187:10000",
        "product_info": "",
        "auth_code": "",
    }
}
app.config.from_mapping(info)
app.start()
```

## 更多 
> 如果想获得更多信息 , 请参见 [wiki](https://github.com/vnpy/vnpy) 或者阅读[examples](https://github.com/somewheve/ctpbee/exmple/app.py)


## 等待完成 
- to fix the root path and optimize code 
- Example created

## 最后一句 
如果这个能帮助到你， 请点击star来支持我噢. QAQ

