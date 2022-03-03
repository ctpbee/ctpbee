# encoding: UTF-8
from copy import deepcopy
from datetime import datetime
from typing import Iterable, Callable

from ctpbee.constant import BarData, TickData, EVENT_BAR
from ctpbee.constant import Event
from ctpbee.date import get_day_from
from ctpbee.signals import common_signals


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
                last_datetime = self.last_datetime[frq]
                if ((last_datetime.minute == tick_data.datetime.minute) and
                    (last_datetime.hour == tick_data.datetime.hour)
                    ) or tick_data.datetime.minute % frq != 0:
                    self.last_entity[frq].high_price = max(self.last_entity[frq].high_price, tick_data.last_price)
                    self.last_entity[frq].low_price = min(self.last_entity[frq].low_price, tick_data.last_price)
                    self.last_entity[frq].close_price = tick_data.last_price
                    self.last_entity[frq].volume += max(tick_data.volume - self.last_entity[frq].first_volume, 0)
                    self.last_entity[frq].first_volume = tick_data.volume
                else:
                    temp = deepcopy(last)
                    if self.check_tick(tick_data):
                        temp.high_price = max(temp.high_price, tick_data.last_price)
                        temp.low_price = min(temp.low_price, tick_data.last_price)
                        temp.close_price = tick_data.last_price
                        temp.volume += max(tick_data.volume - temp.first_volume, 0)
                    self.last_entity[frq] = BarData(
                        datetime=tick_data.datetime,
                        high_price=tick_data.last_price,
                        low_price=tick_data.last_price,
                        close_price=tick_data.last_price,
                        open_price=tick_data.last_price,
                        interval=frq,
                        volume=tick_data.volume - temp.first_volume,
                        first_volume=tick_data.volume,
                        local_symbol=tick_data.local_symbol
                    )
                    self.last_datetime[frq] = tick_data.datetime
                    if abs((tick_data.datetime - last_datetime).seconds) < (frq == 1 and 10 or 60):
                        # 时间太短，丢弃？
                        continue
                    temp.datetime = temp.datetime.replace(second=0, microsecond=0)
                    data.append(temp)
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
        self.lock_free: {int: bool} = {x: True for x in interval}
        self.last_datetime = {x: None for x in interval}
        self._data = data

        self.h = self._data[self.code]["time"].get("night")
        self.night_allow = True if self.h is not None else False

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
                if self.lock_free[frq] is False:
                    if tick_data.datetime.hour == self.last_entity[frq].datetime.hour \
                            and tick_data.datetime.minute == self.last_entity[frq].datetime.minute \
                            and tick_data.datetime.second == self.last_entity[frq].datetime.second:
                        self.lock_free[frq] = True
                if frq != 1 and tick_data.datetime.minute % frq == 0 and abs(
                        (tick_data.datetime - self.last_datetime[frq]).seconds) >= 60 \
                        and self.lock_free[frq] is True:
                    temp = deepcopy(last)
                    check, tim = self.check_tick(tick_data)
                    if check is True:
                        temp.high_price = max(temp.high_price, tick_data.last_price)
                        temp.low_price = min(temp.low_price, tick_data.last_price)
                        temp.close_price = tick_data.last_price
                        temp.volume += max(tick_data.volume - temp.first_volume, 0)
                        self.last_entity[frq] = BarData(
                            datetime=tim,
                            high_price=tick_data.last_price,
                            low_price=tick_data.last_price,
                            close_price=tick_data.last_price,
                            open_price=tick_data.last_price,
                            interval=frq,
                            volume=0,
                            first_volume=tick_data.volume,
                            local_symbol=tick_data.local_symbol
                        )
                        self.lock_free[frq] = False
                        self.last_datetime[frq] = tim
                    else:
                        self.last_entity[frq] = BarData(
                            datetime=tick_data.datetime,
                            high_price=tick_data.last_price,
                            low_price=tick_data.last_price,
                            close_price=tick_data.last_price,
                            open_price=tick_data.last_price,
                            interval=frq,
                            volume=tick_data.volume - temp.first_volume,
                            first_volume=tick_data.volume,
                            local_symbol=tick_data.local_symbol
                        )
                        self.last_datetime[frq] = tick_data.datetime
                    data.append(temp)

                elif frq != 1 and self.lock_free[frq] is True:
                    self.last_entity[frq].high_price = max(self.last_entity[frq].high_price, tick_data.last_price)
                    self.last_entity[frq].low_price = min(self.last_entity[frq].low_price, tick_data.last_price)
                    self.last_entity[frq].close_price = tick_data.last_price
                    self.last_entity[frq].volume += max(tick_data.volume - self.last_entity[frq].first_volume, 0)
                    self.last_entity[frq].first_volume = tick_data.volume
                """
                处理一分钟的k线数据
                """
                if frq == 1 and tick_data.datetime.second == 0 and \
                        abs((tick_data.datetime - self.last_datetime[frq]).seconds) > 10 \
                        and self.lock_free[frq] is True:
                    temp = deepcopy(last)
                    check, tim = self.check_tick(tick_data)
                    if check is True:
                        """ 特殊时间需要特殊有处理 """
                        temp.high_price = max(temp.high_price, tick_data.last_price)
                        temp.low_price = min(temp.low_price, tick_data.last_price)
                        temp.close_price = tick_data.last_price
                        temp.volume += max(tick_data.volume - temp.first_volume, 0)
                        self.last_entity[frq] = BarData(
                            datetime=tim,
                            high_price=tick_data.last_price,
                            low_price=tick_data.last_price,
                            close_price=tick_data.last_price,
                            open_price=tick_data.last_price,
                            interval=frq,
                            volume=0,
                            first_volume=tick_data.volume,
                            local_symbol=tick_data.local_symbol
                        )
                        self.lock_free[frq] = False
                        self.last_datetime[frq] = tim
                    else:
                        self.last_entity[frq] = BarData(
                            datetime=tick_data.datetime,
                            high_price=tick_data.last_price,
                            low_price=tick_data.last_price,
                            close_price=tick_data.last_price,
                            open_price=tick_data.last_price,
                            interval=frq,
                            volume=tick_data.volume - temp.first_volume,
                            first_volume=tick_data.volume,
                            local_symbol=tick_data.local_symbol
                        )
                        self.last_datetime[frq] = tick_data.datetime
                    data.append(temp)
                elif frq == 1 and self.lock_free[frq]:
                    self.last_entity[frq].high_price = max(self.last_entity[frq].high_price, tick_data.last_price)
                    self.last_entity[frq].low_price = min(self.last_entity[frq].low_price, tick_data.last_price)
                    self.last_entity[frq].close_price = tick_data.last_price
                    """ 累积成交量 """
                    self.last_entity[frq].volume += max(tick_data.volume - self.last_entity[frq].first_volume, 0)
                    self.last_entity[frq].first_volume = tick_data.volume

        return data

    def check_tick(self, T: TickData):
        # todo: we need to check other product trade time, Now it only support future trade time
        if T.datetime.hour == 10 and T.datetime.minute == 15:
            return True, datetime.strptime(f"{T.datetime.date()} 10:30:00", "%Y-%m-%d %H:%M:%S")
        elif T.datetime.hour == 11 and T.datetime.minute == 30:
            return True, datetime.strptime(f"{T.datetime.date()} 13:30:00", "%Y-%m-%d %H:%M:%S")
        elif T.datetime.hour == 15 and T.datetime.minute == 0:
            return True, datetime.strptime(f"{T.datetime.date()} 15:00:00", "%Y-%m-%d %H:%M:%S")
        else:
            if self.night_allow:
                """ 处理夜盘 """
                hour, minute, second = [int(x) for x in self.h[0][-1].split(":")]
                hour = hour if hour <= 24 else hour - 24
                if T.datetime.hour == hour and T.datetime.minute == minute:  # make night kline true
                    return True, datetime.strptime(f"{get_day_from(date=str(T.datetime.date()), ne=1)} 09:00:00",
                                                   "%Y-%m-%d %H:%M:%S")
        return False, None
