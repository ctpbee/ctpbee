"""
交易流实现
订单协议


"""

import json
from threading import Thread

from ctpbee.constant import (
    TickData,
    OrderData,
    OrderRequest,
    CancelRequest,
    ContractData,
    QueryContract,
    TradeData,
)
from ctpbee.level import CtpbeeApi

from redis import Redis


class UDDR:
    """
    上行消息 订单数据
    """

    def __init__(self, msg, index=0, parse: bool = True):
        self.index = index
        self.obj = None
        if parse:
            try:
                self.__parse__(msg)
            except Exception as e:
                pass
        else:
            self.obj = msg

    def encode(self):
        from ctpbee import dumps

        return json.dumps(
            dict(data=dumps(self.obj), index=self.index), ensure_ascii=False
        )

    def __parse__(self, msg):

        msg = json.loads(msg)
        from ctpbee import loads

        self.index = msg["index"]
        self.obj = loads(msg["data"])


class DDDR:
    """
    下行消息
    """

    def __init__(self, obj, index=None, parse=False):
        self.index = None
        self.order = None
        if not parse:
            self.order = obj
            self.index = index
        else:
            self.__parse__(obj)

    def __parse__(self, obj):
        """
        fixme: why not loads do not work
        """
        from ctpbee import loads

        locken = loads(obj)
        self.index = locken["index"]
        msg = loads(locken["data"])
        if "order_id" in msg.keys() and "tradeid" in msg.keys():
            self.order = TradeData(**msg)
        elif "order_id" in msg.keys() and "tradeid" not in msg.keys():
            self.order = OrderData(**msg)
        elif "pricetick" in msg.keys() and "size" in msg.keys():
            self.order = ContractData(**msg)
        else:
            self.order = None

    def encode(self) -> str:
        from ctpbee import dumps

        return json.dumps(
            dict(
                data=dumps(self.order),
                index=self.index,
            ),
            ensure_ascii=False,
        )


class Dispatcher(CtpbeeApi):

    def __init__(self, name, app=None):
        super().__init__(name, app=app)
        tcp_addr = self.app.config.get("RD_CLIENT_ADDR", "127.0.0.1")
        tcp_port = self.app.config.get("RD_CLIENT_PORT", 6379)
        db = self.app.config.get("RD_CLIENT_DB", 0)
        self.order_up_kernel = self.app.config.get(
            "ORDER_UP_KERNEL", "ctpbee_order_up_kernel"
        )
        self.tick_kernel = self.app.config.get("TICK_KERNEL", "ctpbee_tick_kernel")
        self.order_down_kernel = self.app.config.get(
            "ORDER_DOWN_KERNEL", "ctpbee_order_down_kernel"
        )
        self.rd_client = Redis(
            host=tcp_addr, port=tcp_port, db=db, decode_responses=True, encoding="utf8"
        )
        self.order_key_map = dict()
        threader = Thread(target=self.listen, daemon=True)
        threader.start()
        self.init = False

    def listen(self):
        """
        监听来自订单通道的消息
        """
        pub = self.rd_client.pubsub()
        pub.subscribe(self.order_up_kernel)
        for item in pub.listen():
            uddr = UDDR(item["data"], parse=True)
            if uddr.obj is None:
                continue
            elif type(uddr.obj) == OrderRequest:
                order_id = self.action.send_order(order=uddr.obj)
                self.order_key_map[order_id] = uddr.index
            elif type(uddr.obj) == CancelRequest:
                self.action.cancel_order(uddr.obj)
                self.order_key_map[uddr.obj.order_id] = uddr.index
            elif type(uddr.obj) == QueryContract:
                for i in self.app.recorder.get_all_contracts():
                    dr = DDDR(obj=i, index=uddr.obj.index, parse=False)
                    self.rd_client.publish(self.order_down_kernel, dr.encode())
            else:
                continue

    def on_order(self, order: OrderData) -> None:
        index = self.order_key_map.get(order.order_id, 0)
        order_message = DDDR(obj=order, index=index)
        self.rd_client.publish(self.order_down_kernel, order_message.encode())

    def on_tick(self, tick: TickData) -> None:
        tick_message = DDDR(obj=tick, index=None)
        self.rd_client.publish(self.tick_kernel, tick_message.encode())

    def on_contract(self, contract: ContractData) -> None:
        if not self.init:
            for i in self.app.config.get("SUBSCRIBE_CONTRACT", []):
                self.action.subscribe(i)
            self.info("行情订阅成功")
            self.init = True
