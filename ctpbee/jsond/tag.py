import re
from datetime import datetime
from enum import Enum

TAG_ENUM = "enum"
TAG_DICT = "dict"
TAG_LIST = "list"
TAG_TUPLE = "tuple"
TAG_DATETIME = "datetime"
TAG_BYTES = "bytes"
TAG_STR = "str"
TAG_NUM = "num"
TAG_DATACLASS = "dataclass"
TAG_NONE = "none"
TAG_SET = "set"


class PollenTag(object):
    def __init__(self, proxy):
        self.proxy = proxy

    def check(self, data):
        """检查类型"""
        pass

    def to_json(self, data):
        """转json"""
        pass

    def to_pollen(self, data):
        """转python"""
        pass


class TagDataClass(PollenTag):
    tag = TAG_DATACLASS

    def check(self, data):
        try:
            return isinstance(data, self.proxy.data_base_class) or isinstance(
                data, self.proxy.request_base_class
            )
        except TypeError:
            return False

    def match_data_class(self, data: dict):
        """
            dict匹配到相应类
        :param data:
        :return:
        """
        attrs = set(data.keys())
        if len(attrs) < 1:
            return None
        for cls_name, cls_attr in self.proxy.data_class_store.items():
            if attrs == cls_attr:
                return cls_name
        return None

    def to_json(self, data):
        """
        调用类_to_dict,同时更新data_class_store
        :param data:
        :return:
        """
        tag_dict = self.proxy.default_tags[TAG_DICT]
        res = data._to_dict()
        self.proxy.update_data_class_store(data)  # 更新
        return tag_dict.to_json(res)

    def to_pollen(self, data: list):
        """
        创建类实例:DataClass,RequestClass
        :param data:
        :return:
        """
        instance = data[0]._create_class(data[1])
        return instance


class TagEnum(PollenTag):
    tag = TAG_ENUM

    def check(self, data):
        return isinstance(data, Enum)

    def find_enum(self, data):
        """
        查找
        :param data:
        :return:
        """
        return self.proxy.enum_store.get(data, None)

    def to_json(self, data):
        return data.value

    def to_pollen(self, data):
        return self.find_enum(data)


class TagDict(PollenTag):
    tag = TAG_DICT

    def check(self, data):
        return isinstance(data, dict)

    def to_json(self, data: dict):
        """
        分解dict,逐项查找替换
        :param data:
        :return:
        """
        if data is None:
            return
        for k in list(data.keys()):
            key_ok = value_ok = False
            for tag in self.proxy.default_tags.values():
                """顺序很重要;先value"""
                if not value_ok and tag.check(data[k]):
                    data[k] = tag.to_json(data[k])
                    value_ok = True
                if not key_ok and tag.check(k):
                    data[tag.to_json(k)] = data.pop(k)
                    key_ok = True
        return data

    def to_pollen(self, data):
        """
        分解dict,逐项查找替换
        :param data:
        :return:
        """
        if data is None:
            return
        tag_dataclass = self.proxy.default_tags[TAG_DATACLASS]
        cls_name = tag_dataclass.match_data_class(data)
        for k in list(data.keys()):
            key_ok = value_ok = False
            for tag in self.proxy.default_tags.values():
                if not value_ok and tag.check(data[k]):
                    data[k] = tag.to_pollen(data[k])
                    value_ok = True
                if not key_ok and tag.check(k):
                    data[tag.to_pollen(k)] = data.pop(k)
                    key_ok = True
        if cls_name:
            return tag_dataclass.to_pollen([cls_name, data])
        return data


class TagList(PollenTag):
    tag = TAG_LIST

    def check(self, data):
        return isinstance(data, list)

    def to_json(self, data):
        """
        遍历list
        :param data:
        :return:
        """
        if data is None:
            return
        size = len(data)
        i = 0
        while i < size:
            li = data[i]
            for tag in self.proxy.default_tags.values():
                if tag.check(li):
                    data[i] = tag.to_json(li)
                    break
            i += 1
        return data

    def to_pollen(self, data):
        if data is None:
            return
        size = len(data)
        i = 0
        while i < size:
            li = data[i]
            for tag in self.proxy.default_tags.values():
                if tag.check(li):
                    data[i] = tag.to_pollen(li)
                    break
            i += 1
        return data


class TagTuple(PollenTag):
    tag = TAG_TUPLE

    def check(self, data):
        return isinstance(data, tuple)

    def to_json(self, data):
        if data is None:
            return
        temp = list(data)
        size = len(data)
        i = 0
        while i < size:
            li = data[i]
            for tag in self.proxy.default_tags.values():
                if tag.check(li):
                    temp[i] = tag.to_json(li)
                    break
            i += 1
        return tuple(temp)

    def to_pollen(self, data):
        pass


class TagSet(PollenTag):
    tag = TAG_SET

    def check(self, data):
        return isinstance(data, set)

    def to_json(self, data):
        return list(data)

    def to_pollen(self, data):
        return data


class TagDatetime(PollenTag):
    tag = TAG_DATETIME
    patternForTimef = r"\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}.\d+"
    patternForTime = r"\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}"

    def check(self, data):
        return isinstance(data, datetime)

    def to_json(self, data):
        if data is None:
            return
        if data.microsecond != 500000:
            time_str = datetime.strftime(data, "%Y-%m-%d %H:%M:%S")
        else:
            time_str = datetime.strftime(data, "%Y-%m-%d %H:%M:%S.%f")
        return time_str

    def to_pollen(self, data):
        if re.match(self.patternForTimef, data):
            return datetime.strptime(data, "%Y-%m-%d %H:%M:%S.%f")
        if re.match(self.patternForTime, data):
            return datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        return None


class TagBytes(PollenTag):
    tag = TAG_BYTES

    def check(self, data):
        return isinstance(data, bytes)

    def to_json(self, data):
        return data.decode()


class TagNum(PollenTag):
    tag = TAG_NUM

    def check(self, data):
        """bool: true == 1 ; false == 0"""
        return isinstance(data, int) or isinstance(data, float)

    def to_json(self, data):
        return data

    def to_pollen(self, data):
        return data


class TagNone(PollenTag):
    tag = TAG_NONE

    def check(self, data):
        return data is None

    def to_json(self, data):
        return data

    def to_pollen(self, data):
        return data


class TagStr(PollenTag):
    tag = TAG_STR

    def check(self, data):
        return isinstance(data, str)

    def to_json(self, data):
        return data

    def to_pollen(self, data):
        """
        字符不能准确判断,但能缩小范围:Enum,Datetime或Int
        :param data:
        :return:
        """
        for s in self.proxy.str_tags.values():
            res = s.to_pollen(data)
            if res is not None:
                return res
        return data


tags = [
    TagStr,
    TagDict,
    TagDataClass,
    TagEnum,
    TagDatetime,
    TagList,
    TagTuple,
    TagNum,
    TagBytes,
    TagNone,
    TagSet,
]
