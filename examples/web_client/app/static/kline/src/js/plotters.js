import Kline from './kline'
import {NamedObject} from './named_object'
import {ChartManager} from './chart_manager'
import {Util} from './util'
import {CPoint} from './cpoint'
import * as exprs from './exprs'
import * as themes from './themes'
import * as data_providers from './data_providers'
import * as data_sources from './data_sources'
import * as ctools from './ctools'


export class Plotter extends NamedObject {

    static isChrome = (navigator.userAgent.toLowerCase().match(/chrome/) !== null);

    constructor(name) {
        super(name);
    }

    static drawLine(context, x1, y1, x2, y2) {
        context.beginPath();
        context.moveTo((x1 << 0) + 0.5, (y1 << 0) + 0.5);
        context.lineTo((x2 << 0) + 0.5, (y2 << 0) + 0.5);
        context.stroke();
    }

    static drawLines(context, points) {
        let i, cnt = points.length;
        context.beginPath();
        context.moveTo(points[0].x, points[0].y);
        for (i = 1; i < cnt; i++)
            context.lineTo(points[i].x, points[i].y);
        if (Plotter.isChrome) {
            context.moveTo(points[0].x, points[0].y);
            for (i = 1; i < cnt; i++)
                context.lineTo(points[i].x, points[i].y);
        }
        context.stroke();
    }

    static drawDashedLine(context, x1, y1, x2, y2, dashLen, dashSolid) {
        if (dashLen < 2) {
            dashLen = 2;
        }
        let dX = x2 - x1;
        let dY = y2 - y1;
        context.beginPath();
        if (dY === 0) {
            let count = (dX / dashLen + 0.5) << 0;
            for (let i = 0; i < count; i++) {
                context.rect(x1, y1, dashSolid, 1);
                x1 += dashLen;
            }
            context.fill();
        } else {
            let count = (Math.sqrt(dX * dX + dY * dY) / dashLen + 0.5) << 0;
            dX = dX / count;
            dY = dY / count;
            let dashX = dX * dashSolid / dashLen;
            let dashY = dY * dashSolid / dashLen;
            for (let i = 0; i < count; i++) {
                context.moveTo(x1 + 0.5, y1 + 0.5);
                context.lineTo(x1 + 0.5 + dashX, y1 + 0.5 + dashY);
                x1 += dX;
                y1 += dY;
            }
            context.stroke();
        }
    }

    static createHorzDashedLine(context, x1, x2, y, dashLen, dashSolid) {
        if (dashLen < 2) {
            dashLen = 2;
        }
        let dX = x2 - x1;
        let count = (dX / dashLen + 0.5) << 0;
        for (let i = 0; i < count; i++) {
            context.rect(x1, y, dashSolid, 1);
            x1 += dashLen;
        }
    }

    static createRectangles(context, rects) {
        context.beginPath();
        let e, i, cnt = rects.length;
        for (i = 0; i < cnt; i++) {
            e = rects[i];
            context.rect(e.x, e.y, e.w, e.h);
        }
    }

    static createPolygon(context, points) {
        context.beginPath();
        context.moveTo(points[0].x + 0.5, points[0].y + 0.5);
        let i, cnt = points.length;
        for (i = 1; i < cnt; i++)
            context.lineTo(points[i].x + 0.5, points[i].y + 0.5);
        context.closePath();
    }

    static drawString(context, str, rect) {
        let w = context.measureText(str).width;
        if (rect.w < w) {
            return false;
        }
        context.fillText(str, rect.x, rect.y);
        rect.x += w;
        rect.w -= w;
        return true;
    }

}


export class BackgroundPlotter extends Plotter {

    constructor(name) {
        super(name);
        this._color = themes.Theme.Color.Background;
    }

    getColor() {
        return this._color;
    }

    setColor(c) {
        this._color = c;
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        let theme = mgr.getTheme(this.getFrameName());
        context.fillStyle = theme.getColor(this._color);
        context.fillRect(area.getLeft(), area.getTop(), area.getWidth(), area.getHeight());
    }

}


export class MainAreaBackgroundPlotter extends BackgroundPlotter {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        let range = mgr.getRange(this.getAreaName());
        let theme = mgr.getTheme(this.getFrameName());
        let rect = area.getRect();
        if (!area.isChanged() && !timeline.isUpdated() && !range.isUpdated()) {
            let first = timeline.getFirstIndex();
            let last = timeline.getLastIndex() - 2;
            let start = Math.max(first, last);
            rect.X = timeline.toColumnLeft(start);
            rect.Width = area.getRight() - rect.X;
        }
        context.fillStyle = theme.getColor(this._color);
        context.fillRect(rect.X, rect.Y, rect.Width, rect.Height);
    }

}


export class RangeAreaBackgroundPlotter extends BackgroundPlotter {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let areaName = this.getAreaName();
        let area = mgr.getArea(areaName);
        let range = mgr.getRange(areaName.substring(0, areaName.lastIndexOf("Range")));
        let isMainRange = range.getNameObject().getCompAt(2) === "main";
        if (!isMainRange && !area.isChanged() && !range.isUpdated()) {
            return;
        }
        let theme = mgr.getTheme(this.getFrameName());
        context.fillStyle = theme.getColor(this._color);
        context.fillRect(area.getLeft(), area.getTop(), area.getWidth(), area.getHeight());
    }

}


export class TimelineAreaBackgroundPlotter extends BackgroundPlotter {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        if (!area.isChanged() && !timeline.isUpdated())
            return;
        let theme = mgr.getTheme(this.getFrameName());
        context.fillStyle = theme.getColor(this._color);
        context.fillRect(area.getLeft(), area.getTop(), area.getWidth(), area.getHeight());
    }

}


export class CGridPlotter extends NamedObject {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        let range = mgr.getRange(this.getAreaName());
        let clipped = false;
        if (!area.isChanged() && !timeline.isUpdated() && !range.isUpdated()) {
            let first = timeline.getFirstIndex();
            let last = timeline.getLastIndex();
            let start = Math.max(first, last - 2);
            let left = timeline.toColumnLeft(start);
            context.save();
            context.rect(left, area.getTop(), area.getRight() - left, area.getHeight());
            context.clip();
            clipped = true;
        }
        let theme = mgr.getTheme(this.getFrameName());
        context.fillStyle = theme.getColor(themes.Theme.Color.Grid0);
        context.beginPath();
        let dashLen = 4,
            dashSolid = 1;
        if (Plotter.isChrome) {
            dashLen = 4;
            dashSolid = 1;
        }
        let gradations = range.getGradations();
        for (let n in gradations) {
            Plotter.createHorzDashedLine(context, area.getLeft(), area.getRight(), range.toY(gradations[n]), dashLen, dashSolid);
        }
        context.fill();
        if (clipped) {
            context.restore();
        }
    }

}


export class CandlestickPlotter extends NamedObject {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let ds = mgr.getDataSource(this.getDataSourceName());
        if (ds.getDataCount() < 1) {
            return;
        }
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        let range = mgr.getRange(this.getAreaName());
        if (range.getRange() === 0.0) {
            return;
        }
        let theme = mgr.getTheme(this.getFrameName());
        let dark = Util.isInstance(theme, themes.DarkTheme);
        let first = timeline.getFirstIndex();
        let last = timeline.getLastIndex();
        let start;
        if (area.isChanged() || timeline.isUpdated() || range.isUpdated())
            start = first;
        else
            start = Math.max(first, last - 2);
        let cW = timeline.getColumnWidth();
        let iW = timeline.getItemWidth();
        let left = timeline.toItemLeft(start);
        let center = timeline.toItemCenter(start);
        let strokePosRects = [];
        let fillPosRects = [];
        let fillUchRects = [];
        let fillNegRects = [];
        for (let i = start; i < last; i++) {
            let data = ds.getDataAt(i);
            let high = range.toY(data.high);
            let low = range.toY(data.low);
            let open = data.open;
            let close = data.close;
            if (close > open) {
                let top = range.toY(close);
                let bottom = range.toY(open);
                let iH = Math.max(bottom - top, 1);
                if (iH > 1 && iW > 1 && dark)
                    strokePosRects.push({x: left + 0.5, y: top + 0.5, w: iW - 1, h: iH - 1});
                else
                    fillPosRects.push({x: left, y: top, w: Math.max(iW, 1), h: Math.max(iH, 1)});
                if (data.high > close) {
                    high = Math.min(high, top - 1);
                    fillPosRects.push({x: center, y: high, w: 1, h: top - high});
                }
                if (open > data.low) {
                    low = Math.max(low, bottom + 1);
                    fillPosRects.push({x: center, y: bottom, w: 1, h: low - bottom});
                }
            } else if (close === open) {
                let top = range.toY(close);
                fillUchRects.push({x: left, y: top, w: Math.max(iW, 1), h: 1});
                if (data.high > close)
                    high = Math.min(high, top - 1);
                if (open > data.low)
                    low = Math.max(low, top + 1);
                if (high < low)
                    fillUchRects.push({x: center, y: high, w: 1, h: low - high});
            } else {
                let top = range.toY(open);
                let bottom = range.toY(close);
                let iH = Math.max(bottom - top, 1);
                fillNegRects.push({x: left, y: top, w: Math.max(iW, 1), h: Math.max(iH, 1)});
                if (data.high > open)
                    high = Math.min(high, top - 1);
                if (close > data.low)
                    low = Math.max(low, bottom + 1);
                if (high < low)
                    fillNegRects.push({x: center, y: high, w: 1, h: low - high});
            }
            left += cW;
            center += cW;
        }
        if (strokePosRects.length > 0) {
            context.strokeStyle = theme.getColor(themes.Theme.Color.Positive);
            Plotter.createRectangles(context, strokePosRects);
            context.stroke();
        }
        if (fillPosRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Positive);
            Plotter.createRectangles(context, fillPosRects);
            context.fill();
        }
        if (fillUchRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Negative);
            Plotter.createRectangles(context, fillUchRects);
            context.fill();
        }
        if (fillNegRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Negative);
            Plotter.createRectangles(context, fillNegRects);
            context.fill();
        }
    }

}


