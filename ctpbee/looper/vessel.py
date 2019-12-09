"""
回测容器模块, 回测
"""
from datetime import datetime
from threading import Thread
from time import sleep

from ctpbee.constant import ContractData, OrderData, TradeData, AccountData, PositionData, BarData, TickData
from ctpbee.log import VLogger
from ctpbee.looper.data import VessData
from ctpbee.looper.interface import LocalLooper
from ctpbee.cprint_config import CP
from ctpbee.looper.report import render_result
from ctpbee.jsond import dumps


class LooperApi:
    instrument_set = set()

    def __init__(self, name):
        self.name = name
        self.active = True

    def on_bar(self, bar):
        raise NotImplemented

    def on_tick(self, tick):
        raise NotImplemented

    def on_trade(self, trade):
        raise NotImplemented

    def on_order(self, order):
        raise NotImplemented

    def on_position(self, position):
        raise NotImplemented

    def on_account(self, account):
        raise NotImplemented

    def on_contract(self, contract):
        raise NotImplemented

    def init_params(self, data):
        """ 用户需要继承此方法"""
        # print("我在设置策略参数")

    def __call__(self, data):
        """
        你必须实现此方法以支持在此层进行中转
        """
        if data.local_symbol not in self.instrument_set:
            return
        if not self.active:
            return

        if isinstance(data, ContractData):
            self.on_contract(data)
        elif isinstance(data, OrderData):
            self.on_order(data)
        elif isinstance(data, TradeData):
            self.on_trade(data)
        elif isinstance(data, AccountData):
            self.on_account(data)
        elif isinstance(data, PositionData):
            self.on_position(data)
        elif data['type'] == "bar":
            self.on_bar(BarData(**data))
        elif data['type'] == "tick":
            self.on_tick(TickData(**data))
        else:
            raise ValueError("unsupported data")


class LooperLogger:
    def __init__(self, v_logger=None):
        if v_logger:
            self.logger = v_logger
        else:
            self.logger = VLogger(CP, app_name="Vessel")
            self.logger.set_default(name=self.logger.app_name, owner='App')

    def info(self, msg, **kwargs):
        kwargs['owner'] = "Looper"
        self.logger.info(msg, **kwargs)

    def error(self, msg, **kwargs):
        kwargs['owner'] = "Looper"
        self.logger.error(msg, **kwargs)

    def debug(self, msg, **kwargs):
        kwargs['owner'] = "Looper"
        self.logger.debug(msg, **kwargs)

    def warning(self, msg, **kwargs):
        kwargs['owner'] = "Looper"
        self.logger.warning(msg, **kwargs)

    def __repr__(self):
        return "LooperLogger -----> just enjoy it"


