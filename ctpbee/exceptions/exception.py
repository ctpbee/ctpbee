class BaseError(Exception):
    def __init__(self, *args):
        self.args = args


class ConfigError(BaseError):
    def __init__(self, code=101, message='配置异常', args=('配置信息存在错误',)):
        self.args = args
        self.message = message
        self.code = code


class DatabaseError(BaseError):
    def __init__(self, code=102, message='数据库异常', args=('数据库存在连接异常',)):
        self.args = args
        self.message = message
        self.code = code


class ContextError(BaseError):
    def __init__(self, code=103, message='上下文异常', args=('上下文索引异常',)):
        self.args = args
        self.message = message
        self.code = code


class TraderError(BaseError):
    def __init__(self, code=104, message='交易异常', args=('交易异常',)):
        self.args = args
        self.message = message
        self.code = code
