# encoding: UTF-8
from copy import deepcopy
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
                if frq != 1 and tick_data.datetime.minute % frq == 0 \
                        and abs((tick_data.datetime - self.last_datetime[frq]).seconds) >= 60:
                    temp = deepcopy(last)
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
                elif frq == 1:
                    self.last_entity[frq].high_price = max(self.last_entity[frq].high_price, tick_data.last_price)
                    self.last_entity[frq].low_price = min(self.last_entity[frq].low_price, tick_data.last_price)
                    self.last_entity[frq].close_price = tick_data.last_price
                    self.last_entity[frq].volume += max(tick_data.volume - self.last_entity[frq].first_volume, 0)
                    self.last_entity[frq].first_volume = tick_data.volume

        return data

    def __del__(self):
        for x in self.last_entity.values():
            event = Event(type=EVENT_BAR, data=x)
            common_signals.bar_signal.send(event)
        self.last_entity.clear()
