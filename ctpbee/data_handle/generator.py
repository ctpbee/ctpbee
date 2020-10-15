# encoding: UTF-8
from copy import deepcopy
from typing import Iterable, Callable

from pandas._typing import FuncType

from ctpbee.signals import common_signals
from ctpbee.constant import BarData, TickData, EVENT_BAR
from ctpbee.constant import Event


class DataGenerator:
    def __init__(self, app):
        self.app = app
        self.XMIN = app.config.get("XMIN")
        self.last_entity: {int: None} = {x: None for x in self.XMIN}

        self.last_datetime = {x: None for x in self.XMIN}

    def update_tick(self, tick: TickData):
        bar = self.resample(tick)
        for x in bar:
            event = Event(type=EVENT_BAR, data=x)
            common_signals.bar_signal.send(event)

    def resample(self, tick_data: TickData) -> BarData or None:
        data = []
        for frq, last in self.last_entity.items():
            if last is None:
                self.last_entity[frq] = BarData(
                    datetime=tick_data.datetime,
                    high_price=tick_data.last_price,
                    low_price=tick_data.last_price,
                    close_price=tick_data.last_price,
                    open_price=tick_data.last_price,
                    interval=frq,
                    volume=0,
                    first_volume=tick_data.volume,
                    local_symbol=tick_data.local_symbol,
                )
                self.last_datetime[frq] = tick_data.datetime
            else:
                if frq != 1 and tick_data.datetime.minute % frq == 0 and abs(
                        (tick_data.datetime - self.last_datetime[frq]).seconds) >= 60:
                    temp = deepcopy(last)
                    if self.check_tick(tick_data):
                        temp.high_price = max(temp.high_price, tick_data.last_price)
                        temp.low_price = min(temp.high_price, tick_data.last_price)
                        temp.close_price = tick_data.last_price
                        temp.volume += max(tick_data.volume - temp.first_volume, 0)
                        self.last_entity[frq] = None
                    else:
                        self.last_entity[frq] = BarData(
                            datetime=tick_data.datetime,
                            high_price=tick_data.last_price,
                            low_price=tick_data.last_price,
                            close_price=tick_data.last_price,
                            open_price=tick_data.last_price,
                            interval=frq,
                            volume=0,
                            first_volume=tick_data.volume,
                            local_symbol=tick_data.local_symbol
                        )
                    self.last_datetime[frq] = tick_data.datetime
                    data.append(temp)
                elif frq != 1:
                    self.last_entity[frq].high_price = max(self.last_entity[frq].high_price, tick_data.last_price)
                    self.last_entity[frq].low_price = min(self.last_entity[frq].low_price, tick_data.last_price)
                    self.last_entity[frq].close_price = tick_data.last_price
                    self.last_entity[frq].volume += max(tick_data.volume - self.last_entity[frq].first_volume, 0)
                    self.last_entity[frq].first_volume = tick_data.volume
                # 处理一分钟的k线
                if frq == 1 and tick_data.datetime.second == 0 and \
                        abs((tick_data.datetime - self.last_datetime[frq]).seconds) > 10:
                    temp = deepcopy(last)
                    if self.check_tick(tick_data):
                        temp.high_price = max(temp.high_price, tick_data.last_price)
                        temp.low_price = min(temp.high_price, tick_data.last_price)
                        temp.close_price = tick_data.last_price
                        temp.volume += max(tick_data.volume - temp.first_volume, 0)
                        self.last_entity[frq] = None
                    else:
                        self.last_entity[frq] = BarData(
                            datetime=tick_data.datetime,
                            high_price=tick_data.last_price,
                            low_price=tick_data.last_price,
                            close_price=tick_data.last_price,
                            open_price=tick_data.last_price,
                            interval=frq,
                            volume=0,
                            first_volume=tick_data.volume,
                            local_symbol=tick_data.local_symbol
                        )
                    self.last_datetime[frq] = tick_data.datetime
                    data.append(temp)
                elif frq == 1:
                    self.last_entity[frq].high_price = max(self.last_entity[frq].high_price, tick_data.last_price)
                    self.last_entity[frq].low_price = min(self.last_entity[frq].low_price, tick_data.last_price)
                    self.last_entity[frq].close_price = tick_data.last_price
                    self.last_entity[frq].volume += max(tick_data.volume - self.last_entity[frq].first_volume, 0)
                    self.last_entity[frq].first_volume = tick_data.volume
        return data

    @staticmethod
    def check_tick(T: TickData):
        if (T.datetime.hour == 10 and T.datetime.minute == 15) or \
                (T.datetime.hour == 11 and T.datetime.minute == 30) or \
                (T.datetime.hour == 15 and T.datetime.minute == 0) or \
                (T.datetime.hour == 23 and T.datetime.minute == 0):
            return True
        return False

    def __del__(self):
        for x in self.last_entity.values():
            event = Event(type=EVENT_BAR, data=x)
            common_signals.bar_signal.send(event)
        self.last_entity.clear()


