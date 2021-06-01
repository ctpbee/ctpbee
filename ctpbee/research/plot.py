from jinja2 import Environment, PackageLoader, select_autoescape

from ctpbee.constant import BarData

env = Environment(
    loader=PackageLoader('ctpbee', 'research'),
    autoescape=select_autoescape(['html', 'xml'])
)

kline_template = env.get_template("bs_template.html")


class Plot(object):

    def __init__(self, name: str, type: str = "bar"):
        """
        根据成交买卖点 生成对应的html文件
        """
        self.name = name
        self.data = {}

    def add_kline(self, local_symbol: str, klines: BarData, trading_record: [dict]):
        """
        给每个品种单独生成k线图
        trading_record: 格式为 [(1,datetime1)]
            1: 开多
            2: 开空
            -1: 平多
            -2： 平空
        """
        self.data.setdefault(local_symbol, {})["record"] = trading_record
        self.data.setdefault(local_symbol, {})["kline"] = [[str(kline.datetime), kline.open_price, kline.high_price,
                                                            kline.low_price, kline.close_price, kline.volume] for kline
                                                           in klines]

    def render(self, path):
        for local_symbol, obj in self.data.items():
            with open(path, "w") as f:
                print(obj)
                kline_string = kline_template.render(draw_klines=obj["kline"], bs=obj["record"])
                f.write(kline_string)


if __name__ == '__main__':
    plot = Plot("some")
    from data_api import DataApi

    code = "rb2105.SHFE"
    data_api = DataApi(uri="http://192.168.1.239:8124")
    kline = data_api.get_n_min_bar(code, 1, "2021-04-15", "2021-04-16")
    plot.add_kline(code, klines=kline, trading_record=[])
    plot.render("x.html")
