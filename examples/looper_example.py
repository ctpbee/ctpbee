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

    class DoubleMaStrategy(LooperApi):
        fast_window = 5
        slow_window = 50

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
                            "commission": 0.005,
                            "deal_pattern": "price",
                            "size_map": {"ag1912.SHFE": 15},
                            "today_commission": 0.005,
                            "yesterday_commission": 0.02,
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
    result = vessel.get_result()
    pprint(result)


if __name__ == '__main__':
    # data = get_data()
    # save_data_json(data)
    data = load_data()
    for x in data:
        x['datetime'] = datetime.strptime(str(x['datetime']), "%Y-%m-%d %H:%M:%S")
    run_main(data)
