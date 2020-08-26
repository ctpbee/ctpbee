import warnings
from collections import defaultdict
from copy import deepcopy
from datetime import datetime

from ctpbee.data_handle import generator
from ctpbee.data_handle.local_position import LocalPositionManager
from ctpbee.constant import Event, TickData
from ctpbee.helpers import helper_call

import ctpbee.signals as signal


class Recorder(object):
    """
    data center
    """

    def __init__(self, app):
        """"""
        self.bar = {}
        self.ticks = {}
        self.orders = {}
        self.trades = {}
        self.positions = {}
        self.account = None
        self.contracts = {}
        self.logs = {}
        self.errors = []
        self.generators = {}
        self.active_orders = {}
        self.local_contract_price_mapping = {}
        self.app = app
        self.register_event()
        self.position_manager = LocalPositionManager(app=self.app)
        self.main_contract_mapping = defaultdict(list)

    @staticmethod
    def get_local_time():
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_func(self, name):
        return getattr(self, f"process_{name}_event")

    def register_event(self):
        """ bind process function """

        def connect(data):
            name = data[0]
            signal = data[1]
            temp_sig = getattr(signal, f"{name}_signal")
            temp_sig.connect(self.get_func(name=name), weak=False)
            return name

        def generate_params(data, signal):
            temp = []
            for x in data:
                temp.append((x, signal))
            return temp

        x = list(map(connect, generate_params(signal.common_signals.event, signal.common_signals)))
        p = list(map(connect, generate_params(self.app.app_signal.event, self.app.app_signal)))

    def process_timer_event(self, event):
        for x in self.app._extensions.values():
            x()

    def process_init_event(self, event):
        """ 处理初始化完成事件 """
        if event.data:
            self.app.init_finished = True
        for x in self.app._extensions.values():
            x(deepcopy(event))

    def process_warning_event(self, event):
        self.app.logger.warning(event.data)

    def process_last_event(self, event):
        """ 处理合约的最新行情数据 """
        data = event.data
        self.local_contract_price_mapping[data.local_symbol] = data.last_price
        # 过滤掉数字 取中文做key
        key = "".join([x for x in data.local_symbol if not x.isdigit()])
        self.main_contract_mapping[key.upper()].append(data)

    def process_error_event(self, event: Event):
        self.errors.append({"time": self.get_local_time(), "data": event.data})
        self.app.logger.error(event.data)

    def process_log_event(self, event: Event):
        self.logs[self.get_local_time()] = event.data
        if self.app.config.get("LOG_OUTPUT"):
            self.app.logger.info(event.data)

    @helper_call
    def process_bar_event(self, event: Event):
        bar = event.data
        local = self.bar.get(bar.local_symbol)
        if local is None:
            self.bar[bar.local_symbol] = {bar.interval: []}
        else:
            if self.bar[bar.local_symbol].get(bar.interval) is None:
                self.bar[bar.local_symbol] = {bar.interval: []}
        self.bar[bar.local_symbol][bar.interval].append(bar)

    @helper_call
    def process_tick_event(self, event: Event):
        tick:TickData = event.data
        self.ticks[tick.local_symbol] = tick
        self.position_manager.update_tick(tick, tick.pre_settlement_price)
        # 生成datetime对象
        if not tick.datetime:
            if '.' in tick.time:
                tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S.%f')
            else:
                tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S')
        bm = self.generators.get(tick.local_symbol, None)
        if bm:
            bm.update_tick(tick)
        if not bm:
            self.generators[tick.local_symbol] = generator(self.app)
            self.generators[tick.local_symbol].update_tick(tick)

    @helper_call
    def process_order_event(self, event: Event):
        """"""
        order = event.data
        self.orders[order.local_order_id] = order
        # If order is active, then update data in dict.
        if order._is_active():
            self.active_orders[order.local_order_id] = order
        # Otherwise, pop inactive order from in dict
        elif order.local_order_id in self.active_orders:
            self.active_orders.pop(order.local_order_id)
        self.position_manager.update_order(order)

    @helper_call
    def process_trade_event(self, event: Event):
        """"""
        trade = event.data
        self.trades[trade.local_trade_id] = trade
        self.position_manager.update_trade(trade)
        for value in self.app._extensions.values():
            if self.app.config['INSTRUMENT_INDEPEND']:
                if len(value.instrument_set) == 0:
                    warnings.warn("你当前开启策略对应订阅行情功能, 当前策略的订阅行情数量为0，请确保你的订阅变量是否为instrument_set，以及订阅具体代码")
                if event.data.local_symbol in value.instrument_set:
                    value(deepcopy(event))
            else:
                value(deepcopy(event))

    @helper_call
    def process_position_event(self, event: Event):
        """"""
        position = event.data
        self.positions[position.local_position_id] = position
        self.position_manager.update_position(position)
        for value in self.app._extensions.values():
            if self.app.config['INSTRUMENT_INDEPEND']:
                if len(value.instrument_set) == 0:
                    warnings.warn("你当前开启策略对应订阅行情功能, 当前策略的订阅行情数量为0，请确保你的订阅变量是否为instrument_set，以及订阅具体代码")
                if event.data.local_symbol in value.instrument_set:
                    value(deepcopy(event))
            else:
                value(deepcopy(event))

    def process_account_event(self, event: Event):
        """"""
        account = event.data
        self.account = account

        for value in self.app._extensions.values():
            value(deepcopy(event))

    def process_contract_event(self, event: Event):
        """"""
        contract = event.data
        self.contracts[contract.local_symbol] = contract
        for value in self.app._extensions.values():
            value(deepcopy(event))

    def get_bar(self, local_symbol):
        return self.bar.get(local_symbol, None)

    def get_all_bar(self):
        return self.bar

    def get_tick(self, local_symbol):
        return self.ticks.get(local_symbol, None)

    def get_order(self, local_order_id):
        return self.orders.get(local_order_id, None)

    def get_trade(self, local_trade_id):
        return self.trades.get(local_trade_id, None)

    def get_position(self, local_position_id):
        return self.positions.get(local_position_id, None)

    def get_account(self):
        return self.account

    def get_contract(self, local_symbol):
        return self.contracts.get(local_symbol, None)

    def get_all_ticks(self):
        """
        Get all tick data.
        """
        return list(self.ticks.values())

    def get_all_orders(self):
        """
        Get all order data.
        """
        return list(self.orders.values())

    def get_all_trades(self):
        """
        Get all trade data.
        """
        return list(self.trades.values())

    def get_all_positions(self):
        """
        Get all position data.
        """
        return self.position_manager.get_all_positions()

    def get_errors(self):
        return self.errors

    def get_new_error(self):
        return self.errors[-1]

    def get_all_contracts(self):
        """
        Get all contract data.
        """
        return list(self.contracts.values())

    def get_all_active_orders(self, local_symbol: str = ""):
        if not local_symbol:
            return list(self.active_orders.values())
        else:
            active_orders = [
                order
                for order in self.active_orders.values()
                if order.local_symbol == local_symbol
            ]
            return active_orders

    @property
    def main_contract_list(self):
        """ 返回主力合约列表 """
        result = []
        for _ in self.main_contract_mapping.values():
            x = sorted(_, key=lambda x: x.open_interest, reverse=True)[0]
            result.append(x.local_symbol)
        return result

    def get_contract_last_price(self, local_symbol):
        """ 获取合约的最新价格 """
        return self.local_contract_price_mapping.get(local_symbol)

    def get_main_contract_by_code(self, code: str):
        """ 根据code取相应的主力合约 """
        d = self.main_contract_mapping.get(code.upper(), None)
        if not d:
            return None
        else:
            now = sorted(d, key=lambda x: x.open_interest, reverse=True)[0]
            pre = sorted(d, key=lambda x: x.pre_open_interest, reverse=True)[0]
            if pre.local_symbol == now.local_symbol:
                return pre
            else:
                return now

    def clear_all(self):
        """
        为了避免数据越来越大，需要清空数据
        :return:
        """

        self.ticks.clear()
        self.orders.clear()
        self.trades.clear()
        self.positions.clear()
        self.contracts.clear()
        self.errors.clear()
        self.generators.clear()
        self.active_orders.clear()
