import json
from collections import defaultdict


class ProxyPollen(object):
    """
    +-------------------+---------------+--------------------+
    | Python            | JSON          |Pollen(Can change   |
    +===================+===============+====================+
    | dict              | object        |cls:Data,Request    |
    +-------------------+---------------+--------------------+
    | list, tuple,set   | array         |                    |
    +-------------------+---------------+--------------------+
    | str               | string        | Enum               |
    +-------------------+---------------+--------------------+
    | int, float        | number        |                    |
    +-------------------+---------------+--------------------+
    | True              | true          |                    |
    +-------------------+---------------+--------------------+
    | False             | false         |                    |
    +-------------------+---------------+--------------------+
    | None              | null          |                    |
    +-------------------+---------------+--------------------+
    |Datetime           | str(Datetime) | Datetime           |
    +-------------------+---------------+--------------------+
    """
    """
        str_can_to:用于筛选str转python类型时的tag类,存在str_tags
        default_tags:所有tag实例
        str_tags: ""
        enum_store:自定义Enum仓库
        data_class_store:自定义Data类仓库[BaseDataClass,BaseRequestClass]
        data_base_class:     BaseData
        request_base_class:  BaseRequest
    """
    str_can_to = ['enum', 'datetime']
    default_tags = dict()
    str_tags = dict()
    enum_store = dict()

    data_class_store = defaultdict(set)
    data_base_class = None
    request_base_class = None

    def __init__(self, tags: list = None, enums: list = None, data_class=None, request_class=None):
        if tags: self.labeling(tags)
        if enums: self.add_enum(enums)
        if data_class: self.add_data_class(data_class)
        if request_class: self.add_request_class(request_class)
        self._init_class_store()

    def _init_class_store(self):
        # 初始化 data_class_store
        data = data_class + request_class
        for cls in data:
            cls_name = cls.__name__
            attribute = set()
            for c in cls.__dict__['__annotations__']:
                if c.startswith("__") or c.startswith("create"):
                    continue
                attribute.add(c)
            self.data_class_store[cls] = attribute

    def labeling(self, tags: list):
        """
        添加tag类
        :param tags:
        :return:
        """
        if not isinstance(tags, list): raise TypeError("[^^]tags must list")
        for t in tags:
            self.default_tags[t.tag] = t(self)
            if t.tag in self.str_can_to:
                self.str_tags[t.tag] = t(self)

    def add_enum(self, enums: list):
        """
        添加自定义Enum类属性值
        :param enums:
        :return:
        """
        if not isinstance(enums, list): raise TypeError("[^^]enums must list")
        for e in enums:
            for _, v in e.__members__.items():
                self.enum_store[v.value] = v

    def add_data_class(self, data_class: list):
        """
        {cls_name:{attr1,attr2},} 模糊获取类变量属性
        :param data_class:
        :return:
        """
        if not isinstance(data_class, list): raise TypeError("[^^]data_class must list")
        self.data_base_class = data_class[0].__bases__

    def add_request_class(self, request_class: list):
        """
        {cls_name:{attr1,attr2},} 模糊获取类变量属性
        :param request_class:
        :return:
        """
        if not isinstance(request_class, list): raise TypeError("[^^]request_class must list")
        self.request_base_class = request_class[0].__bases__

    def update_data_class_store(self, data):
        """
        在dumps时将类实例的全部属性覆盖模糊获取的属性,提高精确性
        :param data:  Dataclass或RequestClass实例
        :return:
        """
        cls_name = data.__class__.__name__
        for c in list(self.data_class_store.keys()):
            if c.__name__ == cls_name:
                self.data_class_store[c] = set(data._to_dict().keys())

    @classmethod
    def find_tag(cls, value):
        """
        :param value:
        :return:
        """
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
        tag = cls.find_tag(json_data)
        if tag:
            return tag.to_pollen(json_data)

    @classmethod
    def dumps(cls, value):
        """
        to json
        :param value:
        :return:
        """
        tag = cls.find_tag(value)
        if tag:
            return json.dumps(tag.to_json(value), ensure_ascii=False)


from .tag import tags
from ctpbee.constant import enums, data_class, request_class

Pollen = ProxyPollen(tags=tags, enums=enums, data_class=data_class, request_class=request_class)
