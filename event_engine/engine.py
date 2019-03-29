# coding:utf-8
from __future__ import print_function
from collections import defaultdict
import inspect
import ctypes


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class Event:
    """事件对象"""

    # ----------------------------------------------------------------------
    def __init__(self, dict=None, type_=None):
        """Constructor"""
        self.type_ = type_  # 事件类型
        # 字典用于保存具体的事件数据
        if dict is None:
            dict = {}
        self.dict_ = dict


class EventEngine(object):
    """
    计时器使用python线程的事件驱动引擎
    """

    def __init__(self):
        """初始化事件引擎"""
        # 事件队列
        # self.__queue = Queue()
        self.__handlers = defaultdict(list)
        self.__general_handlers = []
        self.__active = False
        self.__active = True

    def __process(self, event):
        """处理事件"""
        # 检查是否存在对该事件进行监听的处理函数
        if event.type_ in self.__handlers:
            # 若存在，则按顺序将事件传递给处理函数执行
            [handler(event) for handler in self.__handlers[event.type_]]

        # 调用通用处理函数进行处理
        if self.__general_handlers:
            [handler(event) for handler in self.__general_handlers]

    def register(self, type_, handler):
        """注册事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无defaultDict会自动创建新的list
        handler_list = self.__handlers[type_]

        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handler_list:
            handler_list.append(handler)

    def unregister(self, type_, handler):
        """注销事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
        handler_list = self.__handlers[type_]

        # 如果该函数存在于列表中，则移除
        if handler in handler_list:
            handler_list.remove(handler)

        # 如果函数列表为空，则从引擎中移除该事件类型
        if not handler_list:
            del self.__handlers[type_]

    def put(self, event):
        """向事件队列中存入事件"""
        # self.__queue.put(event)
        # event = self.__queue.get()  # 获取事件的阻塞时间设为1秒
        # 推送进来直接处理
        self.__process(event)

    def registerGeneralHandler(self, handler):
        """注册通用事件处理函数监听"""
        if handler not in self.__general_handlers:
            self.__general_handlers.append(handler)

    def unregisterGeneralHandler(self, handler):
        """注销通用事件处理函数监听"""
        if handler in self.__general_handlers:
            self.__general_handlers.remove(handler)
