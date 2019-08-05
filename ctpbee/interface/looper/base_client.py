from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from ctpbee.interface.looper.protocal import TransferProtocal


class Client:
    ip_re = r".*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}).*"

    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.active = False

    def connect(self, info):
        raise NotImplemented

    def connection_lost(self):
        """ 失去连接触发 """
        raise NotImplemented

    def connection_made(self):
        raise NotImplemented

    def message_distribute(self, data: TransferProtocal):
        raise NotImplemented

    def after_connect(self):
        """
        此函数应该在主动连接之后调用
        然后开始监听消息
        """
        if self.active:
            p = Thread(target=self.run_forever)
            p.setDaemon(daemonic=True)
            p.start()

    def run_forever(self):
        """ 循环监听请求 ，然后解耦后分发到不同的消息处理机制 """
        while True:
            s = self.socket.recv(4096)
            self.message_distribute(TransferProtocal(s))
