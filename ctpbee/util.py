
class RiskController:
    def __init__(self, name):
        self.name = name
        self.func_set = set()

    def connect_via(self):
        def decorator(fn):
            self.connect(fn)
            return fn

        return decorator

    def connect(self, func):
        if len(self.func_set) > 50:
            raise EnvironmentError("不可添加太多函数")
        self.func_set.add(func)

    def send(self, app):
        return [x(app) for x in self.func_set]
