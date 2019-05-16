# you should know  all the libraries should be extral installed  if use the examples

from ctpbee import CtpBee
from ctpbee import DataSolve
from ctpbee import subscribe, send_order
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
app.config.from_mapping(info)
app.start()
subscribe("ag1912")


class UserDefine(DataSolve):
    """
    user should inherit the DataSolve. and program the solve code.

    two ways are provided  on_tick and on_bar.

    if you want to send_order . just from ctpbee import send_order

    just inherit DataSolve class and will automatic process data
    """

    def on_tick(self, tick):
        print(tick)
        pass

    def on_bar(self, bar, interval):
        print(bar)
        pass

    def on_shared(self, shared):
        print(shared)
