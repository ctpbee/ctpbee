import json
from random import randint

result = {}
result_d = []
from datetime import datetime, timedelta


def generate_ramdom(local_symbol, path):
    count = 0

    def get_random():
        return randint(3000, 4000)

    start = datetime.now()
    while True:
        temp = {}
        temp['local_symbol'] = local_symbol
        temp['datetime'] = str(start)
        temp['high_price'] = get_random()
        temp['low_price'] = get_random()
        temp['open_price'] = get_random()
        temp['close_price'] = get_random()
        result_d.append(temp)
        start = start + timedelta(minutes=15)
        if count > 1000:
            break
        count += 1
    with open(path, "w") as f:
        result['data'] = result_d
        json.dump(obj=result, fp=f)


if __name__ == '__main__':
    generate_ramdom("ag1912.SHFE", "data.json")
