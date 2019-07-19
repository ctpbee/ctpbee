import re
from base64 import b64encode, b64decode
from collections import defaultdict
from datetime import datetime
from enum import Enum

TAG_ENUM = 'e'
TAG_DICT = 'd'
TAG_LIST = 'l'
TAG_TUPLE = 't'
TAG_DATETIME = 'dt'
TAG_BYTES = 'b'
TAG_STR = 's'
TAG_NUM = 'n'


class PollenTag(object):
    def __init__(self, tags, enums):
        self.proxy = tags

    def check(self, value):
        """检查类型"""
        pass

    def to_json(self, value):
        """转json"""
        pass

    def to_pollen(self, value):
        """转python"""
        pass


class TagEnum(PollenTag):
    tag = TAG_ENUM

    def __init__(self, tags, enums):
        self.proxy = tags
        self.enum_store = defaultdict(dict)
        for e in enums:
            for _, v in e.__members__.items():
                self.enum_store[v] = v.value
                self.enum_store[v.value] = v

    def check(self, value):
        return isinstance(value, Enum)

    def find_enum(self, value):
        return self.enum_store.get(value, None)

    def to_json(self, value):
        if value is None: return
        e = self.find_enum(value)

        if e:
            return e
        return value


class TagDict(PollenTag):
    tag = TAG_DICT

    def check(self, value):
        return isinstance(value, dict)

    def to_json(self, value: dict):
        if value is None: return
        for k in list(value.keys()):
            for tag in self.proxy.default_tags.values():
                if tag.check(k):
                    value[tag.to_json(k)] = value.pop(k)
                if tag.check(value[k]):
                    value[k] = tag.to_json(value[k])
        return value

    def to_pollen(self, value):
        if value is None: return
        for k in list(value.keys()):
            for tag in self.proxy.default_tags.values():
                if tag.check(value[k]):
                    value[k] = tag.to_pollen(value[k])
                if tag.check(k):
                    value[tag.to_pollen(k)] = value.pop(k)
        return value


class TagList(PollenTag):
    tag = TAG_LIST

    def check(self, value):
        return isinstance(value, list)

    def to_json(self, value):
        if value is None: return
        size = len(value)
        i = 0
        while i < size:
            li = value[i]
            for tag in self.proxy.default_tags.values():
                if tag.check(li):
                    value[i] = tag.to_json(li)
                    i += 1
                    break
            i += 1
        return value

    def to_pollen(self, value):
        if value is None: return
        size = len(value)
        i = 0
        while i < size:
            li = value[i]
            for tag in self.proxy.default_tags.values():
                if tag.check(li):
                    value[i] = tag.to_pollen(li)
                    i += 1
                    break
            i += 1
        return value


class TagTuple(PollenTag):
    tag = TAG_TUPLE

    def check(self, value):
        return isinstance(value, tuple)

    def to_json(self, value):
        if value is None: return
        temp = list(value)
        size = len(value)
        i = 0
        while i < size:
            li = value[i]
            for tag in self.proxy.default_tags.values():
                if tag.check(li):
                    temp[i] = tag.to_json(li)
                    i += 1
                    break
            i += 1
        return tuple(temp)

    def to_pollen(self, value):
        """
        字符list --> list or tuple
        """
        pass


class TagDatetime(PollenTag):
    tag = TAG_DATETIME
    patternForTimef = r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}.\d+'
    patternForTime = r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}'

    def check(self, value):
        return isinstance(value, datetime)

    def to_json(self, value):
        if value is None: return
        time_str = datetime.strftime(value, '%Y-%m-%d %H:%M:%S')
        return time_str

    """
    def to_pollen(self, value):
        TagStr.to_pollen
    """


class TagBytes(PollenTag):
    tag = TAG_BYTES

    def check(self, value):
        return isinstance(value, bytes)

    def to_json(self, value):
        return value.decode()

    """
    def to_pollen(self, value):
        TagStr.to_pollen
    """


class TagNum(PollenTag):
    tag = TAG_NUM

    def check(self, value):
        return isinstance(value, int) or isinstance(value, float)

    def to_json(self, value):
        return value

    def to_pollen(self, value):
        return value


class TagStr(PollenTag):
    tag = TAG_STR

    def check(self, value):
        return isinstance(value, str)

    def to_json(self, value):
        return value

    def to_pollen(self, value):
        tag_enum = self.proxy.default_tags.get(TAG_ENUM)
        tag_datetime = self.proxy.default_tags.get(TAG_DATETIME)
        """if enum"""
        e = tag_enum.find_enum(value)
        if e:
            return e
        """if datetime"""
        if re.match(tag_datetime.patternForTimef, value):
            time = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
            return time
        if re.match(tag_datetime.patternForTime, value):
            time = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return time
        return value


tags = [TagEnum, TagBytes, TagDatetime, TagDict, TagList, TagTuple, TagStr, TagNum]
