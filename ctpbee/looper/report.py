"""
此模块是用来帮助ctpbee的回测来生成指定的策略报告，UI本身采用

"""
import os
import webbrowser
from jinja2 import Environment, PackageLoader, select_autoescape
from ctpbee import get_ctpbee_path
from datetime import datetime

env = Environment(
    loader=PackageLoader('ctpbee', 'looper/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template("looper.html")


def render_result(result, kline=None, strategy=[], account_data=None,cost_time=None, **kwargs):
    """
    渲染结果并写入到本地html文件， 并返回htmk文件地址
    """
    code_string = template.render(result=result, strategy=strategy, account_data=account_data, cost_time=cost_time, datetime=str(datetime.now()))
    file_path = kwargs.get("file_path", None)
    if not file_path:
        path = get_ctpbee_path() + "/looper"
        if not os.path.isdir(path):
            os.mkdir(path)
        file_path = path + "/" + str(datetime.now().strftime("%Y-%m-%d&%H:%M:%S")) + ".html"
    with open(file_path, "w") as f:
        f.write(code_string)
    if kwargs.get("auto_open", None):
        webbrowser.open(file_path)
    return file_path
