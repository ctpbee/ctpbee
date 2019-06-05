# encoding: UTF-8
from collections import Callable

from ctpbee.ctp.constant import BarData, TickData, SharedData
from ctpbee.event_engine import Event
from ctpbee.event_engine import rpo
from ctpbee.ctp.constant import EVENT_BAR, EVENT_SHARED
from ctpbee.context import current_app

class DataGenerator:
    """
    For:
    1. generating 1 minute bar data from tick data
    2. generateing x minute bar data from 1 minute data
    3, generate shared time data
    """

    def __init__(self):
        """Constructor"""
        self.bar = None
        self.last_tick = None
        self.vt_symbol = None
        self.last_price = None
        self.pre_close = None
        self.volume = None
        self.last_volume = None
        self.open_interest = None
        self.average_price = None

        self.denominator = 0
        self.molecule = 0

        self.XMIN = current_app.config.get("XMIN")
        self._generator()
        self.rd = None

    def _generator(self):
        for x in self.XMIN:
            setattr(self, "min_{}".format(x), x)
            setattr(self, "min_{}_bar".format(x), None)

    def update_tick(self, tick: TickData):
        """
        Update new tick data into generator and new_shared time data.
        """
        new_minute = False
        self.last_price = tick.last_price
        self.open_interest = tick.open_interest
        self.volume = tick.volume
        self.molecule = self.molecule + tick.last_price * tick.volume
        self.denominator = self.denominator + tick.volume
        try:
            self.average_price = self.molecule / self.denominator
        except ZeroDivisionError:
            self.average_price = tick.last_price

        if self.last_volume is None:
            self.last_volume = tick.volume
        if self.vt_symbol is None:
            self.vt_symbol = tick.vt_symbol
        if not self.bar:
            new_minute = True
        elif self.bar.datetime.minute != tick.datetime.minute:
            self.bar.datetime = self.bar.datetime.replace(
                second=0, microsecond=0
            )
            self.bar.interval = 1
            event = Event(type=EVENT_BAR, data=self.bar)
            rpo.put(event)
            [self.update_bar(x, getattr(self, "min_{}_bar".format(x)), self.bar) for x in self.XMIN]
            new_minute = True
        if new_minute:
            shared = SharedData(last_price=round(self.last_price, 2), datatime=tick.datetime, vt_symbol=self.vt_symbol,
                                open_interest=self.open_interest, average_price=round(self.average_price, 2),
                                volume=self.volume - self.last_volume)
            self.last_volume = tick.volume
            event = Event(type=EVENT_SHARED, data=shared)
            rpo.put(event)
            self.bar = BarData(
                symbol=tick.symbol,
                exchange=tick.exchange,
                datetime=tick.datetime,
                gateway_name=tick.gateway_name,
                open_price=tick.last_price,
                high_price=tick.last_price,
                low_price=tick.last_price,
                close_price=tick.last_price,
            )
        else:
            self.bar.high_price = max(self.bar.high_price, tick.last_price)
            self.bar.low_price = min(self.bar.low_price, tick.last_price)
            self.bar.close_price = tick.last_price
            self.bar.datetime = tick.datetime

        if self.last_tick:
            volume_change = tick.volume - self.last_tick.volume
            self.bar.volume += max(volume_change, 0)
        self.last_tick = tick

    def update_bar(self, xmin, xmin_bar: BarData, bar: BarData):
        """
        Update 1 minute bar into generator
        """
        if not xmin_bar:
            xmin_bar = BarData(
                symbol=bar.symbol,
                exchange=bar.exchange,
                datetime=bar.datetime,
                gateway_name=bar.gateway_name,
                open_price=bar.open_price,
                high_price=bar.high_price,
                low_price=bar.low_price
            )
        else:
            xmin_bar.high_price = max(
                xmin_bar.high_price, bar.high_price)
            xmin_bar.low_price = min(
                xmin_bar.low_price, bar.low_price)

        xmin_bar.close_price = bar.close_price
        xmin_bar.volume += int(bar.volume)
        if not (bar.datetime.minute + 1) % xmin:
            xmin_bar.datetime = xmin_bar.datetime.replace(
                second=0, microsecond=0
            )
            xmin_bar.interval = xmin
            event = Event(type=EVENT_BAR, data=xmin_bar)
            rpo.put(event)
            xmin_bar = None

    def generate(self):
        if self.bar is not None:
            self.bar.interval = 1
            event = Event(type=EVENT_BAR, data=self.bar)
            rpo.put(event)
        for x in self.XMIN:
            if self.bar is not None:
                bar = getattr(self, "min_{}_bar".format(x))
                bar.interval = x
                event = Event(type=EVENT_BAR, data=bar)
                rpo.put(event)
        self.bar = None
        [setattr(self, "min_{}_bar".format(x), None) for x in self.XMIN]
