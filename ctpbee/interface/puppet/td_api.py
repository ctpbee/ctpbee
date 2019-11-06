from ctpbee.constant import AccountData, EVENT_ACCOUNT
from ctpbee.constant import EVENT_LOG, EVENT_POSITION
from ctpbee.event_engine import EventEngine, Event

class PuppetApi(object):
    def __init__(self, event_engine: EventEngine):
        self.event_engine = event_engine
        self.client = None
        self.api = None

    def connect(self, info):
        try:
            self.client.login(**info)
            title = '广发证券核新网上交易系统7.65'
            self.api = self.client.bind(title).init()
            event = Event(EVENT_LOG, data="股票账户登录成功")
            self.event_engine.put(event)
        except Exception:
            event = Event(EVENT_LOG, data="账户登录失败 ")
            self.event_engine.put(event)

    def query_position(self):
        event = Event(type=EVENT_POSITION, data=self.api.position)
        self.event_engine.put(event)

    def query_account(self):
        data = AccountData(account_id=self.api.account, balance=self.api.balance,
                           frozen=self.api.balance - self.api.assets)
        event = Event(EVENT_ACCOUNT, data=data)
        self.event_engine.put(data)

    def send_order(self):
        pass
