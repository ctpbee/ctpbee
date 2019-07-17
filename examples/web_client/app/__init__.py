# this is the web client in here  you can use it to trade or read market fastly
from flask import Flask

from .ext import io
from .views import LoginView, MarketView, OrderView, IndexView,AccountView


def create_app():
    app = Flask(__name__, static_folder="./static", template_folder="./templates")
    app.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=['GET', "POST"])
    app.add_url_rule("/market", view_func=MarketView.as_view("market"), methods=['GET', "POST"])
    app.add_url_rule("/order_request", view_func=OrderView.as_view("order_request"), methods=['DELETE', "POST"])
    app.add_url_rule("/index", view_func=IndexView.as_view("index"), methods=['GET'])
    app.add_url_rule("/account", view_func=AccountView.as_view("account"), methods=['GET'])
    io.init_app(app)
    return app
