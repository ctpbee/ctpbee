from ctpbee.data_handle import generator
from ctpbee.ctp.constant import *
from ctpbee.event_engine import  Event


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
        self.errors = {}
        self.shared = {}
        self.active_orders = {}
        self.event_engine = event_engine
        self.register_event()
        self.app = app


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
        if self.shared.get(event.data.vt_symbol, None) is not None:
            self.shared[event.data.vt_symbol].append(event.data)
        else:
            self.shared[event.data.vt_symbol] = []
        for key, value in self.app.extensions.items():
            value(event)

    def process_error_event(self, event: Event):
        self.errors[self.get_local_time()] = event.data
        print(self.get_local_time() + ": ", event.data)

    def process_log_event(self, event: Event):
        self.logs[self.get_local_time()] = event.data
        if self.app.config.get("LOG_OUTPUT"):
            print(self.get_local_time() + ": ", event.data)

    def process_bar_event(self, event: Event):
        self.bar[event.data.vt_symbol] = event.data

        for key, value in self.app.extensions.items():
            value(event)

    def process_tick_event(self, event: Event):
        """"""
        tick = event.data
        self.ticks[tick.vt_symbol] = tick
        symbol = tick.symbol
        # 生成datetime对象
        if not tick.datetime:
            if '.' in tick.time:
                tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S.%f')
            else:
                tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S')
        bm = self.bar.get(symbol, None)
        if bm:
            bm.update_tick(tick)
        if not bm:
            self.bar[symbol] = generator()
        for key, value in self.app.extensions.items():
            value(event)

    def process_order_event(self, event: Event):
        """"""
        order = event.data
        self.orders[order.vt_orderid] = order
        # If order is active, then update data in dict.
        if order.is_active():
            self.active_orders[order.vt_orderid] = order
        # Otherwise, pop inactive order from in dict
        elif order.vt_orderid in self.active_orders:
            self.active_orders.pop(order.vt_orderid)
        for key, value in self.app.extensions.items():
            value(event)

    def process_trade_event(self, event: Event):
        """"""
        trade = event.data
        self.trades[trade.vt_tradeid] = trade
        for key, value in self.app.extensions.items():
            value(event)

    def process_position_event(self, event: Event):
        """"""
        position = event.data
        self.positions[position.vt_positionid] = position
        for key, value in self.app.extensions.items():
            value(event)

    def process_account_event(self, event: Event):
        """"""
        account = event.data
        self.accounts[account.vt_accountid] = account
        for key, value in self.app.extensions.items():
            value(event)

    def process_contract_event(self, event: Event):
        """"""
        contract = event.data
        self.contracts[contract.vt_symbol] = contract

    def get_shared(self, symbol):
        return self.shared.get(symbol, None)

    def get_all_shared(self):
        return self.shared

    def get_bar(self, vt_symbol):
        return self.bar.get(vt_symbol, None)

    def get_all_bar(self):
        return self.bar

    def get_tick(self, vt_symbol):
        """
        Get latest market tick data by vt_symbol.
        """
        return self.ticks.get(vt_symbol, None)

    def get_order(self, vt_orderid):
        """
        Get latest order data by vt_orderid.
        """
        return self.orders.get(vt_orderid, None)

    def get_trade(self, vt_tradeid):
        """
        Get trade data by vt_tradeid.
        """
        return self.trades.get(vt_tradeid, None)

    def get_position(self, vt_positionid):
        """
        Get latest position data by vt_positionid.
        """
        return self.positions.get(vt_positionid, None)

    def get_account(self, vt_accountid):
        """
        Get latest account data by vt_accountid.
        """
        return self.accounts.get(vt_accountid, None)

    def get_contract(self, vt_symbol):
        """
        Get contract data by vt_symbol.
        """
        return self.contracts.get(vt_symbol, None)

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

    def get_all_active_orders(self, vt_symbol: str = ""):
        """
        Get all active orders by vt_symbol.
        If vt_symbol is empty, return all active orders.
        """
        if not vt_symbol:
            return list(self.active_orders.values())
        else:
            active_orders = [
                order
                for order in self.active_orders.values()
                if order.vt_symbol == vt_symbol
            ]
            return active_orders
