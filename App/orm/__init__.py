# coding:utf-8
from sqlalchemy import Column, Date, Integer, String, ForeignKey, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base

__all__ = ("generateMap")

Base = declarative_base()


def set_attrs(self, data):
    """
    set the attribute of k-line bar data
    :param self:
    :param data:
    :return:
    """
    for key, value in data.items():
        setattr(self, key, value)

def create_propertys():
    id = Column(Integer, autoincrement=True, primary_key=True)
    symbol = Column(String(56))  # 代码
    vt_symbol = Column(String(56))  # vt系统代码
    exchange = Column(String(56))  # 交易所
    open = Column(Float)  # OHLC
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    date = Column(String(128))  # bar开始的时间，日期
    time = Column(String(128))  # 时间
    datetime = Column(DATETIME)  # python的datetime时间对象
    volume = Column(Integer)  # 成交量
    open_interest = Column(Integer)  # 持仓量
    interval = Column(String(56))  # K线周期

    propertys = dict(__tablename__=None, id=id, symbol=symbol, vtSymbol=vt_symbol,
                     exchange=exchange, open=open, close=close, high=high, low=low, date=date,
                     time=time, datetime=datetime, volume=volume, openInterest=open_interest,
                     interval=interval, setAttrs=set_attrs)
    return propertys


def generate_map(contract_list):
    catch_dict = {}
    for i in contract_list:
        pro_sec = create_propertys()
        pro_min = create_propertys()
        pro_sec['__tablename__'] = i + "SEC"
        item = type(i + "SEC", (Base,), pro_sec)
        catch_dict[i + "SEC"] = item
        pro_min['__tablename__'] = i + "MIN"
        item = type(i + "MIN", (Base,), pro_min)
        catch_dict[i + "MIN"] = item
    return catch_dict
