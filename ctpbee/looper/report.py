"""
此模块是用来帮助ctpbee的回测来生成指定的策略报告，UI本身采用

"""

import os
import webbrowser

from jinja2 import Environment, PackageLoader, select_autoescape

from ctpbee.func import get_ctpbee_path
from ctpbee.func import join_path

env = Environment(
    loader=PackageLoader("ctpbee", "looper/templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

main_template = env.get_template("looper.html")
trade_template = env.get_template("trade_record.html")


def render_result(
    result,
    kline=None,
    trades=None,
    datetimed=None,
    trade_data=None,
    strategy=[],
    position_data=None,
    account_data=None,
    net_pnl=None,
    cost_time=None,
    **kwargs
):
    """
    渲染结果并写入到本地html文件， 并返回html文件地址
    """
    """默认回测文件存放文件夹地址"""
    path = os.path.join(get_ctpbee_path(), "looper")
    time = str(datetimed).replace(" ", "_").replace(".", "_").replace(":", "_")
    filename = "{}_{}".format("_".join(strategy), time)
    abs_path = os.path.join(path, filename)
    datetimed = str(datetimed.strftime("%Y-%m-%d_%H_%M_%S"))
    code_string = main_template.render(
        result=result,
        strategy=strategy,
        account_data=account_data,
        net_pnl=net_pnl,
        cost_time=cost_time,
        datetime=datetimed,
        file_name=filename,
        abs_path=abs_path,
    )
    trade_code_string = trade_template.render(
        trade_data=trade_data, position_data=position_data
    )

    """ 回测主文件存放地址"""
    file_path = kwargs.get("file_path", None)

    """ 成交单文件存放地址 """
    trade_path = kwargs.get("trade_file_path", None)

    if not file_path:
        if not os.path.isdir(path):
            os.mkdir(path)

        file_path = join_path(path, filename + ".html")

    if not trade_path:
        trade_path = join_path(path, filename + "-trade.html")
    with open(file_path, "w", encoding="utf8") as f:
        f.write(code_string)
    with open(trade_path, "w", encoding="utf8") as f:
        f.write(trade_code_string)
    if kwargs.get("auto_open", None):
        webbrowser.open(file_path)
    return file_path
