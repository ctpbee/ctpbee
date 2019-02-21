# coding:utf-8
import json

string_types = (str, unicode)
from werkzeug.utils import import_string


class ModuleType:
    def __init__(self, name): self.name=name


class Settings:
    def __init__(self):
        pass

    def add_environment_from_file(self, file_name):
        via = ModuleType("config")
        with open(file_name, "r") as f:
            exec(compile(f.read(), file_name, 'exec'), via.__dict__)
        self.from_object(via)

    def from_object(self, obj):
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                setattr(self, key, getattr(obj, key))

    def from_json(self, jsons):
        with open(jsons, "r") as f:
            data = json.load(f, encoding="utf-8")
            for key, value in data:
                if key.isupper():
                    setattr(self, key, value)



# def test():
#     """测试代码"""
#     # a = Settings()
#     # a.addEnvironmentFromFile("config.py")
#     #
#     # print a.__dict__
#     pass
