# ctpbee 
bee bee .... for developer's trading ~~ 

>  tiny but strong

`ctpbee` provide a micro core of trading, you can make trade and backtest in it.

> now it supports both ctp interface and backtest interface for using.


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

Here is the [document address](http://docs.ctpbee.com)  

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

## BackTest 
support multiple instrument and multiple frequency

![avatar](source/回测.png)


##  Development 
Now I want to build stock support for `ctpbee`, if you have any interest, 
you can send email to me and join us! 

## Code Contributed
I just only accept [PR](https://github.com/ctpbee/ctpbee/compare) code to `dev` branch, please remember that ! 

Hope to build a reliable and easy product ^_^



### Important 
Now I write a new model which you can use it to produce kline that equal to `wenhua`. 
It depends on `trade_time.json`, you should load it and pass it as params In `HighKlineSupporter`
A simple usage 
```python
import json

from ctpbee import CtpbeeApi, HighKlineSupporter

class M(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        with open("trade_time.json", "r") as f:
            data = json.load(f) 
        """
        code: rb
        interval: 1min, 5min    
        """
        self.kline = HighKlineSupporter("rb", self.process, [1,5], data)

    def process(self, bar):
        print(bar)    

    def on_tick(self, tick):
        self.kline.update_tick(tick)
```

## License

- MIT

