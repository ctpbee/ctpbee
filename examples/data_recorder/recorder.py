from json import dumps
from pymongo import MongoClient
from redis import Redis
from ctpbee import DataSolve


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
