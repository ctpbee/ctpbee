from abc import ABC
from typing import Mapping


class DataPointerAbstract(ABC):
    """
        数据库写入器抽象
        基本数据库操作封装
    """

    def __init__(self):
        pass

    def insert_one(self, **kwargs: Mapping):
        raise NotImplemented

    def insert_many(self, **kwargs: Mapping):
        raise NotImplemented

    def read(self, **kwargs: Mapping):
        raise NotImplemented

    def update(self, **kwargs: Mapping):
        raise NotImplemented

    def delete(self, **kwargs: Mapping):
        raise NotImplemented
