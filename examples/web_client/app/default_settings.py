import time

from flask import make_response
from flask_socketio import SocketIO

from ctpbee import CtpbeeApi
from ctpbee.constant import LogData, AccountData, ContractData, BarData, OrderData, PositionData, TickData, SharedData, \
    TradeData

#  订阅的全局变量
contract_list = []


class DefaultSettings(CtpbeeApi):

    def __init__(self, name, app, socket_io: SocketIO):
        super().__init__(name, app)
        self.io = socket_io

    def on_log(self, log: LogData):
        data = {
            "type": "log",
            "data": log
        }
        self.io.emit('log', data)

    def on_account(self, account: AccountData) -> None:
        data = {
            "type": "account",
            "data": account._to_dict()
        }

        self.io.emit('account', data)

    def on_contract(self, contract: ContractData):
        global contract_list
        contract_list.append(contract.symbol)

    def on_bar(self, bar: BarData) -> None:
        bar.datetime = str(bar.datetime)
        data = {
            "type": "bar",
            "data": bar._to_dict()
        }
        self.io.emit('bar', data)

    def on_order(self, order: OrderData) -> None:
        # 更新活跃报单
        active_orders = []
        for order in self.app.recorder.get_all_active_orders(order.local_symbol):
            active_orders.append(order._to_dict())
        data = {
            "type": "active_order",
            "data": active_orders
        }

        self.io.emit("active_order", data)
        orders = []
        for order in self.app.recorder.get_all_orders():
            orders.append(order._to_dict())
        data = {
            "type": "order",
            "data": orders
        }
        self.io.emit("order", data)

    def on_position(self, position: PositionData) -> None:
        data = {
            "type": "position",
            "data": self.app.recorder.get_all_positions()
        }
        self.io.emit("position", data)

    def on_tick(self, tick: TickData) -> None:
        tick.datetime = str(tick.datetime)
        data = {
            "type": "tick",
            "data": tick._to_dict()
        }
        self.io.emit("tick", data)
        data = {
            "type": "position",
            "data": self.app.recorder.get_all_positions()
        }
        self.io.emit("position", data)
        # 更新持仓数据
        bars = []

        # 获取当前bars
        current_bar = self.app.recorder.get_bar(tick.local_symbol)
        if current_bar is not None:
            value = current_bar.get(1)
            for single_bar in value:
                timeArray = time.strptime(str(single_bar.datetime), "%Y-%m-%d %H:%M:%S")
                # 转换成时间戳
                timestamp = round(time.mktime(timeArray)*1000)
                bars.append([timestamp, single_bar.open_price, single_bar.high_price, single_bar.low_price,
                             single_bar.close_price, single_bar.volume])

        tick = self.app.recorder.get_tick(tick.local_symbol)
        update_result = {
            "success": True,
            "data": {
                "lines": bars,
                "depths": {
                    "asks": [
                        [
                            tick.ask_price_1,
                            tick.ask_volume_1
                        ]
                    ],
                    "bids": [
                        [
                            tick.bid_price_1,
                            tick.bid_volume_1
                        ]
                    ]
                }
            }
        }
        import os
        with open(f"{os.path.dirname(__file__)}/static/json/{tick.symbol}.json", "w+") as f:
            from json import dump
            dump(update_result, f)

        self.io.emit("update_all", update_result)

    def on_shared(self, shared: SharedData) -> None:
        shared.datetime = str(shared.datetime)
        data = {
            "type": "shared",
            "data": shared._to_dict()
        }
        self.io.emit('shared', data)

    def on_trade(self, trade: TradeData) -> None:
        trades = []
        for trade in self.app.recorder.get_all_trades():
            trades.append(trade._to_dict())
        data = {
            "type": "trade",
            "data": trades
        }
        self.io.emit('trade', data)


def true_response(data="", message="操作成功执行"):
    true_response = {
        "result": "success",
        "data.json": data,
        "message": message
    }
    return make_response(true_response)


def false_response(data="", message="出现错误, 请检查"):
    false_response = {
        "result": "error",
        "data.json": data,
        "message": message
    }
    return make_response(false_response)


def warning_response(data="", message="警告"):
    warning_response = {
        "result": "warning",
        "data.json": data,
        "message": message
    }
    return make_response(warning_response)