export class CandlestickHLCPlotter extends Plotter {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let ds = mgr.getDataSource(this.getDataSourceName());
        if (!Util.isInstance(ds, data_sources.MainDataSource) || ds.getDataCount() < 1) {
            return;
        }
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        let range = mgr.getRange(this.getAreaName());
        if (range.getRange() === 0.0) {
            return;
        }
        let theme = mgr.getTheme(this.getFrameName());
        let dark = Util.isInstance(theme, themes.DarkTheme);
        let first = timeline.getFirstIndex();
        let last = timeline.getLastIndex();
        let start;
        if (area.isChanged() || timeline.isUpdated() || range.isUpdated()) {
            start = first;
        } else {
            start = Math.max(first, last - 2);
        }
        let cW = timeline.getColumnWidth();
        let iW = timeline.getItemWidth();
        let left = timeline.toItemLeft(start);
        let center = timeline.toItemCenter(start);
        let strokePosRects = [];
        let fillPosRects = [];
        let fillUchRects = [];
        let fillNegRects = [];
        for (let i = start; i < last; i++) {
            let data = ds.getDataAt(i);
            let high = range.toY(data.high);
            let low = range.toY(data.low);
            let open = data.open;
            if (i > 0) {
                open = ds.getDataAt(i - 1).close;
            }
            let close = data.close;
            if (close > open) {
                let top = range.toY(close);
                let bottom = range.toY(open);
                let iH = Math.max(bottom - top, 1);
                if (iH > 1 && iW > 1 && dark) {
                    strokePosRects.push({x: left + 0.5, y: top + 0.5, w: iW - 1, h: iH - 1});
                } else {
                    fillPosRects.push({x: left, y: top, w: Math.max(iW, 1), h: Math.max(iH, 1)});
                }
                if (data.high > close) {
                    high = Math.min(high, top - 1);
                    fillPosRects.push({x: center, y: high, w: 1, h: top - high});
                }
                if (open > data.low) {
                    low = Math.max(low, bottom + 1);
                    fillPosRects.push({x: center, y: bottom, w: 1, h: low - bottom});
                }
            } else if (close === open) {
                let top = range.toY(close);
                fillUchRects.push({x: left, y: top, w: Math.max(iW, 1), h: 1});
                if (data.high > close) {
                    high = Math.min(high, top - 1);
                }
                if (open > data.low) {
                    low = Math.max(low, top + 1);
                }
                if (high < low) {
                    fillUchRects.push({x: center, y: high, w: 1, h: low - high});
                }
            } else {
                let top = range.toY(open);
                let bottom = range.toY(close);
                let iH = Math.max(bottom - top, 1);
                fillNegRects.push({x: left, y: top, w: Math.max(iW, 1), h: Math.max(iH, 1)});
                if (data.high > open) {
                    high = Math.min(high, top - 1);
                }
                if (close > data.low) {
                    low = Math.max(low, bottom + 1);
                }
                if (high < low) {
                    fillNegRects.push({x: center, y: high, w: 1, h: low - high});
                }
            }
            left += cW;
            center += cW;
        }
        if (strokePosRects.length > 0) {
            context.strokeStyle = theme.getColor(themes.Theme.Color.Positive);
            Plotter.createRectangles(context, strokePosRects);
            context.stroke();
        }
        if (fillPosRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Positive);
            Plotter.createRectangles(context, fillPosRects);
            context.fill();
        }
        if (fillUchRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Negative);
            Plotter.createRectangles(context, fillUchRects);
            context.fill();
        }
        if (fillNegRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Negative);
            Plotter.createRectangles(context, fillNegRects);
            context.fill();
        }
    }

}


export class OHLCPlotter extends Plotter {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let ds = mgr.getDataSource(this.getDataSourceName());
        if (!Util.isInstance(ds, data_sources.MainDataSource) || ds.getDataCount() < 1) {
            return;
        }
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        let range = mgr.getRange(this.getAreaName());
        if (range.getRange() === 0.0) {
            return;
        }
        let theme = mgr.getTheme(this.getFrameName());
        let first = timeline.getFirstIndex();
        let last = timeline.getLastIndex();
        let start;
        if (area.isChanged() || timeline.isUpdated() || range.isUpdated()) {
            start = first;
        } else {
            start = Math.max(first, last - 2);
        }
        let cW = timeline.getColumnWidth();
        let iW = timeline.getItemWidth() >> 1;
        let left = timeline.toItemLeft(start);
        let center = timeline.toItemCenter(start);
        let right = left + timeline.getItemWidth();
        let fillPosRects = [];
        let fillUchRects = [];
        let fillNegRects = [];
        for (let i = start; i < last; i++) {
            let data = ds.getDataAt(i);
            let high = range.toY(data.high);
            let low = range.toY(data.low);
            let iH = Math.max(low - high, 1);
            if (data.close > data.open) {
                let top = range.toY(data.close);
                let bottom = range.toY(data.open);
                fillPosRects.push({x: center, y: high, w: 1, h: iH});
                fillPosRects.push({x: left, y: top, w: iW, h: 1});
                fillPosRects.push({x: center, y: bottom, w: iW, h: 1});
            } else if (data.close === data.open) {
                let y = range.toY(data.close);
                fillUchRects.push({x: center, y: high, w: 1, h: iH});
                fillUchRects.push({x: left, y: y, w: iW, h: 1});
                fillUchRects.push({x: center, y: y, w: iW, h: 1});
            } else {
                let top = range.toY(data.open);
                let bottom = range.toY(data.close);
                fillNegRects.push({x: center, y: high, w: 1, h: iH});
                fillNegRects.push({x: left, y: top, w: iW, h: 1});
                fillNegRects.push({x: center, y: bottom, w: iW, h: 1});
            }
            left += cW;
            center += cW;
            right += cW;
        }
        if (fillPosRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Positive);
            Plotter.createRectangles(context, fillPosRects);
            context.fill();
        }
        if (fillUchRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Negative);
            Plotter.createRectangles(context, fillUchRects);
            context.fill();
        }
        if (fillNegRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Negative);
            Plotter.createRectangles(context, fillNegRects);
            context.fill();
        }
    };

}


export class MainInfoPlotter extends Plotter {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        let ds = mgr.getDataSource(this.getDataSourceName());
        let theme = mgr.getTheme(this.getFrameName());
        context.font = theme.getFont(themes.Theme.Font.Default);
        context.textAlign = "left";
        context.textBaseline = "top";
        context.fillStyle = theme.getColor(themes.Theme.Color.Text4);
        let rect = {
            x: area.getLeft() + 4,
            y: area.getTop() + 2,
            w: area.getWidth() - 8,
            h: 20
        };
        let selIndex = timeline.getSelectedIndex();
        if (selIndex < 0)
            return;
        let data = ds.getDataAt(selIndex);
        let digits = ds.getDecimalDigits();
        let time = new Date(data.date);
        let year = time.getFullYear();
        let month = Util.formatTime(time.getMonth() + 1);
        let date = Util.formatTime(time.getDate());
        let hour = Util.formatTime(time.getHours());
        let minute = Util.formatTime(time.getMinutes());
        let lang = mgr.getLanguage();
        if (lang === "zh-cn") {
            // if (!Plotter.drawString(context, '时间: ' +
            //         year + '-' + month + '-' + date + '  ' + hour + ':' + minute, rect))
            //     return;
            if (!Plotter.drawString(context, '  开: ' + data.open.toFixed(digits), rect))
                return;
            if (!Plotter.drawString(context, '  高: ' + data.high.toFixed(digits), rect))
                return;
            if (!Plotter.drawString(context, '  低: ' + data.low.toFixed(digits), rect))
                return;
            if (!Plotter.drawString(context, '  收: ' + data.close.toFixed(digits), rect))
                return;
        } else if (lang === "en-us") {
            // if (!Plotter.drawString(context, 'DATE: ' +
            //         year + '-' + month + '-' + date + '  ' + hour + ':' + minute, rect))
            //     return;
            if (!Plotter.drawString(context, '  O: ' + data.open.toFixed(digits), rect))
                return;
            if (!Plotter.drawString(context, '  H: ' + data.high.toFixed(digits), rect))
                return;
            if (!Plotter.drawString(context, '  L: ' + data.low.toFixed(digits), rect))
                return;
            if (!Plotter.drawString(context, '  C: ' + data.close.toFixed(digits), rect))
                return;
        } else if (lang === "zh-tw") {
            // if (!Plotter.drawString(context, '時間: ' +
            //         year + '-' + month + '-' + date + '  ' + hour + ':' + minute, rect))
            //     return;
            if (!Plotter.drawString(context, '  開: ' + data.open.toFixed(digits), rect))
                return;
            if (!Plotter.drawString(context, '  高: ' + data.high.toFixed(digits), rect))
                return;
            if (!Plotter.drawString(context, '  低: ' + data.low.toFixed(digits), rect))
                return;
            if (!Plotter.drawString(context, '  收: ' + data.close.toFixed(digits), rect))
                return;
        }
        if (selIndex > 0) {
            if (lang === "zh-cn") {
                if (!Plotter.drawString(context, '  涨幅: ', rect))
                    return;
            } else if (lang === "en-us") {
                if (!Plotter.drawString(context, '  CHANGE: ', rect))
                    return;
            } else if (lang === "zh-tw") {
                if (!Plotter.drawString(context, '  漲幅: ', rect))
                    return;
            }
            let prev = ds.getDataAt(selIndex - 1);
            let change;
            if ((data.close - prev.close) / prev.close * 100.0) {
                change = (data.close - prev.close) / prev.close * 100.0;
            } else {
                change = 0.00;
            }


            if (change >= 0) {
                change = ' ' + change.toFixed(2);
                context.fillStyle = theme.getColor(themes.Theme.Color.TextPositive);
            } else {
                change = change.toFixed(2);
                context.fillStyle = theme.getColor(themes.Theme.Color.TextNegative);
            }
            if (!Plotter.drawString(context, change, rect))
                return;
            context.fillStyle = theme.getColor(themes.Theme.Color.Text4);
            if (!Plotter.drawString(context, ' %', rect))
                return;
        }

        let amplitude;
        if ((data.high - data.low) / data.low * 100.0) {
            amplitude = (data.high - data.low) / data.low * 100.0;
        } else {
            amplitude = 0.00;
        }

