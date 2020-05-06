"""
 此处描述了如何编写模拟器
"""


from ctpbee import CtpBee


if __name__ == '__main__':
    app = CtpBee("sim", __name__)
    info = {
        "CONNECT_INFO": {
            "userid": "089131",
            "password": "350888",
            "brokerid": "9999",
            "md_address": "tcp://218.202.237.33:10112",
            "td_address": "tcp://218.202.237.33:10102",
            "product_info": "",
            "appid": "simnow_client_test",
            "auth_code": "0000000000000000",
        },
        "INTERFACE": "sim",
        "TD_FUNC": True,
        "MD_FUNC": True,
    }

    app.config.from_mapping(info)
    app.start()

