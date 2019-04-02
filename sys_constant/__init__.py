# coding:utf-8

LOG_LEVEL = "INFO"
ERROR_LEVEL = "ERROR"

ERROR_FORMAT = "\033[31;31;0m{0}\t{1} :\t{2:{4}<5}\t{3:{4}<5}"
LOG_FORMAT = "\033[36;34;0m{0}\t{1} :\t{2:{4}<5}\t{3:{4}<5}"

# encoding: UTF-8

LOADING_ERROR = 'Error occurred when loading the config file, please check.'
CONFIG_KEY_MISSING = 'Key missing in the config file, please check.'

DATA_SERVER_CONNECTED = '数据服务器连接.'

DATA_SERVER_DISCONNECTED = '数据服务器断开连接'
DATA_SERVER_LOGIN = '数据服务器登录完成.'
DATA_SERVER_LOGOUT = '数据服务器注销完成'

TRADING_SERVER_CONNECTED = '交易服务器连接.'
TRADING_SERVER_DISCONNECTED = '交易服务器断开连接'
TRADING_SERVER_AUTHENTICATED = '交易服务器身份验证.'
TRADING_SERVER_LOGIN = '交易伺服器登入完成'
TRADING_SERVER_LOGOUT = '交易服务器注销完成'

SETTLEMENT_INFO_CONFIRMED = '结算信息确认'
CONTRACT_DATA_RECEIVED = '收到合约数据'
EVENT_BAR = "ebar"
EVENT_STOP = "estop"

TD_LOGIN_FAIL = "交易服务器登录失败"
TD_CONNECTION_CLOSE = "关闭交易服务器链接"
TD_CONNECTION_STATUS = "交易服务器连接状态:"


MD_LOGIN_FAIL = "行情服务器登录失败"
MD_READY_SUBSCRIBE = "准备订阅新的数据"
MD_SUBSCTIBE_SUCCESS = "成功订阅"
MD_SUBSCTIBE_FAIL = "订阅失败"

EXIT_INFO = "退出当前子进程,强制生成ｋ线"

START_SUCCESS = "启动成功"