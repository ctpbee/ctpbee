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


# def get_data(start, end, symbol, exchange, level):
#     """ using rqdatac to make an example """
#     import rqdatac as rq
#     from rqdatac import get_price, id_convert
#     username = "license"
#     password = "NK-Ci7vnLsRiPPWYwxvvPYdYM90vxN60qUB5tVac2mQuvZ8f9Mq8K_nnUqVspOpi4BLTkSLgq8OQFpOOj7L" \
#                "t7AbdBZEBqRK74fIJH5vsaAfFQgl-tuB8l03axrW8cyN6-nBUho_6Y5VCRI63Mx_PN54nsQOpc1psIGEz" \
#                "gND8c6Y=bqMVlABkpSlrDNk4DgG-1QXNknJtk0Kkw2axvFDa0E_XPMqOcBxifuRa_DFI2svseXU-8A" \
#                "eLjchnTkeuvQkKh6nrfehVDiXjoMeq5sXgqpbgFAd4A5j2B1a0gpE3cb5kXb42n13fGwFaGris" \
#                "8-eKzz_jncvuAamkJEQQV0aLdiw="
#     host = "rqdatad-pro.ricequant.com"
#     port = 16011
#     rq.init(username, password, (host, port))
#     symbol_rq = id_convert(symbol)
#     data = get_price(symbol_rq, start_date=start, end_date=end, frequency=level, fields=None,
#                      adjust_type='pre', skip_suspended=False, market='cn', expect_df=False)
#     origin = data.to_dict(orient='records')
#     result = []
#     for x in origin:
#         do = {}
#         do['open_price'] = x['open']
#         do['low_price'] = x['low']
#         do['high_price'] = x['high']
#         do['close_price'] = x['close']
#         do['datetime'] = datetime.strptime(str(x['trading_date']), "%Y-%m-%d %H:%M:%S")
#         do['symbol'] = symbol
#         do['local_symbol'] = symbol + "." + exchange
#         do['exchange'] = exchange
#         result.append(do)
#     return result


def get_a_strategy():
    from ctpbee.looper.ta_lib import ArrayManager

    class DoubleMaStrategy(LooperApi):
        fast_window = 20
        slow_window = 10

        fast_ma0 = 0.0
        fast_ma1 = 1.0

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

    class BollStrategy(LooperApi):

        boll_window = 18
        boll_dev = 3.4
        cci_window = 10
        atr_window = 30
        sl_multiplier = 5.2
        fixed_size = 1

        boll_up = 0
        boll_down = 0
        cci_value = 0
        atr_value = 0

        intra_trade_high = 0
        intra_trade_low = 0
        long_stop = 0
        short_stop = 0

        parameters = ["boll_window", "boll_dev", "cci_window",
                      "atr_window", "sl_multiplier", "fixed_size"]
        variables = ["boll_up", "boll_down", "cci_value", "atr_value",
                     "intra_trade_high", "intra_trade_low", "long_stop", "short_stop"]

        def __init__(self, name):
            super().__init__(name)
            self.am = ArrayManager()
            self.pos = 0

        def on_bar(self, bar):
            am = self.am
            am.update_bar(bar)
            if not am.inited:
                return

            self.boll_up, self.boll_down = am.boll(self.boll_window, self.boll_dev)
            self.cci_value = am.cci(self.cci_window)
            self.atr_value = am.atr(self.atr_window)

            if self.pos == 0:
                self.intra_trade_high = bar.high_price
                self.intra_trade_low = bar.low_price

                if self.cci_value > 0:
                    self.action.buy(self.boll_up, self.fixed_size, bar)
                elif self.cci_value < 0:
                    self.action.short(self.boll_down, self.fixed_size, bar)

            elif self.pos > 0:
                self.intra_trade_high = max(self.intra_trade_high, bar.high_price)
                self.intra_trade_low = bar.low_price

                self.long_stop = self.intra_trade_high - self.atr_value * self.sl_multiplier
                self.action.sell(self.long_stop, abs(self.pos), bar)

            elif self.pos < 0:
                self.intra_trade_high = bar.high_price
                self.intra_trade_low = min(self.intra_trade_low, bar.low_price)

                self.short_stop = self.intra_trade_low + self.atr_value * self.sl_multiplier
                self.action.cover(self.short_stop, abs(self.pos), bar)

        def on_trade(self, trade):
            if trade.direction == Direction.LONG:
                self.pos += trade.volume
            else:
                self.pos -= trade.volume

        def on_order(self, order):
            pass

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
    # data = get_data(start="2019-1-5", end="2019-9-1", symbol="ag1912", exchange="SHFE", level="15m")
    # save_data_json(data)
    try:
        import talib
    except ImportError:
        print("please install talib first")

    data = load_data()
    for x in data:
        x['datetime'] = datetime.strptime(str(x['datetime']), "%Y-%m-%d %H:%M:%S")
    run_main(data)
