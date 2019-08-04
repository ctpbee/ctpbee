function order(direction, symbol, url_route) {
    // 发单函数
    price = $("#send_price").val();
    volume = $("#volume").val();
    type = $("#type").val();

    // 判断是否填写价格和手数
    if (price === "" || volume === "") {
        alertMsg("请保持价格和手数完整", "err");
        return
    }
    var detail_info = JSON.parse(localStorage.getItem(symbol));
    var exchange = detail_info['exchange'];
    // 生成发单请求
    req = {
        "direction": direction,
        "offset": "open",
        "price": price,
        "volume": volume,
        "type": type,
        "exchange": exchange,
        "local_symbol": symbol
    };

    // ajax进行发单
    $.ajax({
        dataType: "json",
        method: "POST",
        data: req,
        url: url_route,
        success: function (data) {
            console.log(data);
            if (data['result'] === "failed")
                alertMsg("下单失败 原因: " + data['message'], "err");
            else {
                alertMsg(data['message'])
            }
        },
        error: function (err) {
            alertMsg(err)
        }
    })
}

function close_position() {
    // 平仓函数
    // 获取当前 symbol
    // 获取当前价格
    // 获取当前手数
    // 获取方向
    // offset自适应
}

function cancle_order() {
    // 获取id
    // 获取local_symbol
    // 获取交易所

}