        if (lang === "zh-cn") {
            if (!Plotter.drawString(context, '  振幅: ' + amplitude.toFixed(2) + ' %', rect)) {
                return;
            }
            // if (!Plotter.drawString(context, '  量: ' + data.volume.toFixed(2), rect)) {
            //     return;
            // }
        } else if (lang === "en-us") {
            if (!Plotter.drawString(context, '  AMPLITUDE: ' + amplitude.toFixed(2) + ' %', rect)) {
                return;
            }
            // if (!Plotter.drawString(context, '  V: ' + data.volume.toFixed(2), rect)) {
            //     return;
            // }
        } else if (lang === "zh-tw") {
            if (!Plotter.drawString(context, '  振幅: ' + amplitude.toFixed(2) + ' %', rect)) {
                return;
            }
            // if (!Plotter.drawString(context, '  量: ' + data.volume.toFixed(2), rect)) {
            //     return;
            // }
        }
        let dp = mgr.getDataProvider(this.getAreaName() + ".secondary");
        if (dp === undefined) {
            return;
        }
        let indic = dp.getIndicator();
        let n, cnt = indic.getOutputCount();
        for (n = 0; n < cnt; n++) {
            let out = indic.getOutputAt(n);
            let v = out.execute(selIndex);
            if (isNaN(v)) {
                continue;
            }
            let info = "  " + out.getName() + ": " + v.toFixed(digits);
            let color = out.getColor();
            if (color === undefined) {
                color = themes.Theme.Color.Indicator0 + n;
            }
            context.fillStyle = theme.getColor(color);
            if (!Plotter.drawString(context, info, rect)) {
                return;
            }
        }
    }

}


export class IndicatorPlotter extends NamedObject {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        let range = mgr.getRange(this.getAreaName());
        if (range.getRange() === 0.0)
            return;
        let dp = mgr.getDataProvider(this.getName());
        if (!Util.isInstance(dp, data_providers.IndicatorDataProvider))
            return;
        let theme = mgr.getTheme(this.getFrameName());
        let cW = timeline.getColumnWidth();
        let first = timeline.getFirstIndex();
        let last = timeline.getLastIndex();
        let start;
        if (area.isChanged() || timeline.isUpdated() || range.isUpdated())
            start = first;
        else
            start = Math.max(first, last - 2);
        let indic = dp.getIndicator();
        let out, n, outCount = indic.getOutputCount();
        for (n = 0; n < outCount; n++) {
            out = indic.getOutputAt(n);
            let style = out.getStyle();
            if (style === exprs.OutputExpr.outputStyle.VolumeStick) {
                this.drawVolumeStick(context, theme,
                    mgr.getDataSource(this.getDataSourceName()), start, last,
                    timeline.toItemLeft(start), cW, timeline.getItemWidth(), range);
            } else if (style === exprs.OutputExpr.outputStyle.MACDStick) {
                this.drawMACDStick(context, theme,
                    out, start, last,
                    timeline.toItemLeft(start), cW, timeline.getItemWidth(), range);
            } else if (style === exprs.OutputExpr.outputStyle.SARPoint) {
                this.drawSARPoint(context, theme,
                    out, start, last,
                    timeline.toItemCenter(start), cW, timeline.getItemWidth(), range);
            }
        }
        let left = timeline.toColumnLeft(start);
        let center = timeline.toItemCenter(start);
        context.save();
        context.rect(left, area.getTop(), area.getRight() - left, area.getHeight());
        context.clip();
        context.translate(0.5, 0.5);
        for (n = 0; n < outCount; n++) {
            let x = center;
            out = indic.getOutputAt(n);
            if (out.getStyle() === exprs.OutputExpr.outputStyle.Line) {
                let v, points = [];
                if (start > first) {
                    v = out.execute(start - 1);
                    if (isNaN(v) === false)
                        points.push({"x": x - cW, "y": range.toY(v)});
                }
                for (let i = start; i < last; i++, x += cW) {
                    v = out.execute(i);
                    if (isNaN(v) === false)
                        points.push({"x": x, "y": range.toY(v)});
                }
                if (points.length > 0) {
                    let color = out.getColor();
                    if (color === undefined)
                        color = themes.Theme.Color.Indicator0 + n;
                    context.strokeStyle = theme.getColor(color);
                    Plotter.drawLines(context, points);
                }
            }
        }
        context.restore();
    }

    drawVolumeStick(context, theme, ds, first, last, startX, cW, iW, range) {
        let dark = Util.isInstance(theme, themes.DarkTheme);
        let left = startX;
        let bottom = range.toY(0);
        let strokePosRects = [];
        let fillPosRects = [];
        let fillNegRects = [];
        for (let i = first; i < last; i++) {
            let data = ds.getDataAt(i);
            let top = range.toY(data.volume);
            let iH = range.toHeight(data.volume);
            if (data.close > data.open) {
                if (iH > 1 && iW > 1 && dark) {
                    strokePosRects.push({x: left + 0.5, y: top + 0.5, w: iW - 1, h: iH - 1});
                } else {
                    fillPosRects.push({x: left, y: top, w: Math.max(iW, 1), h: Math.max(iH, 1)});
                }
            } else if (data.close === data.open) {
                if (i > 0 && data.close >= ds.getDataAt(i - 1).close) {
                    if (iH > 1 && iW > 1 && dark) {
                        strokePosRects.push({x: left + 0.5, y: top + 0.5, w: iW - 1, h: iH - 1});
                    } else {
                        fillPosRects.push({x: left, y: top, w: Math.max(iW, 1), h: Math.max(iH, 1)});
                    }
                } else {
                    fillNegRects.push({x: left, y: top, w: Math.max(iW, 1), h: Math.max(iH, 1)});
                }
            } else {
                fillNegRects.push({x: left, y: top, w: Math.max(iW, 1), h: Math.max(iH, 1)});
            }
            left += cW;
        }
        if (strokePosRects.length > 0) {
            context.strokeStyle = theme.getColor(themes.Theme.Color.Positive);
            Plotter.createRectangles(context, strokePosRects);
            context.stroke();
        }
        if (fillPosRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Positive);
            Plotter.createRectangles(context, fillPosRects);
            context.fill();
        }
        if (fillNegRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Negative);
            Plotter.createRectangles(context, fillNegRects);
            context.fill();
        }
    }

    drawMACDStick(context, theme, output, first, last, startX, cW, iW, range) {
        let left = startX;
        let middle = range.toY(0);
        let strokePosRects = [];
        let strokeNegRects = [];
        let fillPosRects = [];
        let fillNegRects = [];
        let prevMACD = (first > 0) ? output.execute(first - 1) : NaN;
        for (let i = first; i < last; i++) {
            let MACD = output.execute(i);
            if (MACD >= 0) {
                let iH = range.toHeight(MACD);
                if ((i === 0 || MACD >= prevMACD) && iH > 1 && iW > 1)
                    strokePosRects.push({x: left + 0.5, y: middle - iH + 0.5, w: iW - 1, h: iH - 1});
                else
                    fillPosRects.push({x: left, y: middle - iH, w: Math.max(iW, 1), h: Math.max(iH, 1)});
            } else {
                let iH = range.toHeight(-MACD);
                if ((i === 0 || MACD >= prevMACD) && iH > 1 && iW > 1)
                    strokeNegRects.push({x: left + 0.5, y: middle + 0.5, w: iW - 1, h: iH - 1});
                else
                    fillNegRects.push({x: left, y: middle, w: Math.max(iW, 1), h: Math.max(iH, 1)});
            }
            prevMACD = MACD;
            left += cW;
        }
        if (strokePosRects.length > 0) {
            context.strokeStyle = theme.getColor(themes.Theme.Color.Positive);
            Plotter.createRectangles(context, strokePosRects);
            context.stroke();
        }
        if (strokeNegRects.length > 0) {
            context.strokeStyle = theme.getColor(themes.Theme.Color.Negative);
            Plotter.createRectangles(context, strokeNegRects);
            context.stroke();
        }
        if (fillPosRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Positive);
            Plotter.createRectangles(context, fillPosRects);
            context.fill();
        }
        if (fillNegRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Negative);
            Plotter.createRectangles(context, fillNegRects);
            context.fill();
        }
    }

    drawSARPoint(context, theme, output, first, last, startX, cW, iW, range) {
        let r = iW >> 1;
        if (r < 0.5) r = 0.5;
        if (r > 4) r = 4;
        let center = startX;
        let right = center + r;
        let endAngle = 2 * Math.PI;
        context.save();
        context.translate(0.5, 0.5);
        context.strokeStyle = theme.getColor(themes.Theme.Color.Indicator3);
        context.beginPath();
        for (let i = first; i < last; i++) {
            let y = range.toY(output.execute(i));
            context.moveTo(right, y);
            context.arc(center, y, r, 0, endAngle);
            center += cW;
            right += cW;
        }
        context.stroke();
        context.restore();
    }

}


export class IndicatorInfoPlotter extends Plotter {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        let dp = mgr.getDataProvider(this.getAreaName() + ".secondary");
        let theme = mgr.getTheme(this.getFrameName());
        context.font = theme.getFont(themes.Theme.Font.Default);
        context.textAlign = "left";
        context.textBaseline = "top";
        context.fillStyle = theme.getColor(themes.Theme.Color.Text4);
        let rect = {
            x: area.getLeft() + 4,
            y: area.getTop() + 2,
            w: area.getWidth() - 8,
            h: 20
        };
        let indic = dp.getIndicator();
        let title;
        switch (indic.getParameterCount()) {
            case 0:
                title = indic.getName();
                break;
            case 1:
                title = indic.getName() + "(" +
                    indic.getParameterAt(0).getValue() +
                    ")";
                break;
            case 2:
                title = indic.getName() + "(" +
                    indic.getParameterAt(0).getValue() + "," +
                    indic.getParameterAt(1).getValue() +
                    ")";
                break;
            case 3:
                title = indic.getName() + "(" +
                    indic.getParameterAt(0).getValue() + "," +
                    indic.getParameterAt(1).getValue() + "," +
                    indic.getParameterAt(2).getValue() +
                    ")";
                break;
            case 4:
                title = indic.getName() + "(" +
                    indic.getParameterAt(0).getValue() + "," +
                    indic.getParameterAt(1).getValue() + "," +
                    indic.getParameterAt(2).getValue() + "," +
                    indic.getParameterAt(3).getValue() +
                    ")";
                break;
            default:
                return;
        }
        if (!Plotter.drawString(context, title, rect))
            return;
        let selIndex = timeline.getSelectedIndex();
        if (selIndex < 0)
            return;
        let out, v, info, color;
        let n, cnt = indic.getOutputCount();
        for (n = 0; n < cnt; n++) {
            out = indic.getOutputAt(n);
            v = out.execute(selIndex);
            if (isNaN(v))
                continue;
            info = "  " + out.getName() + ": " + v.toFixed(2);
            color = out.getColor();
            if (color === undefined)
                color = themes.Theme.Color.Indicator0 + n;
            context.fillStyle = theme.getColor(color);
            if (!Plotter.drawString(context, info, rect))
                return;
        }
    }

}


