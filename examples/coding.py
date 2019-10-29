class Action:

    def __init__(self, app):
        self.app = app

    def sell(self, b):
        a = 1 + b
        return a


class App:
    def __init__(self, action_class, cia_class):
        self.action = action_class(self)
        self.cia = cia_class(self)


from functools import wraps


def exec_intercept(self, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        self.api.resolve_callback(func.__name__, result)
        return result

    return wrapper


class CoreAction:
    def __init__(self, action, api):
        self.api = api
        self.action = action
        self.params = exec_intercept

    def __getattr__(self, item):
        p = self.params(self, getattr(self.action, item))
        return p


class Cia:
    def __init__(self, app):
        self.app = app

    @property
    def action(self):
        return CoreAction(self.app.action, self)

    def do(self, i):
        p = self.action.sell(i)
        print(p)

    def resolve_callback(self, i, v):
        print(i, v)


if __name__ == '__main__':
    app = App(Action, Cia)
    app.cia.do(2)
