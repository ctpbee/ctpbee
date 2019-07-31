import {ChartManager} from './chart_manager'
import {NamedObject} from './named_object'
import * as data_sources from './data_sources'
import {Util} from './util'

export class CPoint extends NamedObject {

    static state = {
        Hide: 0,
        Show: 1,
        Highlight: 2
    };

    constructor(name) {
        super(name);
        this.pos = {index: -1, value: -1};
        this.state = CPoint.state.Hide;
    }

    getChartObjects() {
        let ppMgr = ChartManager.instance;
        let ppCDS = ppMgr.getDataSource("frame0.k0");
        if (ppCDS === null || !Util.isInstance(ppCDS, data_sources.MainDataSource))
            return null;
        let ppTimeline = ppMgr.getTimeline("frame0.k0");
        if (ppTimeline === null)
            return null;
        let ppRange = ppMgr.getRange("frame0.k0.main");
        if (ppRange === null)
            return null;
        return {pMgr: ppMgr, pCDS: ppCDS, pTimeline: ppTimeline, pRange: ppRange};
    }

    setPosXY(x, y) {
        let pObj = this.getChartObjects();
        let i = pObj.pTimeline.toIndex(x);
        let v = pObj.pRange.toValue(y);
        let result = this.snapValue(i, v);
        if (result !== null)
            v = result;
        this.setPosIV(i, v);
    }

    setPosXYNoSnap(x, y) {
        let pObj = this.getChartObjects();
        let i = pObj.pTimeline.toIndex(x);
        let v = pObj.pRange.toValue(y);
        this.setPosIV(i, v);
    }

    setPosIV(i, v) {
        this.pos = {index: i, value: v};
    }

    getPosXY() {
        let pObj = this.getChartObjects();
        let _x = pObj.pTimeline.toItemCenter(this.pos.index);
        let _y = pObj.pRange.toY(this.pos.value);
        return {x: _x, y: _y};
    }

    getPosIV() {
        return {i: this.pos.index, v: this.pos.value};
    }

    setState(s) {
        this.state = s;
    }

    getState() {
        return this.state;
    }

    isSelected(x, y) {
        let xy = this.getPosXY();
        if (x < xy.x - 4 || x > xy.x + 4 || y < xy.y - 4 || y > xy.y + 4)
            return false;
        this.setState(CPoint.state.Highlight);
        return true;
    }

    snapValue(i, v) {
        let pObj = this.getChartObjects();
        let result = null;
        let first = Math.floor(pObj.pTimeline.getFirstIndex());
        let last = Math.floor(pObj.pTimeline.getLastIndex());
        if (i < first || i > last)
            return result;
        let y = pObj.pRange.toY(v);
        let pData = pObj.pCDS.getDataAt(i);
        if (pData === null || pData === undefined)
            return result;
        let pDataPre = null;
        if (i > 0)
            pDataPre = pObj.pCDS.getDataAt(i - 1);
        else
            pDataPre = pObj.pCDS.getDataAt(i);
        let candleStickStyle = pObj.pMgr.getChartStyle(pObj.pCDS.getFrameName());
        let open = pObj.pRange.toY(pData.open);
        let high = pObj.pRange.toY(pData.high);
        let low = pObj.pRange.toY(pData.low);
        let close = pObj.pRange.toY(pData.close);
        if (candleStickStyle === "CandleStickHLC") {
            open = pObj.pRange.toY(pDataPre.close);
        }
        let dif_open = Math.abs(open - y);
        let dif_high = Math.abs(high - y);
        let dif_low = Math.abs(low - y);
        let dif_close = Math.abs(close - y);
        if (dif_open <= dif_high && dif_open <= dif_low && dif_open <= dif_close) {
            if (dif_open < 6)
                result = pData.open;
        }
        if (dif_high <= dif_open && dif_high <= dif_low && dif_high <= dif_close) {
            if (dif_high < 6)
                result = pData.high;
        }
        if (dif_low <= dif_open && dif_low <= dif_high && dif_low <= dif_close) {
            if (dif_low < 6)
                result = pData.low;
        }
        if (dif_close <= dif_open && dif_close <= dif_high && dif_close <= dif_low) {
            if (dif_close < 6)
                result = pData.close;
        }
        return result;
    }

}
