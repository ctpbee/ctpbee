"""

面向用户的函数 ,提供极其便捷的体验

"""

import os
import platform
from datetime import time, datetime, timedelta, date
from inspect import isfunction
from multiprocessing import Process
from time import sleep
from typing import Text, Any, List

from ctpbee.constant import (
    OrderRequest,
    CancelRequest,
    Direction,
    Exchange,
    Offset,
    OrderType,
    AccountRegisterRequest,
    AccountBanlanceRequest,
    TransferRequest,
    TransferSerialRequest,
    MarketDataRequest,
)
from ctpbee.context import current_app
from ctpbee.context import get_app
from ctpbee.date import trade_dates
from ctpbee.exceptions import TraderError, MarketError
from ctpbee.constant import ToolRegisterType


def send_order(order_req: OrderRequest, app_name: str = "current_app"):
    """发单"""
    if app_name == "current_app":
        app = current_app
    else:
        app = get_app(app_name)
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    return app.trader.send_order(order_req)


def cancel_order(cancel_req: CancelRequest, app_name: str = "current_app"):
    """撤单"""
    if app_name == "current_app":
        app = current_app
    else:
        app = get_app(app_name)
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    app.trader.cancel_order(cancel_req)


def subscribe(symbol: Text, app_name: str = "current_app") -> None:
    """订阅"""
    if app_name == "current_app":
        app = current_app
    else:
        app = get_app(app_name)
    if not app.config.get("MD_FUNC"):
        raise MarketError(message="行情功能未开启, 无法进行订阅")
    app.market.subscribe(symbol)


def query_func(type: Text, app_name: str = "current_app") -> None:
    """查询持仓或者账户"""
    if app_name == "current_app":
        app = current_app
    else:
        app = get_app(app_name)
    if not app.config.get("TD_FUNC"):
        raise TraderError(message="交易功能未开启", args=("交易功能未开启",))
    if type == "position":
        app.trader.query_position()
    if type == "account":
        app.trader.query_account()


class Helper(object):
    """
    工具函数 帮助你快速构建查询请求
    提供快速生成对象的方法, 参见函数名。
    """

    direction_map = {
        "LONG": Direction.LONG,
        "SHORT": Direction.SHORT,
    }
    exchange_map = {
        "SHFE": Exchange.SHFE,
        "INE": Exchange.INE,
        "CZCE": Exchange.CZCE,
        "CFFEX": Exchange.CFFEX,
        "DCE": Exchange.DCE,
        "CTP": Exchange.CTP,
    }

    offset_map = {
        "CLOSE": Offset.CLOSE,
        "OPEN": Offset.OPEN,
        "CLOSETODAY": Offset.CLOSETODAY,
        "CLOSEYESTERDAY": Offset.CLOSEYESTERDAY,
    }

    price_type_map = {
        "MARKET": OrderType.MARKET,
        "STOP": OrderType.STOP,
        "FAK": OrderType.FAK,
        "LIMIT": OrderType.LIMIT,
        "FOK": OrderType.FOK,
    }

    @classmethod
    def generate_order_req_by_str(
        cls,
        symbol: str,
        exchange: str,
        direction: str,
        offset: str,
        type: str,
        volume,
        price: float,
    ):
        """手动构造发单请求"""
        if "." in symbol:
            symbol = symbol.split(".")[0]

        return OrderRequest(
            exchange=cls.exchange_map.get(exchange.upper()),
            symbol=symbol,
            direction=cls.direction_map.get(direction.upper()),
            offset=cls.offset_map.get(offset.upper()),
            type=cls.price_type_map.get(type.upper()),
            volume=volume,
            price=price,
        )

    @classmethod
    def generate_order_req_by_var(
        cls,
        symbol: str,
        exchange: Exchange,
        direction: Direction,
        offset: Offset,
        type: OrderType,
        volume,
        price: float,
    ):
        if "." in symbol:
            symbol = symbol.split(".")[0]
        return OrderRequest(
            symbol=symbol,
            exchange=exchange,
            direction=direction,
            offset=offset,
            type=type,
            volume=volume,
            price=price,
        )

    @classmethod
    def generate_cancel_req_by_str(cls, symbol: str, exchange: str, order_id: str):
        if "." in symbol:
            symbol = symbol.split(".")[0]
        return CancelRequest(
            symbol=symbol, exchange=cls.exchange_map.get(exchange), order_id=order_id
        )

    @classmethod
    def generate_cancel_req_by_var(cls, symbol: str, exchange: Exchange, order_id: str):
        if "." in symbol:
            symbol = symbol.split(".")[0]
        return CancelRequest(symbol=symbol, exchange=exchange, order_id=order_id)

    @classmethod
    def generate_ac_register_req(cls, bank_id, currency_id="CNY"):

        return AccountRegisterRequest(bank_id=bank_id, currency_id=currency_id)

    @classmethod
    def generate_ac_banlance_req(
        cls, bank_id, bank_account, bank_password, currency_id="CNY"
    ):
        return AccountBanlanceRequest(
            bank_id=bank_id,
            bank_account=bank_account,
            bank_password=bank_password,
            currency_id=currency_id,
        )

    @classmethod
    def generate_transfer_request(
        cls, bank_id, bank_account, bank_password, trade_account, currency_id="CNY"
    ):
        return TransferRequest(
            bank_id=bank_id,
            bank_account=bank_account,
            band_password=bank_password,
            currency_id=currency_id,
            trade_account=trade_account,
        )

    @classmethod
    def generate_transfer_serial_req(cls, bank_id, currency_id="CNY"):
        return TransferSerialRequest(bank_id=bank_id, currency_id=currency_id)

    @classmethod
    def generate_market_request(cls, symbol: str, exchange: Any):
        """生成市场数据请求"""
        if "." in symbol:
            symbol = symbol.split(".")[1]
        if isinstance(exchange, Exchange):
            exchange = exchange.value
        return MarketDataRequest(symbol=symbol, exchange=exchange)


