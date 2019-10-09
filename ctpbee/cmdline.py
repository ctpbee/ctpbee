import argparse
import datetime
import sys

from .trade_time import Papa

parser = argparse.ArgumentParser(description="bee bee bee~")
parser.add_argument('-tt', '--tradetime', help='更新交易日历/Update transaction calendar;Example: 2019 or 2004-2020 or now')


def tradetime_handle(year):
    if "-" in year:
        y = year.split("-")
    elif year == 'now':
        y = [2004, datetime.datetime.now().year]
    else:
        y = [2004, year]
    Papa.run(y)
    Papa.write()


def execute():
    if len(sys.argv) <= 1:
        print('[*]Tip: ctpbee -h view help')
        sys.exit(0)
    args = parser.parse_args()
    # argv_value
    year = args.tradetime
    # handle
    if year:
        tradetime_handle(year)


if __name__ == '__main__':
    execute()
