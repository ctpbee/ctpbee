"""
this is an example program which used to record tick data
database:pymongo / redis

:keyword 补录数据  ---> will be developed in marker_recorder
关于补录数据的一点想法:
能不能构建多个类似的程序运行在不同的服务， 然后将数据提交到 同时提交到web服务器，
web服务器经过校验之后（出错数据， 缺失数据进行修正和补录）写入到内存（or redis）中，负责提供每天的数据。
这样每天的数据应该基本不会出错，然后外部程序每天访问这个web服务器提供的数据接口，
将数据维护到自己本地
"""
from json import dumps
from pymongo import MongoClient
from redis import Redis

from ctpbee import CtpBee
from ctpbee import DataSolve
from ctpbee import subscribe

app = CtpBee(__name__)

info = {
    "CONNECT_INFO": {
        "userid": "142164",
        "password": "040501",
        "brokerid": "9999",
        "md_address": "tcp://180.168.146.187:10011",
        "td_address": "tcp://180.168.146.187:10000",
        "product_info": "",
        "auth_code": "",
    },
    "TD_FUNC": True,
    "XMIN": [3]
}
# loading config from mapping or you can load it
# from pyfile by app.config.from_pyfile()
# from object by app.config.from_object()
# from json by app.config.from_json()

app.config.from_mapping(info)

# start this app
app.start()

subscribe("ag1912")


class DataRecorder(DataSolve):
    def __init__(self):
        self.pointer = MongoClient()
        self.rd = Redis()
        self.tick_database_name = "tick"
        self.bar_base_name = "bar"
        self.shared_data = {}

    def on_tick(self, tick):
        """tick process function"""
        tick.exchange = tick.exchange.value
        self.pointer[self.tick_database_name][tick.symbol].insert_one(tick.__dict__)

    def on_bar(self, bar, interval):
        """bar process function"""
        bar.exchange = bar.exchange.value
        self.pointer[f"{self.tick_database_name}_{interval}"][bar.symbol].insert_one(bar.__dict__)

    def on_shared(self, shared):
        """process shared function"""
        if self.shared_data.get(shared.vt_symbol, None) is None:
            self.shared_data[shared.vt_symbol] = list()
        else:
            temp = shared.__dict__
            temp["datatime"] = str(temp["datatime"])
            self.shared_data[shared.vt_symbol].append(temp)
        self.rd.set(shared.vt_symbol, dumps(self.shared_data))

# 访问当前所有的数据对象
# recorder = current_app().recorder
