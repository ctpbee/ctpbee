# coding:utf-8
import os
import sys
from datetime import datetime
from inspect import ismethod

from threading import Thread
from time import sleep
from typing import Text

from werkzeug.datastructures import ImmutableDict

from ctpbee import __version__
from ctpbee.looper.data import VessData
from ctpbee.looper.report import render_result
from ctpbee.util import RiskLevel
from ctpbee.center import Center
from ctpbee.config import Config
from ctpbee.constant import Exchange
from ctpbee.context import _app_context_ctx
from ctpbee.constant import Event, EVENT_TIMER
from ctpbee.exceptions import ConfigError
from ctpbee.helpers import end_thread
from ctpbee.helpers import find_package, refresh_query, graphic_pattern
from ctpbee.interface import Interface
from ctpbee.level import CtpbeeApi, Action
from ctpbee.log import VLogger
from ctpbee.record import Recorder
from ctpbee.cprint_config import CP
from ctpbee.jsond import dumps
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
             CLOSE_PATTERN="today",  # 面对支持平今的交易所，优先平今或者平昨 ---> today: 平今, yesterday: 平昨， 其他:d
             TODAY_EXCHANGE=[Exchange.SHFE.value, Exchange.INE.value],  # 需要支持平今的交易所代码列表
             AFTER_TIMEOUT=3,  # 设置after线程执行超时,
             TIMER_INTERVAL=1,
             PATTERN="real"
             ))

    config_class = Config
    import_name = None

    # 交易api与行情api / trade api and market api
    market = None
    trader = None
    tools = {}

    def __init__(self,
                 name: Text,
                 import_name,
                 action_class: Action or None = None,
                 engine_method: str = "thread",
                 logger_class=None, logger_config=None,
                 refresh: bool = False,
                 risk: RiskLevel = None,
                 instance_path=None):
        """
        name: 创建运行核心的名字
        import_name: 导入包的名字， 用__name__即可'
        action_class: 执行器 > 默认使用系统自带的Action, 或者由用户继承，然后传入类
        engine_method: Actor模型采用的底层的引擎
        logger_class: logger类，可以自己定义
        refresh: 是否自己主动持仓
        risk: 风险管理类, 可以自己继承RiskLevel进行定制
        sim: 是否进行模拟
        """
        self.start_datetime = datetime.now()
        self.basic_info = None
        self._extensions = {}
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
            self.action: Action = Action(self)
        else:
            self.action: Action = action_class(self)
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
        self.qifi = None
        # default monitor and flag
        self.p = None
        self.p_flag = True

        self.r = None
        self.r_flag = True

        self.center: Center = Center(self)
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

        self.data = []

    def add_data(self, *data):
        """
        载入历史回测数据
        """
        if self.config.get("PATTERN") == "looper":
            self.data = data
        else:
            raise TypeError("此API仅仅接受回测模式, 请通过配置文件 PATTERN 修改运行模式")

    def update_action_class(self, action_class):
        if isinstance(action_class, Action):
            raise TypeError(f"更新action_class出现错误, 你传入的action_class类型为{type(action_class)}")
        self.action = action_class(self)

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

    def _running(self, logout=True):
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

    def start(self, log_output=True, debug=False):
        """
        开启处理
        :param log_output: 是否输出log信息
        :param debug: 是否开启调试模式 ----> 等待完成
        :return:
        """
        if self.config.get("PATTERN") == "real":
            def running_timer(common_signal):
                while True:
                    event = Event(type=EVENT_TIMER)
                    common_signal.timer_signal.send(event)
                    sleep(self.config['TIMER_INTERVAL'])

            self.timer = Thread(target=running_timer, args=(common_signals,))
            self.timer.start()

            self.config["LOG_OUTPUT"] = log_output
            self._running(logout=log_output)
        elif self.config.get("PATTERN") == "looper":
            self.config["INTERFACE"] = "looper"
            show_me = graphic_pattern(__version__, self.engine_method)
            if log_output:
                print(show_me)
            Trader, Market = Interface.get_interface(app=self)
            self.trader = Trader(self.app_signal, self)
            self.market = Market(self.app_signal)
            print(">>>> 回测接口载入成功")
            self._start_looper()
        else:
            raise ValueError("错误的参数, 仅仅支持")

    def get_result(self, report: bool = False, **kwargs):
        """
        计算回测结果，生成回测报告
        :param report: bool ,指定是否输出策略报告
        :param auto_open: bool, 是否让浏览器自动打开回测报告
        :param zh:bpol, 是否输出成中文报告
        """
        strategys = list(self._extensions.keys())
        end_time = datetime.now()
        """
        账户数据
        """
        account_data = self.trader.account.get_mapping("balance")
        """
        耗费时间
        """
        cost_time = f"{str(end_time.hour - self.start_datetime.hour)}" \
                    f"h {str(end_time.minute - self.start_datetime.minute)}m " \
                    f"{str(end_time.second - self.start_datetime.second)}s"
        """
        每日盈利
        """
        net_pnl = self.trader.account.get_mapping("net_pnl")

        """
        成交单数据
        """
        trade_data = list(map(dumps, self.trader.traded_order_mapping.values()))
        position_data = self.trader.position_detail
        if report:
            path = render_result(self.trader.account.result, trade_data=trade_data, strategy=strategys,
                                 net_pnl=net_pnl,
                                 account_data=account_data, datetimed=end_time, position_data=position_data,
                                 cost_time=cost_time, **kwargs)
            print(f"请复制下面的路径到浏览器打开----> \n {path}")
            return path
        return self.trader.account.result

    def add_basic_info(self, info):
        """ 添加基础手续费以及size_map等信息 """
        if self.config.get("PATTERN") != "looper":
            raise TypeError("此API仅在回测模式下进行调用")
        self.basic_info = info

    def _start_looper(self):
        """ 基于现有的数据进行回测数据 """
        d = VessData(*self.data)
        if self.basic_info is not None:
            self.trader.account.basic_info = self.basic_info
        """ trader初始化参数"""
        self.trader.init_params(params=self.config)
        while True:
            try:
                p = next(d)
                self.trader(p)
            except StopIteration:
                self.logger.info("回测结束,正在生成结果")
                break
            except  ValueError:
                raise ValueError("数据存在问题, 请检查")

    def remove_extension(self, extension_name: Text) -> None:
        """移除插件"""
        if extension_name in self._extensions:
            del self._extensions[extension_name]

    def add_extension(self, extension: CtpbeeApi):
        """添加插件"""
        self._extensions.pop(extension.extension_name, None)
        extension.init_app(self)

    def suspend_extension(self, extension_name):
        extension = self._extensions.get(extension_name, None)
        if not extension:
            return False
        extension.frozen = True
        return True

    def get_extension(self, extension_name):
        if extension_name in self._extensions:
            return self._extensions.get(extension_name)
        else:
            return None

    def enable_extension(self, extension_name):
        extension = self._extensions.get(extension_name, None)
        if not extension:
            return False
        extension.frozen = False
        return True

    def del_extension(self, extension_name):
        self._extensions.pop(extension_name, None)

    def reload(self):
        """ 重新载入接口 """
        if self.market is not None:
            self.market.close()
        if self.trader is not None:
            self.trader.close()
        # 清空处理队列
        sleep(3)
        self.market, self.trader = None, None
        self._running()

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



