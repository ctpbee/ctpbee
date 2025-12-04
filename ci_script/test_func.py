"""
this file was used to check function

if raise any error, means test was failed.
the change should compatible with fronted version
"""
from datetime import datetime, time
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

    def test_get_day_from(self):
        from ctpbee import get_day_from
        # 测试正常情况
        self.assertEqual("2020-01-03", get_day_from("2020-01-02", 1))
        self.assertEqual("2019-12-31", get_day_from("2020-01-02", -1))
        
        # 测试边界情况
        with self.assertRaises(IndexError):
            get_day_from("2020-01-02", 100000)
        
        with self.assertRaises(IndexError):
            get_day_from("2020-01-02", -100000)
        
        # 测试2026年的日期
        self.assertEqual("2026-01-06", get_day_from("2026-01-05", 1))
        self.assertEqual("2025-12-31", get_day_from("2026-01-05", -1))

    def test_helper_generate_order_req_by_str(self):
        from ctpbee import helper
        from ctpbee.constant import Exchange, Direction, Offset, OrderType
        
        # 测试生成订单请求
        order_req = helper.generate_order_req_by_str(
            symbol="rb2105", 
            exchange="SHFE", 
            direction="long", 
            offset="open", 
            type="limit", 
            volume=1, 
            price=5000.0
        )
        
        self.assertEqual(order_req.symbol, "rb2105")
        self.assertEqual(order_req.exchange, Exchange.SHFE)
        self.assertEqual(order_req.direction, Direction.LONG)
        self.assertEqual(order_req.offset, Offset.OPEN)
        self.assertEqual(order_req.type, OrderType.LIMIT)
        self.assertEqual(order_req.volume, 1)
        self.assertEqual(order_req.price, 5000.0)
        
        # 测试带有.的symbol
        order_req = helper.generate_order_req_by_str(
            symbol="rb2105.SHFE", 
            exchange="SHFE", 
            direction="short", 
            offset="close", 
            type="market", 
            volume=2, 
            price=5100.0
        )
        self.assertEqual(order_req.symbol, "rb2105")

    def test_get_ctpbee_path(self):
        from ctpbee import get_ctpbee_path
        import os
        import platform
        
        # 测试获取ctpbee路径
        path = get_ctpbee_path()
        self.assertIsInstance(path, str)
        self.assertTrue(os.path.exists(path))
        
        # 检查路径是否在用户目录下
        if platform.system() == "Windows":
            self.assertTrue("\\.ctpbee" in path)
        else:
            self.assertTrue(".ctpbee" in path)

    def test_auth_time(self):
        from ctpbee import auth_time
        from datetime import datetime
        
        # 测试交易时间验证
        # 工作日白天
        dt = datetime(2024, 1, 2, 10, 0, 0)  # 周二
        self.assertTrue(auth_time(dt))
        
        # 工作日晚上
        dt = datetime(2024, 1, 2, 22, 0, 0)  # 周二晚上
        self.assertTrue(auth_time(dt))
        
        # 周末白天
        dt = datetime(2024, 1, 6, 10, 0, 0)  # 周六
        self.assertFalse(auth_time(dt))
        
        # 周末晚上
        dt = datetime(2024, 1, 6, 22, 0, 0)  # 周六晚上
        self.assertFalse(auth_time(dt))
        
        # 非交易时间段
        dt = datetime(2024, 1, 2, 8, 0, 0)  # 周二早上8点
        self.assertFalse(auth_time(dt))

    def test_hickey_auth_time(self):
        from ctpbee import hickey
        from datetime import datetime, time
        
        # 测试hickey的auth_time方法
        # 交易时间段内
        dt = datetime(2024, 1, 2, 10, 0, 0)  # 周二上午
        self.assertTrue(hickey.auth_time(dt))
        
        # 夜盘时间
        dt = datetime(2024, 1, 2, 22, 0, 0)  # 周二晚上
        self.assertTrue(hickey.auth_time(dt))
        
        # 凌晨时间
        dt = datetime(2024, 1, 3, 1, 0, 0)  # 周三凌晨1点
        self.assertTrue(hickey.auth_time(dt))
        
        # 非交易时间段
        dt = datetime(2024, 1, 2, 8, 0, 0)  # 周二早上8点
        self.assertFalse(hickey.auth_time(dt))
        
        # 周末
        dt = datetime(2024, 1, 6, 10, 0, 0)  # 周六
        self.assertFalse(hickey.auth_time(dt))

    def test_hickey_add_seconds(self):
        from ctpbee import hickey
        from datetime import time
        
        # 测试添加秒数
        t = time(10, 0, 0)
        # 向前300秒
        result = hickey.add_seconds(t, 300, direction=False)
        self.assertEqual(result, time(9, 55, 0))
        
        # 向后300秒
        result = hickey.add_seconds(t, 300, direction=True)
        self.assertEqual(result, time(10, 5, 0))

    def test_jsond_functions(self):
        from ctpbee import dumps, loads
        
        # 测试JSON序列化和反序列化
        test_data = {"name": "ctpbee", "version": 1.6, "active": True}
        
        # 序列化
        json_str = dumps(test_data)
        self.assertIsInstance(json_str, str)
        
        # 反序列化
        parsed_data = loads(json_str)
        self.assertEqual(parsed_data, test_data)
        
        # 测试复杂数据
        complex_data = {"list": [1, 2, 3], "dict": {"nested": "value"}, "none": None}
        json_str = dumps(complex_data)
        parsed_data = loads(json_str)
        self.assertEqual(parsed_data, complex_data)
