# this is the web client in here  you can use it to trade or read market fastly
from flask import Flask

from .views import trade
from .ext import io


def create_app():
    app = Flask(__name__)
    app.register_blueprint(trade)
    io.init_app(app)
    return app
