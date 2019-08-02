# this is the web client in here  you can use it to trade or read market fastly
from flask import Flask

from .ext import io
from .views import LoginView, MarketView, OrderView, IndexView, AccountView, OpenOrderView, LogoutView


def create_app():
    app = Flask(__name__, static_folder="./static", template_folder="./templates")
    app.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=['GET', "POST"])
    app.add_url_rule("/market", view_func=MarketView.as_view("market"), methods=['GET', "POST", "PUT"])
    app.add_url_rule("/order_request/symbol=<symbol>", view_func=OrderView.as_view("order_request"), methods=['GET'])
    app.add_url_rule("/index", view_func=IndexView.as_view("index"), methods=['GET'])
    app.add_url_rule("/account", view_func=AccountView.as_view("account"), methods=['GET'])
    app.add_url_rule("/order_solve", view_func=OpenOrderView.as_view("order_solve"), methods=['POST', 'DELETE'])
    app.add_url_rule("/logout", view_func=LogoutView.as_view('logout'), methods=['GET'])

    io.init_app(app)
    return app
