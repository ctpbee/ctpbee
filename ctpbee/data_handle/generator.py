# encoding: UTF-8
from collections import Callable

from ctpbee.api.custom_var import BarData, TickData
from ctpbee.event_engine import Event
from ctpbee.event_engine import controller
from ctpbee.api.custom_var import EVENT_BAR, EVENT_SHARED
from ctpbee.context import current_app
class DataGenerator:
    """
    For:
    1. generating 1 minute bar data from tick data
    2. generateing x minute bar data from 1 minute data
    3,
    """

    def __init__(self):
        """Constructor"""
        self.bar = None
        self.last_tick = None
        self.XMIN = current_app().config.get("XMIN")
        self._generator()

    def _generator(self):
        for x in self.XMIN:
            setattr(self, "min_{}".format(x), x)
            setattr(self, "min_{}_bar".format(x), None)

    def update_tick(self, tick: TickData):
        """
        Update new tick data into generator.
        """
        new_minute = False

        if not self.bar:
            new_minute = True
        elif self.bar.datetime.minute != tick.datetime.minute:
            self.bar.datetime = self.bar.datetime.replace(
                second=0, microsecond=0
            )
            event = Event(type=EVENT_BAR, data=self.bar, interval=1)
            print(event)
            controller.put(event)
            for x in self.XMIN:
                self.update_bar(x, getattr(self, "min_{}_bar".format(x)), self.bar)
            new_minute = True
        if new_minute:
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
            event = Event(type=EVENT_BAR, data=xmin_bar, interval=xmin)
            controller.put(event)
            xmin_bar = None

    def generate(self):
        if self.bar is not None:
            event = Event(type=EVENT_BAR, data=self.bar, interval=1)
            controller.put(event)
        for x in self.XMIN:
            if self.bar is not None:
                event = Event(type=EVENT_BAR, data=getattr(self, "min_{}_bar".format(x)), interval=x)
                controller.put(event)
        self.bar = None
        for x in self.XMIN:
            setattr(self, "min_{}_bar".format(x), None)
