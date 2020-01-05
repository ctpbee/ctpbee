"""
    当前回测示例
    1.当前数据基于rq进行下载的
    2.首先你需要调用get_data 来获得rq的数据 ，然后save_to_json保存到 json文件中去，主要在此过程中你需要手动对数据加入symbol等
    3.然后通过load_data函数重复调用数据
    4.调用run_main进行回测

    当前的strategy是借助vnpy的 ArrayManager . 你需要对此实现一些额外的安装操作

    需要额外安装的包
    ta-lib,  rqdatac( 后面需要被取代  ？？ Maybe use quantdata )

    目前暂时不够完善   ---> hope it will be a  very fancy framework

    written by somewheve  2019-9-30 08:43

"""

import json
from datetime import datetime, date

from ctpbee import LooperApi, Vessel
from ctpbee.constant import Direction
from ctpbee.indicator import Indicator


class DoubleMaStrategy(LooperApi):
    allow_max_price = 5000  # 设置价格上限 当价格达到这个就卖出 防止突然跌 止盈
    allow_low_price = 2000  # 设置价格下限 当价格低出这里就卖 防止巨亏 止损

    def __init__(self, name):
        super().__init__(name)
        self.count = 1
        self.api = Indicator()

        self.instrument_set = ['rb2001.SHFE']
        self.api.open_json("zn1912.SHFE.json")
        self.pos = 0

    def on_bar(self, bar):
        # todo: 均线 和 MACD 和 BOLL 结合使用
        """ """
        am = self.api
        am.add_bar(bar)
        if not am.inited:
            return


        # 收盘
        close = am.close
        # 压力 平均 支撑
        # top, middle, bottom = am.boll()
        # DIF DEA DIF-DEA
        macd, signal, histo = am.macd()

        if self.allow_max_price <= close[-1] and self.pos > 0:
            self.action.sell(bar.close_price, self.pos, bar)

        if self.allow_low_price >= close[-1] and self.pos > 0:
            self.action.sell(bar.close_price, self.pos, bar)
        # 金叉做多 和 均线>平均
        if histo[-1] > 0:
            if self.pos == 0:
                self.action.buy(bar.close_price, 1, bar)

            elif self.pos < 0:
                self.action.cover(bar.close_price, 1, bar)
                self.action.buy(bar.close_price, 1, bar)
        # 死叉做空
        elif histo[-1] < 0:
            if self.pos == 0:
                pass
            elif self.pos > 0:
                self.action.sell(bar.close_price, 1, bar)
                self.action.short(bar.close_price, 1, bar)

    def on_trade(self, trade):
        if trade.direction == Direction.LONG:
            self.pos += trade.volume
        else:
            self.pos -= trade.volume

    def on_order(self, order):
        pass

    def init_params(self, data):
        """"""
        # print("我在设置策略参数")


def load_data():
    with open("data.json", "r") as f:
        from json import load
        data = load(f)
    return data.get("data")


def run_main(data):
    vessel = Vessel()
    vessel.add_data(data)
    # vessel.add_data(dat)
    stra = DoubleMaStrategy("ma")
    vessel.add_strategy(stra)
    vessel.set_params({"looper":
                           {"initial_capital": 100000,
                            "commission": 0.005,
                            "deal_pattern": "price",
                            "size_map": {"rb2001.SHFE": 15},
                            "today_commission": 0.005,
                            "yesterday_commission": 0.05,
                            "close_commission": 0.005,
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
    result = vessel.get_result(report=True, auto_open=True)


if __name__ == '__main__':
    data = load_data()
    from ctpbee import QADataSupport
    su = QADataSupport()
    data = su.get_future_min("rb2001.SHFE", frq="30min",start="2018-8-1 10:00:10", end="2019-10-1 10:00:10")
    run_main(data)
