from ctpbee.json.pollen import Pollen

loads = Pollen.loads
dumps = Pollen.dumps


if __name__ == '__main__':
    from ctpbee.constant import *

    t = SubscribeRequest(symbol='1', exchange=Status.ALLTRADED, datetime=datetime.now())
    tick = {'float2': 53.12321,
            'int': (123, "123", t, Status.ALLTRADED, 23432),
            ' ': None,
            'b': b'ssq',
            'str': "hello",
            'enum': Status.CANCELLED,
            'list_enum': [2, "2", Interval.MINUTE],
            'time': datetime.now(),
            'timef': "2019-2-12 19:30:2.12312",
            "dcit": {"enum": Offset.CLOSE,
                     'int': 999.9}
            }
    res = dumps(tick)
    print(f'dumps-->{type(res)}   {res}')
    pp = loads(res)
    print(f'loads-->{type(pp)}   {pp}')
