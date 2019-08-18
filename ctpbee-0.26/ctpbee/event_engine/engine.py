"""
Event-driven framework of vn.py framework.
"""
import asyncio
from collections import defaultdict
from queue import Empty, Queue
from threading import Thread
from time import sleep
from typing import Any, Callable

EVENT_TIMER = "eTimer"


class Event:
    """
    Event object consists of a type string which is used
    by event engine for distributing event, and a data
    object which contains the real data.
    """

    def __init__(self, type: str, data: Any = None):
        """"""
        self.type = type
        self.data = data

    def __str__(self):
        return "Event(type={})".format(self.type)


# Defines handler function to be used in event engine.
HandlerType = Callable[[Event], None]


class EventEngine:
    """
    Event engine distributes event object based on its type
    to those handlers registered.
    It also generates timer event by every interval seconds,
    which can be used for timing purpose.
    """

    def __init__(self, interval: int = 1):
        """
        Timer event is generated every 1 second by default, if
        interval not specified.
        """
        self._interval = interval
        self._queue = Queue()
        self._active = False
        self._thread = Thread(target=self._run)
        self._timer = Thread(target=self._run_timer)
        self._handlers = defaultdict(list)
        self._general_handlers = []

    @property
    def status(self):
        """ 状态 """
        return self._active

    def _run(self):
        """
        Get event from queue and then process it.
        """
        while self._active:
            try:
                event = self._queue.get(block=True, timeout=1)
                self._process(event)
            except Empty:
                pass

    def _process(self, event: Event):
        """
        First ditribute event to those handlers registered listening
        to this type.
        Then distrubute event to those general handlers which listens
        to all types.
        """
        if event.type in self._handlers:
            [handler(event) for handler in self._handlers[event.type]]

        if self._general_handlers:
            [handler(event) for handler in self._general_handlers]

    def _run_timer(self):
        """
        Sleep by interval second(s) and then generate a timer event.
        """
        while self._active:
            sleep(self._interval)
            event = Event(EVENT_TIMER)
            self.put(event)

    def start(self):
        """
        Start event engine to process events and generate timer events.
        """
        self._active = True
        self._thread.start()
        self._timer.start()

    def stop(self):
        """
        Stop event engine.
        """
        self._active = False
        self._timer.join()
        self._thread.join()

    def put(self, event: Event):
        """
        Put an event object into event queue.
        """
        self._queue.put(event)

    def register(self, type: str, handler: HandlerType):
        """
        Register a new handler function for a specific event type. Every
        function can only be registered once for each event type.
        """
        handler_list = self._handlers[type]
        if handler not in handler_list:
            handler_list.append(handler)

    def unregister(self, type: str, handler: HandlerType):
        """
        Unregister an existing handler function from event engine.
        """
        handler_list = self._handlers[type]

        if handler in handler_list:
            handler_list.remove(handler)

        if not handler_list:
            self._handlers.pop(type)

    def register_general(self, handler: HandlerType):
        """
        Register a new handler function for all event types. Every
        function can only be registered once for each event type.
        """
        if handler not in self._general_handlers:
            self._general_handlers.append(handler)

    def unregister_general(self, handler: HandlerType):
        """
        Unregister an existing general handler function.
        """
        if handler in self._general_handlers:
            self._general_handlers.remove(handler)

    def __del__(self):
        if self._active:
            self.stop()


# 异步引擎 ---> 提升性能  但是你需要学会基于asyncio的编程方式

class AsyncEngine:
    """ 通过单线程的异步效果来获得并发效果 ~~"""

    def __init__(self, work_core=10):
        # 用于主循环
        self.loop = asyncio.new_event_loop()
        self._func = defaultdict(list)
        self.work_core = work_core
        self.init_flag = True
        self._active = False

    @property
    def status(self):
        """ 状态 """
        return self._active

    async def worker(self, queue):
        await asyncio.sleep(0.1)
        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=1)
            except asyncio.TimeoutError:
                continue
            await self.future_finish(event)
            queue.task_done()

    async def _put(self, event):
        await self._queue.put(event)

    def put(self, event):
        self.loop.create_task(self._put(event))

    async def future_finish(self, event: Event):
        for func in self._func.get(event.type):
            await func(event)

    def register(self, type, func):
        # if not iscoroutinefunction(func):
        #     raise TypeError("处理函数错误， 不是一个协程对象")
        handler_list = self._func[type]
        if func not in handler_list:
            handler_list.append(func)

    def unregister(self, type, func):
        handler_list = self._func[type]
        if func in handler_list:
            handler_list.remove(func)

    async def main(self):
        self._active = True
        asyncio.set_event_loop(self.loop)
        self._queue = asyncio.Queue()
        tasks = []
        for i in range(self.work_core):
            task = asyncio.create_task(self.worker(self._queue))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=False)

    def start(self):
        p = Thread(target=self.loop.run_until_complete, args=(self.main(),))
        p.start()