export class MinMaxPlotter extends NamedObject {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let ds = mgr.getDataSource(this.getDataSourceName());
        if (ds.getDataCount() < 1)
            return;
        let timeline = mgr.getTimeline(this.getDataSourceName());
        if (timeline.getInnerWidth() < timeline.getColumnWidth())
            return;
        let range = mgr.getRange(this.getAreaName());
        if (range.getRange() === 0)
            return;
        let dp = mgr.getDataProvider(this.getAreaName() + ".main");
        let first = timeline.getFirstIndex();
        let center = (first + timeline.getLastIndex()) >> 1;
        let theme = mgr.getTheme(this.getFrameName());
        context.font = theme.getFont(themes.Theme.Font.Default);
        context.textBaseline = "middle";
        context.fillStyle = theme.getColor(themes.Theme.Color.Text4);
        context.strokeStyle = theme.getColor(themes.Theme.Color.Text4);
        let digits = ds.getDecimalDigits();
        this.drawMark(context, dp.getMinValue(), digits, range.toY(dp.getMinValue()),
            first, center, dp.getMinValueIndex(), timeline);
        this.drawMark(context, dp.getMaxValue(), digits, range.toY(dp.getMaxValue()),
            first, center, dp.getMaxValueIndex(), timeline);
    }

    drawMark(context, v, digits, y, first, center, index, timeline) {
        let arrowStart, arrowStop, _arrowStop;
        let textStart;
        if (index > center) {
            context.textAlign = "right";
            arrowStart = timeline.toItemCenter(index) - 4;
            arrowStop = arrowStart - 7;
            _arrowStop = arrowStart - 3;
            textStart = arrowStop - 4;
        } else {
            context.textAlign = "left";
            arrowStart = timeline.toItemCenter(index) + 4;
            arrowStop = arrowStart + 7;
            _arrowStop = arrowStart + 3;
            textStart = arrowStop + 4;
        }
        Plotter.drawLine(context, arrowStart, y, arrowStop, y);
        Plotter.drawLine(context, arrowStart, y, _arrowStop, y + 2);
        Plotter.drawLine(context, arrowStart, y, _arrowStop, y - 2);
        context.fillText(Util.fromFloat(v, digits), textStart, y);
    }

}


export class TimelinePlotter extends Plotter {

    static TP_MINUTE = 60 * 1000;
    static TP_HOUR = 60 * TimelinePlotter.TP_MINUTE;
    static TP_DAY = 24 * TimelinePlotter.TP_HOUR;

    static TIME_INTERVAL = [
        5 * TimelinePlotter.TP_MINUTE,
        10 * TimelinePlotter.TP_MINUTE,
        15 * TimelinePlotter.TP_MINUTE,
        30 * TimelinePlotter.TP_MINUTE,
        TimelinePlotter.TP_HOUR,
        2 * TimelinePlotter.TP_HOUR,
        3 * TimelinePlotter.TP_HOUR,
        6 * TimelinePlotter.TP_HOUR,
        12 * TimelinePlotter.TP_HOUR,
        TimelinePlotter.TP_DAY,
        2 * TimelinePlotter.TP_DAY
    ];

    static MonthConvert = {
        1: "Jan.",
        2: "Feb.",
        3: "Mar.",
        4: "Apr.",
        5: "May.",
        6: "Jun.",
        7: "Jul.",
        8: "Aug.",
        9: "Sep.",
        10: "Oct.",
        11: "Nov.",
        12: "Dec."
    };

    constructor(name) {
        super(name);
    }

    Draw(context) {

        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        if (!area.isChanged() && !timeline.isUpdated())
            return;
        let ds = mgr.getDataSource(this.getDataSourceName());
        if (ds.getDataCount() < 2)
            return;
        let timeInterval = ds.getDataAt(1).date - ds.getDataAt(0).date;
        let n, cnt = TimelinePlotter.TIME_INTERVAL.length;
        for (n = 0; n < cnt; n++) {
            if (timeInterval < TimelinePlotter.TIME_INTERVAL[n])
                break;
        }
        for (; n < cnt; n++) {
            if (TimelinePlotter.TIME_INTERVAL[n] % timeInterval === 0)
                if ((TimelinePlotter.TIME_INTERVAL[n] / timeInterval) * timeline.getColumnWidth() > 60)
                    break;
        }
        let first = timeline.getFirstIndex();
        let last = timeline.getLastIndex();
        let d = new Date();
        let local_utc_diff = d.getTimezoneOffset() * 60 * 1000;
        let theme = mgr.getTheme(this.getFrameName());
        context.font = theme.getFont(themes.Theme.Font.Default);
        context.textAlign = "center";
        context.textBaseline = "middle";
        let lang = mgr.getLanguage();
        let gridRects = [];
        let top = area.getTop();
        let middle = area.getMiddle();
        for (let i = first; i < last; i++) {
            let utcDate = ds.getDataAt(i).date;
            let localDate = utcDate - local_utc_diff;
            let time = new Date(utcDate);
            let year = time.getFullYear();
            let month = time.getMonth() + 1;
            let date = time.getDate();
            let hour = time.getHours();
            let minute = time.getMinutes();
            let text = "";
            if (n < cnt) {
                let m = Math.max(
                    TimelinePlotter.TP_DAY,
                    TimelinePlotter.TIME_INTERVAL[n]);
                if (localDate % m === 0) {
                    if (lang === "zh-cn")
                        text = month.toString() + "月" + date.toString() + "日";
                    else if (lang === "zh-tw")
                        text = month.toString() + "月" + date.toString() + "日";
                    else if (lang === "en-us")
                        text = TimelinePlotter.MonthConvert[month] + " " + date.toString();
                    context.fillStyle = theme.getColor(themes.Theme.Color.Text4);
                } else if (localDate % TimelinePlotter.TIME_INTERVAL[n] === 0) {
                    let strMinute = minute.toString();
                    if (minute < 10)
                        strMinute = "0" + strMinute;
                    text = hour.toString() + ":" + strMinute;
                    context.fillStyle = theme.getColor(themes.Theme.Color.Text2);
                }
            } else if (date === 1 && (hour < (timeInterval / TimelinePlotter.TP_HOUR))) {
                if (month === 1) {
                    text = year.toString();
                    if (lang === "zh-cn")
                        text += "年";
                    else if (lang === "zh-tw")
                        text += "年";
                } else {
                    if (lang === "zh-cn")
                        text = month.toString() + "月";
                    else if (lang === "zh-tw")
                        text = month.toString() + "月";
                    else if (lang === "en-us")
                        text = TimelinePlotter.MonthConvert[month];
                }
                context.fillStyle = theme.getColor(themes.Theme.Color.Text4);
            }
            if (text.length > 0) {
                let x = timeline.toItemCenter(i);
                gridRects.push({x: x, y: top, w: 1, h: 4});
                context.fillText(text, x, middle);
            }
        }
        if (gridRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Grid1);
            Plotter.createRectangles(context, gridRects);
            context.fill();
        }
    }

}


export class RangePlotter extends NamedObject {

    constructor(name) {
        super(name);
    }

    getRequiredWidth(context, v) {
        let mgr = ChartManager.instance;
        let theme = mgr.getTheme(this.getFrameName());
        context.font = theme.getFont(themes.Theme.Font.Default);
        return context.measureText((Math.floor(v) + 0.88).toString()).width + 16;
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let areaName = this.getAreaName();
        let area = mgr.getArea(areaName);
        let rangeName = areaName.substring(0, areaName.lastIndexOf("Range"));
        let range = mgr.getRange(rangeName);
        if (range.getRange() === 0.0)
            return;
        let isMainRange = range.getNameObject().getCompAt(2) === "main";
        if (isMainRange) {
        } else {
            if (!area.isChanged() && !range.isUpdated())
                return;
        }
        let gradations = range.getGradations();
        if (gradations.length === 0)
            return;
        let left = area.getLeft();
        let right = area.getRight();
        let center = area.getCenter();
        let theme = mgr.getTheme(this.getFrameName());
        context.font = theme.getFont(themes.Theme.Font.Default);
        context.textAlign = "center";
        context.textBaseline = "middle";
        context.fillStyle = theme.getColor(themes.Theme.Color.Text2);
        let gridRects = [];
        for (let n in gradations) {
            let y = range.toY(gradations[n]);
            gridRects.push({x: left, y: y, w: 6, h: 1});
            gridRects.push({x: right - 6, y: y, w: 6, h: 1});
            context.fillText(Util.fromFloat(gradations[n], 2), center, y);
        }
        if (gridRects.length > 0) {
            context.fillStyle = theme.getColor(themes.Theme.Color.Grid1);
            Plotter.createRectangles(context, gridRects);
            context.fill();
        }
    }

}


