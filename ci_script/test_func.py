"""
this file was used to check function

if raise any error, means test was failed.
the change should compatible with fronted version
"""
from datetime import datetime
from unittest import TestCase


# test the  trading day
class Test(TestCase):

    def test_looper(self):
        pass

    def test_get_current_trade_day(self):
        from ctpbee import get_current_trade_day
        date_string = "2020-02-27 1:30:00"
        x = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        cu = get_current_trade_day(x)
        self.assertEqual("2020-02-27", cu)

        date_string = "2021-02-27 1:30:00"
        x = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        cu = get_current_trade_day(x)
        self.assertEqual("2021-03-01", cu)

        date_string = "2021-02-27 3:30:00"
        x = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        cu = get_current_trade_day(x)
        self.assertEqual(None, cu)

        date_string = "2021-03-01 1:30:00"
        x = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        cu = get_current_trade_day(x)
        self.assertEqual("2021-03-01", cu)

        date_string = "2021-03-01 16:30:00"
        x = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        cu = get_current_trade_day(x)
        self.assertEqual("2021-03-02", cu)