class HighKlineSupporter:
    def __init__(self, code: str, callback: Callable, interval: Iterable, data: dict):
        assert code in data.keys()
        assert data[code].get("time") is not None
        if not isinstance(callback, Callable):
            raise TypeError("callable should be a function")
        self.callback = callback
        self.code = code
        self.last_entity: {int: None} = {x: None for x in interval}
        self.last_datetime = {x: None for x in interval}
        self._data = data

    def update_tick(self, tick: TickData):
        bar = self.resample(tick)
        for x in bar:
            self.callback(x)

    def resample(self, tick_data: TickData) -> BarData or None:
        data = []
        for frq, last in self.last_entity.items():
            if last is None:
                self.last_entity[frq] = BarData(
                    datetime=tick_data.datetime,
                    high_price=tick_data.last_price,
                    low_price=tick_data.last_price,
                    close_price=tick_data.last_price,
                    open_price=tick_data.last_price,
                    interval=frq,
                    volume=0,
                    first_volume=tick_data.volume,
                    local_symbol=tick_data.local_symbol,
                )
                self.last_datetime[frq] = tick_data.datetime
            else:
                if frq != 1 and tick_data.datetime.minute % frq == 0 and abs(
                        (tick_data.datetime - self.last_datetime[frq]).seconds) >= 60:
                    temp = deepcopy(last)
                    if self.check_tick(tick_data):
                        temp.high_price = max(temp.high_price, tick_data.last_price)
                        temp.low_price = min(temp.high_price, tick_data.last_price)
                        temp.close_price = tick_data.last_price
                        temp.volume += max(tick_data.volume - temp.first_volume, 0)
                        self.last_entity[frq] = None
                    else:
                        self.last_entity[frq] = BarData(
                            datetime=tick_data.datetime,
                            high_price=tick_data.last_price,
                            low_price=tick_data.last_price,
                            close_price=tick_data.last_price,
                            open_price=tick_data.last_price,
                            interval=frq,
                            volume=0,
                            first_volume=tick_data.volume,
                            local_symbol=tick_data.local_symbol
                        )
                    self.last_datetime[frq] = tick_data.datetime
                    data.append(temp)
                elif frq != 1:
                    self.last_entity[frq].high_price = max(self.last_entity[frq].high_price, tick_data.last_price)
                    self.last_entity[frq].low_price = min(self.last_entity[frq].low_price, tick_data.last_price)
                    self.last_entity[frq].close_price = tick_data.last_price
                    self.last_entity[frq].volume += max(tick_data.volume - self.last_entity[frq].first_volume, 0)
                    self.last_entity[frq].first_volume = tick_data.volume
                # 处理一分钟的k线
                if frq == 1 and tick_data.datetime.second == 0 and \
                        abs((tick_data.datetime - self.last_datetime[frq]).seconds) > 10:
                    temp = deepcopy(last)
                    if self.check_tick(tick_data):
                        temp.high_price = max(temp.high_price, tick_data.last_price)
                        temp.low_price = min(temp.high_price, tick_data.last_price)
                        temp.close_price = tick_data.last_price
                        temp.volume += max(tick_data.volume - temp.first_volume, 0)
                        self.last_entity[frq] = None
                    else:
                        self.last_entity[frq] = BarData(
                            datetime=tick_data.datetime,
                            high_price=tick_data.last_price,
                            low_price=tick_data.last_price,
                            close_price=tick_data.last_price,
                            open_price=tick_data.last_price,
                            interval=frq,
                            volume=0,
                            first_volume=tick_data.volume,
                            local_symbol=tick_data.local_symbol
                        )
                    self.last_datetime[frq] = tick_data.datetime
                    data.append(temp)
                elif frq == 1:
                    self.last_entity[frq].high_price = max(self.last_entity[frq].high_price, tick_data.last_price)
                    self.last_entity[frq].low_price = min(self.last_entity[frq].low_price, tick_data.last_price)
                    self.last_entity[frq].close_price = tick_data.last_price
                    self.last_entity[frq].volume += max(tick_data.volume - self.last_entity[frq].first_volume, 0)
                    self.last_entity[frq].first_volume = tick_data.volume

        return data

    def __del__(self):
        self.last_entity.clear()

    def check_tick(self, T: TickData):
        h = self._data[self.code]["time"].get("night")
        if h is not None:
            """ 处理夜盘 """
            hour, minute, second = [int(x) for x in h[0][-1].split(":")]
            if hour >= 24:
                hour = hour - 24
            if (T.datetime.hour == 10 and T.datetime.minute == 15) or \
                    (T.datetime.hour == 11 and T.datetime.minute == 30) or \
                    (T.datetime.hour == 15 and T.datetime.minute == 0) or \
                    (T.datetime.hour == hour and T.datetime.minute == minute):  # make night kline true
                return True
        else:
            """ 处理白天 """
            if (T.datetime.hour == 10 and T.datetime.minute == 15) or \
                    (T.datetime.hour == 11 and T.datetime.minute == 30) or \
                    (T.datetime.hour == 15 and T.datetime.minute == 0):
                return True
        return False