export class COrderGraphPlotter extends NamedObject {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        return this._Draw_(context);
    }

    _Draw_(context) {
        if (this.Update() === false) return;
        if (this.updateData() === false) return;
        this.m_top = this.m_pArea.getTop();
        this.m_bottom = this.m_pArea.getBottom();
        this.m_left = this.m_pArea.getLeft();
        this.m_right = this.m_pArea.getRight();
        context.save();
        context.rect(this.m_left, this.m_top, this.m_right - this.m_left, this.m_bottom - this.m_top);
        context.clip();
        let all = ChartManager.instance.getChart()._depthData;
        this.x_offset = 0;
        this.y_offset = 0;
        let ask_tmp = {};
        let bid_tmp = {};
        ask_tmp.x = this.m_left + all.array[this.m_ask_si].amounts * this.m_Step;
        ask_tmp.y = this.m_pRange.toY(all.array[this.m_ask_si].rate);
        bid_tmp.x = this.m_left + all.array[this.m_bid_si].amounts * this.m_Step;
        bid_tmp.y = this.m_pRange.toY(all.array[this.m_bid_si].rate);
        if (Math.abs(ask_tmp.y - bid_tmp.y) < 1) {
            this.y_offset = 1;
        }
        this.x_offset = 1;
        this.DrawBackground(context);
        this.UpdatePoints();
        this.FillBlack(context);
        this.DrawGradations(context);
        this.DrawLine(context);
        context.restore();
    }

    DrawBackground(context) {
        context.fillStyle = this.m_pTheme.getColor(themes.Theme.Color.Background);
        context.fillRect(this.m_left, this.m_top, this.m_right - this.m_left, this.m_bottom - this.m_top);
        let all = ChartManager.instance.getChart()._depthData;
        if (this.m_mode === 0) {
            let ask_bottom = this.m_pRange.toY(all.array[this.m_ask_si].rate) - this.y_offset;
            let bid_top = this.m_pRange.toY(all.array[this.m_bid_si].rate) + this.y_offset;
            let ask_gradient = context.createLinearGradient(this.m_left, 0, this.m_right, 0);
            ask_gradient.addColorStop(0, this.m_pTheme.getColor(themes.Theme.Color.Background));
            ask_gradient.addColorStop(1, this.m_pTheme.getColor(themes.Theme.Color.PositiveDark));
            context.fillStyle = ask_gradient;
            context.fillRect(this.m_left, this.m_top, this.m_right - this.m_left, ask_bottom - this.m_top);
            let bid_gradient = context.createLinearGradient(this.m_left, 0, this.m_right, 0);
            bid_gradient.addColorStop(0, this.m_pTheme.getColor(themes.Theme.Color.Background));
            bid_gradient.addColorStop(1, this.m_pTheme.getColor(themes.Theme.Color.NegativeDark));
            context.fillStyle = bid_gradient;
            context.fillRect(this.m_left, bid_top, this.m_right - this.m_left, this.m_bottom - bid_top);
        } else if (this.m_mode === 1) {
            let ask_gradient = context.createLinearGradient(this.m_left, 0, this.m_right, 0);
            ask_gradient.addColorStop(0, this.m_pTheme.getColor(themes.Theme.Color.Background));
            ask_gradient.addColorStop(1, this.m_pTheme.getColor(themes.Theme.Color.PositiveDark));
            context.fillStyle = ask_gradient;
            context.fillRect(this.m_left, this.m_top, this.m_right - this.m_left, this.m_bottom - this.m_top);
        } else if (this.m_mode === 2) {
            let bid_gradient = context.createLinearGradient(this.m_left, 0, this.m_right, 0);
            bid_gradient.addColorStop(0, this.m_pTheme.getColor(themes.Theme.Color.Background));
            bid_gradient.addColorStop(1, this.m_pTheme.getColor(themes.Theme.Color.NegativeDark));
            context.fillStyle = bid_gradient;
            context.fillRect(this.m_left, this.m_top, this.m_right - this.m_left, this.m_bottom - this.m_top);
        }
    }

    DrawLine(context) {
        if (this.m_mode === 0 || this.m_mode === 1) {
            context.strokeStyle = this.m_pTheme.getColor(themes.Theme.Color.Positive);
            context.beginPath();
            context.moveTo(Math.floor(this.m_ask_points[0].x) + 0.5, Math.floor(this.m_ask_points[0].y) + 0.5);
            for (let i = 1; i < this.m_ask_points.length; i++) {
                context.lineTo(Math.floor(this.m_ask_points[i].x) + 0.5, Math.floor(this.m_ask_points[i].y) + 0.5);
            }
            context.stroke();
        }
        if (this.m_mode === 0 || this.m_mode === 2) {
            context.strokeStyle = this.m_pTheme.getColor(themes.Theme.Color.Negative);
            context.beginPath();
            context.moveTo(this.m_bid_points[0].x + 0.5, this.m_bid_points[0].y + 0.5);
            for (let i = 1; i < this.m_bid_points.length; i++) {
                context.lineTo(this.m_bid_points[i].x + 0.5, this.m_bid_points[i].y + 0.5);
            }
            context.stroke();
        }
    }

    UpdatePoints() {
        let all = ChartManager.instance.getChart()._depthData;
        this.m_ask_points = [];
        let index_ask = {};
        index_ask.x = Math.floor(this.m_left);
        index_ask.y = Math.floor(this.m_pRange.toY(all.array[this.m_ask_si].rate) - this.y_offset);
        this.m_ask_points.push(index_ask);
        let ask_p_i = 0;
        for (let i = this.m_ask_si; i >= this.m_ask_ei; i--) {
            let index0 = {};
            let index1 = {};
            if (i === this.m_ask_si) {
                index0.x = Math.floor(this.m_left + all.array[i].amounts * this.m_Step + this.x_offset);
                index0.y = Math.floor(this.m_pRange.toY(all.array[i].rate) - this.y_offset);
                this.m_ask_points.push(index0);
                ask_p_i = 1;
            } else {
                index0.x = Math.floor(this.m_left + all.array[i].amounts * this.m_Step + this.x_offset);
                index0.y = Math.floor(this.m_ask_points[ask_p_i].y);
                index1.x = Math.floor(index0.x);
                index1.y = Math.floor(this.m_pRange.toY(all.array[i].rate) - this.y_offset);
                this.m_ask_points.push(index0);
                ask_p_i++;
                this.m_ask_points.push(index1);
                ask_p_i++;
            }
        }
        this.m_bid_points = [];
        let index_bid = {};
        index_bid.x = Math.floor(this.m_left);
        index_bid.y = Math.ceil(this.m_pRange.toY(all.array[this.m_bid_si].rate) + this.y_offset);
        this.m_bid_points.push(index_bid);
        let bid_p_i = 0;
        for (let i = this.m_bid_si; i <= this.m_bid_ei; i++) {
            let index0 = {};
            let index1 = {};
            if (i === this.m_bid_si) {
                index0.x = Math.floor(this.m_left + all.array[i].amounts * this.m_Step + this.x_offset);
                index0.y = Math.ceil(this.m_pRange.toY(all.array[i].rate) + this.y_offset);
                this.m_bid_points.push(index0);
                bid_p_i = 1;
            } else {
                index0.x = Math.floor(this.m_left + all.array[i].amounts * this.m_Step + this.x_offset);
                index0.y = Math.ceil(this.m_bid_points[bid_p_i].y);
                index1.x = Math.floor(index0.x);
                index1.y = Math.ceil(this.m_pRange.toY(all.array[i].rate) + this.x_offset);
                this.m_bid_points.push(index0);
                bid_p_i++;
                this.m_bid_points.push(index1);
                bid_p_i++;
            }
        }
    }

    updateData() {
        let all = ChartManager.instance.getChart()._depthData;
        if (all.array === null) return false;
        if (all.array.length <= 50) return false;
        let minRange = this.m_pRange.getOuterMinValue();
        let maxRange = this.m_pRange.getOuterMaxValue();
        this.m_ask_si = all.asks_si;
        this.m_ask_ei = all.asks_si;
        for (let i = all.asks_si; i >= all.asks_ei; i--) {
            if (all.array[i].rate < maxRange)
                this.m_ask_ei = i;
            else
                break;
        }
        this.m_bid_si = all.bids_si;
        this.m_bid_ei = all.bids_si;
        for (let i = all.bids_si; i <= all.bids_ei; i++) {
            if (all.array[i].rate > minRange)
                this.m_bid_ei = i;
            else
                break;
        }
        if (this.m_ask_ei === this.m_ask_si)
            this.m_mode = 2;
        else if (this.m_bid_ei === this.m_bid_si)
            this.m_mode = 1;
        else
            this.m_mode = 0;
        this.m_Step = this.m_pArea.getWidth();
        if (this.m_mode === 0) {
            /*
             * View: B     --------    T
             * Data: Lo      -----     Hi
             */
            if (this.m_ask_ei === all.asks_ei && this.m_bid_ei === all.bids_ei) {
                this.m_Step /= Math.min(all.array[this.m_ask_ei].amounts,
                    all.array[this.m_bid_ei].amounts);
            }
            /*
             * View: B     --------     T
             * Data: Lo         -----   Hi
             */
            else if (this.m_ask_ei !== all.asks_ei && this.m_bid_ei === all.bids_ei) {
                this.m_Step /= all.array[this.m_bid_ei].amounts;
            }
            /*
             * View: B     --------    T
             * Data: Lo  -----         Hi
             */
            else if (this.m_ask_ei === all.asks_ei && this.m_bid_ei !== all.bids_ei) {
                this.m_Step /= all.array[this.m_ask_ei].amounts;
            }
            /*
             * View: B     --------    T
             * Data: Lo  ------------  Hi
             */
            else if (this.m_ask_ei !== all.asks_ei && this.m_bid_ei !== all.bids_ei) {
                this.m_Step /= Math.max(all.array[this.m_ask_ei].amounts,
                    all.array[this.m_bid_ei].amounts);
            }
        } else if (this.m_mode === 1) {
            this.m_Step /= all.array[this.m_ask_ei].amounts;
        } else if (this.m_mode === 2) {
            this.m_Step /= all.array[this.m_bid_ei].amounts;
        }
        return true;
    }

    Update() {
        this.m_pMgr = ChartManager.instance;
        let areaName = this.getAreaName();
        this.m_pArea = this.m_pMgr.getArea(areaName);
        if (this.m_pArea === null)
            return false;
        let rangeName = areaName.substring(0, areaName.lastIndexOf("Range"));
        this.m_pRange = this.m_pMgr.getRange(rangeName);
        if (this.m_pRange === null || this.m_pRange.getRange() === 0.0)
            return false;
        this.m_pTheme = this.m_pMgr.getTheme(this.getFrameName());
        if (this.m_pTheme === null) {
            return false;
        }
        return true;
    }

    DrawGradations(context) {
        let mgr = ChartManager.instance;
        let areaName = this.getAreaName();
        let area = mgr.getArea(areaName);
        let rangeName = areaName.substring(0, areaName.lastIndexOf("Range"));
        let range = mgr.getRange(rangeName);
        if (range.getRange() === 0.0)
            return;
        let gradations = range.getGradations();
        if (gradations.length === 0)
            return;
        let left = area.getLeft();
        let right = area.getRight();
        let gridRects = [];
        for (let n in gradations) {
            let y = range.toY(gradations[n]);
            gridRects.push({x: left, y: y, w: 6, h: 1});
            gridRects.push({x: right - 6, y: y, w: 6, h: 1});
        }
        if (gridRects.length > 0) {
            let theme = mgr.getTheme(this.getFrameName());
            context.fillStyle = theme.getColor(themes.Theme.Color.Grid1);
            Plotter.createRectangles(context, gridRects);
            context.fill();
        }
    }

    FillBlack(context) {
        let ask_point = this.m_ask_points;
        let bid_point = this.m_bid_points;
        let ask_first_add = {};
        let ask_last_add = {};
        ask_first_add.x = this.m_right;
        ask_first_add.y = ask_point[0].y;
        ask_last_add.x = this.m_right;
        ask_last_add.y = ask_point[ask_point.length - 1].y;
        let bid_first_add = {};
        let bid_last_add = {};
        bid_first_add.x = this.m_right;
        bid_first_add.y = bid_point[0].y - 1;
        bid_last_add.x = this.m_right;
        bid_last_add.y = bid_point[bid_point.length - 1].y;
        ask_point.unshift(ask_first_add);
        ask_point.push(ask_last_add);
        bid_point.unshift(bid_first_add);
        bid_point.push(bid_last_add);
        context.fillStyle = this.m_pTheme.getColor(themes.Theme.Color.Background);
        context.beginPath();
        context.moveTo(Math.floor(ask_point[0].x) + 0.5, Math.floor(ask_point[0].y) + 0.5);
        for (let i = 1; i < ask_point.length; i++) {
            context.lineTo(Math.floor(ask_point[i].x) + 0.5, Math.floor(ask_point[i].y) + 0.5);
        }
        context.fill();
        context.beginPath();
        context.moveTo(Math.floor(bid_point[0].x) + 0.5, Math.floor(bid_point[0].y) + 0.5);
        for (let i = 1; i < bid_point.length; i++) {
            context.lineTo(Math.floor(bid_point[i].x) + 0.5, Math.floor(bid_point[i].y) + 0.5);
        }
        context.fill();
        ask_point.shift();
        ask_point.pop();
        bid_point.shift();
        bid_point.pop();
    }

    DrawTickerGraph(context) {
        // return;
        let mgr = ChartManager.instance;
        let ds = mgr.getDataSource(this.getDataSourceName());
        let ticker = ds._dataItems[ds._dataItems.length - 1].close;
        let p1x = this.m_left + 1;
        let p1y = this.m_pRange.toY(ticker);
        let p2x = p1x + 5;
        let p2y = p1y + 2.5;
        let p3x = p1x + 5;
        let p3y = p1y - 2.5;
        context.fillStyle = this.m_pTheme.getColor(themes.Theme.Color.Mark);
        context.strokeStyle = this.m_pTheme.getColor(themes.Theme.Color.Mark);
    };
}


