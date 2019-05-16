from ctpbee.exceptions import ContextError


class LocalProxy(object):

    def __init__(self):
        self.app = []

    def push(self, App) -> None:
        """将实例化后的app 推送进入全局对象并将其冻结"""
        self.app.append(App)
        self.app = frozenset(self.app)

    def get_app(self):
        """返回app实例"""
        if len(list(self.app)) == 0:
            raise ContextError
        return list(self.app)[0]

    def __len__(self) -> int:
        """返回当前环境下app的个数"""
        return len(self.app)


proxy = LocalProxy()
