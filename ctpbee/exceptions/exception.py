import ctpbee.helpers as helpers
class BaseException(Exception):
    def __init__(self, *args):
        self.args = args


class ConfigError(BaseException):
    def __init__(self, code=101, message='配置异常', args=('配置信息存在错误',)):
        self.args = args
        self.message = message
        self.code = code


class DatabaseError(BaseException):
    def __init__(self, code=102, message='数据库异常', args=('数据库存在连接异常',)):
        self.args = args
        self.message = message
        self.code = code


class ContextError(BaseException):
    def __init__(self, code=103, message='上下文异常', args=('上下文索引异常',)):
        self.args = args
        self.message = message
        self.code = code


class TraderError(BaseException):
    def __init__(self, code=104, message='交易异常', args=('交易异常',)):
        self.args = args
        self.message = message
        self.code = code


class ImportStringError(ImportError):

    """Provides information about a failed :func:`import_string` attempt."""

    #: String in dotted notation that failed to be imported.
    import_name = None
    #: Wrapped exception.
    exception = None

    def __init__(self, import_name, exception):
        self.import_name = import_name
        self.exception = exception

        msg = (
            'import_string() failed for %r. Possible reasons are:\n\n'
            '- missing __init__.py in a package;\n'
            '- package or module path not included in sys.path;\n'
            '- duplicated package or module name taking precedence in '
            'sys.path;\n'
            '- missing module, class, function or variable;\n\n'
            'Debugged import:\n\n%s\n\n'
            'Original exception:\n\n%s: %s')

        name = ''
        tracked = []
        for part in import_name.replace(':', '.').split('.'):
            name += (name and '.') + part
            imported = helpers.import_string(name, silent=True)
            if imported:
                tracked.append((name, getattr(imported, '__file__', None)))
            else:
                track = ['- %r found in %r.' % (n, i) for n, i in tracked]
                track.append('- %r not found.' % name)
                msg = msg % (import_name, '\n'.join(track),
                             exception.__class__.__name__, str(exception))
                break

        ImportError.__init__(self, msg)

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.import_name,
                                 self.exception)