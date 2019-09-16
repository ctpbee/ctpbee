from typing import Dict


class MdLooperApi:
    """
    ctpbee采用非本地的回测方式，数据由服务器提供,
    除了使用官方的回测服务器外你也可以自己搭建服务器进行自用
    行情API服务器标准端口为5400
    """

    def __init__(self, event_engine, app=None):
        super().__init__()
        self.md_address = 0
        self.event_engine = event_engine

    def connect(self, info: Dict):
        pass
