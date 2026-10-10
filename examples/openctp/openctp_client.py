from time import sleep

from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import *
from ctpbee import VLogger


class Main(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        self.init = False
        self.count = 0
        self.pos = 0  # 本地净持仓: 多开 +1 / 平多 -1, 空开 -1 / 平空 +1

    def _tick_action(self):
        """发单门控: 每 20 个 tick 至多一次; 无持仓开仓, 有持仓平仓。

        旧实现几乎每根 tick 都发 FOK 单且不跟踪持仓, 会灌爆柜台。
        """
        self.count += 1
        if self.count % 20 != 0:
            return None
        return "close" if self.pos else "open"

    def on_tick(self, tick: TickData) -> None:
        act = self._tick_action()
        if act == "open":
            self.action.buy_open(tick.ask_price_5, 1, tick, price_type=OrderType.FOK)
        elif act == "close":
            self.action.buy_close(tick.bid_price_5, 1, tick, price_type=OrderType.FOK)
        print("tick回报", tick)

    def on_trade(self, trade: TradeData) -> None:
        # 按成交方向/开平维护本地净持仓(示例级: 忽略部分成交与拒单细节)
        if trade.offset == Offset.OPEN:
            self.pos += 1 if trade.direction == Direction.LONG else -1
        else:
            self.pos -= 1 if trade.direction == Direction.LONG else -1
        print("成交回报", trade)

    def on_account(self, account: AccountData) -> None:
        print("账户回报", account)

    def on_order(self, order: OrderData) -> None:
        print("订单回报: ", order)

    def on_contract(self, contract: ContractData):
        print("contract回报: ", contract)

    def on_init(self, init: bool):
        self.info("账户初始化成功回报")
        self.init = True
        self.action.subscribe("rb2310")


if __name__ == '__main__':
    app = CtpBee("openctp", __name__, refresh=True)
    example = Main("DailyCTA")
    config = {
        "CONNECT_INFO": {
            "host": "127.0.0.1",
            "index": 0,
            "port": 6379,
            "db": 0
        },
        "INTERFACE": "local",
        "MD_FUNC": True,
        "TD_FUNC": True,
    }
    app.config.from_mapping(config)
    app.add_extension(example)
    app.start(log_output=True)
    app.action.subscribe("rb2310.SHFE")