export class LastVolumePlotter extends Plotter {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let timeline = mgr.getTimeline(this.getDataSourceName());
        let areaName = this.getAreaName();
        let area = mgr.getArea(areaName);
        let rangeName = areaName.substring(0, areaName.lastIndexOf("Range"));
        let range = mgr.getRange(rangeName);
        if (range.getRange() === 0.0)
            return;
        let ds = mgr.getDataSource(this.getDataSourceName());
        if (ds.getDataCount() < 1)
            return;
        let theme = mgr.getTheme(this.getFrameName());
        context.font = theme.getFont(themes.Theme.Font.Default);
        context.textAlign = "left";
        context.textBaseline = "middle";
        context.fillStyle = theme.getColor(themes.Theme.Color.RangeMark);
        context.strokeStyle = theme.getColor(themes.Theme.Color.RangeMark);
        let v = ds.getDataAt(ds.getDataCount() - 1).volume;
        let y = range.toY(v);
        let left = area.getLeft() + 1;
        Plotter.drawLine(context, left, y, left + 7, y);
        Plotter.drawLine(context, left, y, left + 3, y + 2);
        Plotter.drawLine(context, left, y, left + 3, y - 2);
        context.fillText(Util.fromFloat(v, 2), left + 10, y);
    }

}


export class LastClosePlotter extends Plotter {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let timeline = mgr.getTimeline(this.getDataSourceName());
        let areaName = this.getAreaName();
        let area = mgr.getArea(areaName);
        let rangeName = areaName.substring(0, areaName.lastIndexOf("Range"));
        let range = mgr.getRange(rangeName);
        if (range.getRange() === 0.0)
            return;
        let ds = mgr.getDataSource(this.getDataSourceName());
        if (ds.getDataCount() < 1)
            return;
        let v = ds._dataItems[ds._dataItems.length - 1].close;
        if (v <= range.getMinValue() || v >= range.getMaxValue())
            return;
        let theme = mgr.getTheme(this.getFrameName());
        context.font = theme.getFont(themes.Theme.Font.Default);
        context.textAlign = "left";
        context.textBaseline = "middle";
        context.fillStyle = theme.getColor(themes.Theme.Color.RangeMark);
        context.strokeStyle = theme.getColor(themes.Theme.Color.RangeMark);
        let y = range.toY(v);
        let left = area.getLeft() + 1;
        Plotter.drawLine(context, left, y, left + 7, y);
        Plotter.drawLine(context, left, y, left + 3, y + 2);
        Plotter.drawLine(context, left, y, left + 3, y - 2);
        context.fillText(Util.fromFloat(v, ds.getDecimalDigits()), left + 10, y);
    }

}


export class SelectionPlotter extends Plotter {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        if (mgr._drawingTool !== ChartManager.DrawingTool.CrossCursor) {
            return;
        }
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        if (timeline.getSelectedIndex() < 0) {
            return;
        }
        let range = mgr.getRange(this.getAreaName());
        let theme = mgr.getTheme(this.getFrameName());
        context.strokeStyle = theme.getColor(themes.Theme.Color.Cursor);
        let x = timeline.toItemCenter(timeline.getSelectedIndex());
        Plotter.drawLine(context, x, area.getTop() - 1, x, area.getBottom());
        let pos = range.getSelectedPosition();
        if (pos >= 0) {
            Plotter.drawLine(context, area.getLeft(), pos, area.getRight(), pos);
        }
    }

}


export class TimelineSelectionPlotter extends Plotter {

    static MonthConvert = {
        1: "Jan.",
        2: "Feb.",
        3: "Mar.",
        4: "Apr.",
        5: "May.",
        6: "Jun.",
        7: "Jul.",
        8: "Aug.",
        9: "Sep.",
        10: "Oct.",
        11: "Nov.",
        12: "Dec."
    };

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        let timeline = mgr.getTimeline(this.getDataSourceName());
        if (timeline.getSelectedIndex() < 0)
            return;
        let ds = mgr.getDataSource(this.getDataSourceName());
        if (!Util.isInstance(ds, data_sources.MainDataSource))
            return;
        let theme = mgr.getTheme(this.getFrameName());
        let lang = mgr.getLanguage();
        let x = timeline.toItemCenter(timeline.getSelectedIndex());
        context.fillStyle = theme.getColor(themes.Theme.Color.Background);
        context.fillRect(x - 52.5, area.getTop() + 2.5, 106, 18);
        context.strokeStyle = theme.getColor(themes.Theme.Color.Grid3);
        context.strokeRect(x - 52.5, area.getTop() + 2.5, 106, 18);
        context.font = theme.getFont(themes.Theme.Font.Default);
        context.textAlign = "center";
        context.textBaseline = "middle";
        context.fillStyle = theme.getColor(themes.Theme.Color.Text4);
        let time = new Date(ds.getDataAt(timeline.getSelectedIndex()).date);
        let month = time.getMonth() + 1;
        let date = time.getDate();
        let hour = time.getHours();
        let minute = time.getMinutes();
        let second = time.getSeconds();
        let strMonth = month.toString();
        let strDate = date.toString();
        let strHour = hour.toString();
        let strMinute = minute.toString();
        let strSecond = second.toString();
        if (minute < 10) {
            strMinute = "0" + strMinute;
        }
        if (second < 10) {
            strSecond = "0" + strSecond;
        }
        let text = "";
        if (lang === "zh-cn") {
            text = strMonth + "月" + strDate + "日  " +
                strHour + ":" + strMinute;
        } else if (lang === "zh-tw") {
            text = strMonth + "月" + strDate + "日  " +
                strHour + ":" + strMinute;
        } else if (lang === "en-us") {
            text = TimelineSelectionPlotter.MonthConvert[month] + " " + strDate + "  " +
                strHour + ":" + strMinute;
        }
        if (Kline.instance.range < 60000) {
            text += ":" + strSecond;
        }
        context.fillText(text, x, area.getMiddle());
    }

}


export class RangeSelectionPlotter extends NamedObject {

    constructor(name) {
        super(name);
    }

    Draw(context) {
        let mgr = ChartManager.instance;
        let areaName = this.getAreaName();
        let area = mgr.getArea(areaName);
        let timeline = mgr.getTimeline(this.getDataSourceName());
        if (timeline.getSelectedIndex() < 0) {
            return;
        }
        let rangeName = areaName.substring(0, areaName.lastIndexOf("Range"));
        let range = mgr.getRange(rangeName);
        if (range.getRange() === 0.0 || range.getSelectedPosition() < 0) {
            return;
        }
        let v = range.getSelectedValue();
        if (v === -Number.MAX_VALUE) {
            return;
        }
        let y = range.getSelectedPosition();
        Plotter.createPolygon(context, [
            {"x": area.getLeft(), "y": y},
            {"x": area.getLeft() + 5, "y": y + 10},
            {"x": area.getRight() - 3, "y": y + 10},
            {"x": area.getRight() - 3, "y": y - 10},
            {"x": area.getLeft() + 5, "y": y - 10}
        ]);
        let theme = mgr.getTheme(this.getFrameName());
        context.fillStyle = theme.getColor(themes.Theme.Color.Background);
        context.fill();
        context.strokeStyle = theme.getColor(themes.Theme.Color.Grid4);
        context.stroke();
        context.font = theme.getFont(themes.Theme.Font.Default);
        context.textAlign = "center";
        context.textBaseline = "middle";
        context.fillStyle = theme.getColor(themes.Theme.Color.Text3);
        let digits = 2;
        if (range.getNameObject().getCompAt(2) === "main") {
            digits = mgr.getDataSource(this.getDataSourceName()).getDecimalDigits();
        }
        context.fillText(Util.fromFloat(v, digits), area.getCenter(), y);
    }

}


export class CToolPlotter extends NamedObject {

    constructor(name, toolObject) {
        super(name);
        this.toolObject = toolObject;
        let pMgr = ChartManager.instance;
        let pArea = pMgr.getArea('frame0.k0.main');
        if (pArea === null) {
            this.areaPos = {
                left: 0,
                top: 0,
                right: 0,
                bottom: 0
            };
            return;
        }
        this.areaPos = {
            left: pArea.getLeft(),
            top: pArea.getTop(),
            right: pArea.getRight(),
            bottom: pArea.getBottom()
        };
        this.crossPt = {};
        this.normalSize = 4;
        this.selectedSize = 6;
        this.cursorLen = 4;
        this.cursorGapLen = 3;
        this.theme = ChartManager.instance.getTheme(this.getFrameName());
    }

