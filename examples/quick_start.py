"""
An introduction to function usage
"""
# you should know  all the libraries should be extral installed  if use the examples

from ctpbee import CtpBee
from ctpbee import ExtAbstract
from ctpbee import subscribe, send_order
from ctpbee.ctp.constant import OrderData, TickData


class PrintIt(ExtAbstract):

    def on_order(self, order: OrderData, **kwargs) -> None:
        print()

    def on_tick(self, tick: TickData, **kwargs) -> None:
        print(tick)


ext = PrintIt("print")

app = CtpBee(__name__)

info = {
    "CONNECT_INFO": {
        "userid": "142164",
        "password": "040501",
        "brokerid": "9999",
        "md_address": "tcp://180.168.146.187:10031",
        "td_address": "tcp://180.168.146.187:10030",
        "appid": "",
        "auth_code": "",
    },
    "TD_FUNC": True,
    "XMIN": [3]
}
app.config.from_mapping(info)
ext.init_app(app)
app.start()
subscribe("ag1912")
