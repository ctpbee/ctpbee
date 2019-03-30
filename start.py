# coding:utf-8
from __future__ import print_function
import warnings
warnings.filterwarnings('ignore')
import multiprocessing
from datetime import datetime, time
from time import sleep

import sys_constant
from trade_api.catch import MainEngine
from sys_signal import log_signal, stop_signal
from md_api.mdApi import CtpMdApi
from event_engine import event_engine
from setting import CONNECT_INFO



def get_all_contract():
    engine = MainEngine()
    engine.login(CONNECT_INFO['user_id'], CONNECT_INFO['password'], CONNECT_INFO['broke_id'],
                 CONNECT_INFO['td_address'])
    sleep(1)
    engine.qry_instrument()
    sleep(1)
    log_signal.send(log_message=sys_constant.TD_CONNECTION_STATUS + str(engine.get_login_status()))
    while True:
        sleep(1)
        if len(engine.getAllContracts()) != 0:
            log_signal.send(log_message=sys_constant.CONTRACT_DATA_RECEIVED)
            break
        log_signal.send(log_message="等待数据返回", log_level=sys_constant.ERROR_LEVEL)
    contracts = engine.getAllContracts()
    log_signal.send(log_message=sys_constant.TD_CONNECTION_CLOSE)
    print("*" * 100)
    engine.close_connection()
    print("*" * 100)
    del engine

    return contracts


def tick_start(req_list):
    tick = CtpMdApi(event_engine)
    tick.connect(userID=CONNECT_INFO['user_id'], password=CONNECT_INFO['password'], brokerID=CONNECT_INFO['broke_id'],
                 address=CONNECT_INFO['md_address'])
    sleep(2)
    log_signal.send(log_message=sys_constant.MD_READY_SUBSCRIBE)
    if tick.connectionStatus:
        for r in req_list:
            tick.subscribe(r)
        log_signal.send(log_message=sys_constant.MD_SUBSCTIBE_SUCCESS)
    elif not tick.connectionStatus:
        log_signal.send(log_message=sys_constant.MD_SUBSCTIBE_FAIL, log_level=sys_constant.ERROR_LEVEL)
        import sys
        sys.exit()
    log_signal.send(log_message=sys_constant.START_SUCCESS)
    sleep(10)
    stop_signal.send(message="stop")
    while True:
        sleep(1)



# ----------------------------------- -----------------------------------
def runChildProcess():
    """子进程运行函数"""
    contracts = get_all_contract()
    tick_start(contracts)

runChildProcess()



# # ----------------------------------------------------------------------
# def runParentProcess():
#     """父进程运行函数"""
#     # 创建日志引擎
#     log_signal.send(log_message='启动行情记录守护父进程')
#     DAY_START = time(8, 57)  # 日盘启动和停止时间
#     DAY_END = time(15, 18)
#     NIGHT_START = time(20, 57)  # 夜盘启动和停止时间
#     NIGHT_END = time(2, 33)
#
#     p = None  # 子进程句柄
#
#     while True:
#         currentTime = datetime.now().time()
#         recording = False
#         # 判断当前处于的时间段
#         if ((currentTime >= DAY_START and currentTime <= DAY_END) or
#                 (currentTime >= NIGHT_START) or
#                 (currentTime <= NIGHT_END)):
#             recording = True
#
#         # 过滤周末时间段：周六全天，周五夜盘，周日日盘
#         if ((datetime.today().weekday() == 6) or
#                 (datetime.today().weekday() == 5 and currentTime > NIGHT_END) or
#                 (datetime.today().weekday() == 0 and currentTime < DAY_START)):
#             log_signal.send(log_message="时间不允许")
#             recording = False
#
#         # 记录时间则需要启动子进程
#         if recording and p is None:
#             log_signal.send(log_message='启动子进程')
#             p = multiprocessing.Process(target=runChildProcess)
#             p.start()
#             log_signal.send(log_message='子进程启动成功')
#
#         # 非记录时间则退出子进程
#         if not recording and p is not None:
#             log_signal.send(log_message='关闭子进程')
#             stop_signal.send(message="stop")
#             p.terminate()
#             p.join()
#             p = None
#             log_signal.send(log_message='子进程关闭成功')
#         sleep(5)
#
#
# if __name__ == '__main__':
#     runChildProcess()
    # runParentProcess()
