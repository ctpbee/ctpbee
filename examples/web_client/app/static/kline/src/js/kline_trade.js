import {ChartManager} from './chart_manager'

export class KlineTrade {

    static created = false;
    static instance = null;

    constructor(option) {
        this.browerState = 0;
        this.tradeDate = new Date();
        this.tradesLimit = 20;
        this.lastDepth = null;
        this.depthShowSize = 15;
        this.priceDecimalDigits = 6;
        this.amountDecimalDigits = 4;
        this.symbol = null;
        this.curPrice = null;
        this.title = "";

        Object.assign(this, option);

        if (!KlineTrade.created) {
            KlineTrade.instance = this;
            KlineTrade.created = true;
        }
        return KlineTrade.instance;
    }

    reset(symbol) {
        this.symbol = symbol;
        this.lastDepth = null;
        this.curPrice = null;
        this.klineTradeInit = false;
        $("#trades .trades_list").empty();
        $("#gasks .table").empty();
        $("#gbids .table").empty();
        $("#asks .table").empty();
        $("#bids .table").empty();
    }

    pushTrades(array) {
        let $trades = $("#trades .trades_list");
        let totalUls = "";
        for (let i = 0; i < array.length; i++) {
            let item = array[i];
            if (i >= array.length - this.tradesLimit) {
                this.tradeDate.setTime(item.time);
                let dateStr = this.dateFormatTf(this.tradeDate.getHours())
                    + ":" + this.dateFormatTf(this.tradeDate.getMinutes())
                    + ":" + this.dateFormatTf(this.tradeDate.getSeconds());
                let arr = (item.amount.toFixed(4) + "").split(".");
                let price = item.price;
                if (price > 1) {
                    price = price.toFixed(2)
                }
                if (price < 1 && price > 0.00001) {
                    price = price.toFixed(4)
                }
                if (price < 0.00001) {
                    price = price.toFixed(6)
                }

                if (this.klineTradeInit) {
                    totalUls = "<ul class='newul'><li class='tm'>" + dateStr + "</li><li class='pr-" + (item.type === 'buy' ? 'green' : 'red') + "'>" + price + "</li><li class='vl'>" + arr[0] + "<g>" + (arr.length > 1 ? '.' + arr[1] : '') + "</g></li></ul>" + totalUls;
                } else {
                    totalUls = "<ul><li class='tm'>" + dateStr + "</li><li class='pr-" + (item.type === 'buy' ? 'green' : 'red') + "'>" + price + "</li><li class='vl'>" + arr[0] + "<g>" + (arr.length > 1 ? '.' + arr[1] : '') + "</g></li></ul>" + totalUls;
                }
            }
        }
        let j = 0;
        let that = this;
        if (this.klineTradeInit) {
            clearInterval(myTime);
            let myTime = setInterval(function () {
                let item = array[j];
                //that.curPrice = item.price
                let price = Number(item.price);
                if (price > 1) {
                    price = price.toFixed(2)
                }

                if (price < 1 && price > 0.0001) {
                    price = price.toFixed(4)
                }
                if (price < 0.0001) {
                    price = price.toFixed(6)
                }
                that.curPrice = price;
                $("div#price").attr("class", item.type === 'buy' ? 'green' : 'red').text(price);
                j++;
                if (j >= array.length) {
                    clearInterval(myTime);
                }
            }, 100)
        } else {
            if (array.length > 0) {
                //this.curPrice=array[array.length-1].price.toFixed(6);
                let price = Number(array[array.length - 1].price);
                if (price > 1) {
                    price = price.toFixed(2)
                }

                if (price < 1 && price > 0.0001) {
                    price = price.toFixed(4)
                }
                if (price < 0.0001) {
                    price = price.toFixed(6)
                }
                that.curPrice = price;
                $("div#price").attr("class", array[array.length - 1].type === 'buy' ? 'green' : 'red').text(price);
            }
        }

        if (this.klineTradeInit) {
            $trades.prepend(totalUls);
        } else {
            $trades.append(totalUls);
        }
        totalUls = null;
        $trades.find("ul.newul").slideDown(1000, function () {
            $(this).removeClass("newul");
        });
        $trades.find("ul:gt(" + (this.tradesLimit - 1) + ")").remove();
    }

