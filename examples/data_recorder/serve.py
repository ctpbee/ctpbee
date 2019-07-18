# coding:utf-8
"""
this is an example program which used to record tick data
database:pymongo / redis

:keyword 补录数据  ---> will be developed in marrd https://github.com/somewheve/marrd
关于补录数据的一点想法:
能不能构建多个类似的程序运行在不同的服务， 然后将数据提交到 同时提交到web服务器，
web服务器经过校验之后（出错数据， 缺失数据进行修正和补录）写入到内存（or redis）中，负责提供每天的数据。
这样每天的数据应该基本不会出错，然后外部程序每天访问这个web服务器提供的数据接口，
将数据维护到自己本地
"""
import multiprocessing
from string import digits
import json
from json import dumps
from pymongo import MongoClient
from redis import Redis
from datetime import time, datetime
from time import sleep

rd = Redis()

from ctpbee import ExtAbstract
from ctpbee import CtpBee
from ctpbee import subscribe


def auth_time(timed):
    from datetime import time
    DAY_START = time(9, 0)  # 日盘启动和停止时间
    DAY_END = time(15, 0)
    NIGHT_START = time(21, 0)  # 夜盘启动和停止时间
    NIGHT_END = time(2, 30)

    if timed <= DAY_END and timed >= DAY_START:
        return True
    if timed >= NIGHT_START:
        return True
    if timed <= NIGHT_END:
        return True
    return False


class DataRecorder(ExtAbstract):
    def __init__(self, name, app=None):
        super().__init__(name, app)
        self.rd = Redis()
        self.tick_database_name = "tick"
        self.bar_base_name = "bar"
        self.shared_data = {}
        self.created = False
        self.recover = False
        self.move = []
        self.mimi = set()
        self.pointer = MongoClient()

    def on_trade(self, trade):
        pass

    def on_contract(self, contract):
        pass

    def on_order(self, order):

        pass

    def on_tick(self, tick):
        """tick process function"""
        symbol = tick.symbol
        if not self.created:
            try:
                if tick.datetime.hour >= 16 and tick.datetime.hour <= 20:
                    # 当天数据结束,进行清空
                    with open("con.txt", "r+") as f:
                        for vt in f.readlines():
                            # self.rd.set(vt, dumps([]))
                            self.rd.set(str(vt).replace("\n", ""), dumps([]))
                    print(f"清除所有数据 at {str(tick.datetime)}")
            except Exception as e:
                print(e)
                pass
            finally:
                self.created = True
        self.mimi.add(tick.vt_symbol)
        if not auth_time(tick.datetime.time()):
            return
        tick.datetime = str(tick.datetime)
        tick.exchange = tick.exchange.value
        self.rd.set(symbol, dumps(tick.__dict__))

    def on_bar(self, bar):
        """bar process function"""
        bar.exchange = bar.exchange.value
        interval = bar.interval
        self.pointer[f"min_{interval}"][bar.symbol].insert_one(bar.__dict__)

    def on_shared(self, shared):
        """process shared function"""
        if not self.recover and self.created:
            with open("con.txt", "r+") as f:
                lines = len(f.readlines())
                if lines > 1:
                    f.write("")

            for vt in self.mimi:
                old = self.rd.get(vt)
                try:
                    temp = json.loads(old)
                except TypeError:
                    temp = []
                self.shared_data[vt] = temp
                with open("con.txt", "a+") as f:
                    f.write(vt + "\n")
                # self.rd.set(vt, dumps([]))
            print("恢复数据")
            self.recover = True
        if not auth_time(shared.datetime.time()):
            """过滤非法"""
            return
        try:
            if self.shared_data.get(shared.vt_symbol) is None:
                self.shared_data[shared.vt_symbol] = list()
            else:
                self.shared_data[shared.vt_symbol].append(
                    [shared.datetime.strftime("%H:%M"), shared.last_price, shared.average_price, shared.volume,
                     shared.open_interest])
        except AttributeError:
            print(shared.__dict__)
        self.rd.set(shared.vt_symbol, dumps(self.shared_data.get(shared.vt_symbol)))


def go():
    app = CtpBee("ctpbee", __name__)

    from ctpbee import switch_app

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
        "TD_FUNC": True,
    }
    app.config.from_mapping(info)
    data_recorder = DataRecorder("data_recorder", app)
    app.start()
    sleep(1)
    # 开始订阅 行情
    for contract in app.recorder.get_all_contracts():
        subscribe(contract.symbol)
    print("完成!")


if __name__ == '__main__':
    go()
