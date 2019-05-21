from json import dumps
from ctpbee import DataSolve
from orm import BarPointer, TickPointer


class DataRecorder(DataSolve):
    def __init__(self):
        self.tick_pointer = TickPointer()
        self.bar_pointer = BarPointer()
        self.shared_data = {}

    def on_tick(self, tick):
        """tick process function"""
        print(tick)
        tick.exchange = tick.exchange.value
        self.tick_pointer.insert_one(key=tick.symbol, data=tick.__dict__)

    def on_bar(self, bar, interval):
        """bar process function"""
        bar.exchange = bar.exchange.value
        bar.interval = interval
        self.bar_pointer.insert_one(key=bar.symbol, data=bar.__dict__)

    def on_shared(self, shared):
        """process shared function"""
        if self.shared_data.get(shared.vt_symbol, None) is None:
            self.shared_data[shared.vt_symbol] = list()
        else:
            temp = shared.__dict__
            temp["datatime"] = str(temp["datatime"])
            self.shared_data[shared.vt_symbol].append(temp)
        # self.rd.set(shared.vt_symbol, dumps(self.shared_data))
