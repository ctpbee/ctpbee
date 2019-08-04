class TransferProtocal:
    """ 用于解析回测时候传送的tick数据 """

    def __init__(self, data):
        """ 解析数据 """
        if isinstance(data, bytes):
            data = str(data, encoding="utf-8")
        self.data = data
        self.header = None
        self.code = None
        self.content = None
        self.verification_key = None
        self.auth = False

    def __decrypt__(self, data):
        """ 解析关键data """
        pass

    def __analyzing__(self):
        """ 解析数据 """
        pass

    def __validate__(self):
        """ 校验数据 """

    def to_dict(self):
        """ 提供外部的API """
        if self.auth:
            return {
                "header": self.header,
                "code": self.code,
                "content": self.content,
            }
        else:
            return {}
