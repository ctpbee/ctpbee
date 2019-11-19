"""
    简单滑动平均线sma策略  sar = info.sma()
"""

import json
from datetime import datetime, date
from ctpbee import LooperApi, Vessel
from ctpbee.constant import Direction
from ctpbee.indicator import Indicator


def get_data(start, end, symbol, exchange, level):
    """ using rqdatac to make an example """
    # import rqdatac as rq
    # from rqdatac import get_price, id_convert
    # username = "license"
    # password = "NK-Ci7vnLsRiPPWYwxvvPYdYM90vxN60qUB5tVac2mQuvZ8f9Mq8K_nnUqVspOpi4BLTkSLgq8OQFpOOj7L" \
    #            "t7AbdBZEBqRK74fIJH5vsaAfFQgl-tuB8l03axrW8cyN6-nBUho_6Y5VCRI63Mx_PN54nsQOpc1psIGEz" \
    #            "gND8c6Y=bqMVlABkpSlrDNk4DgG-1QXNknJtk0Kkw2axvFDa0E_XPMqOcBxifuRa_DFI2svseXU-8A" \
    #            "eLjchnTkeuvQkKh6nrfehVDiXjoMeq5sXgqpbgFAd4A5j2B1a0gpE3cb5kXb42n13fGwFaGris" \
    #            "8-eKzz_jncvuAamkJEQQV0aLdiw="
    # host = "rqdatad-pro.ricequant.com"
    # port = 16011
    # rq.init(username, password, (host, port))
    # symbol_rq = id_convert(symbol)
    # data = get_price(symbol_rq, start_date=start, end_date=end, frequency=level, fields=None,
    #                  adjust_type='pre', skip_suspended=False, market='cn', expect_df=False)
    # origin = data.to_dict(orient='records')
    # result = []
    # for x in origin:
    #     do = {}
    #     do['open_price'] = x['open']
    #     do['low_price'] = x['low']
    #     do['high_price'] = x['high']
    #     do['close_price'] = x['close']
    #     do['datetime'] = datetime.strptime(str(x['trading_date']), "%Y-%m-%d %H:%M:%S")
    #     do['symbol'] = symbol
    #     do['local_symbol'] = symbol + "." + exchange
    #     do['exchange'] = exchange
    #     result.append(do)
    # return result


def get_a_strategy():
    class SmaStrategy(LooperApi):

        def __init__(self, name):
            super().__init__(name)
            self.count = 1
            self.pos = 0

            self.bar_3 = Indicator()  # 3分钟bar线
            # self.bar_3.open_json('../zn1912.SHFE.json')  # 读取本地数据

            self.allow_max_price = 5000  # 设置价格上限 当价格达到这个就卖出 防止突然跌
            self.allow_low_price = 2000  # 设置价格下限 当价格低出这里就卖 防止巨亏

        def on_bar(self, bar):
            # todo: 抛物线指标 SAR
            """ """
            self.bar_3.add_bar(bar)
            if not self.bar_3.inited:
                return
            close = self.bar_3.close
            sma = self.bar_3.sma()

            if self.allow_max_price < bar.close_price and self.pos > 0:
                self.action.sell(bar.close_price, self.pos, bar)

            if self.allow_low_price > bar.close_price and self.pos > 0:
                self.action.sell(bar.close_price, self.pos, bar)

            # 连涨就买
            if sma[-1] > sma[-2] and close[-1] > sma[-2]:
                # 没有就买
                if self.pos == 0:
                    self.action.buy(bar.close_price, 1, bar)
                elif self.pos < 0:
                    self.action.cover(bar.close_price, 1, bar)
                    self.action.buy(bar.close_price, 1, bar)
            # 跌就卖
            else:
                if self.pos > 0:
                    self.action.sell(bar.close_price, self.pos, bar)
                    self.action.short(bar.close_price, self.pos, bar)

        def on_trade(self, trade):
            if trade.direction == Direction.LONG:
                self.pos += trade.volume
            else:
                self.pos -= trade.volume

        def init_params(self, data):
            """"""
            # print("我在设置策略参数")

    return SmaStrategy("double_ma")


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

    with open("../data.json", "w") as f:
        json.dump(result, f, cls=CJsonEncoder)


def load_data():
    with open("../data.json", "r") as f:
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
    data = load_data()
    for x in data:
        x['datetime'] = datetime.strptime(str(x['datetime']), "%Y-%m-%d %H:%M:%S")
    run_main(data)