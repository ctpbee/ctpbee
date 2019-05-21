"""底层的数据库引擎， 初期代码可能会比较丑陋"""
from typing import Dict

from peewee import MySQLDatabase, PostgresqlDatabase, SqliteDatabase, Model, CharField, FloatField, IntegerField, \
    DateTimeField
from ctpbee import current_app
from ctpbee.exceptions import ConfigError

type_map = {
    'sqlite': SqliteDatabase,
    'mysql': MySQLDatabase,
    'postgresql': PostgresqlDatabase
}

tick_type = current_app().config.get('TICK_DATABASE_TYPE')
bar_type = current_app().config.get('BAR_DATABASE_TYPE')

if tick_type is None or bar_type is None:
    raise ConfigError(args=("配置信息异常， 请检查TICK_DATABASE_TYPE和BAR_DATABASE_TYPE有没有被设置",))

tick_pointer = type_map[tick_type](
    current_app().config.get('TICK_DATABASE_NAME'),
    user=current_app().config.get('TICK_DATABASE_USER'),
    password=current_app().config.get('TICK_DATABASE_PWD'),
    host=current_app().config.get('TICK_DATABASE_HOST'),
    port=current_app().config.get('TICK_DATABASE_PORT')
)

bar_pointer = type_map[tick_type](
    database=current_app().config.get('BAR_DATABASE_NAME'),
    user=current_app().config.get('BAR_DATABASE_USER'),
    password=current_app().config.get('BAR_DATABASE_PWD'),
    host=current_app().config.get('BAR_DATABASE_HOST'),
    port=current_app().config.get('BAR_DATABASE_PORT')
)


class TickDatabaseBase(Model):
    class Meta: database = tick_pointer


class BarDatabaseBase(Model):
    class Meta: database = bar_pointer


def set_attr(self, data: Dict):
    for key, d in data.items():
        if hasattr(self, key):
            raise ValueError('赋值对象不存在该键')
        setattr(self, key, d)


def generate_data_class():
    """generate orm class map"""
    orm_map = {}
    subsribed_symbols = current_app().config.get('SUBSCRIBED_SYMBOL')
    '''generate tick map and bar map'''

    tfield = {
        'symbol': CharField(),
        'exchange': CharField(),
        'vt_symbol': CharField(),
        'datetime': DateTimeField,
        'name': CharField(),
        'volume': FloatField(),
        'last_price': FloatField(),
        'last_volume': FloatField(),
        'limit_up': FloatField(),
        'limit_down': FloatField(),
        'open_interest': IntegerField(),
        'average_price': FloatField(),
        'open_price': FloatField(),
        'high_price': FloatField(),
        'low_price': FloatField(),
        'pre_price': FloatField(),
        'bid_price_1': FloatField(),
        'bid_price_2': FloatField(),
        'bid_price_3': FloatField(),
        'bid_price_4': FloatField(),
        'bid_price_5': FloatField(),
        'ask_price_1': FloatField(),
        'ask_price_2': FloatField(),
        'ask_price_3': FloatField(),
        'ask_price_4': FloatField(),
        'ask_price_5': FloatField(),
        'bid_volume_1': FloatField(),
        'bid_volume_2': FloatField(),
        'bid_volume_3': FloatField(),
        'bid_volume_4': FloatField(),
        'bid_volume_5': FloatField(),
        'ask_volume_1': FloatField(),
        'ask_volume_2': FloatField(),
        'ask_volume_3': FloatField(),
        'ask_volume_4': FloatField(),
        'ask_volume_5': FloatField(),
        'to': set_attr
    }
    bfield = {
        'symbol': CharField(),
        'exchange': CharField(),
        'vt_symbol': CharField(),
        'datetime': DateTimeField,
        'volume': FloatField(),
        'open_price': FloatField(),
        'high_price': FloatField(),
        'low_price': FloatField(),
        'pre_price': FloatField(),
        'interval': IntegerField(),
        'to': set_attr
    }

    for symbol in subsribed_symbols:
        orm_map[f"t{symbol}"] = type(symbol, (TickDatabaseBase,), tfield)
        orm_map[f"b{symbol}"] = type(symbol, (BarDatabaseBase,), bfield)
    return orm_map
