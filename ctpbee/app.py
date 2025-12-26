# coding:utf-8
import os
import sys
from datetime import datetime
from inspect import ismethod
from threading import Thread
from time import sleep
from typing import Text

from ctpbee import __version__
from ctpbee.center import Center
from ctpbee.config import Config
from ctpbee.constant import ContractData, Event, Exchange, Mode
from ctpbee.context import _app_context_ctx
from ctpbee.exceptions import ConfigError
from ctpbee.helpers import find_package, graphic_pattern, refresh_query
from ctpbee.interface import Interface
from ctpbee.jsond import dumps
from ctpbee.level import Action, CtpbeeApi
from ctpbee.log import VLogger
from ctpbee.looper.data import VessData
from ctpbee.looper.report import render_result
from ctpbee.record import Recorder
from ctpbee.signals import AppSignal, common_signals
from ctpbee.stream import Dispatcher


class CtpBee(object):
    """
    ctpbee 旨在开发出一套具有完整api的交易微框架
    """

    # 默认配置参数
    default_config = dict(
        LOG_OUTPUT=True,  # 是否开启输出模式
        TD_FUNC=False,  # 是否开启交易功能
        INTERFACE="ctp",  # 接口参数,默认指定国内期货ctp
        MD_FUNC=True,  # 是否开启行情功能
        ALL_SUBSCRIBE=False,
        SHARE_MD=False,  # 是否多账户之间共享行情,---> 等待完成
        SLIPPAGE_COVER=0,  # 平多头滑点设置
        SLIPPAGE_SELL=0,  # 平空头滑点设置
        SLIPPAGE_SHORT=0,  # 卖空滑点设置
        SLIPPAGE_BUY=0,  # 买多滑点设置
        SHARED_FUNC=False,  # 分时图数据 --> 等待优化
        REFRESH_INTERVAL=3,  # 定时刷新秒数, 需要在CtpBee实例化的时候将refresh设置为True才会生效
        INSTRUMENT_INDEPEND=False,  # 是否开启独立行情,策略对应相应的行情
        CLOSE_PATTERN="today",  # 面对支持平今的交易所,优先平今或者平昨 ---> today: 平今, yesterday: 平昨, 其他:d
        TODAY_EXCHANGE=[
            Exchange.SHFE.value,
            Exchange.INE.value,
        ],  # 需要支持平今的交易所代码列表
        AFTER_TIMEOUT=3,  # 设置after线程执行超时,
        TIMER_INTERVAL=1,  # 定时器触发间隔
        PATTERN="real",  # 实盘交易模式
        WAIT_INIT=60,  # 强制init时间
    )

    config_class = Config
    import_name = None

    # 交易api与行情api / trade api and market api

    def __init__(
        self,
        name: Text,
        import_name,
        action_class: Action or None = None,
        engine_method: str = "thread",
        refresh: bool = True,
        work_mode: Mode = Mode.API,
        instance_path=None,
    ):
        """
        name: 创建运行核心的名字
        import_name: 导入包的名字, 用__name__即可'
        action_class: 执行器 > 默认使用系统自带的Action, 或者由用户继承,然后传入类
        engine_method: Actor模型采用的底层的引擎
        logger_class: logger类,可以自己定义
        work_mode: 判断工作模式 默认为API, 可以填为`dispatcher`
        refresh: 是否自己主动查询账户 默认开启
        """
        self.market = None
        self.trader = None
        self.start_datetime = datetime.now()
        self.basic_info = None
        self._extensions = {}
        self.name = name
        self.import_name = import_name
        self.engine_method = engine_method

        if not refresh:
            raise ValueError("ctpbee 1.7+ only support refresh=True")
        self.refresh = refresh
        self.active = False
        self.logger = VLogger
        self.logger.set_field_default(name=self.name, owner=self.name)
        self.tools = {}
        self.app_signal = AppSignal(self.name)
        if engine_method == "thread":
            self.recorder = Recorder(self)
        else:
            raise TypeError("引擎参数错误,只支持 thread 和 async,请检查代码")
        """
        If no action is specified by default, use the default Action class
        如果默认不指定action参数, 那么使用默认的Action类
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
        如果不指定engine_method参数,那么使用默认的事件引擎 或者根据你的参数使用不同的引擎和记录器
        """

        if instance_path is None:
            instance_path = self.auto_find_instance_path()
        elif not os.path.isabs(instance_path):
            raise ValueError(
                "If an instance path is provided it must be absolute."
                " A relative path was given instead."
            )
        self.instance_path = instance_path
        self.config = self.make_config()
        self.init_finished = False
        # default monitor and flag
        self.p = None
        self.p_flag = True

        self.r = None
        self.r_flag = True

        self.center: Center = Center(self)

        self._init_interface = False
        """ update """

        for x in dir(self.action):
            func = getattr(self.action, x)
            if x.startswith("__"):
                continue
            if ismethod(func):
                setattr(self, func.__name__, func)
        _app_context_ctx.push(self.name, self)

        self.data = []

        self.work_mode = work_mode

        self._temp_contracts = []

    def add_data(self, *data):
        """
        在回测模式下添加历史数据到系统中去

        Args:
          data (list): 多个数据载入

        Examples:
            # first style
            app.add_data(data1_iter, data2_iter)

            # second style
            data = [data1_iter, data2_iter)
            app.add_data(*data)
        """
        if self.config.get("PATTERN") == "looper":
            self.data = data
        else:
            raise TypeError(
                "此API仅仅接受回测模式, 请通过配置文件 PATTERN 修改运行模式"
            )

    def update_action_class(self, action_class: Action):
        """
        更新操作类,除了在CtpBee的构造函数中传入action外, 你还可以通过此接口更新Action类

        Args:
          action_class (Action): 操作类
        """
        if not issubclass(action_class, Action):
            raise TypeError(
                f"更新action_class出现错误, 你传入的action_class类型为{type(action_class)}"
            )
        self.action = action_class(self)

    def make_config(self):
        """
        生成config实例
        """
        defaults = dict(self.default_config)
        return self.config_class(self.instance_path, defaults)

    def auto_find_instance_path(self):
        """
        找到实例地址
        """
        prefix, package_path = find_package(self.import_name)
        if prefix is None:
            return os.path.join(package_path)
        return os.path.join(prefix, "var", self.name + "-instance")

    @property
    def td_login_status(self):
        """
        交易接口状态
        交易 API 都应该实现td_status
        """
        return self.trader.td_status

    @property
    def md_login_status(self):
        """
        行情接口状态
        行情 API 都应该实现md_status
        """
        return self.market.md_status

    def _running(self, logout=True):
        """
        根据当前配置文件下的信息载入行情api和交易api
        注意此函数同时会根据构造函数中的refresh参数决定开启定时线程, 向CtpBee里面提供定时查询账户持仓功能
        """
        show_me = graphic_pattern(__version__, self.engine_method)
        if logout:
            print(show_me)

        self.init_interface()
        if self.config["PATTERN"] == "real" and self.r is None:
            self.r = Thread(
                target=refresh_query,
                args=(
                    self,
                    common_signals,
                    self.refresh,
                ),
                daemon=False,
            )
            self.r.start()
        else:
            pass

    def init_interface(self):
        if self.config.get("PATTERN", "real") == "real" and not self._init_interface:
            self.active = True
            if "CONNECT_INFO" in self.config.keys():
                info = self.config.get("CONNECT_INFO")
            else:
                raise ConfigError(
                    message="没有相应的登录信息", args=("没有发现登录信息",)
                )
            MdApi, TdApi = Interface.get_interface(self)
            if self.config.get("MD_FUNC"):
                self.market = MdApi(self.app_signal)
                self.market.connect(info)
            if self.config.get("TD_FUNC"):
                self.trader = TdApi(self.app_signal)
                self.trader.connect(info)
            self._init_interface = True
        elif (
            self.config.get("PATTERN", "real") == "looper" and not self._init_interface
        ):
            self.config["INTERFACE"] = "looper"
            Market, Trader = Interface.get_interface(app=self)
            self.trader = Trader(self.app_signal, self)
            self.market = Market(self.app_signal)
            self._init_interface = True

    def add_local_contract(self, contract: ContractData):
        """
        给本地合约添加合约以及给account对象添加合约
        """
        self._temp_contracts.append(contract)

    def start(self, log_output=False, debug=False):
        """
        开启处理整个事件处理循环

        Args:
          log_output(bool): 是否输出log信息

          debug(bool): 是否开启调试模式 ----> 等待完成
        """
        if self.config.get("PATTERN") == "real":
            if self.work_mode == Mode.DISPATCHER:
                dispatcher = Dispatcher(name="ctpbee_dispatcher", app=self)
                self.add_extension(dispatcher)
            log_output = self.config.get("LOG_OUTPUT", False) | log_output
            self._running(logout=log_output)
        elif self.config.get("PATTERN") == "looper":
            self.config["INTERFACE"] = "looper"
            show_me = graphic_pattern(__version__, self.engine_method)
            if log_output:
                print(show_me)
            self.init_interface()
            print(">>>> 回测接口载入成功")
            return self._start_looper()
        else:
            raise ValueError("错误的参数, 仅仅支持")

    def get_result(self, report: bool = False, **kwargs):
        """
        计算回测结果,生成回测报告

        Args:
          report(bool): 是否生成报告

          auto_open(bool): 是否让浏览器自动打开回测报告

        Return:
            Dataframe: 生成结果, 以Dataframe形式.
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
        cost_time = (
            f"{str(end_time.hour - self.start_datetime.hour)}"
            f"h {str(end_time.minute - self.start_datetime.minute)}m "
            f"{str(end_time.second - self.start_datetime.second)}s"
        )
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
            path = render_result(
                self.trader.account.result,
                trade_data=trade_data,
                strategy=strategys,
                net_pnl=net_pnl,
                account_data=account_data,
                datetimed=end_time,
                position_data=position_data,
                cost_time=cost_time,
                **kwargs,
            )
            print(f"请复制下面的路径到浏览器打开----> \n {path}")

        return self.trader.account.result, list(
            self.trader.traded_order_mapping.values()
        )

    def add_basic_info(self, info):
        """
        添加基础手续费以及size_map等信息
        todo: 暂未开源data_api

        Args:
            info(dict): 配置信息

        """
        if self.config.get("PATTERN") != "looper":
            raise TypeError("此API仅在回测模式下进行调用")
        self.basic_info = info
        if self.trader is not None:
            self.trader.account.basic_info = self.basic_info

    def _start_looper(self):
        """
        基于现有的数据进行回测数据, 此API用户不需要关注
        """
        d = VessData(*self.data)
        if self.basic_info is not None:
            self.trader.account.basic_info = self.basic_info
        """ trader初始化参数"""
        self.trader.init_params(params=self.config)
        for contract in self._temp_contracts:
            self.trader.account.add_contract(contract)
            self.recorder.contracts[contract.local_symbol] = contract
        flag = False
        while True:
            try:
                if flag:
                    p = next(d)
                    self.trader(p)
                else:
                    print("===> 发送初始化信号")
                    from ctpbee.constant import EVENT_INIT_FINISHED

                    self.app_signal.init_signal.send(
                        Event(type=EVENT_INIT_FINISHED, data=None)
                    )
                    flag = True
            except StopIteration:
                self.logger.info("回测结束,正在生成结果")
                break
            except ValueError:
                raise ValueError("数据存在问题, 请检查")

        return self.trader

    def remove_extension(self, extension_name: Text) -> None:
        """
        移除插件(策略)

        Args:
          extension_name(Text): 策略名

        """
        if extension_name in self._extensions:
            del self._extensions[extension_name]

    def add_extension(self, extension: CtpbeeApi) -> None:
        """
        添加插件(策略)

        Args:
          extension(CtpbeeApi): 策略实例

        """
        self._extensions.pop(extension.extension_name, None)
        extension.init_app(self)

    def suspend_extension(self, extension_name: Text) -> bool:
        """
        停止插件(策略)

        Args:
           extension_name(Text): 策略名字

        """
        extension = self._extensions.get(extension_name, None)
        if not extension:
            return False
        extension.__frozen = True
        return True

    def get_extension(self, extension_name) -> None or CtpbeeApi:
        """
        获取插件(策略)实例

        Args:
           extension_name(Text): 策略名字

        Return:
            CtpbeeApi/None: 存在就返回实体,不存在返回None

        """
        if extension_name in self._extensions:
            return self._extensions.get(extension_name)
        else:
            return None

    def enable_extension(self, extension_name) -> bool:
        """
        启用插件(策略)实例

        Args:
           extension_name(Text): 策略名字

        Return:
            bool: 操作结果

        """
        extension = self._extensions.get(extension_name, None)
        if not extension:
            return False
        extension.__frozen = False
        return True

    def del_extension(self, extension_name: Text):
        """
        卸载插件(策略)实例

        Args:
           extension_name(Text): 策略名字

        Return:
            None

        """
        self._extensions.pop(extension_name, None)

    def reload(self):
        """
        重新载入接口
        """
        if self.market is not None:
            self.market.close()
        if self.trader is not None:
            self.trader.close()
        # 清空处理队列
        sleep(3)
        self.market, self.trader = None, None
        self._running()

    def add_tool(self, tool):
        self.tools[tool.name] = tool

    def get_tool(self, name):
        return self.tools.get(name)

    def delete_tool(self, name):
        if name in self.tools.keys():
            self.tools.pop(name)
            return 1
        return -1

    def with_tools(self, *args):
        for i in args:
            i.init_app(self)
        return self

    def with_extensions(self, *args):
        for i in args:
            i.init_app(self)
        return self

    def release(self):
        """
        释放账户,安全退出
        """
        try:
            if self.market is not None:
                self.market.close()
            if self.trader is not None:
                self.trader.close()
            self.market, self.trader = None, None
            if self.r is not None:
                # 安全终止线程：设置退出标志，让线程自己退出
                self.r_flag = False
                # 等待线程退出，最多等待1秒
                self.r.join(timeout=1.0)
                self.r = None
        except AttributeError:
            pass
