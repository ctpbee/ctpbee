import os
import platform
from multiprocessing import Process
from datetime import datetime
from inspect import isfunction
from time import sleep

now = datetime.now()


def auth_time(current):
    if (current - now).seconds < 10:
        return True
    elif 10 <= (current - now).seconds <= 20:
        return False
    elif (current - now).seconds > 20:
        return True


def run_all_app(app_func):
    app_func()


def printme():
    while True:
        print("I AM RUNNING STRATEGY")
        sleep(1)


def start_all(app_func, info=True, interface="ctp", in_front=300):
    """
    开始进程管理
    * app_func: 创建app的函数
    * interface: 接口名字
    * in_front: 相较于开盘提前多少秒进行运行登陆.单位: seconds
    """
    print("""
     Ctpbee 7*24 Manager started !
     Warning: program will automatic start at trade time ....
     Hope you will have a  good profit ^_^
     """)
    if not isfunction(app_func):
        raise TypeError(f"请检查你传入的app_func是否是创建app的函数,  而不是{type(app_func)}")

    p = None
    while True:
        current = datetime.now()

        status = auth_time(current)
        print(f"time: {current} auth status： {status}")

        if p is None and status:
            p = Process(target=run_all_app, args=(app_func,), daemon=True)
            p.start()
            print(f"program start successful, pid: {p.pid}")
        if not status and p is not None:
            print(f"invalid time, 查杀子进程  pid: {p.pid}")
            if platform.uname().system == "Windows":
                os.popen('taskkill /F /pid ' + str(p.pid))
            else:
                import signal
                os.kill(p.pid, signal.SIGKILL)
            p = None
        sleep(1)


if __name__ == '__main__':
    start_all(printme)
