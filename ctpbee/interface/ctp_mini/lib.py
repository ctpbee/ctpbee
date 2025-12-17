import pytz
from ctpbee_api.ctp_mini import *

from ctpbee.constant import *

STATUS_MINI2VT = {
    THOST_FTDC_OAS_Submitted: Status.SUBMITTING,
    THOST_FTDC_OAS_Accepted: Status.SUBMITTING,
    THOST_FTDC_OAS_Rejected: Status.REJECTED,
    THOST_FTDC_OST_NoTradeQueueing: Status.NOTTRADED,
    THOST_FTDC_OST_PartTradedQueueing: Status.PARTTRADED,
    THOST_FTDC_OST_AllTraded: Status.ALLTRADED,
    THOST_FTDC_OST_Canceled: Status.CANCELLED,
}

DIRECTION_VT2MINI = {
    Direction.LONG: THOST_FTDC_D_Buy,
    Direction.SHORT: THOST_FTDC_D_Sell,
}
DIRECTION_MINI2VT = {v: k for k, v in DIRECTION_VT2MINI.items()}
DIRECTION_MINI2VT[THOST_FTDC_PD_Long] = Direction.LONG
DIRECTION_MINI2VT[THOST_FTDC_PD_Short] = Direction.SHORT

ORDERTYPE_VT2MINI = {
    OrderType.LIMIT: THOST_FTDC_OPT_LimitPrice,
    OrderType.MARKET: THOST_FTDC_OPT_AnyPrice,
}
ORDERTYPE_MINI2VT = {v: k for k, v in ORDERTYPE_VT2MINI.items()}

OFFSET_VT2MINI = {
    Offset.OPEN: THOST_FTDC_OF_Open,
    Offset.CLOSE: THOST_FTDC_OFEN_Close,
    Offset.CLOSETODAY: THOST_FTDC_OFEN_CloseToday,
    Offset.CLOSEYESTERDAY: THOST_FTDC_OFEN_CloseYesterday,
}
OFFSET_MINI2VT = {v: k for k, v in OFFSET_VT2MINI.items()}

EXCHANGE_MINI2VT = {
    "CFFEX": Exchange.CFFEX,
    "SHFE": Exchange.SHFE,
    "CZCE": Exchange.CZCE,
    "DCE": Exchange.DCE,
    "INE": Exchange.INE,
    "GFEX": Exchange.GFEX,
}

PRODUCT_MINI2VT = {
    THOST_FTDC_PC_Futures: Product.FUTURES,
    THOST_FTDC_PC_Options: Product.OPTION,
    THOST_FTDC_PC_Combination: Product.SPREAD,
    THOST_FTDC_PC_SpotOption: Product.OPTION,
}

OPTIONTYPE_MINI2VT = {
    THOST_FTDC_CP_CallOptions: OptionType.CALL,
    THOST_FTDC_CP_PutOptions: OptionType.PUT,
}

CHINA_TZ = pytz.timezone("Asia/Shanghai")

symbol_exchange_map = {}
symbol_name_map = {}
symbol_size_map = {}
