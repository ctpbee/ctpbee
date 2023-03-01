#!/usr/bin/env python
# coding=utf-8
"""
 tick 驱动 交易
"""

from ctpbee import CtpbeeApi, CtpBee
from ctpbee.constant import ContractData, LogData, TickData, BarData, OrderData, \
    TradeData, PositionData, AccountData, OrderType
from ctpbee import Action
from ctpbee.helpers import run_forever


class ActionMe(Action):
    def __init__(self, app):
        # 请记住要对父类进行实例化
        super().__init__(app)
        # 通过add_risk_check接口添加风控
        self.add_risk_check(self.sell)


class TL(CtpbeeApi):
    def __init__(self, name):
        super().__init__(name)
        # self.instrument_set = limit_ctp_symbol
        self.instrument_set = ["rb2205.SHFE"]  # need to fill in
        print(self.instrument_set)
        self.clock = 0
        self.isok = True

    def on_contract(self, contract: ContractData):
        """ 处理推送的合约信息 """
        if contract.local_symbol in self.instrument_set:
            self.app.subscribe(contract.local_symbol)

    def on_log(self, log: LogData):
        """ 处理日志信息 ,特殊需求才用到 """
        pass

    def on_tick(self, tick: TickData) -> None:
        """ 处理推送的tick """

        ins = (''.join(list(filter(str.isalpha, tick.symbol)))).upper()
        # check active_order
        # if self.isok == False:
        #    return

        # check position for free
        positionInsArray = []
        position = self.center.positions
        for i in position:
            positionIns = (''.join(list(filter(str.isalpha, i.symbol)))).upper()
            positionInsArray.append(positionIns)
            if ins == positionIns:
                result = self.check_free(ins, tick.last_price, i.price, str(i.direction))
                if result == "sell":
                    self.action.sell(tick.limit_up, i.volume, tick)  # to prevent extreme circumstances must be done
                elif result == "cover":
                    self.action.cover(tick.limit_down, i.volume, tick)  # to prevent extreme circumstances must be done
                else:
                    pass
                return

                # only one
        # if(len (positionInsArray) > 0):
        #    return 

        # check condition  do
        if (ins not in positionInsArray):
            result = self.check_obey(ins, tick.last_price)
            if result == "buy":
                maxh = self.get_max_h(tick, result, 0.5)
                if maxh == 0:
                    return
                self.action.buy(tick.last_price, maxh, tick)
            elif result == "short":
                maxh = self.get_max_h(tick, result, 0.5)
                if maxh == 0:
                    return
                self.action.short(tick.last_price, maxh, tick)
            else:
                pass
        pass

    def check_free(self, curPrice, costPrice, direct):
        # the reality of evolution doesn't match expectations, free
        # why?
        # how?
        # what?
        pass

    def check_obey(self, symbol, curPrice):
        # go with the flow, in the past, in the present, in human nature
        # why?
        # how?
        # what?
        pass

    def get_max_h(self, tick: TickData, direct, capital_ratio):
        constantS = self.center.get_contract(tick.local_symbol)
        account = self.center.account
        if (account is None) or (constantS is None):
            return 0
        margin_ratio = 0.0
        if direct == "buy":
            margin_ratio = constantS.long_margin_ratio
        else:
            margin_ratio = constantS.short_margin_ratio
        maxh = (account.available * capital_ratio) // (tick.last_price * constantS.size * margin_ratio)
        return int(maxh)

    def on_bar(self, bar: BarData) -> None:
        """ 处理ctpbee生成的bar """

    def on_init(self, init):
        pass

    def on_order(self, order: OrderData) -> None:
        """ 报单回报 """
        self.isok = False

    def on_trade(self, trade: TradeData) -> None:
        """ 成交回报 """
        self.isok = True

    def on_position(self, position: PositionData) -> None:
        """ 处理持仓回报 """

    def on_account(self, account: AccountData) -> None:
        """ 处理账户信息 """
        # print("on_account\n")
        # print("account","\n")

    def on_realtime(self):
        # 定时清理掉未成交的单
        self.clock += 1
        if (self.clock >= 10 and len(self.center.active_orders)):
            self.action.cancel_all()
            self.clock = 0
        pass


def obey():
    app = CtpBee("power", __name__, action_class=ActionMe)
    tl = TL("tl")
    app.add_extension(tl)
    app.config.from_json("config.json")
    app.start(log_output=True)


if __name__ == '__main__':
    obey()
