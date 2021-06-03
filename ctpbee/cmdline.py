import argparse
import os
import sys

parser = argparse.ArgumentParser(description="bee bee bee~")

parser.add_argument("-auto", '--generate', help="对于linux自动生成中文环境")


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

    auto = args.generate
    if auto == "generate":
        update_locale()
        return
