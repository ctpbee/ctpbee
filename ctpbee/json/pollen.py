import json


class ProxyPollen(object):
    default_tags = {}

    def __init__(self, tags, enums):
        for t in tags:
            self.default_tags[t.tag] = t(self, enums)

    @classmethod
    def _check(cls, value):
        for t in cls.default_tags.values():
            if t.check(value):
                return t

    @classmethod
    def loads(cls, json_data):
        """
        to json
        :param value:
        :return:
        """
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        tag = cls._check(json_data)
        if tag:
            return tag.to_pollen(json_data)

    @classmethod
    def dumps(cls, value):
        """
        to json
        :param value:
        :return:
        """
        tag = cls._check(value)
        if tag:
            return json.dumps(tag.to_json(value), ensure_ascii=False)


from .tag import tags
from ctpbee.constant import enums

Pollen = ProxyPollen(tags=tags, enums=enums)
