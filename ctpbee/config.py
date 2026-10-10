# -*- coding: utf-8 -*-
"""
use for refrence from flask config
"""
import errno
import json
import os
import types
from typing import Text


class ConfigAttribute(object):
    """Makes an attribute forward to the config"""

    def __init__(self, name, get_converter=None):
        self.__name__ = name
        self.get_converter = get_converter

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        rv = obj.config[self.__name__]
        if self.get_converter is not None:
            rv = self.get_converter(rv)
        return rv

    def __set__(self, obj, value):
        obj.config[self.__name__] = value


class Config(dict):
    def __init__(self, root_path, defaults=None):
        dict.__init__(self, defaults or {})
        self.root_path = root_path

    def from_pyfile(self, filename, silent=False):
        """
        编译py文件,读取其中配置

        Args:
          filename(Text): py文件名

        Return:
          bool: 导入是否正确
        """
        filename = os.path.join(self.root_path, filename)
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (
                    errno.ENOENT, errno.EISDIR, errno.ENOTDIR
            ):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def save(self, path):
        """
        导出为json文件

        Examples:
          app.config.save("a.json")
        """

        with open(path, "w") as f:
            json.dump(self, f)

    def from_object(self, obj):
        """
        从实例中导入配置 , 最佳体验为可将配置写在一个dataclass中

        Examples:
          class Ext:
              TD_FUNC = True
              MD_FUNC = True
          ext = Ext()
          app.config.from_object(ext)
        """
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def from_json(self, filename: Text, silent=False):
        """
        从json文件中导入文件配置

        Args:
          filename(Text): json文件名

        Examples:
          app.config.from_json(json_file_path) -- > absolute path or relative path
        """
        filename = os.path.join(self.root_path, filename)
        try:
            with open(filename, "r") as f:
                obj = json.load(f)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        return self.from_mapping(obj)

    def from_mapping(self, *mapping, **kwargs):
        """
        从mapping映射中导入配置

        Examples:
          config = {"TD_FUNC":True}
          app.config.from_mapping(config)
        """
        mappings = []
        if len(mapping) == 1:
            if hasattr(mapping[0], 'items'):
                mappings.append(mapping[0].items())
            else:
                mappings.append(mapping[0])
        elif len(mapping) > 1:
            raise TypeError(
                'expected at most 1 positional argument, got %d' % len(mapping)
            )
        mappings.append(kwargs.items())
        for mapping in mappings:
            for (key, value) in mapping:
                if key.isupper():
                    self[key] = value
        return True

    def from_envvars(self, prefix: Text = "CTPBEE_", silent: bool = True):
        """
        从环境变量导入配置: 所有以 prefix 开头的环境变量, 去掉前缀后
        作为配置键(要求全大写, 与 from_mapping 一致), 值优先按 JSON 解析
        ——bool/int/float/list/dict 均可表达(如 CONNECT_INFO 传 JSON 字符串),
        解析失败时保留原始字符串。

        Args:
          prefix(Text): 环境变量前缀, 默认 "CTPBEE_"
          silent(bool): True 时忽略不规范项(非大写键/非 JSON 值回退字符串);
                        False 时对它们显式抛 ValueError

        Examples:
          export CTPBEE_TD_FUNC=false          → config["TD_FUNC"] is False
          export CTPBEE_RD_CLIENT_PORT=6379    → config["RD_CLIENT_PORT"] == 6379
          export CTPBEE_CONNECT_INFO='{"userid": "001", ...}'  → dict

          # 推荐优先级: 文件值 < 环境变量
          app.config.from_json("config.json")
          app.config.from_envvars()
        """
        loaded = {}
        for key, value in os.environ.items():
            if not key.startswith(prefix):
                continue
            config_key = key[len(prefix):]
            if not config_key or not config_key.isupper():
                if not silent:
                    raise ValueError(
                        f"环境变量 {key} 去前缀后的键 {config_key!r} 非法(须为非空全大写)")
                continue
            try:
                parsed = json.loads(value)
            except ValueError:
                if not silent:
                    raise
                parsed = value
            loaded[config_key] = parsed
        return self.from_mapping(loaded)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))