helper = Helper()

DAY_START = time(9, 0)  # 日盘启动和停止时间
DAY_END = time(15, 5)
NIGHT_START = time(21, 0)  # 夜盘启动和停止时间
NIGHT_END = time(2, 35)


def get_current_trade_day(timing: datetime) -> None or date:
    current_string = str(timing.date())

    last_day = str((timing + timedelta(days=-1)).date())

    if timing.time() <= DAY_END and current_string in trade_dates:
        return current_string
    if timing.time() > DAY_END and current_string in trade_dates:
        index = trade_dates.index(current_string)
        return trade_dates[index + 1]

    if (
        current_string not in trade_dates
        and last_day in trade_dates
        and timing.time() < NIGHT_END
    ):
        """如果是周六凌晨2：30以前, 当前不为交易日 且前一日为交易日 返回下一个交易日"""
        index = trade_dates.index(last_day)
        return trade_dates[index + 1]
    return None


class Hickey(object):
    """
    Hickey任务调度机制

    主要为了完成自动拉起程序
    """

    from datetime import time

    DAY_START = time(9, 0)  # 日盘启动和停止时间
    DAY_END = time(15, 0)
    NIGHT_START = time(21, 0)  # 夜盘启动和停止时间
    NIGHT_END = time(2, 30)

    TIME_MAPPING = {
        "dy_st": "DAY_START",
        "dy_ed": "DAY_END",
        "ng_st": "NIGHT_START",
        "ng_ed": "NIGHT_END",
    }

    def __init__(self):
        self.names = []
        from datetime import time

        self.open_trading = {
            "ctp": {"DAY_START": time(9, 0), "NIGHT_START": time(21, 0)}
        }

    def auth_time(self, current: datetime):
        current_string = str(current.date())

        last_day = str((current + timedelta(days=-1)).date())
        """
        如果前一天是交易日, 今天不是 那么交易到今晚晚上2点：30
        
        如果前一天不是交易日,今天是  那么早盘前 不启动 
        
        如果前一天不是交易日, 今天也不是交易日 那么不启动 
        """
        if (
            (
                last_day in trade_dates
                and current_string not in trade_dates
                and current.time() > self.NIGHT_END
            )
            or (
                last_day not in trade_dates
                and current_string in trade_dates
                and current.time() < self.DAY_START
            )
            or (last_day not in trade_dates and current_string not in trade_dates)
        ):
            return False

        if self.DAY_END >= current.time() >= self.DAY_START:
            return True
        if current.time() >= self.NIGHT_START:
            return True
        if current.time() <= self.NIGHT_END:
            return True
        return False

    def run_all_app(self, app_func):
        from ctpbee.app import CtpBee

        apps = app_func()
        if isinstance(apps, CtpBee):
            if not apps.active:
                apps.start()
            else:
                raise ValueError("你选择的app已经在函数中启动")

        elif isinstance(apps, List) and isinstance(apps[0], CtpBee):
            for app in apps:
                if app.name not in self.names and not app.active:
                    app.start()
                    self.names.append(app.name)
                else:
                    continue
        else:
            raise ValueError("你传入的创建的func无法创建CtpBee变量, 请检查返回值")

    @staticmethod
    def add_seconds(tm, seconds, direction=False):
        full_date = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        if not direction:
            full_date = full_date - timedelta(seconds=seconds)
        else:
            full_date = full_date + timedelta(seconds=seconds)
        return full_date.time()

    def start_all(self, app_func, info=True, interface="ctp", in_front=300):
        """
        开始进程管理
        * app_func: 创建app的函数
        * interface: 接口名字
        * in_front: 相较于开盘提前多少秒进行运行登陆.单位: seconds
        """
        print(
            "Hi, ctpbee 7*24 Manager has been started!\nWarning: program will automatic start at trade time,"
            "we recommend you to use pickle to save and reload variables....\n"
            "Hope you will have a  good profit ^_^"
        )
        if not isfunction(app_func):
            raise TypeError(
                f"请检查你传入的app_func是否是创建app的函数,  而不是{type(app_func)}"
            )

        for i, v in self.open_trading[interface].items():
            setattr(self, i, self.add_seconds(getattr(self, i), in_front))
        p = None
        while True:
            current = datetime.now()

            status = self.auth_time(current)

            if info:
                print(
                    f"{current.strftime('%Y-%m-%d %H:%M:%S')} ctpbee manager running ---> ^_^ "
                )

            if p is None and status:
                p = Process(target=self.run_all_app, args=(app_func,))
                p.start()
                print("===> program start successful")
            if not status and p is not None:
                print("===> 非交易时间, 即将查杀子进程")
                if platform.uname().system == "Windows":
                    os.popen("taskkill /F /pid " + str(p.pid))
                else:
                    import signal

                    os.kill(p.pid, signal.SIGKILL)

                p = None
            sleep(30)

    def update_time(self, timed: time, flag: str):
        """
            此函数被用来修改更新启动时间或者关闭时间

            :param timed:
            :param flag:需要修改的字段 仅仅
                      "dy_st": "白天开始",
                     "dy_ed": "白天结束",
                    "ng_st": "晚上开始",
                   "ng_ed": "晚上结束"
        }
            :return: None
        """
        if flag not in self.TIME_MAPPING.keys():
            raise ValueError(
                f"注意你的flag是不被接受的,我们仅仅支持\n "
                f"{str(list(self.TIME_MAPPING.keys()))}四种"
            )
        if not isinstance(timed, time):
            raise ValueError(f"timed错误的数据类型,期望 time, 当前{str(type(timed))}")

        setattr(self, self.TIME_MAPPING[flag], timed)

    def __repr__(self):
        return "ctpbee 7*24 manager ^_^"


hickey = Hickey()


def join_path(rootdir, *args):
    """路径添加器"""
    for i in args:
        rootdir = os.path.join(rootdir, i)
    return rootdir


def get_ctpbee_path():
    """
    获取ctpbee的路径默认路径
    """
    system_ = platform.system()
    if system_ == "Linux":
        home_path = os.environ["HOME"]
    elif system_ == "Windows":
        home_path = os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"]
    elif system_ == "Darwin":
        home_path = os.environ["HOME"]
    else:
        raise Exception("ctpbee does not know the system!")
    ctpbee_path = os.path.join(home_path, ".ctpbee")
    if not os.path.exists(ctpbee_path):
        os.mkdir(ctpbee_path)
    return ctpbee_path


def tool_register(tool_type: ToolRegisterType):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            ret = func(self, *args, **kwargs)
            for take in self._linked[tool_type]:
                take(ret)
            return ret

        return wrapper

    return decorator
