# ctpbee 
bee bee .... for developer's trading ~~ 

>  tiny but strong

`ctpbee` provide a micro core of trading, you can trade and backtest in it,
 now it supports both ctp interface and backtest interface for using.


## Environment Setup 
```bash
# just for linux/ Generate Chinese environment
sudo ctpbee -auto generate
```
## Origin 

- Thanks to [vnpy](https://github.com/vnpy/vnpy) and [flask](https://github.com/pallets/flask)  

## Quick Install  
```bash
# code install 
git clone https://github.com/ctpbee/ctpbee && cd ctpbee && python3 setup.py install  

# or by  pip install
pip3 install ctpbee
```

## Document

[doc address](http://docs.ctpbee.com)  

## Quick Start 
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
    "TD_FUNC": True,  # Open trading feature
}
app.config.from_mapping(info)  # loading config from dict object
app.start() 

```

## Command Running 
![avatar](source/运行.png)

## Looper  
![avatar](source/回测.png)

## Code Contributed
I just only accept `PR` code to `dev` branch, please remember that ! 

## At last  
just so so  ~~  

## License

- MIT

