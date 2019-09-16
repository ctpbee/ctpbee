# ctpbee

bee bee .... created for secondary development ~~

ctpbee just provide a micro framework, you can extent the function by this tiny core. of course your programm

![ctpbee](https://github.com/ctpbee/ctpbee/blob/master/docs/source/ctpbee.jpg)

# Before you start
```bash
# just for linux 
sudo locale-gen zh_CN.GB18030
```

## Download the code 

```
git clone https://github.com/somewheve/ctpbee
```


## Origin

- Derived from [vnpy](https://github.com/vnpy/vnpy) and [flask](https://github.com/pallets/flask)

## Install 
```bash
git clone https://github.com/somewheve/ctpbee & cd ctpbee & python3 setup.py install

or   

pip3 install ctpbee 
```

## Docker 

```bash
docker pull yutiansut/ctpbee:latest
docker run -p 5000:5000 yutiansut/ctpbee:latest
```

## Documention
local generated:
    1. git clone https://github.com/somewheve/ctpbee 
    2. pip3 install sphinx
    3. cd ./ctpbee/docs && make html
    4. you can see the index.html at /build/html, just use web browser to open it  
  [Online docs](http://docs.ctpbee.com)

## Function

- [x] k-line data support
- [x] time-shared data support
- [x] trade support
- [x] market support
- [x] multiple style of sending order
- [x] multi-account support
- [x] apply penetrating interface
- [x] generate the order fastly
- [x] risk level
- [x] documentary signal
- [x] multiplex market comparison
- [ ] optimizing code
- [ ] establishment of back measuring system
- [ ] cta support 



## Quick start 
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
        "product_info":""
    },
    "INTERFACE":"ctp",
    "TD_FUNC": True,  # 开启交易功能 
}
app.config.from_mapping(info)  # 从dict中载入信息 对于更多配置载入方式, 请参阅文档或者阅读代码
app.start() 
```

## More 
read the [examples](https://github.com/somewheve/ctpbee/blob/master/examples/)
 
## End
If this is helpful for you, click the star to support me. QAQ, if you want to communicate  together just [click](https://jq.qq.com/?_wv=1027&k=5xWbIq3) if you have a Tencent QQ Account


