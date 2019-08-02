# coding:utf-8
import os
import sys
from time import sleep
from typing import Text, AnyStr

from werkzeug.datastructures import ImmutableDict

from ctpbee.config import Config
from ctpbee.constant import OrderRequest, CancelRequest, EVENT_LOG
from ctpbee.context import _app_context_ctx
from ctpbee.event_engine import EventEngine, Event
from ctpbee.exceptions import ConfigError
from ctpbee.func import CtpbeeApi, send_monitor, cancle_monitor
from ctpbee.helpers import locked_cached_property, find_package, check
from ctpbee.interface import Interface
from ctpbee.record import Recorder
from ctpbee.util import RiskController


class CtpBee(object):
    """
    ctpbee 源于我对于做项目的痛点需求, 旨在开发出一套具有完整api的交易微框架 ,
    在这里你可以看到很多借鉴自flask的设计 , 毕竟本人实在热爱flask ....
    ctpbee提供完整的支持 ，一个CtpBee对象可以登录一个账户 ，
    当你登录多个账户时， 可以通过current_app, 以及switch_app还有 get_app提供完整的支持,
    每个账户对象都拥有单独的发单接口 ,在你实现策略的地方 可以通过上述api实现发单支持,
    当然ctpbee提供了ExtAbstract 抽象插件 ，继承此插件即可快速载入支持.
    总而言之,希望能够极大的简化目前的开发流程 !
    """

    # 默认配置
    default_config = ImmutableDict(
        dict(LOG_OUTPUT=True, TD_FUNC=False, INTERFACE="ctp", MD_FUNC=True, XMIN=[], ALL_SUBSCRIBE=False,
             SHARE_MD=False))
    config_class = Config
    import_name = None
    # 数据记录载体
    __active = False

    # 交易api与行情api
    market = None
    trader = None

    # 插件系统
    # todo :等共享内存块出来了 是否可以尝试在外部进行
    extensions = {}

    def __init__(self, name: Text, import_name, instance_path=None):
        """ 初始化 """
        self.name = name
        self.import_name = import_name
        self.event_engine = EventEngine()
        if instance_path is None:
            instance_path = self.auto_find_instance_path()
        elif not os.path.isabs(instance_path):
            raise ValueError(
                'If an instance path is provided it must be absolute.'
                ' A relative path was given instead.'
            )
        self.risk_gateway = RiskController(self.name)
        self.recorder = Recorder(self, self.event_engine)
        self.instance_path = instance_path
        self.config = self.make_config()
        self.interface = Interface()
        _app_context_ctx.push(self.name, self)

    def make_config(self):
        """ 生成class类"""
        defaults = dict(self.default_config)
        return self.config_class(self.instance_path, defaults)

    def auto_find_instance_path(self):
        prefix, package_path = find_package(self.import_name)
        if prefix is None:
            return os.path.join(package_path)
        return os.path.join(prefix, 'var', self.name + '-instance')

    @property
    def td_login_status(self):
        """ 交易 API 都应该实现td_status"""
        return self.trader.td_status

    @property
    def md_login_status(self):
        """ 行情 API 都应该实现md_status"""
        return self.market.md_status

    def _load_ext(self):
        """根据当前配置文件下的信息载入行情api和交易api,记住这个api的选项是可选的"""
        self.__active = True
        if "CONNECT_INFO" in self.config.keys():
            info = self.config.get("CONNECT_INFO")
        else:
            raise ConfigError(message="没有相应的登录信息", args=("没有发现登录信息",))
        MdApi, TdApi = self.interface.get_interface(self)
        if self.config.get("MD_FUNC"):
            self.market = MdApi(self.event_engine)
            self.market.connect(info)

        if self.config.get("TD_FUNC"):
            self.trader = TdApi(self.event_engine)
            self.trader.connect(info)
            sleep(0.5)

    @locked_cached_property
    def name(self):
        if self.import_name == '__main__':
            fn = getattr(sys.modules['__main__'], '__file__', None)
            if fn is None:
                return '__main__'
            return os.path.splitext(os.path.basename(fn))[0]
        return self.import_name

    def start(self, log_output=True):
        """开始"""
        if not self.event_engine.status:
            self.event_engine.start()
        self.config["LOG_OUTPUT"] = log_output
        self._load_ext()

    def stop(self):
        """ 停止运行 """
        if self.event_engine.status:
            self.event_engine.stop()

    @check(type="trader")
    def send_order(self, order_req: OrderRequest) -> AnyStr:
        """发单"""
        result = self.risk_gateway.send(self)
        if False in result:
            event = Event(type=EVENT_LOG, data="风控阻止下单")
            self.event_engine.put(event)
            return
        send_monitor.send(order_req)
        return self.trader.send_order(order_req)

    @check(type="trader")
    def cancle_order(self, cancle_req: CancelRequest):
        """撤单"""
        cancle_monitor.send(cancle_req)
        self.trader.cancel_order(cancle_req)

    @check(type="market")
    def subscribe(self, symbol: AnyStr):
        """订阅行情"""
        if "." in symbol:
            symbol = symbol.split(".")[1]
        return self.market.subscribe(symbol)

    @check(type="trader")
    def query_position(self):
        """查询持仓"""
        return self.trader.query_position()

    @check(type="trader")
    def transfer(self, req, type):
        """
        req currency attribute
        ["USD", "HKD", "CNY"]
        :param req:
        :param type:
        :return:
        """
        self.trader.transfer(req, type=type)

    @check(type="trader")
    def query_account_register(self, req):
        self.trader.query_account_register(req)

    @check(type="trader")
    def query_bank_account_money(self, req):
        self.trader.query_bank_account_money(req)

    @check(type="trader")
    def query_transfer_serial(self, req):
        self.trader.query_transfer_serial(req)

    @check(type="trader")
    def query_bank(self):
        pass

    @check(type="trader")
    def query_account(self):
        """查询账户"""
        return self.trader.query_account()

    def remove_extension(self, extension_name: Text) -> None:
        """移除插件"""
        if extension_name in self.extensions:
            del self.extensions[extension_name]

    def add_extension(self, extension: CtpbeeApi):
        """添加插件"""
        if extension.extension_name in self.extensions:
            return
        extension.init_app(self)
        self.extensions[extension.extension_name] = extension

    def suspend_extension(self, extension_name):
        extension = self.extensions.get(extension_name, None)
        if not extension:
            return False
        extension.frozen = True
        return True

    def enable_extension(self, extension_name):
        extension = self.extensions.get(extension_name, None)
        if not extension:
            return False
        extension.frozen = False
        return True

    def reload(self):
        """ 重新载入接口 """
        if self.market is not None:
            self.market.close()
        if self.trader is not None:
            self.trader.close()
        self._load_ext()

    def __del__(self):
        """释放账户 安全退出"""
        print("注销")
        if self.market is not None:
            self.market.close()
        if self.trader is not None:
            self.trader.close()
        self.market, self.trader = None, None

        del self.event_engine
