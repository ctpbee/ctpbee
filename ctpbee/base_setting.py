from collections import OrderedDict

TICK_DB = "tick_me"
XMIN = [3, 5, 10, 15]

XMIN_DATABASE_NAME = ["min_" + str(x) for x in XMIN]

XMIN_MAP = OrderedDict(zip(XMIN, XMIN_DATABASE_NAME))

CONNECT_INFO = {
    "userid": "089131",
    "password": "350888",
    "brokerid": "9999",
    "md_address": "tcp://180.168.146.187:10031",
    "td_address": "tcp://180.168.146.187:10030",
    "product_info": "",
    "auth_code": "",
}

MD_FUNC = True
TD_FUNC = False

LOG_OUTPUT = True