    drawCursor(context) {
        this.drawCrossCursor(context);
    }

    drawCrossCursor(context) {
        context.strokeStyle = this.theme.getColor(themes.Theme.Color.LineColorNormal);
        context.fillStyle = this.theme.getColor(themes.Theme.Color.LineColorNormal);
        let tempPt = this.toolObject.getPoint(0).getPosXY();
        if (tempPt === null) {
            return;
        }
        let x = tempPt.x;
        let y = tempPt.y;
        let cursorLen = this.cursorLen;
        let cursorGapLen = this.cursorGapLen;
        context.fillRect(x, y, 1, 1);
        Plotter.drawLine(context, x - cursorLen - cursorGapLen, y, x - cursorGapLen, y);
        Plotter.drawLine(context, x + cursorLen + cursorGapLen, y, x + cursorGapLen, y);
        Plotter.drawLine(context, x, y - cursorLen - cursorGapLen, x, y - cursorGapLen);
        Plotter.drawLine(context, x, y + cursorLen + cursorGapLen, x, y + cursorGapLen);
    }

    drawCircle(context, center, radius) {
        let centerX = center.x;
        let centerY = center.y;
        context.beginPath();
        context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
        context.fillStyle = this.theme.getColor(themes.Theme.Color.CircleColorFill);
        context.fill();
        context.stroke();
    }

    drawCtrlPt(context) {
        context.strokeStyle = this.theme.getColor(themes.Theme.Color.CircleColorStroke);
        for (let i = 0; i < this.ctrlPtsNum; i++) {
            this.drawCircle(context, this.ctrlPts[1][i], this.normalSize);
        }
    }

    highlightCtrlPt(context) {
        context.strokeStyle = this.theme.getColor(themes.Theme.Color.CircleColorStroke);
        for (let i = 0; i < this.ctrlPtsNum; i++) {
            if (this.toolObject.getPoint(i).getState() === CPoint.state.Highlight)
                this.drawCircle(context, this.ctrlPts[1][i], this.selectedSize);
        }
    }

    drawFibRayLines(context, startPoint, endPoint) {
        for (let i = 0; i < this.fiboFansSequence.length; i++) {
            let stageY = startPoint.y + (100 - this.fiboFansSequence[i]) / 100 * (endPoint.y - startPoint.y);
            let tempStartPt = {x: startPoint.x, y: startPoint.y};
            let tempEndPt = {x: endPoint.x, y: stageY};
            this.drawRayLines(context, tempStartPt, tempEndPt);
        }
    }

    drawRayLines(context, startPoint, endPoint) {
        this.getAreaPos();
        let tempStartPt = {x: startPoint.x, y: startPoint.y};
        let tempEndPt = {x: endPoint.x, y: endPoint.y};
        let crossPt = this.getRectCrossPt(this.areaPos, tempStartPt, tempEndPt);
        let tempCrossPt;
        if (endPoint.x === startPoint.x) {
            if (endPoint.y === startPoint.y) {
                tempCrossPt = endPoint;
            } else {
                tempCrossPt = endPoint.y > startPoint.y ? {x: crossPt[1].x, y: crossPt[1].y} : {
                    x: crossPt[0].x,
                    y: crossPt[0].y
                };
            }
        } else {
            tempCrossPt = endPoint.x > startPoint.x ? {x: crossPt[1].x, y: crossPt[1].y} : {
                x: crossPt[0].x,
                y: crossPt[0].y
            };
        }
        Plotter.drawLine(context, startPoint.x, startPoint.y, tempCrossPt.x, tempCrossPt.y);
    }

    lenBetweenPts(pt1, pt2) {
        return Math.sqrt(Math.pow((pt2.x - pt1.x), 2) + Math.pow((pt2.y - pt1.y), 2));
    }

    getCtrlPts() {
        for (let i = 0; i < this.ctrlPtsNum; i++) {
            this.ctrlPts[0][i] = this.toolObject.getPoint(i);
        }
    }

    updateCtrlPtPos() {
        for (let i = 0; i < this.ctrlPtsNum; i++) {
            this.ctrlPts[1][i] = this.ctrlPts[0][i].getPosXY();
        }
    }

    getAreaPos() {
        let pMgr = ChartManager.instance;
        let pArea = pMgr.getArea('frame0.k0.main');
        if (pArea === null) {
            this.areaPos = {
                left: 0,
                top: 0,
                right: 0,
                bottom: 0
            };
            return;
        }
        this.areaPos = {
            left: Math.floor(pArea.getLeft()),
            top: Math.floor(pArea.getTop()),
            right: Math.floor(pArea.getRight()),
            bottom: Math.floor(pArea.getBottom())
        };
    }

    updateDraw(context) {
        context.strokeStyle = this.theme.getColor(themes.Theme.Color.LineColorNormal);
        this.draw(context);
        this.drawCtrlPt(context);
    }

    finishDraw(context) {
        context.strokeStyle = this.theme.getColor(themes.Theme.Color.LineColorNormal);
        this.draw(context);
    }

    highlight(context) {
        context.strokeStyle = this.theme.getColor(themes.Theme.Color.LineColorSelected);
        this.draw(context);
        this.drawCtrlPt(context);
        this.highlightCtrlPt(context);
    }

}


export class DrawStraightLinesPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name, toolObject);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 2;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.getAreaPos();
        this.startPoint = this.ctrlPts[1][0];
        this.endPoint = this.ctrlPts[1][1];
        if (this.startPoint.x === this.endPoint.x && this.startPoint.y === this.endPoint.y) {
            Plotter.drawLine(context, this.areaPos.left, this.startPoint.y, this.areaPos.right, this.startPoint.y);
        } else {
            this.crossPt = this.getRectCrossPt(this.areaPos, this.startPoint, this.endPoint);
            Plotter.drawLine(context, this.crossPt[0].x, this.crossPt[0].y, this.crossPt[1].x, this.crossPt[1].y);
        }
    }

}


export class DrawSegLinesPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name, toolObject);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 2;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.startPoint = this.ctrlPts[1][0];
        this.endPoint = this.ctrlPts[1][1];
        if (this.startPoint.x === this.endPoint.x && this.startPoint.y === this.endPoint.y) {
            this.endPoint.x += 1;
        }
        Plotter.drawLine(context, this.startPoint.x, this.startPoint.y, this.endPoint.x, this.endPoint.y);
    }

}


export class DrawRayLinesPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 2;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.getAreaPos();
        this.startPoint = this.ctrlPts[1][0];
        this.endPoint = this.ctrlPts[1][1];
        if (this.startPoint.x === this.endPoint.x && this.startPoint.y === this.endPoint.y) {
            this.endPoint.x += 1;
        }
        this.drawRayLines(context, this.startPoint, this.endPoint);
    }

}


export class DrawArrowLinesPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name, toolObject);
        this.toolObject = toolObject;
        this.arrowSizeRatio = 0.03;
        this.arrowSize = 4;
        this.crossPt = {x: -1, y: -1};
        this.ctrlPtsNum = 2;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    drawArrow(context, startPoint, endPoint) {
        let len = this.lenBetweenPts(startPoint, endPoint);
        let vectorA = [endPoint.x - startPoint.x, endPoint.y - startPoint.y];
        this.crossPt.x = startPoint.x + (1 - this.arrowSize / len) * vectorA[0];
        this.crossPt.y = startPoint.y + (1 - this.arrowSize / len) * vectorA[1];
        let vectorAautho = [-vectorA[1], vectorA[0]];
        let Aautho = {x: vectorAautho[0], y: vectorAautho[1]};
        let origin = {x: 0, y: 0};
        vectorAautho[0] = this.arrowSize * Aautho.x / this.lenBetweenPts(Aautho, origin);
        vectorAautho[1] = this.arrowSize * Aautho.y / this.lenBetweenPts(Aautho, origin);
        let arrowEndPt = [this.crossPt.x + vectorAautho[0], this.crossPt.y + vectorAautho[1]];
        Plotter.drawLine(context, endPoint.x, endPoint.y, arrowEndPt[0], arrowEndPt[1]);
        arrowEndPt = [this.crossPt.x - vectorAautho[0], this.crossPt.y - vectorAautho[1]];
        Plotter.drawLine(context, endPoint.x, endPoint.y, arrowEndPt[0], arrowEndPt[1]);
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.startPoint = this.ctrlPts[1][0];
        this.endPoint = this.ctrlPts[1][1];
        if (this.startPoint.x === this.endPoint.x && this.startPoint.y === this.endPoint.y) {
            this.endPoint.x += 1;
        }
        Plotter.drawLine(context, this.startPoint.x, this.startPoint.y, this.endPoint.x, this.endPoint.y);
        this.drawArrow(context, this.startPoint, this.endPoint);
    }

}


export class DrawHoriStraightLinesPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 1;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.getAreaPos();
        this.startPoint = this.ctrlPts[1][0];
        Plotter.drawLine(context, this.areaPos.left, this.startPoint.y, this.areaPos.right, this.startPoint.y);
    }

}


export class DrawHoriRayLinesPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 2;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.getAreaPos();
        this.startPoint = this.ctrlPts[1][0];
        this.endPoint = this.ctrlPts[1][1];
        if (this.startPoint.x === this.endPoint.x) {
            Plotter.drawLine(context, this.startPoint.x, this.startPoint.y, this.areaPos.right, this.startPoint.y);
        } else {
            let tempEndPt = {x: this.endPoint.x, y: this.startPoint.y};
            this.drawRayLines(context, this.startPoint, tempEndPt);
        }
    }

}


export class DrawHoriSegLinesPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name, toolObject);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 2;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.startPoint = this.ctrlPts[1][0];
        this.endPoint = this.ctrlPts[1][1];
        this.endPoint.y = this.startPoint.y;
        if (this.startPoint.x === this.endPoint.x && this.startPoint.y === this.endPoint.y) {
            Plotter.drawLine(context, this.startPoint.x, this.startPoint.y, this.endPoint.x + 1, this.startPoint.y);
        } else {
            Plotter.drawLine(context, this.startPoint.x, this.startPoint.y, this.endPoint.x, this.startPoint.y);
        }
    }

}


export class DrawVertiStraightLinesPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 1;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.getAreaPos();
        this.startPoint = this.ctrlPts[1][0];
        Plotter.drawLine(context, this.startPoint.x, this.areaPos.top, this.startPoint.x, this.areaPos.bottom);
    }

}


