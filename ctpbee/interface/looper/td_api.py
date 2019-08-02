import re
from typing import Dict

from ctpbee.interface.looper.base_client import Client


class BeeTdLooperApi(Client):
    """
    ctpbee采用非本地的回测方式，数据由服务器提供,
    除了使用官方的回测服务器外你也可以自己搭建服务器进行自用
    行情API服务器标准端口为5400
    """

    def __init__(self, event_engine):
        super().__init__()
        self.md_address = 0
        self.event_engine = event_engine

    def connect(self, info: Dict):
        md_address = info.get("md_address")
        # 通过正则表达式进行
        result = re.match(self.ip_re, md_address)
        if result is None:
            raise ValueError("错误行情地址，不符合要求")
        add, port = result.group(1).split(":")
        self.md_address = (add, int(port))
        self.socket.connect(self.md_address)
        self.after_connect()

    def message_distribute(self, message:bytes):
        """ 实现消息的封装与分发到具体的处理函数 """

    def onRspTickEvent(self, data, bool):
        pass



