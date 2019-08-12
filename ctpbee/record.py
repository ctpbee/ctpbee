from copy import deepcopy
from datetime import datetime

from ctpbee.constant import EVENT_TICK, EVENT_ORDER, EVENT_TRADE, EVENT_POSITION, EVENT_ACCOUNT, \
    EVENT_CONTRACT, EVENT_BAR, EVENT_LOG, EVENT_ERROR, EVENT_SHARED
from ctpbee.data_handle import generator
from ctpbee.data_handle.local_position import LocalPositionManager
from ctpbee.event_engine import Event


class Recorder(object):
    """
    data center
    """

    def __init__(self, app, event_engine):
        """"""
        self.bar = {}
        self.ticks = {}
        self.orders = {}
        self.trades = {}
        self.positions = {}
        self.accounts = {}
        self.contracts = {}
        self.logs = {}
        self.errors = []
        self.shared = {}
        self.generators = {}
        self.active_orders = {}
        self.event_engine = event_engine
        self.register_event()

        self.app = app
        self.position_manager = LocalPositionManager(app=self.app)

    @staticmethod
    def get_local_time():
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def register_event(self):
        """bind process function"""
        self.event_engine.register(EVENT_TICK, self.process_tick_event)
        self.event_engine.register(EVENT_ORDER, self.process_order_event)
        self.event_engine.register(EVENT_TRADE, self.process_trade_event)
        self.event_engine.register(EVENT_POSITION, self.process_position_event)
        self.event_engine.register(EVENT_ACCOUNT, self.process_account_event)
        self.event_engine.register(EVENT_CONTRACT, self.process_contract_event)
        self.event_engine.register(EVENT_BAR, self.process_bar_event)
        self.event_engine.register(EVENT_LOG, self.process_log_event)
        self.event_engine.register(EVENT_ERROR, self.process_error_event)
        self.event_engine.register(EVENT_SHARED, self.process_shared_event)

    def process_shared_event(self, event):
        if self.shared.get(event.data.local_symbol, None) is not None:
            self.shared[event.data.local_symbol].append(event.data)
        else:
            self.shared[event.data.local_symbol] = []
        for value in self.app.extensions.values():
            value(deepcopy(event))

    def process_error_event(self, event: Event):
        self.errors.append({"time": self.get_local_time(), "data": event.data})
        print(self.get_local_time() + ": ", event.data)

    def process_log_event(self, event: Event):
        self.logs[self.get_local_time()] = event.data
        if self.app.config.get("LOG_OUTPUT"):
            print(self.get_local_time() + ": ", event.data)
        for value in self.app.extensions.values():
            value(deepcopy(event))

    def process_bar_event(self, event: Event):
        bar = event.data
        local = self.bar.get(bar.local_symbol)
        if local is None:
            self.bar[bar.local_symbol] = {bar.interval: []}
        else:
            if self.bar[bar.local_symbol].get(bar.interval) is None:
                self.bar[bar.local_symbol] = {bar.interval: []}
        self.bar[bar.local_symbol][bar.interval].append(bar)

        for value in self.app.extensions.values():
            value(deepcopy(event))

    def process_tick_event(self, event: Event):
        """"""
        tick = event.data
        self.ticks[tick.local_symbol] = tick
        symbol = tick.symbol
        self.position_manager.update_tick(tick)
        # 生成datetime对象
        if not tick.datetime:
            if '.' in tick.time:
                tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S.%f')
            else:
                tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S')
        bm = self.generators.get(symbol, None)
        if bm:
            bm.update_tick(tick)
        if not bm:
            self.generators[symbol] = generator(self.event_engine)

        for value in self.app.extensions.values():
            value(deepcopy(event))

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
        for value in self.app.extensions.values():
            value(deepcopy(event))

    def process_trade_event(self, event: Event):
        """"""
        trade = event.data
        self.trades[trade.local_trade_id] = trade

        self.position_manager.update_trade(trade)
        for value in self.app.extensions.values():
            value(deepcopy(event))

    def process_position_event(self, event: Event):
        """"""
        position = event.data
        self.positions[position.local_position_id] = position
        # 本地实时计算 --> todo :优化
        self.position_manager.update_position(position)
        for value in self.app.extensions.values():
            value(deepcopy(event))

    def process_account_event(self, event: Event):
        """"""
        account = event.data
        self.accounts[account.local_account_id] = account
        for value in self.app.extensions.values():
            value(deepcopy(event))

    def process_contract_event(self, event: Event):
        """"""
        contract = event.data
        self.contracts[contract.local_symbol] = contract
        for value in self.app.extensions.values():
            value(deepcopy(event))

    def get_shared(self, symbol):
        return self.shared.get(symbol, None)

    def get_all_shared(self):
        return self.shared

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

    def get_account(self, local_account_id):
        return self.accounts.get(local_account_id, None)

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
        return list(self.positions.values())
        # return self.position_manager.get_all_positions()

    def get_errors(self):
        return self.errors

    def get_new_error(self):
        return self.errors[-1]

    def get_all_accounts(self):
        """
        Get all account data.
        """
        return list(self.accounts.values())

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


