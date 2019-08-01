# ctpbee

bee bee .... there is an industrious bee created ~~

ctpbee just provide a tiny core, you can extent the function by programming


>  Using Old Interface
# Before you start
```bash
sudo locale-gen zh_CN.GB18030
```

## Download the code 

```
git clone https://github.com/somewheve/ctpbee
```


## Origin

- Derived from [vnpy](https://github.com/vnpy/vnpy) 

## Install 
```bash
git clone https://github.com/somewheve/ctpbee & cd ctpbee & python3 setup.py install

or   

pip3 install ctpbee 
```

## Function

1. k-line data support
2. time-shared data support
3. trade support
4. market support
5. monitor

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
    },
    "TD_FUNC": True,  # 开启交易功能
}
app.config.from_mapping(info)  # 载入信息
app.start()  

```
## Documention
for README in English please see [戳我戳我](https://github.com/somewheve/ctpbee/blob/master/README_EN.MD)

document is developing....  just waiting for it.


## More 
> for more information , please see the [wiki](https://github.com/somewheve/ctpbee/wiki)
or  read the [examples](https://github.com/somewheve/ctpbee/blob/master/examples/app.py)


## Todo 
- To optimize code 
- Example created
- Add local position 

## End
If this is helpful for you, click the star to support me. QAQ

