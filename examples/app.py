from ctpbee import CtpBee
from ctpbee import DataSolve
from ctpbee import subscribe ,send_order
from ctpbee import current_app
app = CtpBee(__name__)

info = {
    "CONNECT_INFO": {
        "userid": "142164",
        "password": "040501",
        "brokerid": "9999",
        "md_address": "tcp://180.168.146.187:10011",
        "td_address": "tcp://180.168.146.187:10000",
        "product_info": "",
        "auth_code": "",
    },
    "TD_FUNC": True,
    "XMIN": [3]
}
# loading config from mapping or you can load it
# from pyfile by app.config.from_pyfile()
# from object by app.config.from_object()
# from json by app.config.from_json()

app.config.from_mapping(info)

# start this app
app.start()

subscribe("ag1912")
# for i in app.recorder.get_all_contracts():
#     print(i)
# # subscribe symbol
#     subscribe(i.symbol)


class UserDefine(DataSolve):
    """
    user should inherit the DataSolve. and program the solve code.

    two ways are provided  on_tick and on_bar.

    if you want to send_order . just from ctpbee import send_order

    just inherit DataSolve class and will automatic process data
    """

    def on_tick(self, tick):
        pass

    def on_bar(self, bar, interval):
        pass

    def on_shared(self, shared):
        print(shared)

# 访问当前所有的数据对象
# recorder = current_app().recorder
