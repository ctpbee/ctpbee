from collections import OrderedDict

TICK_DB = "Tick_DB"
XMIN = [3, 5, 15]

XMIN_DATABASE_NAME = ["min_" + str(x) for x in XMIN]

XMIN_MAP = OrderedDict(zip(XMIN, XMIN_DATABASE_NAME))

CONNECT_INFO = {
    "user_id": "089131",
    "password": "350888",
    "broke_id": "9999",
    "md_address": "tcp://180.168.146.187:10031",
    "td_address":"tcp://180.168.146.187:10030",
    "pro_info": "",
    "auth_code": "",
}
