#  provide data pointer
from .abstract import DataPointerAbstract


class TickPointer(DataPointerAbstract):

    def insert(self, **kwargs):
        pass

    def read(self, **kwargs):
        """read  condition in here"""
        pass

    def delete(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass


class BarPointer(DataPointerAbstract):
    def insert(self, **kwargs):
        pass

    def read(self, **kwargs):
        """read  condition in here"""
        pass

    def delete(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass
