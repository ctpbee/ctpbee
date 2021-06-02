"""
实现了
"""
from copy import deepcopy
from dataclasses import dataclass
from typing import List


@dataclass
class Order:
    offset: str = ""
    direction: str = ""
    datetime: str = ""
    local_symbol: str = ""
    price: float = 0
    counted: float = 0

    def __post_init__(self):
        self.share = self.offset + "-" + self.direction


@dataclass
class Deal:
    buy_price: float = 0
    sell_price: float = 0
    buy_datetime: str = ""
    sell_datetime: str = ""
    local_symbol: str = ""
    counted: float = 0


class MetaPattern(object):
    """一个非常小的匹配单程序 仅仅支持股票和期货
    如果是多开那么对应 空平
    如果是空开 那么对应多平
    """
    match_pattern = {
        "close-short": "open-long",
        "close-long": "open-short"
    }

    def __init__(self, mode="stock", **kwargs):
        """

        params(mode): 匹配模式
        **************  相关参数

        # 仅仅在stock模式下有效
        sh_commission_ratio: 上海交易所手续费率
        stamp_duty_ratio: 印花税率
        sz_commission_ratio: 深圳交易所手续费率

        # 仅仅在future模式下
        buy_commission_ratio: 买入手续费
        buy_commission_ratio: 卖出入手续费

        """
        self.mode = mode
        for i, v in kwargs.items():
            setattr(self, i, v)
        # self.sh_commission_ratio = 0.0002
        # self.stamp_duty_ratio = 0.001
        # self.sz_commission_ratio = 0.0002

    def update_config(self, config: dict):
        pass

    def match_trade(self, trades: List):
        n = [x._to_order() for x in trades]
        return self.match_(n)

    def match_(self, orders: List[Order]):
        if len(orders) == 0:
            raise ValueError("请不要传入空列表")

        temp_order = [orders.pop(0)]
        deals = []
        for order in orders:
            # 此处应用最后匹配原则,为了兼容以后可能出现的碎股
            deal, x = self.scan(order, temp_order)
            deals.extend(deal)
            temp_order = x
        return deals, temp_order

    def scan(self, order, temp_order) -> (List[Deal], List[Order]):
        """ 此处我们使用一个扫描程序,使得order成交全部被消耗或者"""
        deal_list: List[Deal] = []
        box = []
        # print("开始匹配单", order, "此时暂存空间", temp_order)
        if len(temp_order) == 0:
            return [], [order]
        while True:
            try:
                temp = temp_order.pop(-1)
                if self.match_pattern.get(order.share) == temp.share:
                    """ 如果行为能匹配上 """
                    if order.counted > temp.counted:
                        """ 如果成交数量要大于暂存的数量 """
                        new_order = deepcopy(order)
                        order.counted = order.counted - temp.counted
                        new_order.counted = temp.counted
                        deal_list.append(self.get_deal(new_order, temp))

                    elif order.counted == temp.counted:
                        """ 成交数量刚好相等 """
                        deal_list.append(self.get_deal(order, temp))
                        break
                    else:
                        """仅仅只能成交一部分, 比如开了5手, 平2手然后加入到暂存空间中去 直到全部被匹配完毕 """
                        new_order_temp = deepcopy(temp)
                        new_order_temp.counted = temp.counted - order.counted
                        temp_order.append(new_order_temp)
                        temp.counted = order.counted
                        deal_list.append(self.get_deal(order, temp))
                        break
                else:
                    """ 如果成交行为没有匹配上 那么归还temp,同时把order进去"""
                    box.append(temp)
                    # box.append(order)
            except IndexError:
                box.append(order)
                break
        temp_order.extend(box)
        return deal_list, temp_order

    @staticmethod
    def get_deal(order, temp) -> Deal:
        assert order.counted == temp.counted
        if order.direction == "long":
            """ 如果平空头  """
            deal = Deal(local_symbol=order.local_symbol, buy_price=order.price, sell_price=temp.price,
                        buy_datetime=order.datetime, sell_datetime=temp.datetime, counted=order.counted)
        elif order.direction == "short":
            """ 平多头 """
            deal = Deal(local_symbol=order.local_symbol, buy_price=temp.price, sell_price=order.price,
                        buy_datetime=temp.datetime, sell_datetime=order.datetime, counted=order.counted)
        else:
            raise ValueError("错误的成交方向")
        return deal

    def get_profit(self, deals: [Deal]):
        all_count = 0
        profit_count = 0
        pnl, duty, commission = 0, 0, 0
        for deal in deals:

            if self.mode == "stock":
                stamp_duty = deal.sell_price * deal.counted * self.stamp_duty_ratio
                if deal.local_symbol.startswith("6"):
                    buy_commission = deal.buy_price * deal.counted * self.sh_commission_ratio
                    sell_commission = deal.sell_price * deal.counted * self.sh_commission_ratio
                else:
                    buy_commission = deal.buy_price * deal.counted * self.sz_commission_ratio
                    sell_commission = deal.sell_price * deal.counted * self.sz_commission_ratio
            elif self.mode == "future":
                stamp_duty = 0
                sell_commission = deal.sell_price * deal.counted * self.size * self.sell_commission_ratio
                buy_commission = deal.sell_price * deal.counted * self.size * self.buy_commission_ratio
            else:
                raise ValueError(f"暂不支持的模式: {self.mode}")
            pnl += (deal.sell_price - deal.buy_price) * deal.counted - stamp_duty - buy_commission - sell_commission
            commission += buy_commission + sell_commission
            duty += stamp_duty
            all_count += 1
            if pnl > 0:
                profit_count += 1
        return dict(profit=pnl, stamp_duty=duty, commission=commission, profit_count=profit_count,
                    all_count=all_count)
