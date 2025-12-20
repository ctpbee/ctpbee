from .lib import *
from ..func import get_folder_path, LoginRequired


class MTdApi(MiniTdApi, LoginRequired):
    """"""

    def __init__(self, app_signal):
        """Constructor"""
        LoginRequired.__init__(self)
        super(MTdApi, self).__init__()
        self.gateway_name = "ctp_mini"

        self.reqid = 0
        self.order_ref = 0
        self.app_signal = app_signal
        self.userid = ""
        self.password = ""
        self.brokerid = ""
        self.auth_code = ""
        self.appid = ""
        self.product_info = ""

        self.frontid = 0
        self.sessionid = 0

        self.order_data = []
        self.trade_data = []
        self.positions = {}
        self.sysid_orderid_map = {}
        self.local_order_id = []

        self.position_instrument_mapping = dict()

    @property
    def td_status(self):
        return self.login_required

    def on_event(self, type, data):
        event = Event(type=type, data=data)
        signal = getattr(self.app_signal, f"{type}_signal")
        signal.send(event)

    def onFrontConnected(self):
        """"""
        self.on_event(EVENT_LOG, "交易服务器连接成功")

        if self.auth_code:
            self.authenticate()
        else:
            self.login()

    def onFrontDisconnected(self, reason: int):
        """"""
        self.connect_required = False
        self.on_event(EVENT_LOG, f"交易服务器连接断开，原因{reason}")

    def onRspAuthenticate(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        if not error["ErrorID"]:
            self.connect_required = True
            self.on_event(EVENT_LOG, "交易服务器授权验证成功")
            self.login()
        else:
            self.on_event(EVENT_ERROR, f"交易服务器授权验证失败: {error}")

    def onRspUserLogin(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        if not error["ErrorID"]:
            self.frontid = data["FrontID"]
            self.sessionid = data["SessionID"]
            self.login_required = True
            self.on_event(EVENT_LOG, "交易服务器登录成功")

            # Get instrument data directly without confirm settlement
            self.reqid += 1
            self.reqQryInstrument({}, self.reqid)
        else:
            self.on_event(EVENT_ERROR, f"交易服务器登录失败: {error}")

    def onRspOrderInsert(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        order_ref = data["OrderRef"]
        orderid = f"{self.frontid}_{self.sessionid}_{order_ref}"

        symbol = data["InstrumentID"]
        exchange = symbol_exchange_map[symbol]

        order = OrderData(
            symbol=symbol,
            exchange=exchange,
            order_id=orderid,
            direction=DIRECTION_MINI2VT[data["Direction"]],
            offset=OFFSET_MINI2VT.get(data["CombOffsetFlag"], Offset.NONE),
            price=data["LimitPrice"],
            volume=data["VolumeTotalOriginal"],
            status=Status.REJECTED,
            gateway_name=self.gateway_name,
        )
        self.on_event(EVENT_ORDER, order)
        error["detail"] = "交易委托失败"
        self.on_event(EVENT_ERROR, error)

    def onRspOrderAction(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        self.on_event(EVENT_ERROR, f"交易撤单失败 :{error}")

    def onRspQueryMaxOrderVolume(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        pass

    def onRspSettlementInfoConfirm(
        self, data: dict, error: dict, reqid: int, last: bool
    ):
        """
        Callback of settlment info confimation.
        """
        pass

    def onRspQryInvestorPosition(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
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
                    direction=DIRECTION_MINI2VT[data["PosiDirection"]],
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
            pass

        if last:
            for position in self.positions.values():
                self.on_event(type=EVENT_POSITION, data=position)
                self.position_instrument_mapping[position.local_symbol] = False
            self.positions.clear()
            self.open_cost_dict.clear()
            self.position_required = True

    def onRspQryTradingAccount(self, data: dict, error: dict, reqid: int, last: bool):
        """"""
        if "AccountID" not in data:
            return

        account = AccountData(
            accountid=data["AccountID"],
            balance=data["Balance"],
            frozen=data["FrozenMargin"] + data["FrozenCash"] + data["FrozenCommission"],
            gateway_name=self.gateway_name,
            available=data["Available"],
        )

        self.on_event(EVENT_ACCOUNT, account)
        if not self.account_required:
            self.account_required = True
            from time import sleep

            sleep(1)
            self.query_position()

    def onRspQryInstrument(self, data: dict, error: dict, reqid: int, last: bool):
        """
        Callback of instrument query.
        """
        product = PRODUCT_MINI2VT.get(data.get("ProductClass", None), None)
        # For option only
        # 此处去掉 if product 原因是：if product 过滤掉了交易所标准套利合约
        # 如果 ProductClass 的字段，在 PRODUCT_CTP2VT 中没有定义，那么该合约是交易所标准套利合约，如：SP eb2402&eb2403
        if product == Product.OPTION:
            option_underlying = data["UnderlyingInstrID"]
            option_type = OPTIONTYPE_MINI2VT.get(data["OptionsType"], None)
            option_strike = data["StrikePrice"]
            option_expiry = datetime.strptime(data["ExpireDate"], "%Y%m%d")
        else:
            option_strike: float = 0
            option_underlying: str = ""
            option_type: OptionType = None
            option_expiry: datetime = None

        contract = ContractData(
            symbol=data["InstrumentID"],
            exchange=EXCHANGE_MINI2VT[data["ExchangeID"]],
            name=data["InstrumentName"],
            product=product,
            size=data["VolumeMultiple"],
            pricetick=data["PriceTick"],
            gateway_name=self.gateway_name,
            option_strike=option_strike,
            option_underlying=option_underlying,
            option_type=option_type,
            option_expiry=option_expiry,
            if_last=last,
        )

        self.on_event(EVENT_CONTRACT, contract)
        symbol_exchange_map[contract.symbol] = contract.exchange
        symbol_name_map[contract.symbol] = contract.name
        symbol_size_map[contract.symbol] = contract.size

        if last:
            self.on_event(EVENT_LOG, "合约信息查询成功")
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
        order_id = f"{frontid}_{sessionid}_{order_ref}"
        is_local = (
            True
            if int(self.frontid) == int(frontid)
            and int(self.sessionid) == int(sessionid)
            else False
        )
        timestamp = f"{data['InsertDate']} {data['InsertTime']}"
        # dt = datetime.strptime(timestamp, "%Y%m%d %H:%M:%S")
        # dt = CHINA_TZ.localize(dt)
        dt = timestamp
        if is_local:
            self.local_order_id.append(order_id)
        order = OrderData(
            symbol=symbol,
            exchange=exchange,
            order_id=order_id,
            is_local=is_local,
            type=ORDERTYPE_MINI2VT[data["OrderPriceType"]],
            direction=DIRECTION_MINI2VT[data["Direction"]],
            offset=OFFSET_MINI2VT[data["CombOffsetFlag"]],
            price=data["LimitPrice"],
            volume=data["VolumeTotalOriginal"],
            traded=data["VolumeTraded"],
            status=STATUS_MINI2VT[data["OrderStatus"]],
            datetime=dt,
            gateway_name=self.gateway_name,
        )
        self.on_event(EVENT_ORDER, order)
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
        timestamp = f"{data['TradeDate']} {data['TradeTime']}"
        dt = datetime.strptime(timestamp, "%Y%m%d %H:%M:%S")
        dt = CHINA_TZ.localize(dt)

        trade = TradeData(
            symbol=symbol,
            exchange=exchange,
            order_id=order_id,
            is_local=is_local,
            tradeid=data["TradeID"],
            direction=DIRECTION_MINI2VT[data["Direction"]],
            offset=OFFSET_MINI2VT[data["OffsetFlag"]],
            price=data["Price"],
            volume=data["Volume"],
            datetime=dt,
            gateway_name=self.gateway_name,
        )
        self.on_event(EVENT_TRADE, trade)

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
        address = info.get("td_address")
        if not address.startswith("tcp://"):
            address = "tcp://" + address

        if not self.connect_required:
            path = get_folder_path(self.gateway_name.lower() + f"/{self.userid}")
            self.createFtdcTraderApi(str(path) + "\\Td")

            self.subscribePrivateTopic(0)
            self.subscribePublicTopic(0)
            self.registerFront(address)
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
        Login onto server.
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

    def send_order(self, req: OrderRequest):
        """
        Send new order.
        """
        self.order_ref += 1

        mini_req = {
            "InstrumentID": req.symbol,
            "ExchangeID": req.exchange.value,
            "LimitPrice": req.price,
            "VolumeTotalOriginal": int(req.volume),
            "OrderPriceType": ORDERTYPE_VT2MINI.get(req.type, ""),
            "Direction": DIRECTION_VT2MINI.get(req.direction, ""),
            "CombOffsetFlag": OFFSET_VT2MINI.get(req.offset, ""),
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
        }

        if req.type == OrderType.FAK:
            mini_req["OrderPriceType"] = THOST_FTDC_OPT_LimitPrice
            mini_req["TimeCondition"] = THOST_FTDC_TC_IOC
            mini_req["VolumeCondition"] = THOST_FTDC_VC_AV
        elif req.type == OrderType.FOK:
            mini_req["OrderPriceType"] = THOST_FTDC_OPT_LimitPrice
            mini_req["TimeCondition"] = THOST_FTDC_TC_IOC
            mini_req["VolumeCondition"] = THOST_FTDC_VC_CV

        self.reqid += 1
        self.reqOrderInsert(mini_req, self.reqid)

        order_id = f"{self.frontid}_{self.sessionid}_{self.order_ref}"
        order = req._create_order_data(order_id, self.gateway_name)
        self.on_event(type=EVENT_ORDER, data=order)
        return order.local_order_id

    def cancel_order(self, req: CancelRequest):
        """
        Cancel existing order.
        """
        frontid, sessionid, order_ref = req.order_id.split("_")

        mini_req = {
            "InstrumentID": req.symbol,
            "ExchangeID": req.exchange.value,
            "OrderRef": order_ref,
            "FrontID": int(frontid),
            "SessionID": int(sessionid),
            "ActionFlag": THOST_FTDC_AF_Delete,
            "BrokerID": self.brokerid,
            "InvestorID": self.userid,
        }

        self.reqid += 1
        self.reqOrderAction(mini_req, self.reqid)

    def query_account(self):
        """
        Query account balance data.
        """
        self.reqid += 1
        self.reqQryTradingAccount({}, self.reqid)

    def query_position(self):
        """
        Query position holding data.
        """
        if not symbol_exchange_map:
            return

        req = {"BrokerID": self.brokerid, "InvestorID": self.userid}

        self.reqid += 1
        self.reqQryInvestorPosition(req, self.reqid)

    def close(self):
        """"""
        # if self.connect_status:
        #     self.()
