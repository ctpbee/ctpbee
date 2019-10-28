class Action:

    def __init__(self, app):
        self.app = app

    def sell(self, **kwargs):
        return [1]


class App:
    def __init__(self, action_class, cia_class):
        self.action = action_class(self)
        self.cia = cia_class(self)



class Cia:
    def __init__(self, app):
        self.app = app

    @property
    def action(self):
        return Core(self.app.action, self)

    def do(self):
        p = self.action.sell()
        print(p)


if __name__ == '__main__':
    app = App(Action, Cia)
    app.cia.do()
