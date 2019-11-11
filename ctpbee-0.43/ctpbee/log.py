from colour_printing.custom import PrintMe

VLogger = PrintMe
"""
实现一个默认的LoggerClass<<<<<<< dev

log格式

时间 ---- 执行者 ---- 等级 ---- 信息

"""

if __name__ == '__main__':
    from ctpbee.cprint_config import CP
    logger_me = VLogger(CP)

    # logger_me.set_formatter("handler")
    logger_me.warning("这里发生了警告", owner="somewheve")
    logger_me.error("这里发生了错误", owner="somewheve")
    logger_me.info("这里发生了信息输出", owner="somewheve")
    logger_me.debug("这里发生了调试", owner="somewheve")
