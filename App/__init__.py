# coding:utf-8
# created by somewheve on 2019-1-23 13:22:00
from __future__ import print_function
from time import sleep, time
from pymongo import MongoClient
from redis import Redis
from datetime import datetime
from vnpy.trader.vtEvent import EVENT_TICK, EVENT_TIMER
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import Settings
from bar.generator import BarGenerator, ArrayManager
from orm import generate_map, set_attrs, Base
from .tcp_ping import calculate_delay


class WriteInto(object):
    all_database = ("mysql", "mongo", "redis")

    def __init__(self, engine, orm_map, name, particular_database_type=None):
        self.orm_map = orm_map
        self.engine = engine
        self.mongo_database_name = particular_database_type
        self.name = name
        if name not in self.all_database:
            raise Exception("数据库不存在")

    def insert_into_mysql(self, tablename, datas):
        data_map = self.orm_map[tablename]()
        set_attrs(data_map, datas)
        self.engine.add(data_map)
        self.engine.commit()

    def insert_into_redis(self, key, value):
        self.engine.set(key, value)

    def insert_into_mongo(self, gather_name, value):
        self.engine[self.mongo_database_name][gather_name].insert(value)

    def insert(self, **kwargs):
        if "key" not in kwargs.keys():
            raise Exception("缺少表名和数据")
        if "data" not in kwargs.keys():
            raise Exception("缺少表名和数据")
        if self.name == "mysql":
            if "key" and "data" in kwargs.keys():
                self.insert_into_mysql(kwargs['key'], kwargs['data'])

        if self.name == "mongo":
            if "data" and "key" in kwargs.keys():
                self.insert_into_mongo(kwargs['key'], kwargs['data'])

        if self.name == "redis":
            if "data" and "key" in kwargs.keys():
                self.insert_into_mongo(kwargs['key'], kwargs['data'])


