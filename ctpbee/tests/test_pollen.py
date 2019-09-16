import unittest

from ctpbee.constant import *
from ctpbee.json import dumps, loads


class TestPollen(unittest.TestCase):
    def test_init(self):
        """ 载入测试数据 """
        pass

    def test_transfer_serial_request(self):
        """ 测试转账数据载入 """
        a = AccountRegisterRequest(bank_id="wh", currency_id="123")
        test = {"data": a}
        p = dumps(test)
        print("转换json: ", p)
        print("转回", loads(p))

        self.assertEqual(type(loads(p)['data']), AccountRegisterRequest)


if __name__ == '__main__':
    unittest.main()
