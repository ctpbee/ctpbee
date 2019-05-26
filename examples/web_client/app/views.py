from flask import Blueprint, url_for
from flask import request, render_template, redirect
from ctpbee import CtpBee

trade = Blueprint('trade', __name__, url_prefix="/trade", static_folder="/statics", template_folder="/templates")


@trade.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        info = request.values
        app = CtpBee(__name__)
        app.config.from_mapping(info)
        app.start()
        return redirect(url_for("personal_center"))
    return render_template("trade_login.html")


@trade.route("/send_order", methods=['GET', "POST"])
def send_order():
    """下单"""
    from ctpbee import send_order
    pass


@trade.route("/cancle_order", methods=['GET', "POST"])
def cancle_order():
    """下单"""
    from ctpbee import cancle_order
    pass


@trade.route("/close_position", methods=['GET', "POST"])
def close_position():
    """下单"""
    from ctpbee import send_order
    info = request.values
    pass


