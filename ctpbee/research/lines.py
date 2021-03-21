import numpy as np
import matplotlib.pyplot as plt
from typing import List

# import matplotlib.text.Text
from matplotlib.font_manager import FontProperties


def plot_multi(data, cols=None, spacing=.1, **kwargs):
    """ 帮助快速绘画出多个图
     从网上找的 QAQ 好用

     data: DataFrame
     cols: 列表
     """
    from pandas import plotting

    # Get default color style from pandas - can be changed to any other color list
    if cols is None: cols = data.columns
    if len(cols) == 0: return
    try:
        colors = getattr(getattr(plotting, '_matplotlib').style, '_get_standard_colors')(num_colors=len(cols))
    except AttributeError:
        colors = plotting._style._get_standard_colors(num_colors=len(cols))
    except Exception:
        raise ValueError("版本错误无法获取颜色")
    # First axis
    ax = data.loc[:, cols[0]].plot(label=cols[0], color=colors[0], **kwargs)
    ax.set_ylabel(ylabel=cols[0])
    lines, labels = ax.get_legend_handles_labels()

    for n in range(1, len(cols)):
        # Multiple y-axes
        ax_new = ax.twinx()
        ax_new.spines['right'].set_position(('axes', 1 + spacing * (n - 1)))
        data.loc[:, cols[n]].plot(ax=ax_new, label=cols[n], color=colors[n % len(colors)])
        ax_new.set_ylabel(ylabel=cols[n])

        # Proper legend position
        line, label = ax_new.get_legend_handles_labels()
        lines += line
        labels += label

    ax.legend(lines, labels, loc=0)
    return ax


def Aux(yy: List, xx: List, ovx: dict, **kwargs):
    """
    yx: 纵坐标数据
    ax: 横坐标数据
    ovx: {
        "buy": [横坐标下标]
        "sell": [横坐标下标]
    }


    """
    fig, ax = plt.subplots(**kwargs)

    line, = ax.plot(xx, yy, lw=2)
    for index in ovx["buy"]:
        ax.annotate('↑', xy=(xx[index], yy[index]),
                    fontproperties=FontProperties(size=20),
                    color="red",
                    annotation_clip=True,
                    )
    for index in ovx["sell"]:
        ax.annotate('↓', xy=(xx[index], yy[index]),
                    fontproperties=FontProperties(size=20),
                    # arrowprops=dict(facecolor='green', shrink=0.05),
                    color="green",
                    annotation_clip=True,
                    )
    # ax.set_ylim(-2, 2)
    return plt


if __name__ == '__main__':
    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(5 * np.pi * t)
    o = Aux(s, t, {"buy": [11, 100], "sell": [200]})
    o.show()
