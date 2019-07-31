import {NamedObject} from './named_object'
import {ChartManager} from './chart_manager'
import {Util} from './util'
import * as data_sources from './data_sources'


export class DataProvider extends NamedObject {

    constructor(name) {
        super(name);
        this._minValue = 0;
        this._maxValue = 0;
        this._minValueIndex = -1;
        this._maxValueIndex = -1;
    }

    getMinValue() {
        return this._minValue;
    }

    getMaxValue() {
        return this._maxValue;
    }

    getMinValueIndex() {
        return this._minValueIndex;
    }

    getMaxValueIndex() {
        return this._maxValueIndex;
    }

    getMinMaxAt(index, minmax) {
        return true;
    }

    calcRange(firstIndexes, lastIndex, minmaxes, indexes) {
        let min = Number.MAX_VALUE;
        let max = -Number.MAX_VALUE;
        let minIndex = -1;
        let maxIndex = -1;
        let minmax = {};
        let i = lastIndex - 1;
        let n = firstIndexes.length - 1;
        for (; n >= 0; n--) {
            let first = firstIndexes[n];
            if (i < first) {
                minmaxes[n] = {"min": min, "max": max};
            } else {
                for (; i >= first; i--) {
                    if (this.getMinMaxAt(i, minmax) === false) {
                        continue;
                    }
                    if (min > minmax.min) {
                        min = minmax.min;
                        minIndex = i;
                    }
                    if (max < minmax.max) {
                        max = minmax.max;
                        maxIndex = i;
                    }
                }
                minmaxes[n] = {"min": min, "max": max};
            }
            if (indexes !== null && indexes !== undefined) {
                indexes[n] = {"minIndex": minIndex, "maxIndex": maxIndex};
            }
        }
    }

    updateRange() {
        let mgr = ChartManager.instance;
        let timeline = mgr.getTimeline(this.getDataSourceName());
        let firstIndexes = [timeline.getFirstIndex()];
        let minmaxes = [{}];
        let indexes = [{}];
        this.calcRange(firstIndexes, timeline.getLastIndex(), minmaxes, indexes);
        this._minValue = minmaxes[0].min;
        this._maxValue = minmaxes[0].max;
        this._minValueIndex = indexes[0].minIndex;
        this._maxValueIndex = indexes[0].maxIndex;
    }

}


export class MainDataProvider extends DataProvider {

    constructor(name) {
        super(name);
        this._candlestickDS = null;
    }

    updateData() {
        let mgr = ChartManager.instance;
        let ds = mgr.getDataSource(this.getDataSourceName());
        if (!Util.isInstance(ds, data_sources.MainDataSource)) {
            return;
        }
        this._candlestickDS = ds;
    }

    getMinMaxAt(index, minmax) {
        let data = this._candlestickDS.getDataAt(index);
        minmax.min = data.low;
        minmax.max = data.high;
        return true;
    }

}


export class IndicatorDataProvider extends DataProvider {

    getIndicator() {
        return this._indicator;
    }

    setIndicator(v) {
        this._indicator = v;
        this.refresh();
    }

    refresh() {
        let mgr = ChartManager.instance;
        let ds = mgr.getDataSource(this.getDataSourceName());
        if (ds.getDataCount() < 1) {
            return;
        }
        let indic = this._indicator;
        let i, last = ds.getDataCount();
        indic.clear();
        indic.reserve(last);
        for (i = 0; i < last; i++) {
            indic.execute(ds, i);
        }
    }

    updateData() {
        let mgr = ChartManager.instance;
        let ds = mgr.getDataSource(this.getDataSourceName());
        if (ds.getDataCount() < 1) {
            return;
        }
        let indic = this._indicator;
        let mode = ds.getUpdateMode();
        switch (mode) {
            case data_sources.DataSource.UpdateMode.Refresh: {
                this.refresh();
                break;
            }
            case data_sources.DataSource.UpdateMode.Append: {
                indic.reserve(ds.getAppendedCount());
                break;
            }
            case data_sources.DataSource.UpdateMode.Update: {
                let i, last = ds.getDataCount();
                let cnt = ds.getUpdatedCount() + ds.getAppendedCount();
                for (i = last - cnt; i < last; i++) {
                    indic.execute(ds, i);
                }
                break;
            }
        }
    }

    getMinMaxAt(index, minmax) {
        minmax.min = Number.MAX_VALUE;
        minmax.max = -Number.MAX_VALUE;
        let result, valid = false;
        let i, cnt = this._indicator.getOutputCount();
        for (i = 0; i < cnt; i++) {
            result = this._indicator.getOutputAt(i).execute(index);
            if (isNaN(result) === false) {
                valid = true;
                if (minmax.min > result) {
                    minmax.min = result;
                }
                if (minmax.max < result) {
                    minmax.max = result;
                }
            }
        }
        return valid;
    }

}