class App(object):
    __slots__ = (
        "settings", "last_timer_time", "redis", "timer_count", "market_close_time", "opreator", "config",
        "name", "event_engine", "tickDict", "mdApi", "tick_type", "bar_type", "le",
        "bg_dict", "bg", "am", "status", "bar_write", "caution", "tick_write", "is_flag", "tick_notification_status")

    def __init__(self, name, event_engine, mdApi, le):
        self.name = name
        self.le = le
        self.event_engine = event_engine
        self.tickDict = {}
        self.bg_dict = {}
        self.timer_count = 0
        self.event_engine.register(EVENT_TICK, self.procecss_tick_event)
        self.event_engine.register(EVENT_TIMER, self.process_timer_event)
        self.mdApi = mdApi(event_engine)
        self.config = Settings()
        self.am = ArrayManager()
        self.last_timer_time = datetime.now().time()
        self.status = {"mysql": self.mysql_init, "mongo": self.mongodb_init, "redis": self.redis_init}
        self.bar_write = None
        self.tick_write = None
        self.caution = {"tick": False, "bar": False}
        self.is_flag = False
        self.tick_notification_status = True

    def mysql_init(self):
        try:
            mysql_url = getattr(self.config, "MYSQL_URL")
            mysql_port = getattr(self.config, "MYSQL_PORT")
            mysql_username = getattr(self.config, "MYSQL_USERNAME")
            mysql_password = getattr(self.config, "MYSQL_PASSWORD")
            mysql_database_name = getattr(self.config, "MYSQL_DATABASE")
        except AttributeError as e:
            self.le.info("必须提供完整的mysql配置信息")
            raise Exception("Error in mysql setup")
        url = "mysql+pymysql://{}:{}@{}:{}/{}".format(mysql_username, mysql_password, mysql_url, mysql_port,
                                                      mysql_database_name)
        engine = create_engine(url, echo=False)
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        return Session()

    def mongodb_init(self):
        try:
            mongo_url = getattr(self.config, "MONGO_HOST")
            mongo_port = getattr(self.config, "MONGO_PORT")
        except AttributeError:
            self.le.info("未能找到正确的mongodb配置, 使用默认配置")
            mongo_port = 27017
            mongo_url = "127.0.0.1"
        # mongo_database = getattr(self.config, "MONGO_DATABASE_NAME")
        return MongoClient(host=mongo_url, port=mongo_port)

    def redis_init(self):
        try:
            redis_url = getattr(self.config, "REDIS_URL")
            redis_port = getattr(self.config, "REDIS_PORT")
        except AttributeError as e:
            redis_url = "127.0.0.1"
            redis_port = "27017"
        return Redis(host=redis_url, port=redis_port)

    def start(self):
        self.event_engine.start()

    def init_bar(self, database_name):
        # 获取写入指针
        if database_name not in self.status.keys():
            raise Exception("目标数据库不支持")
        kor = None
        self.bar_type = database_name
        if database_name == "mongo":
            kor = "bar"
        contractList = getattr(self.config, "CONTRACT_LIST")
        orm_map = generate_map(contract_list=contractList)
        self.bar_write = WriteInto(self.status[database_name](), orm_map, database_name, kor)

    def init_tick(self, database_name):
        if database_name not in self.status.keys():
            raise Exception("目标数据库不支持")
        kor = None
        self.tick_type = database_name
        if database_name == "mongo":
            kor = "tick"
        self.tick_write = WriteInto(self.status[database_name](), {}, database_name, kor)

    def _subscribe(self, symbol):
        result = self.mdApi.subscribe(symbol=symbol)
        return result

    def _get_close_time(self):
        try:
            market_close_time = getattr(self.config, "MARK_CLOSE_TIME")
        except AttributeError as e:
            market_close_time = None
        return market_close_time

    def init_setup(self):
        """登录订阅数据"""
        subscribe_result = list()
        contract_list = getattr(self.config, "CONTRACT_LIST")
        for symbol in contract_list:
            result = self._subscribe(symbol)
            subscribe_result.append(int(result))
        self.market_close_time = self._get_close_time()
        return subscribe_result

    def load_settings_from_py_file(self, filename):
        """
        loading config from py file
        :param filename: file path
        :return: None
        """
        self.config.add_environment_from_file(filename)

    def load_settings_from_Json_file(self, filename):
        """
        :param filename: file path
        :return:None
        """
        self.config.from_json(filename)

    def procecss_tick_event(self, event):
        """处理行情事件"""
        tick = event.dict_
        vtSymbol = tick.vtSymbol
        if not tick.datetime:
            if '.' in tick.time:
                tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S.%f')
            else:
                tick.datetime = datetime.strptime(' '.join([tick.date, tick.time]), '%Y%m%d %H:%M:%S')
        self.on_tick(tick)
        bm = self.bg_dict.get(vtSymbol, None)
        if bm:
            bm.updateTick(tick)
        if not bm:
            self.bg_dict[vtSymbol] = BarGenerator(self.on_bar, 1, self.on_x_min_bar)  # 创建K线合成器对象

    def process_timer_event(self, event):
        """处理定时事件"""
        if not self.market_close_time:
            return
        self.timer_count += 1
        if self.timer_count < 1:
            return
        self.timer_count = 0
        current_time = datetime.now().time()
        if not self.last_timer_time:
            self.last_timer_time = current_time
            return
        if (self.last_timer_time < self.market_close_time and current_time >= self.market_close_time):
            for bg in self.bg_dict.values():
                bg.generate()
        self.last_timer_time = current_time

    def notifacation(self, signal):
        """通知函数"""
        if signal == self.tick_notification_status:
            return
        if signal == "stop":
            self.le.info("tick 停止运行中")
        if signal == "start":
            self.le.info("tick 运行中")
        self.tick_notification_status = signal

    def on_bar(self, bar):
        """生成5s　k线"""
        # print("正在写入k线数据---{}---- 5s线".format(self.bar_type))
        self.notifacation("start")
        vt_symbol = bar.vtSymbol
        tablename = vt_symbol + "SEC"
        self.bar_write.insert(key=tablename, data=bar.__dict__)

    def on_x_min_bar(self, bar):
        """生成1分钟的k线"""
        # print("正在写入k线数据---{}---- 分钟线".format(self.bar_type))
        vtSymbol = bar.vtSymbol
        tablename = vtSymbol + "MIN"
        self.bar_write.insert(key=tablename, data=bar.__dict__)

    def on_tick(self, tick):
        """
        处理tick数据 , 写入redis, 保证最新行情
        """
        symbol = tick.symbol
        # print("正在写入tick数据---{}---- s线".format(self.tick_type))
        data = tick.__dict__
        self.tick_write.insert(key=symbol, data=data)

    def close_connection(self):
        result = self.mdApi.close()
        return result

    def connect_ctp(self, **kwargs):
        # userID="089131", password="350888", BrokeID="9999", mdAddress="tcp://180.168.146.187:10011"
        md_address = getattr(self.config, "MD_ADDRESS")
        self.le.info("计算最佳行情服务器")
        point = None
        result = {}
        new_time = time()
        # self.mdApi = mdApi(event_engine)
        for i, value in enumerate(md_address):
            test_result = calculate_delay(host=value['host'], port=value['port'])
            result[i] = test_result
        max_c = max(result.values())
        for key, val in result.items():
            if val == max_c:
                point = key
        match_result = md_address[point]
        end_time = time()
        self.le.info("计算完毕，耗时{}秒， 即将登录".format(end_time - new_time))
        try:
            self.mdApi.connect("089131", "350888", match_result['broke_id'],
                               "tcp://{}:{}".format(match_result["host"], match_result['port']))
        except AttributeError as e:
            raise Exception("请检查配置文件中 MD_ADDRESS是否正确")
        login_result = self.mdApi.loginStatus
        self.le.info("登录信息结算: 主机: {}:{} , broke_id: {}, 登录结果: {}".format(match_result['host'], match_result['port'],
                                                               match_result['broke_id'], login_result))
        sleep(0.1)
        sub_result = self.init_setup()
        if -1 in sub_result:
            self.le.info("订阅失败 请检查信息")
        self.le.info("登录完成")

    def register(self, address):
        self.mdApi.register(address)

    def get_login_status(self):
        return self.mdApi.loginStatus
