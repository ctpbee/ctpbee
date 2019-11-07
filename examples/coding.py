from pprint import pprint
from time import sleep

from ctpbee import CtpBee

app = CtpBee("dete",__name__, refresh=True)
info =  {
        "CONNECT_INFO": {
            "userid": "089131",
            "password": "350888",
            "brokerid": "9999",
            # 24小时
            # "md_address": "tcp://180.168.146.187:10131",
            # "td_address": "tcp://180.168.146.187:10130",
            # # 移动
            "md_address": "tcp://218.202.237.33:10112",
            "td_address": "tcp://218.202.237.33:10102",
            "product_info": "",
            "appid": "simnow_client_test",
            "auth_code": "0000000000000000",
        },
        "INTERFACE": "ctp",
        "TD_FUNC": True,
        "MD_FUNC": True,
    }


app.config.from_mapping(info)

app.start()
app.action.subscribe("IC1912.CFFEX")

while True:
    dictd=app.recorder.get_all_positions()
    result = [{x['local_symbol']:x['stare_position_profit']} for x in dictd if x['local_symbol'] == "IC1912.CFFEX" ]
    print("\r", result, end="")