    updateDepth(data) {
        ChartManager.instance.getChart().updateDepth(data);
        if (!data) return;
        $("#gasks .table").html(this.getgview(this.getgasks(data.asks)));
        $("#gbids .table").html(this.getgview(this.getgbids(data.bids)));
        if (this.lastDepth === null) {
            this.lastDepth = {};
            this.lastDepth.asks = this.getAsks(data.asks, this.depthShowSize);
            this.depthInit(this.lastDepth.asks, $("#asks .table"));
            this.lastDepth.bids = this.getBids(data.bids, this.depthShowSize);
            this.depthInit(this.lastDepth.bids, $("#bids .table"));
        } else {
            let parentAsks = $("#asks .table");
            parentAsks.find("div.remove").remove();
            parentAsks.find("div.add").removeClass("add");
            let newasks = this.getAsks(data.asks, this.depthShowSize);
            let oldasks = this.lastDepth.asks;
            this.lastDepth.asks = newasks;
            this.asksAndBids(newasks.slice(0), oldasks, parentAsks);

            let parentBids = $("#bids .table");
            parentBids.find("div.remove").remove();
            parentBids.find("div.add").removeClass("add");
            let newbids = this.getBids(data.bids, this.depthShowSize);
            let oldbids = this.lastDepth.bids;
            this.lastDepth.bids = newbids;
            this.asksAndBids(newbids.slice(0), oldbids, $("#bids .table"));
        }
    }

    depthInit(data, $obj) {
        $obj.empty();
        if (data && data.length > 0) {
            let lastInt, view = "";
            for (let i = 0; i < data.length; i++) {
                let arr = (data[i][0] + "").split(".");
                let prices = this.getPrice(arr, lastInt);
                lastInt = arr[0];
                arr = (data[i][1] + "").split(".");
                let amounts = this.getAmount(arr);
                view += "<div class='row'><span class='price'>" + prices[0] + "<g>" + prices[1] + "</g></span> <span class='amount'>" + amounts[0] + "<g>" + amounts[1] + "</g></span></div>";
            }
            $obj.append(view);
            view = null;
        }
    }

    asksAndBids(addasks, oldasks, tbDiv) {
        for (let i = 0; i < oldasks.length; i++) {
            let isExist = false;
            for (let j = 0; j < addasks.length; j++) {
                if (oldasks[i][0] === addasks[j][0]) {
                    isExist = true;
                    if (oldasks[i][1] !== addasks[j][1]) {
                        let $amount = tbDiv.find("div:eq(" + i + ") .amount");
                        $amount.addClass(oldasks[i][1] > addasks[j][1] ? "red" : "green");
                        let amounts = this.getAmount((addasks[j][1] + "").split("."));
                        setTimeout((function ($amount, amounts) {
                            return function () {
                                $amount.html(amounts[0] + "<g>" + amounts[1] + "</g>");
                                $amount.removeClass("red").removeClass("green");
                                $amount = null;
                                amounts = null;
                            };
                        })($amount, amounts), 500);
                    }
                    addasks.splice(j, 1);
                    break;
                }
            }
            if (!isExist) {
                tbDiv.find("div:eq(" + i + ")").addClass("remove");
                oldasks[i][2] = -1;//标识该数据对应div被移除
            }
        }
        for (let j = 0; j < oldasks.length; j++) {
            for (let i = 0; i < addasks.length; i++) {
                if (addasks[i][0] > oldasks[j][0]) {
                    let arr = (addasks[i][1] + "").split(".");
                    let amounts = this.getAmount(arr);
                    tbDiv.find("div:eq(" + j + ")").before("<div class='row add'><span class='price'></span> <span class='amount'>" + amounts[0] + "<g>" + amounts[1] + "</g></span></div>");
                    oldasks.splice(j, 0, addasks[i]);
                    addasks.splice(i, 1);
                    break;
                }
            }
        }
        let totalDiv = "";
        for (let i = 0; i < addasks.length; i++) {
            oldasks.push(addasks[i]);
            let arr = (addasks[i][1] + "").split(".");
            let amounts = this.getAmount(arr);
            totalDiv += "<div class='row add'><span class='price'></span> <span class='amount'>" + amounts[0] + "<g>" + amounts[1] + "</g></span></div>";
        }
        if (totalDiv.length > 0) {
            tbDiv.append(totalDiv);
        }
        totalDiv = null;

        let lastInt;
        for (let i = 0; i < oldasks.length; i++) {
            let $div = tbDiv.find("div:eq(" + i + ")");
            if (!(oldasks[i].length >= 3 && oldasks[i][2] === -1)) {
                let arr = (oldasks[i][0] + "").split(".");
                let prices = this.getPrice(arr, lastInt);
                lastInt = arr[0];
                $div.find(".price").html(prices[0] + "<g>" + prices[1] + "</g>");
            }
        }
        addasks = null;
        oldasks = null;
        tbDiv.find("div.add").slideDown(800);
        setTimeout((function ($remove, $add) {
            return function () {
                $remove.slideUp(500, function () {
                    $(this).remove();
                });
                $add.removeClass("add");
            };
        })(tbDiv.find("div.remove"), tbDiv.find("div.add")), 1000);

    }

