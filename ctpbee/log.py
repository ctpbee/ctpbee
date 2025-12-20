"""
实现一个默认的LoggerClass<<<<<<< dev

log格式

时间 ---- 执行者 ---- 等级 ---- 信息

"""

from cologer import loger, Fore, Back, Style
from datetime import datetime


def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


loger.set_format("{created} {name}     {levelname}  {owner}   {message}")

# info
loger.info.fields.created.set_fore(Fore.RED).set_default(get_time)
loger.info.fields.name
loger.info.fields.levelname.set_fore(Fore.MAGENTA).set_default("INFO")
loger.info.fields.owner.set_fore(Fore.CYAN)
loger.info.fields.message.set_fore(Fore.GREEN)
# success
loger.success.fields.created.set_fore(Fore.CYAN).set_default(get_time)
loger.success.fields.name.set_fore(Fore.CYAN)
loger.success.fields.levelname.set_default("SUCCESS")
loger.success.fields.owner.set_fore(Fore.CYAN)
loger.success.fields.message.set_fore(Fore.CYAN)
# warning
loger.warning.fields.created.set_fore(Fore.RED).set_default(get_time)
loger.warning.fields.name
loger.warning.fields.levelname.set_fore(Fore.MAGENTA).set_default("WARNING")
loger.warning.fields.owner.set_fore(Fore.CYAN)
loger.warning.fields.message.set_fore(Fore.YELLOW)
# error
loger.error.fields.created.set_fore(Fore.RED).set_default(get_time)
loger.error.fields.name
loger.error.fields.levelname.set_fore(Fore.MAGENTA).set_default("ERROR")
loger.error.fields.owner.set_fore(Fore.CYAN)
loger.error.fields.message.set_fore(Fore.RED)
# debug
loger.debug.fields.created.set_fore(Fore.RED).set_default(get_time)
loger.debug.fields.name
loger.debug.fields.levelname.set_fore(Fore.MAGENTA).set_default("DEBUG")
loger.debug.fields.owner.set_fore(Fore.CYAN)
loger.debug.fields.message.set_fore(Fore.MAGENTA)

VLogger = loger

if __name__ == "__main__":
    loger.warning("这里发生了警告", owner="ctpbee")
    loger.success("这里发生了成功", owner="ctpbee")
    loger.error("这里发生了错误", owner="ctpbee")
    loger.info("这里发生了信息输出", owner="ctpbee")
    loger.debug("这里发生了调试", owner="ctpbee")
