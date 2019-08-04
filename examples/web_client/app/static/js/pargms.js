var tick_map = {
    "ask_price_1": "买一价",
    "ask_volume_1": "买一量",
    "bid_price_1": "卖一价",
    "bid_volume_1": "卖一量",
    "last_price": "最新价格",
    "local_symbol": "本地id",
    "exchange": "交易所",
    "open_interest": "持仓量",
    "pre_close": "昨日收盘价",
    "volume": "成交量",
    "datetime": "时间",
};
var tick_par_array = [];
for (key in tick_map) {
    tick_par_array.push(key);
}