class AsyncRecorder(object):
    """
    data center
    """

    def __init__(self, app, event_engine):
        """"""
        self.bar = {}
        self.ticks = {}
        self.orders = {}
        self.trades = {}
        self.positions = {}
        self.accounts = {}
        self.contracts = {}
        self.logs = {}
        self.errors = []
        self.shared = {}
        self.generators = {}
        self.active_orders = {}
        self.event_engine = event_engine
        self.register_event()

        self.app = app
        self.position_manager = LocalPositionManager(app=self.app)

    @staticmethod
    def get_local_time():
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def register_event(self):
        """bind process function"""
        self.event_engine.register(EVENT_TICK, self.process_tick_event)
        self.event_engine.register(EVENT_ORDER, self.process_order_event)
        self.event_engine.register(EVENT_TRADE, self.process_trade_event)
        self.event_engine.register(EVENT_POSITION, self.process_position_event)
        self.event_engine.register(EVENT_ACCOUNT, self.process_account_event)
        self.event_engine.register(EVENT_CONTRACT, self.process_contract_event)
        self.event_engine.register(EVENT_BAR, self.process_bar_event)
        self.event_engine.register(EVENT_LOG, self.process_log_event)
        self.event_engine.register(EVENT_ERROR, self.process_error_event)
        self.event_engine.register(EVENT_SHARED, self.process_shared_event)

    async def process_shared_event(self, event):
        if self.shared.get(event.data.local_symbol, None) is not None:
            self.shared[event.data.local_symbol].append(event.data)
        else:
            self.shared[event.data.local_symbol] = []
        for value in self.app.extensions.values():
            await value(deepcopy(event))

    async def process_error_event(self, event: Event):
        self.errors.append({"time": self.get_local_time(), "data": event.data})
        print(self.get_local_time() + ": ", event.data)

    async def process_log_event(self, event: Event):
        self.logs[self.get_local_time()] = event.data
        if self.app.config.get("LOG_OUTPUT"):
            print(self.get_local_time() + ": ", event.data)
        for value in self.app.extensions.values():
            await value(deepcopy(event))

    async def process_bar_event(self, event: Event):
        bar = event.data
        local = self.bar.get(bar.local_symbol)
        if local is None:
            self.bar[bar.local_symbol] = {bar.interval: []}
        else:
            if self.bar[bar.local_symbol].get(bar.interval) is None:
                self.bar[bar.local_symbol] = {bar.interval: []}
        self.bar[bar.local_symbol][bar.interval].append(bar)

        for value in self.app.extensions.values():
            await value(deepcopy(event))

    async def process_tick_event(self, event: Event):
        """"""
        tick = event.data
        self.ticks[tick.local_symbol] = tick
        symbol = tick.symbol
        self.position_manager.update_tick(tick)
        # 生成datetime对象
        if not tick.datetime:
            if '.' in tick.time:
                tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S.%f')
            else:
                tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S')
        bm = self.generators.get(symbol, None)
        if bm:
            bm.update_tick(tick)
        if not bm:
            self.generators[symbol] = generator(self.event_engine)

        for value in self.app.extensions.values():
            await value(deepcopy(event))

    async def process_order_event(self, event: Event):
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
        for value in self.app.extensions.values():
            await value(deepcopy(event))

    async def process_trade_event(self, event: Event):
        """"""
        trade = event.data
        self.trades[trade.local_trade_id] = trade

        self.position_manager.update_trade(trade)
        for value in self.app.extensions.values():
            await value(deepcopy(event))

    async def process_position_event(self, event: Event):
        """"""
        position = event.data
        self.positions[position.local_position_id] = position
        self.position_manager.update_position(position)
        for value in self.app.extensions.values():
            await value(deepcopy(event))

    async def process_account_event(self, event: Event):
        """"""
        account = event.data
        self.accounts[account.local_account_id] = account
        for value in self.app.extensions.values():
            await value(deepcopy(event))

    async def process_contract_event(self, event: Event):
        """"""
        contract = event.data
        self.contracts[contract.local_symbol] = contract
        for value in self.app.extensions.values():
            await value(deepcopy(event))

    def get_shared(self, symbol):
        return self.shared.get(symbol, None)

    def get_all_shared(self):
        return self.shared

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

    def get_account(self, local_account_id):
        return self.accounts.get(local_account_id, None)

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
        return list(self.positions.values())
        # return self.position_manager.get_all_positions()

    def get_errors(self):
        return self.errors

    def get_new_error(self):
        return self.errors[-1]

    def get_all_accounts(self):
        """
        Get all account data.
        """
        return list(self.accounts.values())

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
