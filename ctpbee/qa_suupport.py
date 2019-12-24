from pprint import pprint

import QUANTAXIS as qa
import pymongo as pg
from pandas import DataFrame


class QDataSupport:

    def __init__(self, **kwargs):
        """
        param in kwargs:
            type: database type : now only support mongodb
            host: database host
            port: database port
            user: database user
            pwd : database password
        """
        self.pg_client = pg.MongoClient(self._get_link(**kwargs))

    @property
    def quantaxis(self):
        return self.pg_client['quantaxis']

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
        if df:
            return qa.QA_fetch_future_list()
        else:
            def remove_id(data):
                del data['_id']
                return data

            return list(map(remove_id, list(self.quantaxis["future_list"].find())))

    def get_future_min(self, local_symbol, min, **kwargs):
        start = kwargs.get("")

    def get_future_tick(self, local_symbol: str, **kwargs):
        pass

    def covert_index(self, type_="future"):
        """ 更新下标"""
        pass


a = QDataSupport()

rst = a.get_future_list()

pprint(rst)
