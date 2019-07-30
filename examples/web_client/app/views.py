from threading import Thread
from time import sleep

from flask import redirect, url_for
from flask import request, render_template
from flask.views import MethodView

from ctpbee import CtpBee, current_app
from ctpbee import helper
from .default_settings import DefaultSettings, true_response, false_response
from .ext import io, current_user

is_send = True


def login_required(f):
    """Checks whether user is logged in or raises error 401."""

    def decorator(*args, **kwargs):
        global current_user
        if not current_user:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorator


class AccountView(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template("account.html")


class LoginView(MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
        info = request.values
        app = CtpBee(info.get("username"), __name__)
        login_info = {
            "CONNECT_INFO": info,
            "INTERFACE": "ctp",
            "TD_FUNC": True,
            "MD_FUNC": True,
        }
        app.config.from_mapping(login_info)
        default = DefaultSettings("default_settings", app, io)
        app.start()
        sleep(1)
        if not app.td_login_status:
            return false_response(message="登录出现错误")

        def run(app: CtpBee):
            while True:
                app.query_position()
                sleep(1)
                app.query_account()
                sleep(1)

        p = Thread(target=run, args=(app,))
        p.start()

        global current_user
        current_user = info
        return true_response(message="登录成功")


class IndexView(MethodView):
    decorators = [login_required]

    def get(self):
        from .default_settings import contract_list
        global current_user
        global is_send
        if is_send:
            sleep(1)
            if len(contract_list) != 0:
                io.emit("contract", contract_list)
            is_send = False
        return render_template("index.html", username=current_user.get("userid"))


class MarketView(MethodView):
    decorators = [login_required]

    def post(self):
        symbol = request.values.get("symbol")
        try:
            current_app.subscribe(symbol)
            return true_response(message="订阅成功")
        except Exception:
            return false_response(message="订阅失败")

    def get(self):
        return render_template("market.html")


class OrderView(MethodView):
    decorators = [login_required]

    def get(self, symbol):
        return render_template("send_order.html", symbol=symbol)


class OpenOrderView(MethodView):
    decorators = [login_required]

    def post(self):
        """ 发单 """
        info = request.values.to_dict()

        print(info)
        local_symbol = info.get("local_symbol")
        direction = info.get("direction")
        offset = info.get("offset")
        type = info.get("type")
        price = info.get("price")
        volume = info.get("volume")
        exchange = info.get("exchange")
        req = helper.generate_order_req_by_str(symbol=local_symbol,
                                               exchange=exchange,
                                               direction=direction, offset=offset, volume=int(volume),
                                               price=float(price),
                                               type=type)
        print(req)
        try:
            current_app.send_order(req)
            return true_response(message="成功下单")
        except Exception as e:
            print(e)
            return false_response(message="下单失败")

    def delete(self):
        """ 撤单 """
        info = request.values
        local_symbol = info.get("local_symbol")
        order_id = info.get("order_id")
        exchange = info.get("exchange")
        req = helper.generate_cancle_req_by_str(symbol=local_symbol, exchange=exchange, order_id=order_id)
        try:
            current_app.cancle_order(req)
            return true_response(message="成功撤单")
        except Exception:
            return false_response(message="撤单失败")


class LogoutView(MethodView):
    decorators = [login_required]

    def get(self):
        global current_user
        current_user = None

