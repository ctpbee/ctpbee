# this is the web client in here  you can use it to trade or read market fastly
from flask import Flask

from .views import trade


def create_app():
    app = Flask(__name__)

    app.register_blueprint(trade)

    return app
