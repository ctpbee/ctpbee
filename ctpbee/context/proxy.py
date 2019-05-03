from ctpbee.exceptions import ContextError


class LocalProxy(object):

    def __init__(self):
        self.app = []

    def push(self, App):
        self.app.append(App)
        self.app = frozenset(self.app)

    def get_app(self):
        if len(list(self.app)) == 0:
            raise ContextError
        return list(self.app)[0]

    def __len__(self):
        return len(self.app)


proxy = LocalProxy()
