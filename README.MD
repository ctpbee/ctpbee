# ctpbee

bee bee .... there is an industrious bee created ~~

ctpbee provide a tiny core, you can extent the function by programming

## Download the code 

```
git clone https://github.com/somewheve/ctpbee
```

## Libraries

- [vnpy](https://github.com/vnpy/vnpy) version>=2

## Install 
```bash
git clone https://github.com/somewheve/ctpbee & cd ctpbee-master & python3 setup.py install

or   

pip3 install ctpbee 
```

## Function
1. k-line data support
2. time-shared data support
3. trade support
4. market support

## Quick start 
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
## Documention
for README in chinese please see [戳我戳我](https://github.com/somewheve/ctpbee/blob/master/README_CN.MD)

document is developing....  just waiting for it.


## More 
> for more information , please see the [wiki](https://github.com/somewheve/ctpbee/wiki)
or  read the [examples](https://github.com/somewheve/ctpbee/blob/master/examples/app.py)


## Todo 
- To fix the root path and optimize code 
- Exmaple created
 

## End
If this is helpful for you, click the star to support me. QAQ

