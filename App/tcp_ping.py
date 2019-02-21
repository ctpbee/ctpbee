# coding:utf-8
import subprocess
import re
import concurrent.futures as futures
from time import time
from functools import wraps

__all__ = ['calculate_delay']


def measure_fun(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """label the time-cosuming by remove # in the next code"""
        host = kwargs['host']
        current = time()
        result = func(*args, **kwargs)
        end_time = time()
        # print "host: {} time-consuming：{} sec".format(host, end_time - current)
        return result

    return wrapper


@measure_fun
def calculate_delay(**kwargs):
    host = kwargs['host']
    port = kwargs['port']
    test = []
    def tcp_ping(host, port):
        ''' 调用系统自带的ping.exe实现PING domain，返回值为：ip,丢包率,最短，最长，平均'''
        command = "tcping {} -p {} -c 1".format(host, port)
        p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = str(p.stdout.read().decode('gbk')).replace("\n", "")
        average_re = r".*average = (.*)ms.*"
        result = re.match(average_re, out).group(1)
        test.append(float(result))

    curr = [host] * 25
    port = [port] * 25
    with futures.ThreadPoolExecutor(25) as executor:
        res = executor.map(tcp_ping, curr, port)
    if 0.00 in test:
        test.remove(0.00)
    sum = 0
    for x in test:
        sum += x
    return sum / len(test)


if __name__ == '__main__':
    # test code
    domain = "180.168.146.187"
    port = 10011

    result = calculate_delay(host=domain, port=port)
    print "result", result
