from ctpbee.constant import TickData, BarData
from ctpbee import CtpbeeApi
from ctpbee.indicator.indicator import ma



class SpreadArbitrage(CtpbeeApi):
    """
    跨期套利策略
    利用同一品种不同月份合约之间的价格差异进行交易
    """
    
    # 策略参数
    fast_period = 5  # 价差的快速均线周期
    slow_period = 20  # 价差的慢速均线周期
    threshold = 0.5  # 套利触发阈值
    volume = 1  # 套利手数
    
    def __init__(self, name: str, main_contract, sub_contract):
        """
        初始化套利策略
        
        Args:
            name: 策略名称
            main_contract: 主合约代码（如 "rb2401.SHFE"）
            sub_contract: 子合约代码（如 "rb2402.SHFE"）
        """
        super().__init__(name, )
        
        # 合约配置
        self.main_contract = main_contract
        self.sub_contract = sub_contract
        self.instrument_set = set([main_contract, sub_contract])
        
        # 数据存储
        self.main_bars = []  # 主合约K线数据
        self.sub_bars = []  # 子合约K线数据
        self.spreads = []  # 价差数据
        self.name = name 
        
        # 持仓状态
        self.pos = 0  # 套利持仓状态：1表示主多空子，-1表示主空多子，0表示无持仓
        
        # 其他配置
        self.length = max(self.fast_period, self.slow_period)

        
    def on_tick(self, tick: TickData) -> None:
        """处理tick数据"""
        pass
    
    def on_bar(self, bar: BarData):
        """处理K线数据"""
        self.debug(
            f"收到K线数据 - {bar.local_symbol} {bar.datetime.strftime('%Y-%m-%d %H:%M:%S')} 收盘价: {bar.close_price}", 
   
        )
        
        # 存储K线数据
        if bar.local_symbol == self.main_contract:
            self.main_bars.append(bar)
            self.main_bars = self.main_bars[-self.length * 2:]
        elif bar.local_symbol == self.sub_contract:
            self.sub_bars.append(bar)
            self.sub_bars = self.sub_bars[-self.length * 2:]
        else:
            return
        
        # 检查是否有足够的K线数据
        if len(self.main_bars) < self.length or len(self.sub_bars) < self.length:
            self.debug(
                f"数据不足 - 主合约K线: {len(self.main_bars)}/{self.length}, 子合约K线: {len(self.sub_bars)}/{self.length}", 
              
            )
            return
        
        # 确保主合约和子合约的K线数量匹配
        if len(self.main_bars) != len(self.sub_bars):
            self.debug(
                f"合约K线数量不匹配 - 主合约: {len(self.main_bars)}, 子合约: {len(self.sub_bars)}", 
       
            )
            return
        
        # 计算价差（主合约 - 子合约）
        self.calculate_spread()
        
        # 执行套利逻辑
        self.execute_arbitrage()
    
    def calculate_spread(self):
        """计算主合约和子合约之间的价差"""
        # 确保使用最新的相同数量的K线
        min_length = min(len(self.main_bars), len(self.sub_bars))
        recent_main = self.main_bars[-min_length:]
        recent_sub = self.sub_bars[-min_length:]
        
        # 计算价差
        for main_bar, sub_bar in zip(recent_main, recent_sub):
            spread = main_bar.close_price - sub_bar.close_price
            self.spreads.append(spread)
        
        # 只保留最近的价差数据
        self.spreads = self.spreads[-self.length * 2:]
    
    def execute_arbitrage(self):
        """执行套利交易逻辑"""
        if len(self.spreads) < self.length * 2:
            self.debug(
                f"价差数据不足 - 需要 {self.length * 2} 个价差，当前 {len(self.spreads)} 个", 
            
            )
            return
        
        # 计算价差的均线
        spread_array = self.spreads[-self.length * 2:]
        fast_ma = ma(spread_array, self.fast_period)
        slow_ma = ma(spread_array, self.slow_period)
        
        # 获取当前和前一个价差及均线值
        current_spread = spread_array[-1]
        previous_spread = spread_array[-2]
        current_fast = fast_ma[-1]
        previous_fast = fast_ma[-2]
        current_slow = slow_ma[-1]
        previous_slow = slow_ma[-2]
        
        # 计算价差偏离均线的程度
        spread_deviation = abs(current_spread - current_slow)
        
        self.debug(
            f"价差分析 - 当前价差: {current_spread:.2f}, "
            f"快速MA: {current_fast:.2f}, 慢速MA: {current_slow:.2f}, "
            f"偏离度: {spread_deviation:.2f}, 阈值: {self.threshold}", 

        )
        
        # 套利入场条件
        # 1. 价差偏离均线超过阈值
        # 2. 快速均线和慢速均线出现金叉或死叉
        
        # 多头套利信号：价差过低，买入主合约，卖出子合约
        buy_signal = spread_deviation > self.threshold and current_spread < current_slow
        
        # 空头套利信号：价差过高，卖出主合约，买入子合约
        sell_signal = spread_deviation > self.threshold and current_spread > current_slow
        
        # 平仓信号：价差回归均线，或均线出现反向交叉
        close_signal = spread_deviation <= self.threshold
        
        # 执行交易
        if self.pos == 0:
            # 无持仓状态
            if buy_signal:
                # 执行多头套利：买入主合约，卖出子合约
                self.success(
                    f"多头套利入场 - 主合约: {self.main_contract}, 子合约: {self.sub_contract}, "
                    f"当前价差: {current_spread:.2f}, 均线: {current_slow:.2f}, 偏离度: {spread_deviation:.2f}", 
          
                )
                
                # 获取最新的K线数据
                main_bar = self.main_bars[-1]
                sub_bar = self.sub_bars[-1]
                
                # 下单：买入主合约，卖出子合约
                self.action.buy_open(main_bar.close_price, self.volume, main_bar)
                self.action.sell_open(sub_bar.close_price, self.volume, sub_bar)
                
                self.pos = 1  # 多头套利持仓状态
            
            elif sell_signal:
                # 执行空头套利：卖出主合约，买入子合约
                self.success(
                    f"空头套利入场 - 主合约: {self.main_contract}, 子合约: {self.sub_contract}, "
                    f"当前价差: {current_spread:.2f}, 均线: {current_slow:.2f}, 偏离度: {spread_deviation:.2f}", 
         
                )
                
                # 获取最新的K线数据
                main_bar = self.main_bars[-1]
                sub_bar = self.sub_bars[-1]
                
                # 下单：卖出主合约，买入子合约
                self.action.sell_open(main_bar.close_price, self.volume, main_bar)
                self.action.buy_open(sub_bar.close_price, self.volume, sub_bar)
                
                self.pos = -1  # 空头套利持仓状态
        
        elif close_signal:
            # 价差回归，平仓获利
            self.success(
                f"套利平仓 - 主合约: {self.main_contract}, 子合约: {self.sub_contract}, "
                f"当前价差: {current_spread:.2f}, 均线: {current_slow:.2f}, 偏离度: {spread_deviation:.2f}", 
    
            )
            
            # 获取最新的K线数据
            main_bar = self.main_bars[-1]
            sub_bar = self.sub_bars[-1]
            
            if self.pos == 1:
                # 平多头套利：卖出主合约，买入子合约
                self.action.sell_close(main_bar.close_price, self.volume, main_bar)
                self.action.buy_close(sub_bar.close_price, self.volume, sub_bar)
            
            elif self.pos == -1:
                # 平空头套利：买入主合约，卖出子合约
                self.action.buy_close(main_bar.close_price, self.volume, main_bar)
                self.action.sell_close(sub_bar.close_price, self.volume, sub_bar)
            
            self.pos = 0  # 平仓后恢复无持仓状态
    
    def on_order(self, order):
        """处理订单事件"""
        self.info(
            f"订单更新 - {order.local_symbol}, 订单ID: {order.local_order_id}, "
            f"状态: {order.status}, 方向: {order.direction}, 开平: {order.offset}, "
            f"价格: {order.price}, 数量: {order.volume}, 成交: {order.traded}", 

        )
    
    def on_trade(self, trade):
        """处理成交事件"""
        self.success(
            f"成交更新 - {trade.local_symbol}, 成交ID: {trade.local_trade_id}, "
            f"方向: {trade.direction}, 开平: {trade.offset}, "
            f"价格: {trade.price}, 数量: {trade.volume}, 成交额: {trade.volume * trade.price}", 

        )
    
    def on_position(self, position):
        """处理持仓事件"""
        # self.info(
        #     f"持仓更新 - {position.local_symbol}, 方向: {position.direction}, "
        #     f"数量: {position.volume}, 可用: {position.volume - position.frozen}, "
        #     f"价格: {position.price}, 盈亏: {position.pnl}", 
        #     owner=self.name
        # )
    
    def on_account(self, account):
        """处理账户事件"""
        # self.info(
        #     f"账户更新 - 可用资金: {account.available:.2f}, 总资金: {account.balance:.2f}, "
        #     f"冻结资金: {account.frozen:.2f}", 
        #     owner=self.name
        # )
