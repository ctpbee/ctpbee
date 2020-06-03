# coding:utf-8
import os
import sys
from inspect import ismethod
from threading import Thread
from time import sleep
from typing import Text

from werkzeug.datastructures import ImmutableDict

from ctpbee import __version__
from ctpbee.util import RiskLevel
from ctpbee.center import Center
from ctpbee.config import Config
from ctpbee.constant import Exchange
from ctpbee.context import _app_context_ctx
from ctpbee.constant import Event, EVENT_TIMER
from ctpbee.exceptions import ConfigError
from ctpbee.helpers import end_thread
from ctpbee.context import current_app
from ctpbee.helpers import locked_cached_property, find_package, refresh_query, graphic_pattern
from ctpbee.interface import Interface
from ctpbee.level import CtpbeeApi, Action
from ctpbee.log import VLogger
from ctpbee.record import Recorder
from ctpbee.cprint_config import CP

from ctpbee.signals import AppSignal, common_signals


class CtpBee(object):
    """
    ctpbee 源于我对于做项目的痛点需求, 旨在开发出一套具有完整api的交易微框架
    I hope it will help you !

    """
    # 默认回测配置参数
    default_params = {
        'cash': 10000.0,
        'check_submit': True,
        'eos_bar': False,
        'filler': None,
        "commision": 0.01,
        # slippage options
        'slip_percent': 0.0,
        'slip_fixed': 0.0,
        'slip_open': False,
        'slip_match': True,
        'slip_limit': True,
        'slip_out': False,
        'coc': False,
        'coo': False,
        'int2pnl': True,
        'short_cash': True,
        'fund_start_val': 100.0,
        'fund_mode': False
    }
    default_config = ImmutableDict(
        dict(LOG_OUTPUT=True,  # 是否开启输出模式
             TD_FUNC=False,  # 是否开启交易功能
             INTERFACE="ctp",  # 接口参数，默认指定国内期货ctp
             MD_FUNC=True,  # 是否开启行情功能
             XMIN=[],  # k线序列周期， 支持一小时以内的k线任意生成
             ALL_SUBSCRIBE=False,
             SHARE_MD=False,  # 是否多账户之间共享行情，---> 等待完成
             SLIPPAGE_COVER=0,  # 平多头滑点设置
             SLIPPAGE_SELL=0,  # 平空头滑点设置
             SLIPPAGE_SHORT=0,  # 卖空滑点设置
             SLIPPAGE_BUY=0,  # 买多滑点设置
             LOOPER_PARAMS=default_params,  # 回测需要设置的参数
             SHARED_FUNC=False,  # 分时图数据 --> 等待优化
             REFRESH_INTERVAL=1.5,  # 定时刷新秒数， 需要在CtpBee实例化的时候将refresh设置为True才会生效
             INSTRUMENT_INDEPEND=False,  # 是否开启独立行情，策略对应相应的行情
             CLOSE_PATTERN="today",  # 面对支持平今的交易所，优先平今或者平昨 ---> today: 平今, yesterday: 平昨， 其他:处罚异常
             TODAY_EXCHANGE=[Exchange.SHFE.value, Exchange.INE.value],  # 需要支持平今的交易所代码列表
             AFTER_TIMEOUT=3,  # 设置after线程执行超时,
             TIMER_INTERVAL=1,
             SIM=False
             ))

    config_class = Config
    import_name = None

    # 交易api与行情api / trade api and market api
    market = None
    trader = None

    # 插件Api系统 /Extension system
    extensions = {}

    """ 
    工具, 用于提供一些比较优秀的工具/ Toolbox, using by providing some good tools
    
    注意当前社区接受捐赠，如果你有兴趣发起捐赠 ---> 支付宝 somewheve@gmail.com 
                    注意你的捐赠都会被用到社区发展上面  
    for developers:
        ctpbee发展至今，已经具备微小的基本核模型，我为你们开放了插件接口，
        用于你们自定义扩展接口，注意如果你有好的插件想分享，我会用上述基金发起奖励，并本人送出小礼物一份！！  

    """
    tools = {}

    def __init__(self,
                 name: Text,
                 import_name,
                 action_class: Action = None,
                 engine_method: str = "thread",
                 logger_class=None, logger_config=None,
                 refresh: bool = False,
                 risk: RiskLevel = None,
                 sim: bool = False,
                 instance_path=None):
        """ 初始化 """
        self.name = name if name else 'ctpbee'
        self.import_name = import_name
        self.engine_method = engine_method
        self.refresh = refresh
        self.active = False
        # 是否加载以使用默认的logger类/ choose if use the default logging class
        if logger_class is None:
            self.logger = VLogger(CP, app_name=self.name)
            self.logger.set_default(name=self.logger.app_name, owner=self.name)
        else:
            if logger_config:
                self.logger = logger_class(logger_config, app_name=self.name)
            else:
                self.logger = logger_class(CP, app_name=self.name)
            self.logger.set_default(name=self.logger.app_name, owner='App')

        self.app_signal = AppSignal(self.name)

        if engine_method == "thread":
            self.recorder = Recorder(self)
        else:
            raise TypeError("引擎参数错误，只支持 thread 和 async，请检查代码")

        """
              If no risk is specified by default, set the risk_decorator to None
              如果默认不指定action参数， 那么使用设置风控装饰器为空
              """
        if risk is None:
            self.risk_decorator = None
        else:
            self.risk_decorator = risk
        """
        If no action is specified by default, use the default Action class
        如果默认不指定action参数， 那么使用默认的Action类 
        """
        if action_class is None:
            self.action = Action(self)
        else:
            self.action = action_class(self)
        """
        根据action里面的函数更新到CtpBee上面来
        bind the function of action to CtpBee
        """

        """
        If engine_method is specified by default, use the default EventEngine and Recorder or use the engine
            and recorder basis on your choice
        如果不指定engine_method参数，那么使用默认的事件引擎 或者根据你的参数使用不同的引擎和记录器
        """

        if instance_path is None:
            instance_path = self.auto_find_instance_path()
        elif not os.path.isabs(instance_path):
            raise ValueError(
                'If an instance path is provided it must be absolute.'
                ' A relative path was given instead.'
            )
        self.instance_path = instance_path
        self.config = self.make_config()
        self.init_finished = False

        # default monitor and flag
        self.p = None
        self.p_flag = True

        self.r = None
        self.r_flag = True

        self.center = Center(self)
        """ update """
        if self.risk_decorator is not None:
            self.risk_decorator.update_app(self)

        for x in dir(self.action):
            func = getattr(self.action, x)
            if x.startswith("__"):
                continue
            if ismethod(func):
                setattr(self, func.__name__, func)

        _app_context_ctx.push(self.name, self)

    def update_action_class(self, action_class):
        if isinstance(action_class, Action):
            raise TypeError(f"更新action_class出现错误, 你传入的action_class类型为{type(action_class)}")
        self.action = action_class()

    def update_risk_gateway(self, gateway_class):
        self.risk_decorator = gateway_class
        self.risk_decorator.update_app(self)

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

    def _load_ext(self, logout=True):
        """
        根据当前配置文件下的信息载入行情api和交易api,记住这个api的选项是可选的
        """
        self.active = True
        if "CONNECT_INFO" in self.config.keys():
            info = self.config.get("CONNECT_INFO")
        else:
            raise ConfigError(message="没有相应的登录信息", args=("没有发现登录信息",))
        show_me = graphic_pattern(__version__, self.engine_method)
        if logout:
            print(show_me)
        MdApi, TdApi = Interface.get_interface(self)
        if self.config.get("MD_FUNC"):
            self.market = MdApi(self.app_signal)
            self.market.connect(info)

        if self.config.get("TD_FUNC"):
            if self.config['INTERFACE'] == "looper":
                self.trader = TdApi(self.app_signal, self)
            else:
                self.trader = TdApi(self.app_signal)
            self.trader.connect(info)

        if self.refresh:
            if self.r is not None:
                self.r_flag = False
                sleep(self.config['REFRESH_INTERVAL'] + 1.5)
                self.r = Thread(target=refresh_query, args=(self,), daemon=True)
                self.r.start()
            else:
                self.r = Thread(target=refresh_query, args=(self,), daemon=True)
                self.r.start()
            self.r_flag = True

    @locked_cached_property
    def name(self):
        if self.import_name == '__main__':
            fn = getattr(sys.modules['__main__'], '__file__', None)
            if fn is None:
                return '__main__'
            return os.path.splitext(os.path.basename(fn))[0]
        return self.import_name

    def start(self, log_output=True, debug=False):
        """
        开启处理
        :param log_output: 是否输出log信息
        :param debug: 是否开启调试模式 ----> 等待完成
        :return:
        """
        if current_app is None:
            def running_timer(common_signal):
                while True:
                    event = Event(type=EVENT_TIMER)
                    common_signal.timer_signal.send(event)
                    sleep(self.config['TIMER_INTERVAL'])

            self.timer = Thread(target=running_timer, args=(common_signals,))
            self.timer.start()

        self.config["LOG_OUTPUT"] = log_output
        self._load_ext(logout=log_output)

    def remove_extension(self, extension_name: Text) -> None:
        """移除插件"""
        if extension_name in self.extensions:
            del self.extensions[extension_name]

    def add_extension(self, extension: CtpbeeApi):
        """添加插件"""
        self.extensions.pop(extension.extension_name, None)
        extension.init_app(self)

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

    def del_extension(self, extension_name):
        self.extensions.pop(extension_name, None)

    def reload(self):
        """ 重新载入接口 """
        if self.market is not None:
            self.market.close()
        if self.trader is not None:
            self.trader.close()
        # 清空处理队列
        sleep(3)
        self.market, self.trader = None, None
        self._load_ext()

    def release(self):
        """ 释放账户,安全退出 """
        try:
            if self.market is not None:
                self.market.close()
            if self.trader is not None:
                self.trader.close()
            self.market, self.trader = None, None
            if self.r is not None:
                """ 强行终结掉线程 """
                end_thread(self.r)
            if self.timer is not None:
                end_thread(self.timer)
        except AttributeError:
            pass
