from types import MethodType
from typing import Callable


class A:
    XMIN = [1, 2, 3, 4, 5]

    def __init__(self):
        for x in self.XMIN:
            setattr(self, f"min_{x}_bar", x)

        gen = lambda item: setattr(self, f"get_min_{item}_bar",
                                   property(MethodType(lambda self: getattr(self, f"min_{item}_bar"), self)).fget())
        for x in self.XMIN:
            gen(x)


if __name__ == '__main__':
    a = A()
    print(a.get_min_1_bar)
