"""底层的数据库引擎， 初期代码可能会比较丑陋"""
from peewee import MySQLDatabase, PostgresqlDatabase, SqliteDatabase, Model, CharField
from ctpbee import current_app

orm_map = {}
type_map = {
    'sqlite': SqliteDatabase,
    'mysql': MySQLDatabase,
    'postgresql': PostgresqlDatabase
}
tick_type = current_app().config.get('TICK_DATABASE_TYPE')
bar_type = current_app().config.get('BAR_DATABASE_TYPE')

tick_pointer = type_map[tick_type](
    ddatabase=current_app().config.get('TICK_DATABASE_NAME'),
    user=current_app().config.get('TICK_DATABASE_USER'),
    password=current_app().config.get('TICK_DATABASE_PWD'),
    host=current_app().config.get('TICK_DATABASE_HOST'),
    port=current_app().config.get('TICK_DATABASE_PORT')
)

bar_pointer = type_map[tick_type](
    ddatabase=current_app().config.get('BAR_DATABASE_NAME'),
    user=current_app().config.get('BAR_DATABASE_USER'),
    password=current_app().config.get('BAR_DATABASE_PWD'),
    host=current_app().config.get('BAR_DATABASE_HOST'),
    port=current_app().config.get('BAR_DATABASE_PORT')
)


class DatabaseBase(Model):
    class Meta:
        database = tick_pointer


class TickDatabaseBase(DatabaseBase): pass


class BarDatabaseBase(DatabaseBase): pass


def generate_data_class():
    """generate orm class map"""
    subsribed_symbols = current_app().config.get('SUBSCRIBED_SYMBOL')

    '''generate tick map'''

    ttype = {
        'symbol': CharField
    }

    for symbol in subsribed_symbols:
        orm_map[symbol] = type(symbol, (TickDatabaseBase), ttype)

    pass
