"""
回测容器模块, 回测
"""
import json
import os
from datetime import datetime, date
from threading import Thread
from time import sleep

from ctpbee.constant import Direction
from ctpbee.log import VLogger
from ctpbee.looper.data import VessData
from ctpbee.looper.interface import LocalLooper


class LooperStrategy:
    def __init__(self, name):
        self.name = name

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


class LooperLogger:
    def __init__(self, v_logger=None):
        if v_logger:
            self.logger = v_logger
        else:
            self.logger = VLogger(app_name="Vessel")
            self.logger.config.from_pyfile(os.path.join(os.path.abspath(os.path.pardir), 'cprint_config.py'))
            self.logger.set_default(name=self.logger.app_name, owner='App')

    def info(self, msg, **kwargs):
        self.logger.info(msg, owner="Looper", **kwargs)

    def error(self, msg, **kwargs):
        self.logger.error(msg, owner="Looper", **kwargs)

    def debug(self, msg, **kwargs):
        self.logger.debug(msg, owner="Looper", **kwargs)

    def warning(self, msg, **kwargs):
        self.logger.warning(msg, owner="Looper", **kwargs)

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
        self.looper_data: VessData = None
        if logger_class:
            self.logger = logger_class()
        else:
            self.logger = LooperLogger()

        self.risk = None
        self.strategy = None
        self.interface = LocalLooper(logger=self.logger, strategy=self.strategy, risk=self.risk)
        self.params = dict()
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

    def add_strategy(self, strategy):
        """ 添加策略到本容器 """
        self.strategy = strategy

        self.interface.update_strategy(strategy)
        self._strategy_status = True

        self.check_if_ready()

    def add_data(self, data):
        """ 添加data到本容器, 如果没有经过处理 """
        d = VessData(data)
        self.looper_data = d
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
        if not isinstance(params, dict):
            raise ValueError(f"配置信息格式出现问题， 你当前的配置信息为 {type(params)}")
        self.params = params

    def get_result(self):
        """ 计算回测结果，生成回测报告 """
        return self.interface.account.result

    def letsgo(self, parmas, ready):
        if self.looper_data.init_flag:
            self.logger.info(f"产品: {self.looper_data.product}")
            self.logger.info(f"回测模式: {self.looper_pattern}")
        for x in range(self.looper_data.length):
            if ready:
                """ 如果处于就绪状态 那么直接开始继续回测 """
                try:
                    p = next(self.looper_data)
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
        p = Thread(name="looper", target=self.letsgo, args=(self.params, self.ready,))
        p.start()
        p.join()

    def __repr__(self):
        return "Backtesting Vessel powered by ctpbee current version: 0.1"


def get_data():
    """ using rqdatac to make an example """
    import rqdatac as rq
    from rqdatac import get_price, id_convert
    username = "license"
    password = "NK-Ci7vnLsRiPPWYwxvvPYdYM90vxN60qUB5tVac2mQuvZ8f9Mq8K_nnUqVspOpi4BLTkSLgq8OQFpOOj7L" \
               "t7AbdBZEBqRK74fIJH5vsaAfFQgl-tuB8l03axrW8cyN6-nBUho_6Y5VCRI63Mx_PN54nsQOpc1psIGEz" \
               "gND8c6Y=bqMVlABkpSlrDNk4DgG-1QXNknJtk0Kkw2axvFDa0E_XPMqOcBxifuRa_DFI2svseXU-8A" \
               "eLjchnTkeuvQkKh6nrfehVDiXjoMeq5sXgqpbgFAd4A5j2B1a0gpE3cb5kXb42n13fGwFaGris" \
               "8-eKzz_jncvuAamkJEQQV0aLdiw="
    host = "rqdatad-pro.ricequant.com"
    port = 16011
    rq.init(username, password, (host, port))
    symbol = id_convert("ag1912")
    data = get_price(symbol, start_date='2019-01-04', end_date='2019-08-04', frequency='1m', fields=None,
                     adjust_type='pre', skip_suspended=False, market='cn', expect_df=False)
    origin = data.to_dict(orient='records')
    result = []
    for x in origin:
        do = {}
        do['open_price'] = x['open']
        do['low_price'] = x['low']
        do['high_price'] = x['high']
        do['close_price'] = x['close']
        do['datetime'] = datetime.strptime(str(x['trading_date']), "%Y-%m-%d %H:%M:%S")
        do['symbol'] = "ag1912"
        do['local_symbol'] = "ag1912.SHFE"
        do['exchange'] = "SHFE"
        result.append(do)
    return result


