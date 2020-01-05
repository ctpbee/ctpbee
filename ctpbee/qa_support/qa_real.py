"""
this package will be developer in the next version
"""
from ctpbee.qa_support.abstract import DataSupport

try:
    import QUANTAXIS as QA
except ImportError:
    raise EnvironmentError("请安装ctpbee[QA_SUPPORT]版本，安装详见: https://docs.ctpbee.com/install\n"
                           "please install ctpbee[QA_SUPPORT] version. see the url before")


class QARealTimeCollector(DataSupport):
    """
    需要同时支持QA旧版本和新版本
    """
