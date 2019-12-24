import argparse
import copy
import distutils.cmd
import distutils.log
import datetime
import os
import subprocess
import sys

from .trade_time import Papa

parser = argparse.ArgumentParser(description="bee bee bee~")
parser.add_argument('-tt', '--tradetime', help='更新交易日历/Update transaction calendar;'
                                               'Example: -tt 2019 or -tt 2004-2020 or -tt now')

parser.add_argument("-auto", '--generate', help="对于linux自动生成中文环境")


def tradetime_handle(year):
    if "-" in year:
        y = year.split("-")
    elif year == 'now':
        y = [2004, datetime.datetime.now().year]
    else:
        y = [2004, year]
    Papa.run(y)
    Papa.write()


def update_locale():
    with open("/etc/locale.gen", "a+") as f:
        code_lines = [
            "zh_CN.GB18030 GB18030",
            "en_US.UTF-8 UTF-8",
            "zh_CN.UTF-8 UTF-8"
        ]
        for x in code_lines:
            f.write(x + "\n")
    os.system("locale-gen")


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
        return

    auto = args.generate
    if auto == "generate":
        update_locale()
        return


