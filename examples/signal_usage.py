from time import sleep

from ctpbee import CtpBee
from ctpbee import common_signals


@common_signals.tick_signal.connect
def solve_tick(tick):
    print(tick.data)


info = {
    "CONNECT_INFO": {
        "userid": "089131",
        "password": "350888",
        "brokerid": "9999",
        "md_address": "tcp://180.168.146.187:10131",
        "td_address": "tcp://180.168.146.187:10130",
        "product_info": "",
        "appid": "simnow_client_test",
        "auth_code": "0000000000000000"
    },
    "INTERFACE": "ctp",
    "TD_FUNC": True,
    "MD_FUNC": True
}
app = CtpBee("somewheve", __name__)
app.config.from_mapping(info)
app.start()
sleep(3)
for x in app.recorder.get_all_contracts():
    app.action.subscribe(x.local_symbol)
