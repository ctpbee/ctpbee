from time import sleep

from ctpbee import CtpBee
from ctpbee.constant import *

if __name__ == '__main__':
    app = CtpBee("openctp", __name__, refresh=True, work_mode=Mode.DISPATCHER)

    config = {
        "CONNECT_INFO": {
            "userid": "6984",
            "password": "123456",
            "brokerid": "9999",
            "md_address": "tcp://121.37.80.177:20004",
            "td_address": "tcp://121.37.80.177:20002",
            "appid": "simnow_client_test",
            "auth_code": "0000000000000000"
        },
        "SUBSCRIBE_CONTRACT": ["rb2310.SHFE"],
        "INTERFACE": "ctp",
        "MD_FUNC": True,
        "TD_FUNC": True,
    }
    app.config.from_mapping(config)
    app.start(log_output=True)
