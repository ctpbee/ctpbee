"""
An introduction to function usage
"""
# you should know  all the libraries should be extral installed  if use the examples

from ctpbee import CtpBee, switch_app, current_app
from ctpbee import ExtAbstract
from ctpbee import subscribe, send_order
from ctpbee.ctp.constant import OrderData, TickData


class PrintIt(ExtAbstract):

    def on_tick(self, tick: TickData) -> None:
        """tick process function"""
        symbol = tick.symbol
        tick.datetime = str(tick.datetime)
        tick.exchange = tick.exchange.value
        print(tick)


app = CtpBee("wanghuang", __name__)
info = {
    "CONNECT_INFO": {
        "userid": "8000007459",
        "password": "su198951",
        "brokerid": "8899",
        "md_address": "tcp://116.228.171.152:31214",
        "td_address": "tcp://116.228.171.152:50214",
        "product_info": "",
        "auth_code": "",
    },
    "TD_FUNC": True,
}
app.config.from_mapping(info)
ex = PrintIt("bee", app)
app.start()
for x in app.recorder.get_all_contracts():
    subscribe(x.symbol)
