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


if __name__ == '__main__':
    # An very easy simple
    risk_control = RiskController("risk_control")


    @risk_control.connect_via()
    def add(app):
        print("执行B", app)
        return True


    @risk_control.connect_via()
    def comm(app):
        print("执行A", app)
        return True


    print(risk_control.func_set)
    result = risk_control.send(app="123")
    print(result)
