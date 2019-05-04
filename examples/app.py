from ctpbee import CtpBee
from ctpbee import DataSolve

app = CtpBee(__name__)
info = {
    "CONNECT_INFO": {
        "userid": "8018",
        "password": "123",
        "brokerid": "0",
        "md_address": "tcp://180.168.146.187:10031",
        "td_address": "tcp://47.97.31.68:41206",
        "product_info": "",
        "auth_code": "",
    },
    "TD_FUNC": True
}
app.config.from_mapping(info)

class Check(DataSolve):
    def data_solve(self, event):
        pass


pointer = Check(app)
app.start()
