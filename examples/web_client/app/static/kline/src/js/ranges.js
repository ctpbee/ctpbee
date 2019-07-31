import {NamedObject} from './named_object'
import {ChartManager} from './chart_manager'

export class Range extends NamedObject {

    constructor(name) {
        super(name);
        this._updated = true;
        this._minValue = Number.MAX_VALUE;
        this._maxValue = -Number.MAX_VALUE;
        this._outerMinValue = Number.MAX_VALUE;
        this._outerMaxValue = -Number.MAX_VALUE;
        this._ratio = 0;
        this._top = 0;
        this._bottom = 0;
        this._paddingTop = 0;
        this._paddingBottom = 0;
        this._minInterval = 36;
        this._selectedPosition = -1;
        this._selectedValue = -Number.MAX_VALUE;
        this._gradations = [];
    }

    isUpdated() {
        return this._updated;
    }

    setUpdated(v) {
        this._updated = v;
    }

    getMinValue() {
        return this._minValue;
    }

    getMaxValue() {
        return this._maxValue;
    }

    getRange() {
        return this._maxValue - this._minValue;
    }

    getOuterMinValue() {
        return this._outerMinValue;
    }

    getOuterMaxValue() {
        return this._outerMaxValue;
    }

    getOuterRange() {
        return this._outerMaxValue - this._outerMinValue;
    }

    getHeight() {
        return Math.max(0, this._bottom - this._top);
    }

    getGradations() {
        return this._gradations;
    }

    getMinInterval() {
        return this._minInterval;
    }

    setMinInterval(v) {
        this._minInterval = v;
    }

    getSelectedPosition() {
        if (this._selectedPosition >= 0) {
            return this._selectedPosition;
        }
        if (this._selectedValue > -Number.MAX_VALUE) {
            return this.toY(this._selectedValue);
        }
        return -1;
    }

    getSelectedValue() {
        if (this._selectedValue > -Number.MAX_VALUE) {
            return this._selectedValue;
        }
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        if (area === null) {
            return -Number.MAX_VALUE;
        }
        if (this._selectedPosition < area.getTop() + 12 || this._selectedPosition >= area.getBottom() - 4) {
            return -Number.MAX_VALUE;
        }
        return this.toValue(this._selectedPosition);
    }

    setPaddingTop(p) {
        this._paddingTop = p;
    }

    setPaddingBottom(p) {
        this._paddingBottom = p;
    }

    toValue(y) {
        return this._maxValue - (y - this._top) / this._ratio;
    }

    toY(value) {
        if (this._ratio > 0) {
            return this._top + Math.floor((this._maxValue - value) * this._ratio + 0.5);
        }
        return this._top;
    }

    toHeight(value) {
		if (value == Infinity || this._ratio == 0) {
		  return 1.5;
		}
	  	return Math.floor(value * this._ratio + 1.5);
    }

    update() {
        let min = Number.MAX_VALUE;
        let max = -Number.MAX_VALUE;
        let mgr = ChartManager.instance;
        let dp, dpNames = [".main", ".secondary"];
        for (let i = 0; i < dpNames.length; i++) {
            dp = mgr.getDataProvider(this.getName() + dpNames[i]);
            if (dp !== null && dp !== undefined) {
                min = Math.min(min, dp.getMinValue());
                max = Math.max(max, dp.getMaxValue());
            }
        }
        let r = {"min": min, "max": max};
        this.preSetRange(r);
        this.setRange(r.min, r.max);
    }

    select(v) {
        this._selectedValue = v;
        this._selectedPosition = -1;
    }

    selectAt(y) {
        this._selectedPosition = y;
        this._selectedValue = -Number.MAX_VALUE;
    }

    unselect() {
        this._selectedPosition = -1;
        this._selectedValue = -Number.MAX_VALUE;
    }

    preSetRange(r) {
        if (r.min === r.max) {
            r.min = -1.0;
            r.max = 1.0;
        }
    }

    setRange(minValue, maxValue) {
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        if (this._minValue === minValue && this._maxValue === maxValue && !area.isChanged()) {
            return;
        }
        this._updated = true;
        this._minValue = minValue;
        this._maxValue = maxValue;
        this._gradations = [];
        let top = area.getTop() + this._paddingTop;
        let bottom = area.getBottom() - (this._paddingBottom + 1);
        if (top >= bottom) {
            this._minValue = this._maxValue;
            return;
        }
        this._top = top;
        this._bottom = bottom;
        if (this._maxValue > this._minValue)
            this._ratio = (bottom - top) / (this._maxValue - this._minValue);
        else {
            this._ratio = 1;
        }
        this._outerMinValue = this.toValue(area.getBottom());
        this._outerMaxValue = this.toValue(area.getTop());
        this.updateGradations();
    }

