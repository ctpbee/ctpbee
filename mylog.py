#自带的日志不会用我自己写了个.

from termcolor import cprint

from myhelper import cleanlogs, mylogger


class MyLogger():
    cleanlogs()

    @classmethod
    def info(self, msg,ignore_print=False, **kv):
        mylogger.info(msg)
        if ignore_print:
            return
        cprint(f"{msg}", "green")
        
    @classmethod
    def warning(self, msg, ignore_print=False,**kv):
        mylogger.warning(msg)
        if ignore_print:
            return
        cprint(f"{msg}", "yellow")

    @classmethod
    def debug(self, msg, ignore_print=False,**kv):
        mylogger.debug(msg)
        if ignore_print:
            return
        cprint(f"{msg}", "blue")

    @classmethod
    def error(self, msg, ignore_print=False, **kv):
        mylogger.error(msg)
        if ignore_print:
            return
        cprint(f"{msg}", "red")

    @classmethod
    def set_field_default(name, owner):
        ...
