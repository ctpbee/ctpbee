from collections import defaultdict

import ctpbee.signals as signal
from ctpbee.constant import Event, TickData, BarData
from ctpbee.data_handle.local_position import LocalPositionManager
from ctpbee.helpers import call


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
        self.active_orders = {}
        self.local_contract_price_mapping = {}
        self.app = app
        self.register_event()
        self.position_manager = LocalPositionManager(app=self.app)
        self.main_contract_mapping = defaultdict(list)

        self.__common_sig_name = None
        self.__app_sig_name = None

    @staticmethod
    def get_local_time():
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_func(self, name):
        return getattr(self, f"process_{name}_event")

    def register_event(self):
        """bind process function"""

        def connect(data):
            name = data[0]
            sgl = data[1]
            temp_sig = getattr(sgl, f"{name}_signal")
            temp_sig.connect(self.get_func(name=name), weak=False)
            return name

        def generate_params(data, ctl):
            temp = []
            for x in data:
                temp.append((x, ctl))
            return temp

        self.__common_sig_name = list(
            map(
                connect,
                generate_params(signal.common_signals.event, signal.common_signals),
            )
        )
        self.__app_sig_name = list(
            map(
                connect, generate_params(self.app.app_signal.event, self.app.app_signal)
            )
        )

    def process_timer_event(self, _event):
        for x in self.app._extensions.values():
            x.on_realtime()

    def process_init_event(self, event):
        """处理初始化完成事件"""
        if event.data:
            self.app.init_finished = True
        for value in self.app._extensions.values():
            value(event)

    def process_warning_event(self, event):
        self.app.logger.warning(event.data)

    # process_last_event 方法已被整合到 process_tick_event 中，避免重复处理
    def process_last_event(self, event):
        pass

    def process_error_event(self, event: Event):
        self.errors.append({"time": self.get_local_time(), "data": event.data})
        self.app.logger.error(event.data)

    def process_log_event(self, event: Event):
        self.logs[self.get_local_time()] = event.data
        if self.app.config.get("LOG_OUTPUT"):
            self.app.logger.info(event.data)

    @call
    def process_tick_event(self, event: Event):
        tick: TickData = event.data
        local_symbol = tick.local_symbol

        # 更新行情数据
        self.ticks[local_symbol] = tick

        # 更新合约最新价格映射
        self.local_contract_price_mapping[local_symbol] = tick.last_price

        # 过滤掉数字，取中文做key
        key = "".join([x for x in local_symbol if not x.isdigit()]).upper()
        self.main_contract_mapping[key].append(tick)

        # 更新持仓信息
        self.position_manager.update_tick(tick, tick.pre_settlement_price)

        # 调用工具的回调方法
        tools = self.app.tools.values()
        if tools:
            for tool in tools:
                tool.on_tick(tick)

    @call
    def process_bar_event(self, event: Event):
        bar: BarData = event.data
        self.bar[bar.local_symbol] = bar
        for tool in self.app.tools.values():
            tool.on_bar(bar)

    @call
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

        for tool in self.app.tools.values():
            tool.on_order(order)

    @call
    def process_trade_event(self, event: Event):
        """"""
        trade = event.data
        self.trades[trade.local_trade_id] = trade
        self.position_manager.update_trade(trade)
        for tool in self.app.tools.values():
            tool.on_trade(trade)

    @call
    def process_position_event(self, event: Event):
        """"""
        position = event.data
        self.positions[position.local_position_id] = position
        self.position_manager.update_position(position)

    def process_account_event(self, event: Event):
        """"""
        account = event.data
        self.account = account

        for value in self.app._extensions.values():
            value(event)

    def process_contract_event(self, event: Event):
        """"""
        contract = event.data
        self.contracts[contract.local_symbol] = contract
        for value in self.app._extensions.values():
            value(event)

    def get_last_price(self, local_symbol) -> None or float:
        tick = self.ticks.get(local_symbol)
        return tick.last_price if tick is not None else None

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

    def get_all_positions(self, obj=False):
        """
        Get all position data.
        """
        return self.position_manager.get_all_positions(obj=obj)

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
        """返回主力合约列表"""
        result = []
        for _ in self.main_contract_mapping.values():
            x = sorted(_, key=lambda _x: _x.open_interest, reverse=True)[0]
            result.append(x.local_symbol)
        return result

    def get_contract_last_price(self, local_symbol):
        """获取合约的最新价格"""
        return self.local_contract_price_mapping.get(local_symbol)

    def get_main_contract_by_code(self, code: str):
        """根据code取相应的主力合约"""
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

    @property
    def order_amount(self):
        """
        返回当日报单总数
        """
        return len(self.orders)

    def clear_all(self):
        """
        为了避免数据越来越大,需要清空数据
        :return:
        """

        self.ticks.clear()
        self.orders.clear()
        self.trades.clear()
        self.positions.clear()
        self.contracts.clear()
        self.errors.clear()
        self.active_orders.clear()
