"""
ctpbee里面的核心数据访问模块

此模块描述了ctpbee里面默认的数据访问中心，同时它也可以被回测模块所调用
整齐高于混乱
"""
from abc import ABCMeta, ABC


class Missing:
    def __str__(self):
        return "属性缺失/ Attribute Missing"


missing = Missing


class BasicCenterModel(ABC):
    __dict__ = {}

    def __new__(cls, app):
        # temp = cls.__init__(cls, app)
        super(BasicCenterModel, cls).__new__(cls)

    def __getattr__(self, item):
        """ 返回"""
        if item not in self.__dict__:
            return missing

    def __setattr__(self, key, value):
        """ 拦截任何设置属性的操作 它应该不运行任何关于set的操作 """
        return


class Center(BasicCenterModel):

    def __init__(self, app):
        super().__init__(app)

    def __str__(self):
        return "ctpbee 统一数据调用接口"


if __name__ == '__main__':
    a = Center(app="123")
    print(a)
    # print(a.b)
