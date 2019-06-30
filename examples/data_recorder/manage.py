import os

from multiprocessing import Process
from datetime import datetime
from time import sleep


def run():
    file_path = os.getcwd() + "/serve.py"
    # for sudo user
    # os.system(f'echo "your password in here" |sudo -S python3.7 {file_path}')

    # for general user
    os.system(f'python3.7 {file_path}')


def close_program(keyword):
    """用于关闭子程序"""
    import os
    command = f"ps aux | grep {keyword}"
    f = os.popen(command)
    results = f.readlines()
    pids = [c.split()[1] for c in results if "grep" not in c]
    for pid in pids:
        # for sudo user
        # os.system(f'echo "your password in here" |sudo -S kill -9 {pid}')

        # for general user
        os.system(f'kill -9 {pid}')


def auth_time(current: datetime):
    from datetime import time
    DAY_START = time(8, 57)  # 日盘启动和停止时间
    DAY_END = time(15, 5)
    NIGHT_START = time(20, 57)  # 夜盘启动和停止时间
    NIGHT_END = time(2, 35)
    if ((current.today().weekday() == 6) or
            (current.today().weekday() == 5 and current.time() > NIGHT_END) or
            (current.today().weekday() == 0 and current.time() < DAY_START)):
        return False
    if current.time() <= DAY_END and current.time() >= DAY_START:
        return True
    if current.time() >= NIGHT_START:
        return True
    if current.time() <= NIGHT_END:
        return True
    return False


def main():
    p = None
    while True:
        current = datetime.now()
        status = auth_time(current)
        if p is None and status == True:
            p = Process(target=run)
            p.start()
            print("启动程序")
        if not status and p is not None:
            print("查杀子进程")
            close_program("serve.py")
            p.kill()
            print("关闭成功")
            p = None
        p = Process(target=run)
        p.start()
        sleep(30)


if __name__ == '__main__':
    main()