export class DrawPriceLinesPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 1;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    draw(context) {
        context.font = "12px Tahoma";
        context.textAlign = "left";
        context.fillStyle = this.theme.getColor(themes.Theme.Color.LineColorNormal);
        this.updateCtrlPtPos();
        this.getAreaPos();
        this.startPoint = this.ctrlPts[1][0];
        let text = this.ctrlPts[0][0].getPosIV().v;
        Plotter.drawLine(context, this.startPoint.x, this.startPoint.y, this.areaPos.right, this.startPoint.y);
        context.fillText(text.toFixed(2), this.startPoint.x + 2, this.startPoint.y - 15);
    }

}


export class ParallelLinesPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name);
        this.toolObject = toolObject;
    }

    getParaPt() {
        let vectorA = [];
        vectorA[0] = this.endPoint.x - this.startPoint.x;
        vectorA[1] = this.endPoint.y - this.startPoint.y;
        let vectorB = [];
        vectorB[0] = this.paraStartPoint.x - this.startPoint.x;
        vectorB[1] = this.paraStartPoint.y - this.startPoint.y;
        this.paraEndPoint = {x: -1, y: -1};
        this.paraEndPoint.x = vectorA[0] + vectorB[0] + this.startPoint.x;
        this.paraEndPoint.y = vectorA[1] + vectorB[1] + this.startPoint.y;
    }

}


export class DrawBiParallelLinesPlotter extends ParallelLinesPlotter {

    constructor(name, toolObject) {
        super(name, toolObject);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 3;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.getAreaPos();
        this.startPoint = this.ctrlPts[1][0];
        this.paraStartPoint = this.ctrlPts[1][1];
        this.endPoint = this.ctrlPts[1][2];
        this.getParaPt();
        this.getAreaPos();
        this.crossPt0 = this.getRectCrossPt(this.areaPos, this.startPoint, this.endPoint);
        Plotter.drawLine(context, this.crossPt0[0].x, this.crossPt0[0].y, this.crossPt0[1].x, this.crossPt0[1].y);
        this.crossPt1 = this.getRectCrossPt(this.areaPos, this.paraStartPoint, this.paraEndPoint);
        Plotter.drawLine(context, this.crossPt1[0].x, this.crossPt1[0].y, this.crossPt1[1].x, this.crossPt1[1].y);
    }

}


export class DrawBiParallelRayLinesPlotter extends ParallelLinesPlotter {

    constructor(name, toolObject) {
        super(name, toolObject);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 3;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.getAreaPos();
        this.startPoint = this.ctrlPts[1][0];
        this.paraStartPoint = this.ctrlPts[1][1];
        this.endPoint = this.ctrlPts[1][2];
        if (this.startPoint.x === this.endPoint.x && this.startPoint.y === this.endPoint.y) {
            this.endPoint.x += 1;
        }
        this.getParaPt();
        this.drawRayLines(context, this.startPoint, this.endPoint);
        this.drawRayLines(context, this.paraStartPoint, this.paraEndPoint);
    }

}


export class DrawTriParallelLinesPlotter extends ParallelLinesPlotter {

    constructor(name, toolObject) {
        super(name, toolObject);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 3;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.getAreaPos();
        this.startPoint = this.ctrlPts[1][0];
        this.paraStartPoint = this.ctrlPts[1][1];
        this.endPoint = this.ctrlPts[1][2];
        let vectorA = [];
        vectorA[0] = this.endPoint.x - this.startPoint.x;
        vectorA[1] = this.endPoint.y - this.startPoint.y;
        let vectorB = [];
        vectorB[0] = this.paraStartPoint.x - this.startPoint.x;
        vectorB[1] = this.paraStartPoint.y - this.startPoint.y;
        this.para1EndPoint = {x: -1, y: -1};
        this.para2EndPoint = {x: -1, y: -1};
        this.para2StartPoint = {x: -1, y: -1};
        this.para1EndPoint.x = vectorA[0] + vectorB[0] + this.startPoint.x;
        this.para1EndPoint.y = vectorA[1] + vectorB[1] + this.startPoint.y;
        this.para2StartPoint.x = this.startPoint.x - vectorB[0];
        this.para2StartPoint.y = this.startPoint.y - vectorB[1];
        this.para2EndPoint.x = this.endPoint.x - vectorB[0];
        this.para2EndPoint.y = this.endPoint.y - vectorB[1];
        this.getAreaPos();
        this.crossPt0 = this.getRectCrossPt(this.areaPos, this.startPoint, this.endPoint);
        Plotter.drawLine(context, this.crossPt0[0].x, this.crossPt0[0].y, this.crossPt0[1].x, this.crossPt0[1].y);
        this.crossPt1 = this.getRectCrossPt(this.areaPos, this.paraStartPoint, this.para1EndPoint);
        Plotter.drawLine(context, this.crossPt1[0].x, this.crossPt1[0].y, this.crossPt1[1].x, this.crossPt1[1].y);
        this.crossPt2 = this.getRectCrossPt(this.areaPos, this.para2StartPoint, this.para2EndPoint);
        Plotter.drawLine(context, this.crossPt2[0].x, this.crossPt2[0].y, this.crossPt2[1].x, this.crossPt2[1].y);
    }

}


export class BandLinesPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name);
        this.toolObject = toolObject;
        this.ctrlPtsNum = 2;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    drawLinesAndInfo(context, startPoint, endPoint) {
        context.font = "12px Tahoma";
        context.textAlign = "left";
        context.fillStyle = this.theme.getColor(themes.Theme.Color.LineColorNormal);
        let text;
        if (this.toolObject.state === ctools.CToolObject.state.Draw) {
            this.startPtValue = this.toolObject.getPoint(0).getPosIV().v;
            this.endPtValue = this.toolObject.getPoint(1).getPosIV().v;
        }
        this.getAreaPos();
        for (let i = 0; i < this.fiboSequence.length; i++) {
            let stageY = startPoint.y + (100 - this.fiboSequence[i]) / 100 * (endPoint.y - startPoint.y);
            if (stageY > this.areaPos.bottom)
                continue;
            let stageYvalue = this.startPtValue + (100 - this.fiboSequence[i]) / 100 * (this.endPtValue - this.startPtValue);
            Plotter.drawLine(context, this.areaPos.left, stageY, this.areaPos.right, stageY);
            text = this.fiboSequence[i].toFixed(1) + '% ' + stageYvalue.toFixed(1);
            context.fillText(text, this.areaPos.left + 2, stageY - 15);
        }
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.getAreaPos();
        this.startPoint = this.ctrlPts[1][0];
        this.endPoint = this.ctrlPts[1][1];
        this.drawLinesAndInfo(context, this.startPoint, this.endPoint);
    }

}


export class DrawFibRetracePlotter extends BandLinesPlotter {

    constructor(name, toolObject) {
        super(name, toolObject);
        this.toolObject = toolObject;
        this.fiboSequence = [100.0, 78.6, 61.8, 50.0, 38.2, 23.6, 0.0];
    }

}


export class DrawBandLinesPlotter extends BandLinesPlotter {

    constructor(name, toolObject) {
        super(name, toolObject);
        this.toolObject = toolObject;
        this.fiboSequence = [0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100];
    }

}


export class DrawFibFansPlotter extends CToolPlotter {

    constructor(name, toolObject) {
        super(name);
        this.toolObject = toolObject;
        this.fiboFansSequence = [0, 38.2, 50, 61.8];
        this.ctrlPtsNum = 2;
        this.ctrlPts = [new Array(this.ctrlPtsNum), new Array(2)];
        this.getCtrlPts();
    }

    drawLinesAndInfo(context, startPoint, endPoint) {
        this.drawFibRayLines(context, startPoint, endPoint);
    }

    draw(context) {
        this.updateCtrlPtPos();
        this.getAreaPos();
        this.startPoint = this.ctrlPts[1][0];
        this.endPoint = this.ctrlPts[1][1];
        if (this.startPoint.x === this.endPoint.x && this.startPoint.y === this.endPoint.y) {
            this.endPoint.x += 1;
        }
        this.drawLinesAndInfo(context, this.startPoint, this.endPoint);
    }

}


export class CDynamicLinePlotter extends NamedObject {

    constructor(name) {
        super(name);
        this.flag = true;
        this.context = ChartManager.instance._overlayContext;
    }

    getAreaPos() {
        let pMgr = ChartManager.instance;
        let pArea = pMgr.getArea('frame0.k0.main');
        if (pArea === null) {
            this.areaPos = {
                left: 0,
                top: 0,
                right: 0,
                bottom: 0
            };
            return;
        }
        this.areaPos = {
            left: Math.floor(pArea.getLeft()),
            top: Math.floor(pArea.getTop()),
            right: Math.floor(pArea.getRight()),
            bottom: Math.floor(pArea.getBottom())
        };
    }

    Draw(context) {
        this.getAreaPos();
        let pMgr = ChartManager.instance;
        let pTDP = pMgr.getDataSource(this.getDataSourceName());
        if (pTDP === null || !Util.isInstance(pTDP, data_sources.MainDataSource))
            return;
        this.context.save();
        this.context.rect(this.areaPos.left, this.areaPos.top, this.areaPos.right - this.areaPos.left, this.areaPos.bottom - this.areaPos.top);
        this.context.clip();
        let count = pTDP.getToolObjectCount();
        for (let i = 0; i < count; i++) {
            let toolObject = pTDP.getToolObject(i);
            let state = toolObject.getState();
            switch (state) {
                case ctools.CToolObject.state.BeforeDraw:
                    toolObject.getPlotter().theme = ChartManager.instance.getTheme(this.getFrameName());
                    toolObject.getPlotter().drawCursor(this.context);
                    break;
                case ctools.CToolObject.state.Draw:
                    toolObject.getPlotter().theme = ChartManager.instance.getTheme(this.getFrameName());
                    toolObject.getPlotter().updateDraw(this.context);
                    break;
                case ctools.CToolObject.state.AfterDraw:
                    toolObject.getPlotter().theme = ChartManager.instance.getTheme(this.getFrameName());
                    toolObject.getPlotter().finishDraw(this.context);
                    break;
                default:
                    break;
            }
        }
        let sel = pTDP.getSelectToolObjcet();
        if (sel !== null && sel !== ctools.CToolObject.state.Draw)
            sel.getPlotter().highlight(this.context);
        this.context.restore();

    }

}

