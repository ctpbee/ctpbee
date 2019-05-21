#  provide data pointer
from typing import Mapping

from .abstract import DataPointerAbstract
from .support import generate_data_class

orm_map = generate_data_class()


class TickPointer(DataPointerAbstract):
    def __init__(self):
        super().__init__()
        self.map = {key: orm_map[key] for key in orm_map.keys() if key.startswith('t')}

    def insert_one(self, **kwargs: Mapping) -> bool:

        """
        insert into single data
        :param kwargs: {'symbol':'AP910', 'data':{}}
        :return bool
        """
        print(kwargs)
        cls = self.map.get(f"t{kwargs.get('symbol')}")
        if cls is None:
            raise AttributeError('orm map is None, please check your config')
        single = cls().to(kwargs.get('data'))
        single.save()
        return True

    def insert_many(self, **kwargs: Mapping) -> bool:
        cls = self.map.get(f"t{kwargs.get('symbol')}")
        try:
            cls.insert_many(kwargs.get('data_list')).excute()
        except Exception as e:
            print(e)
            return False
        return True

    def read(self, **kwargs: Mapping):
        """read  condition in here"""
        pass

    def delete(self, **kwargs: Mapping):
        pass

    def update(self, **kwargs: Mapping):
        pass


class BarPointer(DataPointerAbstract):

    def __init__(self):
        super().__init__()
        self.map = {key: orm_map[key] for key in orm_map.keys() if key.startswith('b')}

    def insert_one(self, **kwargs: Mapping) -> bool:
        """insert into single data
        :param kwargs: {'symbol':'AP910', 'data':{}}
        :return bool
        """
        cls = self.map.get(f"t{kwargs.get('symbol')}")
        single = cls().to(kwargs.get('data'))
        single.save()
        return True

    def insert_many(self, **kwargs: Mapping) -> bool:
        cls = self.map.get(f"t{kwargs.get('symbol')}")
        try:
            cls.insert_many(kwargs.get('data_list')).excute()
        except Exception as e:
            print(e)
            return False
        return True

    def read(self, **kwargs: Mapping):
        """read  condition in here"""
        pass

    def delete(self, **kwargs: Mapping):
        pass

    def update(self, **kwargs: Mapping):
        pass
