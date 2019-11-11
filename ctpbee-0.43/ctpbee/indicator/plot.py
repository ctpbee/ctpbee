"""
    plot显示线
"""
from .indicator import Indicator

colors = {
    "sma": "b",
    "ema": "r",
    "wma": "c",
    "rsi": "g",
    "smma": "r",
    "atr": "w",
    "stddev": "k",
    "trix": "c",
    "mtm": "y",
    "tema": "m",
    "wr": "r",
    "macd": "g",
    "MACD": "r",
    "signal": "b",
    "K": "g",
    "D": "r",
    "mid": "g",
    "top": "r",
    "bottom": "b"
}


class ShowLine(Indicator):

    def __init__(self):
        super().__init__()

    def plot(self, width=8, height=6, color="k", lw=0.5):
        try:
            from matplotlib import pyplot as plt
            from matplotlib.widgets import MultiCursor
            import matplotlib.dates as mdate
        except ImportError:
            raise ImportError("please pip install matplotlib")
        # 一个画布
        fig = plt.figure(figsize=(width, height))
        # 画布分块 块1
        ax1 = fig.add_subplot(211)
        datetime = self.ret_date
        volume = self.ret_volume
        close = self.ret_close
        # 柱
        ax1.bar(datetime, volume, color='y', label='volume')
        ax1.set_ylabel('volume')
        ax2 = ax1.twinx()

        # 线
        ax2.plot(datetime, close, "#000000", label="CLOSE")
        for average_line in self.average_message:
            ax2.plot(datetime, self.average_message[average_line], colors[average_line], label=average_line)

        ax2.set_ylabel('price')
        # 标题
        plt.title("CTPBEE")
        # 网格
        plt.grid(True)
        # 图列
        plt.legend()
        # 显示时间间隔
        ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))
        # plt.xticks(pd.date_range(datetime[0], datetime[-1]))

        # 块2
        ax3 = plt.subplot(212)
        # 柱形图
        for indicator_line in self.indicator_message:
            plt.plot(datetime, self.indicator_message[indicator_line], colors[indicator_line], label=indicator_line)
        # 网格
        plt.grid(True)
        plt.title("indicator")
        plt.legend()
        ax3.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))  # %H:%M:%S
        # plt.xticks(pd.date_range(datetime[0], datetime[-1]))
        multi = MultiCursor(fig.canvas, (ax1, ax3), color=color, lw=lw, useblit=True, linestyle=':', horizOn=True)
        plt.show()


Scheduler = ShowLine()