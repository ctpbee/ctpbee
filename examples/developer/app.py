
from ctpbee import CtpBee

def create_app():
    app = CtpBee("ctpbee", __name__)

    app.config.from_mapping()