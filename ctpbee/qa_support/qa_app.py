import time
import pymongo as pg
from pandas import DataFrame

from ctpbee.qa_support.qa_func import QA_util_time_stamp


class QADataSupport:
    price = ["open", "high", "low", "close"]

    def __init__(self, **kwargs):
        """
        param in kwargs:
            type: database type : now only support mongodb
            host: database host
            port: database port
            user: database user
            pwd : database password
        """
        self.mongo_client = pg.MongoClient(self._get_link(**kwargs))

        #  > todo: 是否能够通过创建索引来进一步提高查询速度？
        # self.fix_index()

    def fix_index(self):
        """
        检查索引
        """
        self.quantaxis.future_min.create_index("time_stamp")

    @property
    def quantaxis(self):
        return self.mongo_client['quantaxis']

    @staticmethod
    def _get_link(**kwargs):
        if "host" in kwargs.keys():
            host = kwargs.get("host")
        else:
            host = "127.0.0.1"

        if "port" in kwargs.keys():
            port = kwargs.get("port")

        else:
            port = 27017

        if "user" in kwargs.keys():
            user = kwargs.get("user")
        else:
            user = None
        if "pwd" in kwargs.keys():
            pwd = kwargs.get("pwd")
        else:
            pwd = None
        auth = ""
        if user and pwd:
            auth = f"{user}:{'*' * len(pwd)}@"
        return f"mongodb://{auth}{host}:{port}"

    def get_future_list(self, df=False) -> list or DataFrame:
        """
        返回期货产品列表
        :param df: 是否转换成dataframe
        :return: list or DataFrame
        """

        def remove_id(data):
            del data['_id']
            return data

        return list(map(remove_id, list(self.quantaxis["future_list"].find())))

    def get_future_min(self, local_symbol: str, frq: str = "1min", **kwargs):
        # 此处需要一个更加完善的参数检查器 ---> 也许我能通过阅读pip源码获取灵感。

        if local_symbol.count(".") > 1:
            raise ValueError("local_symbol格式错误, 期望: 合约代码.交易所")
        if "." in local_symbol:
            symbol = local_symbol.split(".")[0]
        else:
            symbol = local_symbol
        try:
            exchange = local_symbol.split(".")[1]
        except IndexError:
            exchange = kwargs.get("exchange", None)
            if not exchange:
                raise ValueError("local_symbol中,你仅仅传入了合约名称，请通过exchange参数传入交易所代码")
        start = kwargs.get("start")
        end = kwargs.get("end")

        query = {
            "code": symbol.upper(),
            "type": frq
        }
        if start and end:
            query['time_stamp'] = \
                {
                    "$gte": QA_util_time_stamp(start),
                    "$lte": QA_util_time_stamp(end)
                }
        format_option = dict(open=1, close=1, high=1, low=1, datetime=1, code=1, price=1,
                             _id=0, tradetime=1, trade=1)
        _iterable = self.quantaxis['future_min'].find(query, format_option, batch_size=10000)

        def pack(data: dict):
            data['symbol'] = data.pop("code")
            data['local_symbol'] = data['symbol'] + "." + exchange
            data['volume'] = data.pop("trade")
            for key in self.price:
                data[key + "_price"] = data.pop(key)
            return data

        return list(map(pack, _iterable))

    def get_future_tick(self, local_symbol: str, **kwargs):
        pass

    def covert_index(self, type_="future"):
        """ 更新下标"""
        pass


if __name__ == '__main__':
    support = QADataSupport(host="127.0.0.1")
    ctime = time.time()
    rst = support.get_future_min("rb2001.SHFE", start="2019-8-1 10:00:10", end="2019-10-1 10:00:10")
    print(f"cost: {time.time() - ctime}s")

# 7935
# cost: 0.14893150329589844
