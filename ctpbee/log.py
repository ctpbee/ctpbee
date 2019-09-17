import copy
import logging
import logging.config
import time

logger = logging.Logger("ctpbee")

"""
实现一个默认的LoggerClass

log格式

时间 ---- 执行者 ---- 等级 ---- 信息

"""


class VLogger():
    attributes = ["created", "levelname", "name", "owner", "msg"]
    extra_attributes = []

    class Filter(logging.Filter):
        def __init__(self, loggerd):
            super().__init__()
            setattr(self, "filter", getattr(loggerd, "_handler_record"))

    class Handler(logging.StreamHandler):
        red = '\x1b[31m'
        yellow = '\x1b[33m'
        green = '\x1b[32m'
        pink = '\x1b[35m'
        normal = '\x1b[0m'
        white = '\x1b[37m'
        blue = '\x1b[34m'
        cyan = '\x1b[36m'
        fuchsin = '\x1b[35m'

        def emit(self, record):
            temp_record = copy.copy(record)
            level = temp_record.levelno
            if (level >= 50):  # CRITICAL / FATAL
                color = self.red
            elif (level >= 40):  # ERROR
                color = self.red
            elif (level >= 30):  # WARNING
                color = self.yellow
            elif (level >= 20):  # INFO
                color = self.green
            elif (level >= 10):  # DEBUG
                color = self.pink
            else:  # normal
                color = self.normal
            temp_record.levelname = (self.fuchsin + str(temp_record.levelname).ljust(8) + '\x1b[0m')
            temp_record.msg = color + str(temp_record.msg) + '\x1b[0m'
            """ I don't know why this will be called by other framework """
            try:
                temp_record.owner = self.cyan + str(temp_record.owner).ljust(10) + '\x1b[0m'
            except Exception as e:
                setattr(temp_record, "owner", "Unknown")

            temp_record.name = self.white + str(temp_record.name).ljust(10) + '\x1b[0m'
            for x in VLogger.extra_attributes:
                setattr(temp_record, x, self.white + str(getattr(temp_record, x)) + '\x1b[0m')
            logging.StreamHandler.emit(self, temp_record)

    def __init__(self, app_name="ctpbee"):
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.DEBUG)
        self.handler = self.Handler()
        self.logger.addFilter(filter=self.Filter(self))
        self._init()

    def update_log_file(self, filename):
        logging.config.fileConfig(filename)

    def _init(self):
        """ 分别添加相应的处理器 """
        self.handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)
        # 设置默认的格式处理器
        self.set_formatter("handler")

    def warning(self, msg, owner="App", logger_name="logger", **kwargs):
        getattr(self, logger_name).warning(msg=msg, extra=dict({'owner': owner}, **kwargs))

    def error(self, msg, owner="App", logger_name="logger", **kwargs):
        getattr(self, logger_name).error(msg=msg, extra=dict({'owner': owner}, **kwargs))

    def info(self, msg, owner="App", logger_name="logger", **kwargs):
        getattr(self, logger_name).info(msg=msg, extra=dict({'owner': owner}, **kwargs))

    def debug(self, msg, owner="App", logger_name="logger", **kwargs):
        getattr(self, logger_name).debug(msg=msg, extra=dict({'owner': owner}, **kwargs))

    def set_formatter(self, handler="handler", attribute=[]):
        """ 传入属性来设置额外的输出格式 """
        if hasattr(self, handler):
            handle_me: logging.Handler = getattr(self, handler)
        else:
            raise ValueError(f"无此处理器对象, 当前只支持[debug_handler, error_handler, warn_handler, info_handler]")

        p = "%(asctime)s %(name)s %(levelname)s %(owner)s {fmt} %(message)s".format(
            fmt="".join([f"%({p})s " for p in attribute]))

        self.attributes += attribute
        self.extra_attributes += attribute
        formatter = logging.Formatter(p)
        handle_me.setFormatter(formatter)

    def _handler_record(self, record):
        self.handler_record(self.covert_record(record))
        return True

    def handler_record(self, record):
        """ 处理日志信息 重写此函数以应用每个不同的使用场景 """

    def covert_record(self, record: logging.LogRecord):
        """ 将record里面的数据提取出来然后转换为正常的字符串 """
        result = {}
        for x in self.attributes:
            p = getattr(record, x)
            if isinstance(p, float) and p > 1000000000:
                time_local = time.localtime(p)
                p = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            result[x] = str(p)
        return result

    def add_logger(self, name, level):
        temp_logger = logging.getLogger(name)
        temp_logger.setLevel(level)
        setattr(name, temp_logger)
        temp_handler = self.Handler()
        setattr(name + "_hanlder", temp_handler)
        temp_logger.addHandler(temp_handler)

    def del_logger(self, name):
        if hasattr(name) and hasattr(self, name + "_handler"):
            delattr(self, name)
            delattr(self, name + "_handler")


if __name__ == '__main__':
    logger_me = VLogger()
    logger_me.set_formatter("handler")
    logger_me.warning("这里发生了警告", owner="somewheve")
    logger_me.error("这里发生了错误", owner="somewheve")
    logger_me.info("这里发生了信息输出", owner="somewheve")
    logger_me.debug("这里发生了调试", owner="somewheve")
