from time import sleep

from ctpbee import CtpBee
from ctpbee import common_signals


@common_signals.tick_signal.connect
def solve_tick(tick):
    print(tick.data)


# info = {
#     "CONNECT_INFO": {
#         "userid": "089131",
#         "password": "350888",
#         "brokerid": "9999",
#         "md_address": "tcp://180.168.146.187:10131",
#         "td_address": "tcp://180.168.146.187:10130",
#         "product_info": "",
#         "appid": "simnow_client_test",
#         "auth_code": "0000000000000000"
#     },
#     "INTERFACE": "ctp",
#     "TD_FUNC": True,
#     "MD_FUNC": True
# }
info = {
    "CONNECT_INFO": {
        "userid": "8000007459",
        "password": "su198951",
        "brokerid": "8899",
        "md_address": "tcp://116.228.171.152:31213",
        "td_address": "tcp://116.228.171.152:31205",
        "appid": "client_jlb_3.0.0",
        "auth_code": "TMGC1IKOL7ZRHE7X",
    },
    "INTERFACE": "ctp",
    "TD_FUNC": True,
}
app = CtpBee("somewheve", __name__)
app.config.from_mapping(info)
app.start(log_output=True)
sleep(3)
for x in app.recorder.get_all_contracts():
    app.action.subscribe(x.local_symbol)
