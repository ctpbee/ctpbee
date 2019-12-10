from datetime import datetime
from functools import total_ordering
from queue import Queue

from ctpbee import CtpbeeApi, auth_time
from pymongo import MongoClient

DATABASE_NAME = "ctpbee_tick"
mongo_client = MongoClient()

database_c = mongo_client[DATABASE_NAME]


@total_ordering
class TimeIt:
    """ 主要是来实现一个减法"""

    def __init__(self, datetime_obj: datetime):
        self._datetime = datetime_obj

    def __sub__(self, other: datetime):
        """
        实现减法操作
        返回绝对值
        """
        if not isinstance(other, TimeIt) and not isinstance(other, datetime):
            raise ValueError("参数类型不同无法使用减法")
        if isinstance(other, datetime):
            return int(abs(self._datetime.timestamp() - other.timestamp()))
        elif isinstance(other, TimeIt):
            return int(abs(self._datetime.timestamp() - other._datetime.timestamp()))

    def __eq__(self, other):
        if isinstance(other, datetime):
            return self._datetime == other
        elif isinstance(other, TimeIt):
            return self._datetime == other._datetime

    def __lt__(self, other):
        if isinstance(other, datetime):
            return self._datetime < other
        elif isinstance(other, TimeIt):
            return self._datetime < other._datetime


class Market(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        # 创建一个datetime队列
        self.datetime_queue = Queue()
        # 队列长度
        self.queue_length = 5

    def on_bar(self, bar):
        """ 处理k线数据 """

    def on_contract(self, contract):
        """ 订阅到推送过来的合约 """
        self.action.subscribe(contract.local_symbol)

    def on_tick(self, tick):
        """ 处理tick信息 """
        if not auth_time(tick.datetime.time()):
            """ 过滤非交易时间段的数据 """
            return

        if self.datetime_queue.empty() or self.datetime_queue.qsize() <= self.queue_length:
            pass
        else:
            q = self.datetime_queue.get()
            interval = q - tick.datetime
            if interval > 3600 * 4 or q < tick.datetime:
                """ 如果出现间隔过大或者时间小于队列的里面的数据，那么代表着脏数据"""
                return
        self.datetime_queue.put(TimeIt(tick.datetime))
        database_c[tick.local_symbol].insert_one(tick._to_dict())
        print(tick)


def create_app():
    from ctpbee import CtpBee
    app = CtpBee("recorder", __name__)
    info = {
        "CONNECT_INFO": {
            "userid": "",  # 期货账户名
            "password": "",  # 登录密码
            "brokerid": "",  # 期货公司id
            "md_address": "",  # 行情地址
            "td_address": "",  # 交易地址
            "appid": "",  # 产品名
            "auth_code": "",  # 认证码
            "product_info": ""  # 产品信息
        },
        "INTERFACE": "ctp",  # 登录期货生产环境接口
    }
    # 载入配置信息
    app.config.from_mapping(info)
    # 创建实例
    ext = Market("market")
    # 载入容器
    app.add_extension(ext)
    return app


if __name__ == '__main__':
    from ctpbee import hickey
    # 使用24小时模块进行分发
    hickey.start_all(create_app)
