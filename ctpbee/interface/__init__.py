"""
Notice : 神兽保佑 ，测试一次通过
//      
//      ┏┛ ┻━━━━━┛ ┻┓
//      ┃　　　　　　 ┃
//      ┃　　　━　　　┃
//      ┃　┳┛　  ┗┳　┃
//      ┃　　　　　　 ┃
//      ┃　　　┻　　　┃
//      ┃　　　　　　 ┃
//      ┗━┓　　　┏━━━┛
//        ┃　　　┃   Author: somewheve
//        ┃　　　┃   Datetime: 2019/7/7 下午2:45  ---> 无知即是罪恶
//        ┃　　　┗━━━━━━━━━┓
//        ┃　　　　　　　    ┣┓
//        ┃　　　　         ┏┛
//        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
//          ┃ ┫ ┫   ┃ ┫ ┫
//          ┗━┻━┛   ┗━┻━┛
//
"""


class Interface:
    """ 按照接口进行加载而不是一次性进行加载 """

    @classmethod
    def load_interface(cls, interface):
        if interface == "ctp":
            from ctpbee.interface.ctp import BeeTdApi, BeeMdApi
            return BeeMdApi, BeeTdApi
        if interface == "ctp_se":
            from ctpbee.interface.ctp import BeeTdApiApp, BeeMdApiApp
            return BeeMdApiApp, BeeTdApiApp
        if interface == "looper":
            from ctpbee.interface.looper import LooperMe, LooperYou
            return LooperYou, LooperMe
        else:
            raise ValueError("错误参数")

    @classmethod
    def get_interface(cls, app):
        return cls.load_interface(app.config.get("INTERFACE"))
