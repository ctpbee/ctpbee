"""
Notice : 神兽保佑 ，测试一次通过
//
//      ┏┛ ┻━━━━━┛ ┻┓
//      ┃　　　　　　 ┃
//      ┃　　　━　　　┃
//      ┃　┳┛　  ┗┳　┃
//      ┃　　　　　　 ┃
//      ┃　　　┻　　　┃
//      ┃　　　　　　 ┃
//      ┗━┓　　　┏━━━┛
//        ┃　　　┃   Author: somewheve
//        ┃　　　┃   Datetime: 2019/6/13 下午7:54  ---> 无知即是罪恶
//        ┃　　　┗━━━━━━━━━┓
//        ┃　　　　　　　    ┣┓
//        ┃　　　　         ┏┛
//        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
//          ┃ ┫ ┫   ┃ ┫ ┫
//          ┗━┻━┛   ┗━┻━┛
//
"""

from collections import defaultdict

from ctpbee.constant import *
from ctpbee.interface.ctp.lib import *
from ctpbee.interface.func import *


class BeeTdApi(TdApi, LoginRequired):
    """"""

    def __init__(self, app_signal):
        LoginRequired.__init__(self)
        super(BeeTdApi, self).__init__()
        self.app_signal = app_signal
        self.gateway_name = "ctp"
        self.reqid = 0
        self.userid = ""
        self.password = ""
        self.brokerid = 0
        self.auth_code = ""
        self.product_info = ""
        self.appid = ""

        self.frontid = 0
        self.sessionid = 0

        self.order_data = []
        self.trade_data = []
        self.positions = {}

        self.choices = list(range(50000, 1000000))
        self.order_ref = 0

        self.symbol_exchange_mapping = {}
        self.sysid_orderid_map = {}
        self.open_cost_dict = defaultdict(dict)
        self.position_instrument_mapping = dict()

        self.init_status = False
        self.contact_data = {}
        self.local_order_id = []
        self.subscribe_type = "future"

    @property
    def td_status(self):
        return self.login_required

    def on_event(self, type, data):
        event = Event(type=type, data=data)
        signal = getattr(self.app_signal, f"{type}_signal")
        signal.send(event)

    def onFrontConnected(self):
        """"""
        self.connect_status = True
        self.on_event(type=EVENT_LOG, data="交易连接成功")

        if self.auth_code:
            self.authenticate()
        else:
            self.login()

    def onFrontDisconnected(self, reason: int):
        """"""
        self.connect_required = False
        self.login_required = False
        self.on_event(type=EVENT_LOG, data=f"交易连接断开，原因{reason}")

    def onRspAuthenticate(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        if not error["ErrorID"]:
            self.connect_required = True
            self.on_event(type=EVENT_LOG, data="交易服务器验证成功")
            self.login()
        else:
            error["detail"] = "交易服务器验证失败"
            self.on_event(type=EVENT_ERROR, data=error)

    def onRspUserLogin(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        if not error["ErrorID"]:
            self.frontid = data["FrontID"]
            self.sessionid = data["SessionID"]
            self.login_required = True
            self.on_event(type=EVENT_LOG, data="交易登录成功")

            # Confirm settlement
            req = {"BrokerID": self.brokerid, "InvestorID": self.userid}
            self.reqid += 1

            self.reqSettlementInfoConfirm(req, self.reqid)
        else:
            error["detail"] = "交易登录失败"
            self.on_event(type=EVENT_ERROR, data=error)

    def onRspOrderInsert(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        order_ref = data["OrderRef"]
        order_id = f"{self.frontid}_{self.sessionid}_{order_ref}"
        symbol = data["InstrumentID"]
        exchange = symbol_exchange_map[symbol]
        order = OrderData(
            symbol=symbol,
            exchange=exchange,
            order_id=order_id,
            direction=DIRECTION_CTP2VT[data["Direction"]],
            offset=OFFSET_CTP2VT[data["CombOffsetFlag"]],
            price=data["LimitPrice"],
            volume=data["VolumeTotalOriginal"],
            status=Status.REJECTED,
            gateway_name=self.gateway_name,
        )
        self.on_event(type=EVENT_ORDER, data=order)
        error["detail"] = "交易委托失败"
        self.on_event(type=EVENT_ERROR, data=error)

    def onRspOrderAction(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        error["detail"] = "交易撤单失败"
        self.on_event(type=EVENT_ERROR, data=error)

    def onRspQueryMaxOrderVolume(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        pass

    def onRspSettlementInfoConfirm(
        self, data: dict, error: dict, reqid: int, last: bool
    ):
        """
        Callback of settlment info confimation.
        """
        self.on_event(type=EVENT_LOG, data="结算信息确认成功")
        self.reqid += 1
        # 需要实现按需订阅 按照瓶中
        self.reqQryInstrument({}, self.reqid)

    def onRspQryInvestorPosition(self, data: dict, error: dict, reqid: int, last: bool):
        """
        仓位回调逻辑
        """
        if not data:
            if last:
                self.position_required = True
            return
        key = f"{data['InstrumentID'], data['PosiDirection']}"
        position = self.positions.get(key, None)
        try:
            if not position:
                position = PositionData(
                    symbol=data["InstrumentID"],
                    exchange=symbol_exchange_map[data["InstrumentID"]],
                    direction=DIRECTION_CTP2VT[data["PosiDirection"]],
                    gateway_name=self.gateway_name,
                )
                self.positions[key] = position
            # For SHFE position data update
            if position.exchange == Exchange.SHFE:
                if data["YdPosition"] and not data["TodayPosition"]:
                    # position.yd_volume = data["Position"]
                    position.__set_hole__("yd_volume", data["Position"])
            # For other exchange position data update
            else:
                # position.yd_volume = data["Position"] - data["TodayPosition"]
                position.__set_hole__(
                    "yd_volume", data["Position"] - data["TodayPosition"]
                )

            # Get contract size (spread contract has no size value)
            size = symbol_size_map.get(position.symbol, 0)

            # Calculate previous position cost
            cost = position.price * position.volume * size

            # Update new position volume
            # position.volume += data["Position"]
            position.__set_hole__("volume", position.volume + data["Position"])
            # position.pnl += data["PositionProfit"]
            position.__set_hole__("pnl", position.pnl + data["PositionProfit"])

            # Calculate average position price
            if position.volume and size:
                cost += data["PositionCost"]
                # position.price = cost / (position.volume * size)
                position.__set_hole__("price", cost / (position.volume * size))
                self.open_cost_dict[position.symbol]["size"] = size

            # Get frozen volume
            if position.direction == Direction.LONG:
                # position.frozen += data["ShortFrozen"]
                position.__set_hole__("frozen", position.frozen + data["ShortFrozen"])

                if position.volume and size:
                    if not self.open_cost_dict[position.symbol].get("long"):
                        self.open_cost_dict[position.symbol]["long"] = 0

                    self.open_cost_dict[position.symbol]["long"] += data["OpenCost"]
                    # position.open_price = self.open_cost_dict[position.symbol]["long"] / (
                    #         position.volume * size)
                    position.__set_hole__(
                        "open_price",
                        self.open_cost_dict[position.symbol]["long"]
                        / (position.volume * size),
                    )
                    # 先算出当前的最新价格
                    current_price = (
                        position.pnl / (size * position.volume) + position.price
                    )

                    # position.float_pnl = (current_price - position.open_price) * size * position.volume
                    position.__set_hole__(
                        "float_pnl",
                        (current_price - position.open_price) * size * position.volume,
                    )

            else:
                # position.frozen += data["LongFrozen"]
                position.__set_hole__("frozen", position.frozen + data["LongFrozen"])

                if position.volume and size:
                    if not self.open_cost_dict[position.symbol].get("short"):
                        self.open_cost_dict[position.symbol]["short"] = 0

                    self.open_cost_dict[position.symbol]["short"] += data["OpenCost"]
                    # position.open_price = self.open_cost_dict[position.symbol]["short"] / (
                    #         position.volume * size)
                    position.__set_hole__(
                        "open_price",
                        self.open_cost_dict[position.symbol]["short"]
                        / (position.volume * size),
                    )
                    current_price = position.price - position.pnl / (
                        size * position.volume
                    )
                    # position.float_pnl = (position.open_price - current_price) * size * position.volume
                    position.__set_hole__(
                        "float_pnl",
                        (position.open_price - current_price) * size * position.volume,
                    )

        except KeyError:
            print(data)

        if last:
            for position in self.positions.values():
                self.on_event(type=EVENT_POSITION, data=position)
                self.position_instrument_mapping[position.local_symbol] = False
            if not self.position_required:
                self.on_event(type=EVENT_LOG, data="持仓初始化成功")
            self.positions.clear()
            self.open_cost_dict.clear()
            self.position_required = True

    def onRspQryTradingAccount(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        account = AccountData(
            accountid=data["AccountID"],
            balance=data["Balance"],
            frozen=data["FrozenMargin"] + data["FrozenCash"] + data["FrozenCommission"],
            gateway_name=self.gateway_name,
            available=data["Available"],
        )
        self.on_event(type=EVENT_ACCOUNT, data=account)
        if not self.account_required:
            """当前合约查询完毕 且账户未查询 那么请求查询深度行情和持仓数据"""
            self.on_event(type=EVENT_LOG, data="账户查询成功")
            self.reqid += 1
            self.account_required = True
            self.query_position()

    def onRspQryInstrument(self, data: dict, error: dict, reqid: int, last: bool):
        """
        Callback of instrument query.
        """
        product = PRODUCT_CTP2VT.get(data["ProductClass"], None)
        try:
            end_delivery_date = (datetime.strptime(data["EndDelivDate"], "%Y%m%d"),)
            start_delivery_date = (datetime.strptime(data["StartDelivDate"], "%Y%m%d"),)
            open_date = (datetime.strptime(data["OpenDate"], "%Y%m%d"),)
            is_trading = (bool(data["IsTrading"]),)
            create_date = datetime.strptime(data["CreateDate"], "%Y%m%d")
        except ValueError:
            end_delivery_date = None
            start_delivery_date = None
            open_date = None
            is_trading = None
            create_date = None

        # 此处去掉 if product 原因是：if product 过滤掉了交易所标准套利合约
        # 如果 ProductClass 的字段，在 PRODUCT_CTP2VT 中没有定义，那么该合约是交易所标准套利合约，如：SP eb2402&eb2403
        try:
            # For option only
            if product == Product.OPTION:
                option_underlying = (data["UnderlyingInstrID"],)
                option_type = (OPTIONTYPE_CTP2VT.get(data["OptionsType"], None),)
                option_strike = (data["StrikePrice"],)
                option_expiry = (datetime.strptime(data["ExpireDate"], "%Y%m%d"),)
            else:
                option_strike: float = 0
                option_underlying: str = ""
                option_type: OptionType = None
                option_expiry: datetime = None
            contract = ContractData(
                symbol=data["InstrumentID"],
                exchange=EXCHANGE_CTP2VT[data["ExchangeID"]],
                name=data["InstrumentName"],
                product=product,
                max_market_order_volume=data["MaxMarketOrderVolume"],
                min_market_order_volume=data["MinMarketOrderVolume"],
                max_limit_order_volume=data["MaxLimitOrderVolume"],
                min_limit_order_volume=data["MaxLimitOrderVolume"],
                size=data["VolumeMultiple"],
                pricetick=data["PriceTick"],
                delivery_month=data["DeliveryMonth"],
                delivery_year=data["DeliveryYear"],
                long_margin_ratio=data["LongMarginRatio"],
                short_margin_ratio=data["ShortMarginRatio"],
                combination_type=data["CombinationType"],
                gateway_name=self.gateway_name,
                end_delivery_date=end_delivery_date,
                start_delivery_date=start_delivery_date,
                open_date=open_date,
                is_trading=is_trading,
                create_date=create_date,
                option_strike=option_strike,
                option_underlying=option_underlying,
                option_type=option_type,
                option_expiry=option_expiry,
                if_last=last,
            )
        except KeyError as e:
            import warnings

            warnings.warn(f"未预料到的合约问题 错误信息: {e}")
            return
        self.symbol_exchange_mapping[data["InstrumentID"]] = EXCHANGE_CTP2VT[
            data["ExchangeID"]
        ]

        symbol_exchange_map[contract.symbol] = contract.exchange
        symbol_name_map[contract.symbol] = contract.name
        symbol_size_map[contract.symbol] = contract.size

        if self.subscribe_type == "future" and contract.product == Product.FUTURES:
            self.on_event(type=EVENT_CONTRACT, data=contract)

        elif self.subscribe_type != "future":
            self.on_event(type=EVENT_CONTRACT, data=contract)
        if (
            self.subscribe_type == "future"
            and contract.product != Product.FUTURES
            and not self.contract_required
        ):
            self.on_event(EVENT_LOG, data="期货合约信息查询成功")
            self.contract_required = True
            for data in self.order_data:
                self.onRtnOrder(data)
            self.order_data.clear()
            for data in self.trade_data:
                self.onRtnTrade(data)
            self.trade_data.clear()
            self.query_account()
        else:
            if last and not self.contract_required:
                self.on_event(EVENT_LOG, data="所有合约信息查询成功")
                self.contract_required = True
                for data in self.order_data:
                    self.onRtnOrder(data)
                self.order_data.clear()
                for data in self.trade_data:
                    self.onRtnTrade(data)
                self.trade_data.clear()
                self.query_account()

    def onRtnOrder(self, data: dict):
        """
        Callback of order status update.
        """
        symbol = data["InstrumentID"]
        exchange = symbol_exchange_map.get(symbol, "")
        if not exchange:
            self.order_data.append(data)
            return

        frontid = data["FrontID"]
        sessionid = data["SessionID"]
        order_ref = data["OrderRef"]
        if int(order_ref) > self.order_ref:
            self.order_ref = int(order_ref) + 1
        order_id = f"{frontid}_{sessionid}_{order_ref}"
        if data["OrderPriceType"] in ORDERTYPE_VT2CTP.values():
            ordertype = ORDERTYPE_CTP2VT[data["OrderPriceType"]]
        else:
            ordertype = "non_support"
        is_local = (
            True
            if int(self.frontid) == int(frontid)
            and int(self.sessionid) == int(sessionid)
            else False
        )

        if is_local:
            self.local_order_id.append(order_id)

        order = OrderData(
            symbol=symbol,
            exchange=exchange,
            order_id=order_id,
            type=ordertype,
            direction=DIRECTION_CTP2VT[data["Direction"]],
            offset=OFFSET_CTP2VT[data["CombOffsetFlag"]],
            price=data["LimitPrice"],
            volume=data["VolumeTotalOriginal"],
            traded=data["VolumeTraded"],
            status=STATUS_CTP2VT[data["OrderStatus"]],
            time=data["InsertTime"],
            gateway_name=self.gateway_name,
            is_local=is_local,
        )
        self.on_event(type=EVENT_ORDER, data=order)
        self.sysid_orderid_map[data["OrderSysID"]] = order_id

    def onRtnTrade(self, data: dict):
        """
        Callback of trade status update.
        """
        symbol = data["InstrumentID"]
        exchange = symbol_exchange_map.get(symbol, "")
        if not exchange:
            self.trade_data.append(data)
            return

        order_id = self.sysid_orderid_map[data["OrderSysID"]]
        is_local = order_id in self.local_order_id

        trade = TradeData(
            symbol=symbol,
            exchange=exchange,
            order_id=order_id,
            tradeid=data["TradeID"],
            direction=DIRECTION_CTP2VT[data["Direction"]],
            offset=OFFSET_CTP2VT[data["OffsetFlag"]],
            price=data["Price"],
            volume=data["Volume"],
            time=data["TradeTime"],
            is_local=is_local,
            gateway_name=self.gateway_name,
        )
        self.on_event(type=EVENT_TRADE, data=trade)

    def connect(self, info: dict):
        """
        Start connection to server.
        """
        self.userid = info.get("userid")
        self.password = info.get("password")
        self.brokerid = info.get("brokerid")
        self.auth_code = info.get("auth_code")
        self.appid = info.get("appid")
        self.product_info = info.get("product_info")
        self.subscribe_type = info.get("contract_type", "future")
        subscribe_info = info.get(
            "subscribe_topic", (0, 0)
        )  # 默认采用(0, 0)的方式进行订阅

        if not self.connect_status:
            path = get_folder_path(self.gateway_name.lower() + f"/{self.userid}")
            self.createFtdcTraderApi(str(path) + "\\Td")
            self.subscribePrivateTopic(subscribe_info[0])
            self.subscribePublicTopic(subscribe_info[1])
            self.registerFront(info.get("td_address"))
            self.init()
        else:
            self.authenticate()

    def authenticate(self):
        """
        Authenticate with auth_code and appid.
        """
        req = {
            "UserID": self.userid,
            "BrokerID": self.brokerid,
            "AuthCode": self.auth_code,
            "AppID": self.appid,
        }
        if self.product_info:
            req["UserProductInfo"] = self.product_info

        self.reqid += 1
        self.reqAuthenticate(req, self.reqid)

    def login(self):
        """
        Login into server.
        """
        req = {
            "UserID": self.userid,
            "Password": self.password,
            "BrokerID": self.brokerid,
            "AppID": self.appid,
        }
        if self.product_info:
            req["UserProductInfo"] = self.product_info
        self.reqid += 1
        self.reqUserLogin(req, self.reqid)

    def onRspQryDepthMarketData(self, data, error, reqid, last):
        try:
            exchange = self.symbol_exchange_mapping[data["InstrumentID"]]
        except KeyError:
            return
        market = LastData(
            symbol=data["InstrumentID"],
            exchange=exchange,
            pre_open_interest=data["PreOpenInterest"],
            open_interest=data["OpenInterest"],
            volume=data["Volume"],
            last_price=data["LastPrice"],
        )
        self.on_event(type=EVENT_LAST, data=market)
        self.position_instrument_mapping[market.symbol] = True

    def request_market_data(self, req: object):
        """请求市场数据"""

        self.reqid += 1
        self.reqQryDepthMarketData({}, self.reqid)

    def send_order(self, req: OrderRequest, **kwargs):
        """
        Send new order.
        """
        self.order_ref += 1
        ctp_req = {
            "InstrumentID": req.symbol,
            "LimitPrice": req.price,
            "VolumeTotalOriginal": int(req.volume),
            "OrderPriceType": ORDERTYPE_VT2CTP.get(req.type, ""),
            "Direction": DIRECTION_VT2CTP.get(req.direction, ""),
            "CombOffsetFlag": OFFSET_VT2CTP.get(req.offset, ""),
            "OrderRef": str(self.order_ref),
            "InvestorID": self.userid,
            "UserID": self.userid,
            "BrokerID": self.brokerid,
            "CombHedgeFlag": THOST_FTDC_HF_Speculation,
            "ContingentCondition": THOST_FTDC_CC_Immediately,
            "ForceCloseReason": THOST_FTDC_FCC_NotForceClose,
            "IsAutoSuspend": 0,
            "TimeCondition": THOST_FTDC_TC_GFD,
            "VolumeCondition": THOST_FTDC_VC_AV,
            "MinVolume": 1,
            "ExchangeID": (
                req.exchange.value
                if isinstance(req.exchange, Exchange)
                else req.exchange
            ),
        }

        if req.type == OrderType.FAK:
            ctp_req["OrderPriceType"] = THOST_FTDC_OPT_LimitPrice
            ctp_req["TimeCondition"] = THOST_FTDC_TC_IOC
            ctp_req["VolumeCondition"] = THOST_FTDC_VC_AV
        elif req.type == OrderType.FOK:
            ctp_req["OrderPriceType"] = THOST_FTDC_OPT_LimitPrice
            ctp_req["TimeCondition"] = THOST_FTDC_TC_IOC
            ctp_req["VolumeCondition"] = THOST_FTDC_VC_CV

        self.reqid += 1
        self.reqOrderInsert(ctp_req, self.reqid)
        order_id = f"{self.frontid}_{self.sessionid}_{self.order_ref}"
        order = req._create_order_data(order_id, self.gateway_name)
        self.on_event(type=EVENT_ORDER, data=order)
        return order.local_order_id

    def cancel_order(self, req: CancelRequest, **kwargs):
        """
        Cancel existing order.
        """
        frontid, sessionid, order_ref = req.order_id.split("_")
        ctp_req = {
            "InstrumentID": req.symbol,
            "OrderRef": order_ref,
            "FrontID": int(frontid),
            "SessionID": int(sessionid),
            "ActionFlag": THOST_FTDC_AF_Delete,
            "BrokerID": self.brokerid,
            "InvestorID": self.userid,
            "ExchangeID": req.exchange.value,
        }

        self.reqid += 1
        return self.reqOrderAction(ctp_req, self.reqid)

    def connect(self, info: dict):
        self.userid = info.get("userid")
        self.password = info.get("password")
        self.brokerid = info.get("brokerid")
        self.auth_code = info.get("auth_code")
        self.appid = info.get("appid")
        self.product_info = info.get("product_info")
        subscribe_info = info.get(
            "subscribe_topic", (0, 0)
        )  # 默认采用(0, 0)的方式进行订阅

        if not self.connect_required:
            path = get_folder_path(self.gateway_name.lower() + f"/{self.userid}")
            self.createFtdcTraderApi(str(path) + "\\Td")
            self.subscribePrivateTopic(subscribe_info[0])
            self.subscribePublicTopic(subscribe_info[1])
            self.registerFront(info.get("td_address"))
            self.init()
        else:
            self.authenticate()

    def query_account(self):
        """
        Query account balance data.
        """
        self.reqid += 1
        return self.reqQryTradingAccount({}, self.reqid)

    def query_position(self):
        """
        Query position holding data.
        """
        if not symbol_exchange_map:
            return
        req = {"BrokerID": self.brokerid, "InvestorID": self.userid}

        self.reqid += 1
        return self.reqQryInvestorPosition(req, self.reqid)

    def close(self):
        """"""
        if self.connect_required:
            self.exit()