class Vessel:
    """
    策略运行容器

    本地回测与在线数据回测
    >> 基于在线数据推送的模式 是否可以减少本机器的内存使用量

    """

    def __init__(self, logger_class=None, pattern="T0"):
        self.ready = False

        """
        回测数据安放点/Data point
        """
        self.looper_data: [VessData] = []

        """
        创建日志调试器
        """
        if logger_class:
            self.logger = logger_class()
        else:
            self.logger = LooperLogger()
        """ 
        账户级别的风险控制
        """
        self.risk = None

        """
        回测主要接口
        """
        self.interface = LocalLooper(logger=self.logger, risk=self.risk)

        """
        参数配置
        """
        self.params = dict()
        """
        回测模式
        """
        self.looper_pattern = pattern

        """
        _data_status : 数据状态, 准备就绪时候应该被修改为True
        _looper_status: 回测状态, 分为五个
            "unready": 未就绪
            "ready":就绪
            "running": 运行中
            "stopped":暂停
            "finished":结束
        _strategy_status: 策略状态, 载入后应该被修改True
        _risk_status: "风控状态"
        """
        self._data_status = False
        self._looper_status = "unready"
        self._strategy_status = False
        self._risk_status = True

        self.start_time = None

    def add_strategy(self, strategy: LooperApi):
        """ 添加策略到本容器 """
        if not isinstance(strategy, LooperApi):
            raise ValueError(f"你传入的策略类型出现问题，期望: LooperApi, 当前:{type(strategy)}")
        self.interface.update_strategy(strategy)
        self._strategy_status = True
        self.check_if_ready()

    def add_data(self, data):
        """
        注意此处的Add Data,可以添加多个数据源 ---> 他们的长度应该是一开始就对齐！！！
        ： ---> 必须在时间戳上进行对齐， 否则数据进行回放会出现问题。
        """
        d = VessData(data)
        self.looper_data.append(d)
        self._data_status = True
        self.check_if_ready()

    def check_if_ready(self):
        if self._data_status and self._strategy_status and self._risk_status:
            self._looper_status = "ready"
        self.ready = True

    def add_risk(self, risk):
        """ 添加风控 """
        self._risk_status = True
        self.interface.update_risk(risk)
        self.check_if_ready()

    def set_params(self, params):
        """
        设置参数
        :param params: 参数值 dict
        :return:
        """
        if not isinstance(params, dict):
            raise ValueError(f"配置信息格式出现问题， 你当前的配置信息为 {type(params)}")
        self.params = params

    def get_result(self, report: bool = False, **kwargs):
        """
        计算回测结果，生成回测报告
        :param report: bool ,指定是否输出策略报告
        :param auto_open: bool, 是否让浏览器自动打开回测报告
        :param zh:bpol, 是否输出成中文报告
        """
        strategys = list(self.interface.strategy_mapping.keys())
        end_time = datetime.now()
        """
        账户数据
        """
        account_data = self.interface.account.get_mapping("balance")
        """
        耗费时间
        """
        cost_time = f"{str(end_time.hour - self.start_time.hour)}" \
                    f"h {str(end_time.minute - self.start_time.minute)}m " \
                    f"{str(end_time.second - self.start_time.second)}s"
        """
        每日盈利
        """
        net_pnl = self.interface.account.get_mapping("net_pnl")

        """
        成交单数据
        """
        trade_data = list(map(dumps, self.interface.traded_order_mapping.values()))
        if report:
            path = render_result(self.interface.account.result, trade_data=trade_data, strategy=strategys,
                                 net_pnl=net_pnl,
                                 account_data=account_data, datetimed=end_time,
                                 cost_time=cost_time, **kwargs)
            print(f"请复制下面的路径到浏览器打开----> \n {path}")
            return path
        return self.interface.account.result

    def letsgo(self, parmas, ready):

        """
        开始进行回测
        :param parmas:  参数
        :param ready:
        :return:
        """
        if False not in [x.init_flag for x in self.looper_data]:
            # self.logger.info(f"产品: {self.looper_data.product}")
            self.logger.info(f"回测模式: {self.looper_pattern}")
        for x in range(self.looper_data[0].length):
            if ready:
                """ 如果处于就绪状态 那么直接开始继续回测 """
                try:
                    """ 注意开始回放每个数据源的数据 """
                    for _origin_data in self.looper_data:
                        p = next(_origin_data)
                        self.interface(p, parmas)

                except StopIteration:
                    self._looper_status = "finished"
                    break
            else:
                """ 如果处于未就绪状态 那么暂停回测 """
                sleep(1)
        self.logger.info("回测结束,正在生成回测报告")

    def suspend_looper(self):
        """ 暂停回测 """
        self.ready = False
        self._looper_status = "stopped"

    def enable_looper(self):
        """ 继续回测 """
        self.ready = True
        self._looper_status = "running"

    @property
    def looper_status(self):
        return self._looper_status

    @property
    def risk_status(self):
        return self._risk_status

    @property
    def data_status(self):
        return self._data_status

    @property
    def strategy_status(self):
        return self._strategy_status

    @property
    def status(self):
        return (self._looper_status, self._risk_status, self._strategy_status, self._data_status)

    def run(self):
        """ 开始运行回测 """
        self.start_time = datetime.now()
        p = Thread(name="looper", target=self.letsgo, args=(self.params, self.ready,))
        p.start()
        p.join()

    def __repr__(self):
        return "ctpbee Backtesting Vessel powered by ctpbee current version: 0.1"
