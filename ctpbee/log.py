"""
实现一个默认的LoggerClass<<<<<<< dev

log格式

时间 ---- 执行者 ---- 等级 ---- 信息

"""
from cologer import loger,Fore,Back,Style

loger.set_format('{time} {name}     {level}  {owner}   {message}')
# info 
loger.info.fields.time.set_fore(Fore.RED)
loger.info.fields.name
loger.info.fields.level.set_fore(Fore.MAGENTA)
loger.info.fields.owner.set_fore(Fore.CYAN)
loger.info.fields.message.set_fore(Fore.GREEN)
# success 
loger.success.fields.time.set_fore(Fore.CYAN)
loger.success.fields.name.set_fore(Fore.CYAN)
loger.success.fields.level
loger.success.fields.owner.set_fore(Fore.CYAN)
loger.success.fields.message.set_fore(Fore.CYAN)
# warning 
loger.warning.fields.time.set_fore(Fore.RED)
loger.warning.fields.name
loger.warning.fields.level.set_fore(Fore.MAGENTA)
loger.warning.fields.owner.set_fore(Fore.CYAN)
loger.warning.fields.message.set_fore(Fore.YELLOW)
# error 
loger.error.fields.time.set_fore(Fore.RED)
loger.error.fields.name
loger.error.fields.level.set_fore(Fore.MAGENTA)
loger.error.fields.owner.set_fore(Fore.CYAN)
loger.error.fields.message.set_fore(Fore.RED)
# debug 
loger.debug.fields.time.set_fore(Fore.RED)
loger.debug.fields.name
loger.debug.fields.level.set_fore(Fore.MAGENTA)
loger.debug.fields.owner.set_fore(Fore.CYAN)
loger.debug.fields.message.set_fore(Fore.MAGENTA)

VLogger = loger

if __name__ == '__main__':
    loger.warning("这里发生了警告", owner="somewheve")
    loger.success("这里发生了成功", owner="somewheve")
    loger.error("这里发生了错误", owner="somewheve")
    loger.info("这里发生了信息输出", owner="somewheve")
    loger.debug("这里发生了调试", owner="somewheve")