from abc import ABC


class DataPointerAbstract(ABC):
    """
        数据库写入器抽象
        基本数据库操作封装
    """
    config = dict()
    default_config = {}
    def __init__(self):
        pass

    def insert_one(self, **kwargs):
        raise NotImplemented
    def insert_many(self, **kwargs):
        raise NotImplemented

    def read(self, **kwargs):
        raise NotImplemented

    def update(self, **kwargs):
        raise NotImplemented

    def delete(self, **kwargs):
        raise NotImplemented