def get_a_strategy():
    from ctpbee.looper.ta_lib import ArrayManager

    class DoubleMaStrategy(LooperStrategy):
        fast_window = 10
        slow_window = 20

        fast_ma0 = 0.0
        fast_ma1 = 0.0

        slow_ma0 = 0.0
        slow_ma1 = 0.0

        parameters = ["fast_window", "slow_window"]
        variables = ["fast_ma0", "fast_ma1", "slow_ma0", "slow_ma1"]

        def __init__(self, name):
            super().__init__(name)
            self.count = 1
            self.am = ArrayManager()
            self.pos = 0

        def on_bar(self, bar):
            # todo: 双均线
            """ """

            am = self.am
            am.update_bar(bar)
            if not am.inited:
                return

            fast_ma = am.sma(self.fast_window, array=True)
            self.fast_ma0 = fast_ma[-1]
            self.fast_ma1 = fast_ma[-2]

            slow_ma = am.sma(self.slow_window, array=True)
            self.slow_ma0 = slow_ma[-1]
            self.slow_ma1 = slow_ma[-2]
            # 计算金叉 死叉
            cross_over = self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1
            cross_below = self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1
            # 金叉做多
            if cross_over:
                if self.pos == 0:
                    self.action.buy(bar.close_price, 1, bar)
                # 反向进行开仓
                elif self.pos < 0:
                    self.action.cover(bar.close_price, 1, bar)
                    self.action.buy(bar.close_price, 1, bar)
            # 死叉做空
            elif cross_below:
                if self.pos == 0:
                    self.action.short(bar.close_price, 1, bar)
                # 反向进行开仓
                elif self.pos > 0:
                    self.action.sell(bar.close_price, 1, bar)
                    self.action.short(bar.close_price, 1, bar)

        def on_trade(self, trade):
            if trade.direction == Direction.LONG:
                self.pos += trade.volume
            else:
                self.pos -= trade.volume

        def init_params(self, data):
            """"""
            # print("我在设置策略参数")

    return DoubleMaStrategy("double_ma")


def save_data_json(data):
    result = {"result": data}

    class CJsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            else:
                return json.JSONEncoder.default(self, obj)

    with open("data.json", "w") as f:
        json.dump(result, f, cls=CJsonEncoder)


def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data.get("result")


def run_main(data):
    vessel = Vessel()
    vessel.add_data(data)
    stra = get_a_strategy()
    vessel.add_strategy(stra)
    vessel.set_params({"looper":
                           {"initial_capital": 100000,
                            "commission": 0.01,
                            "deal_pattern": "price",
                            "size_map": {"ag1912.SHFE": 10},
                            "today_commission": 0.01,
                            "yesterday_commission": 0.02,
                            "close_commission": 0.01,
                            "slippage_sell": 0,
                            "slippage_cover": 0,
                            "slippage_buy": 0,
                            "slippage_short": 0,
                            "close_pattern": "yesterday",

                            },
                       "strategy": {}
                       })
    vessel.run()
    from pprint import pprint

    result = vessel.get_result()
    pprint(result)


if __name__ == '__main__':
    # data = get_data()
    # save_data_json(data)

    data = load_data()
    for x in data:
        x['datetime'] = datetime.strptime(str(x['datetime']), "%Y-%m-%d %H:%M:%S")
    run_main(data)
