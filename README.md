# ctpbee 
bee bee .... for developer's trading ~  

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

## QUICK LOOK 
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

## High Performance Version 
Python version is too slow for HFT.  If you need faster speed and are interested in `Rust` , 
please read the code of [FlashFunk](https://github.com/HFQR/FlashFunk) 


## IM
Due to the laziness of the main developer, fans have spontaneously formed a QQ group`521545606`. 

You can join the group by search `ctpbee` or `521545606` in QQ and contact with them. 

If you  have any confusion about developing, please send email to me. 

Email: `somewheve@gmail.com`


At last, have a good luck.

## License

- MIT

