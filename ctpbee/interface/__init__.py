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
    """按照接口进行加载而不是一次性进行加载"""

    @classmethod
    def load_interface(cls, interface):

        if interface == "local":
            from ctpbee.interface.local import MdApi, TdApi

            return MdApi, TdApi
        if interface == "ctp":
            from ctpbee.interface.ctp import BeeTdApi, BeeMdApi

            return BeeMdApi, BeeTdApi
        elif interface == "looper":
            from ctpbee.interface.looper import LooperMe, LooperYou

            return LooperMe, LooperYou
        elif interface == "ctp_mini":
            from ctpbee.interface.ctp_mini import MMdApi, MTdApi

            return MMdApi, MTdApi
        elif interface == "rohon":
            from ctpbee.interface.ctp import BeeTdApi, BeeMdApi
            from ctpbee.interface.ctp_rohon import RHMdApi, RHTdApi

            return RHMdApi, RHTdApi
        else:
            raise ValueError("错误参数")

    @classmethod
    def get_interface(cls, app):
        return cls.load_interface(app.config.get("INTERFACE"))