    getAsks(array, len) {
        if (array.length > len) {
            array.splice(0, array.length - len);
        }
        return array;
    }

    getBids(array, len) {
        if (array.length > len) {
            array.splice(len, array.length - 1);
        }
        return array;
    }

    getgview(g) {
        let gstr = "";
        let lastInt;
        for (let i = 0; i < g.length; i++) {
            let arr = g[i][0].split(".");
            if (arr.length === 1 || arr[0] !== lastInt) {
                gstr += "<div class='row'><span class='price'>" + g[i][0] + "</span> <span class='amount'>" + g[i][1] + "</span></div>";
                lastInt = arr[0];
            } else {
                gstr += "<div class='row'><span class='price'><h>" + arr[0] + ".</h>" + arr[1] + "</span> <span class='amount'>" + g[i][1] + "</span></div>";
            }
        }
        return gstr;
    }

    getgasks(array) {
        if (array.length < 2) {
            return [];
        }
        let low = array[array.length - 1][0];//最低价
        let high = array[0][0];//最高价
        let r = high - low;
        let block = this.getBlock(r, 100);
        let n = Math.abs(Number(Math.log(block) / Math.log(10))).toFixed(0);//精确小数位数
        if (r / block < 2) {
            block = block / 2;
            n++;
        }
        if (block >= 1) (n = 0);
        low = parseInt(low / block) * block;
        high = parseInt(high / block) * block;
        let gasks = [];
        let amount = 0;
        for (let i = array.length - 1; i >= 0; i--) {
            if (array[i][0] > low) {
                let amountInt = parseInt(amount, 10);
                if (amountInt > 0) {
                    gasks.unshift([Number(low).toFixed(n), amountInt]);
                }
                if (low >= high) {
                    break;
                }
                low += block;
            }
            amount += array[i][1];
        }
        return gasks;
    }

    getgbids(array) {
        if (array.length < 2) {
            return [];
        }
        let low = array[array.length - 1][0];
        let high = array[0][0];
        let r = high - low;
        let block = this.getBlock(r, 100);
        let n = Math.abs(Number(Math.log(block) / Math.log(10))).toFixed(0);//精确小数位数
        if (r / block < 2) {
            block = block / 2;
            n++;
        }
        if (block >= 1) (n = 0);
        low = parseInt(low / block) * block;
        high = parseInt(high / block) * block;

        let gbids = [];
        let amount = 0;
        for (let i = 0; i < array.length; i++) {
            if (array[i][0] < high) {
                let amountInt = parseInt(amount, 10);
                if (amountInt > 0) {
                    gbids.push([Number(high).toFixed(n), amountInt]);
                }
                if (high <= low) {
                    break;
                }
                high -= block;
            }
            amount += array[i][1];
        }
        return gbids;
    }

    getBlock(b, scale) {
        if (b > scale || b <= 0) {
            return scale;
        } else {
            scale = scale / 10;
            return this.getBlock(b, scale);
        }
    }

    getZeros(i) {
        let zeros = "";
        while (i > 0) {
            i--;
            zeros += "0";
        }
        return zeros;
    }

    getPrice(arr, lastInt) {
        let price1 = arr[0];
        if (lastInt === price1) {
            price1 = "<h>" + price1 + ".</h>";
        } else {
            price1 += ".";
        }
        let price2 = "";
        if (arr.length === 1) {
            price1 += "0";
            price2 = this.getZeros(this.priceDecimalDigits - 1);
        } else {
            price1 += arr[1];
            price2 = this.getZeros(this.priceDecimalDigits - arr[1].length);
        }
        return [price1, price2];
    }

    getAmount(arr) {
        let amount1 = arr[0];
        let amount2 = "";
        let zerosLen = this.amountDecimalDigits - amount1.length + 1;
        if (zerosLen > 0) {
            amount2 = ".";
            if (arr.length === 1) {
                amount2 += this.getZeros(zerosLen);
            } else if (zerosLen > arr[1].length) {
                amount2 += arr[1] + this.getZeros(zerosLen - arr[1].length);
            } else if (zerosLen === arr[1].length) {
                amount2 += arr[1];
            } else {
                amount2 += arr[1].substring(0, zerosLen);
            }
        }
        return [amount1, amount2];
    }

    dateFormatTf(i) {
        return (i < 10 ? '0' : '') + i;
    }

}