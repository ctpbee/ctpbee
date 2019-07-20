import json


class ProxyPollen(object):
    """
    python_eq_json:用于筛选str转python类型时的tag类,存在str_tags
    default_tags:所有tag实例
    str_tags: ""
    enum_store:自定义Enum仓库
    data_class_store:自定义Data类仓库
    """
    python_eq_json = ['dict', 'list', 'tuple', 'num', 'str']
    default_tags = dict()
    str_tags = dict()
    enum_store = dict()
    data_class_store = dict()

    def __init__(self, tags: list = None, enums: list = None, data_class=None):
        if tags: self.labeling(tags)
        if enums: self.add_enum(enums)
        if data_class: self.add_data_class(data_class)

    def labeling(self, tags: list):
        """
        添加tag类
        :param tags:
        :return:
        """
        for t in tags:
            self.default_tags[t.tag] = t(self)
            if t.tag not in self.python_eq_json:
                self.str_tags[t.tag] = t(self)

    def add_enum(self, enums: list):
        """
        添加自定义Enum类属性值
        :param enums:
        :return:
        """
        for e in enums:
            for _, v in e.__members__.items():
                self.enum_store[v.value] = v

    def add_data_class(self, data_class: list):
        pass

    @classmethod
    def run(cls, value):
        for t in cls.default_tags.values():
            if t.check(value):
                return t

    @classmethod
    def loads(cls, json_data):
        """
        to python
        :param value:
        :return:
        """
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        tag = cls.run(json_data)
        if tag:
            return tag.to_pollen(json_data)

    @classmethod
    def dumps(cls, value):
        """
        to json
        :param value:
        :return:
        """
        tag = cls.run(value)
        if tag:
            return json.dumps(tag.to_json(value), ensure_ascii=False)



from .tag import tags
from ctpbee.constant import enums

Pollen = ProxyPollen(tags=tags, enums=enums)