    calcInterval() {
        let H = this.getHeight();
        let h = this.getMinInterval();
        if ((H / h) <= 1) {
            h = H >> 1;
        }
        let d = this.getRange();
        let i = 0;
        while (i > -2 && Math.floor(d) < d) {
            d *= 10.0;
            i--;
        }
        let m, c;
        for (; ; i++) {
            c = Math.pow(10.0, i);
            m = c;
            if (this.toHeight(m) > h)
                break;
            m = 2.0 * c;
            if (this.toHeight(m) > h)
                break;
            m = 5.0 * c;
            if (this.toHeight(m) > h)
                break;
        }
        return m;
    }

    updateGradations() {
        this._gradations = [];
        let interval = this.calcInterval();
        if (interval <= 0.0) {
            return;
        }
        let v = Math.floor(this.getMaxValue() / interval) * interval;
        do {
            this._gradations.push(v);
            v -= interval;
        } while (v > this.getMinValue());
    }

}


export class PositiveRange extends Range {

    constructor(name) {
        super(name);
    }

    preSetRange(r) {
        if (r.min < 0) r.min = 0;
        if (r.max < 0) r.max = 0;
    }

}


export class ZeroBasedPositiveRange extends Range {

    constructor(name) {
        super(name);
    }

    preSetRange(r) {
        r.min = 0;
        if (r.max < 0) r.max = 0;
    }

}


export class MainRange extends Range {

    constructor(name) {
        super(name);
    }

    preSetRange(r) {
        let mgr = ChartManager.instance;

        let timeline = mgr.getTimeline(this.getDataSourceName());
        let dIndex = timeline.getMaxIndex() - timeline.getLastIndex();
        if (dIndex < 25) {
            let ds = mgr.getDataSource(this.getDataSourceName());

            let data = ds.getDataAt(ds.getDataCount() - 1);
            let d = ((r.max - r.min) / 4) * (1 - (dIndex / 25));

            r.min = Math.min(r.min, Math.max(data.low - d, 0));
            r.max = Math.max(r.max, data.high + d);
        }

        if (r.min > 0) {
            let a = r.max / r.min;

            if (a < 1.016) {
                let m = (r.max + r.min) / 2.0;
                let c = (a - 1.0) * 1.5;
                r.max = m * (1.0 + c);
                r.min = m * (1.0 - c);
            } else if (a < 1.048) {
                let m = (r.max + r.min) / 2.0;
                r.max = m * 1.024;
                r.min = m * 0.976;
            }
        }
        if (r.min < 0) r.min = 0;
        if (r.max < 0) r.max = 0;
    }

}


export class ZeroCenteredRange extends Range {

    constructor(name) {
        super(name);
    }

    calcInterval(area) {
        let h = this.getMinInterval();
        if (area.getHeight() / h < 2) {
            return 0.0;
        }
        let r = this.getRange();
        let i;
        for (i = 3; ; i += 2) {
            if (this.toHeight(r / i) <= h)
                break;
        }
        i -= 2;
        return r / i;
    }

    updateGradations() {
        this._gradations = [];
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        let interval = this.calcInterval(area);
        if (interval <= 0.0) {
            return;
        }
        let v = interval / 2.0;
        do {
            this._gradations.push(v);
            this._gradations.push(-v);
            v += interval;
        } while (v <= this.getMaxValue());
    }

    preSetRange(r) {
        let abs = Math.max(Math.abs(r.min), Math.abs(r.max));
        r.min = -abs;
        r.max = abs;
    }

}


export class PercentageRange extends Range {

    constructor(name) {
        super(name);
    }

    updateGradations() {
        this._gradations = [];
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getAreaName());
        let interval = 10.0;
        let h = Math.floor(this.toHeight(interval));
        if ((h << 2) > area.getHeight())
            return;
        let v = Math.ceil(this.getMinValue() / interval) * interval;
        if (v === 0.0)
            v = 0;
        if ((h << 2) < 24) {
            if ((h << 1) < 8)
                return;
            do {
                if (v === 20.0 || v === 80.0)
                    this._gradations.push(v);
                v += interval;
            } while (v < this.getMaxValue());
        } else {
            do {
                if (h < 8) {
                    if (v === 20.0 || v === 50.0 || v === 80.0)
                        this._gradations.push(v);
                } else {
                    if (v === 0.0 || v === 20.0 || v === 50.0 || v === 80.0 || v === 100.0)
                        this._gradations.push(v);
                }
                v += interval;
            } while (v < this.getMaxValue());
        }
    }

}

