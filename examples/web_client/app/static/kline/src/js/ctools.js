import {ChartManager} from './chart_manager'
import {NamedObject} from './named_object'
import {CPoint} from './cpoint'
import {Util} from './util'
import * as data_sources from './data_sources'
import * as plotters from './plotters'


export class CToolObject extends NamedObject {

    static state = {
        BeforeDraw: 0,
        Draw: 1,
        AfterDraw: 2
    };

    constructor(name) {
        super(name);
        this.drawer = null;
        this.state = CToolObject.state.BeforeDraw;
        this.points = [];
        this.step = 0;
    }

    getChartObjects() {
        let ppMgr = ChartManager.instance;
        let ppCDS = ppMgr.getDataSource("frame0.k0");
        if (ppCDS === null || !Util.isInstance(ppCDS, data_sources.MainDataSource))
            return null;
        let ppTimeline = ppMgr.getTimeline("frame0.k0");
        if (ppTimeline === null)
            return null;
        let ppArea = ppMgr.getArea('frame0.k0.main');
        if (ppArea === null)
            return null;
        let ppRange = ppMgr.getRange("frame0.k0.main");
        if (ppRange === null)
            return null;
        return {pMgr: ppMgr, pCDS: ppCDS, pTimeline: ppTimeline, pArea: ppArea, pRange: ppRange};
    }

    isValidMouseXY(x, y) {
        let pObj = this.getChartObjects();
        let areaPos = {
            left: pObj.pArea.getLeft(),
            top: pObj.pArea.getTop(),
            right: pObj.pArea.getRight(),
            bottom: pObj.pArea.getBottom()
        };
        return !(x < areaPos.left || x > areaPos.right ||
            y < areaPos.top || y > areaPos.bottom);
    }

    getPlotter() {
        return this.drawer;
    }

    setState(s) {
        this.state = s;
    }

    getState() {
        return this.state;
    }

    addPoint(point) {
        this.points.push(point);
    }

    getPoint(i) {
        return this.points[i];
    }

    acceptMouseMoveEvent(x, y) {
        if (this.isValidMouseXY(x, y) === false) {
            return false;
        }
        if (this.state === CToolObject.state.BeforeDraw) {
            this.setBeforeDrawPos(x, y);
        } else if (this.state === CToolObject.state.Draw) {
            this.setDrawPos(x, y);
        } else if (this.state === CToolObject.state.AfterDraw) {
            this.setAfterDrawPos(x, y);
        }
        return true;
    }

    acceptMouseDownEvent(x, y) {
        if (this.isValidMouseXY(x, y) === false) {
            return false;
        }
        if (this.state === CToolObject.state.BeforeDraw) {
            this.setDrawPos(x, y);
            this.setState(CToolObject.state.Draw);
        } else if (this.state === CToolObject.state.Draw) {
            this.setAfterDrawPos(x, y);
            if (this.step === 0)
                this.setState(CToolObject.state.AfterDraw);
        } else if (this.state === CToolObject.state.AfterDraw) {
            if (CToolObject.prototype.isSelected(x, y)) {
                this.setDrawPos(x, y);
                this.setState(CToolObject.state.Draw);
            } else {
                this.oldx = x;
                this.oldy = y;
            }
        }
        return true;
    }

    acceptMouseDownMoveEvent(x, y) {
        if (this.isValidMouseXY(x, y) === false) {
            return false;
        }
        if (this.state === CToolObject.state.Draw) {
            this.setDrawPos(x, y);
        } else if (this.state === CToolObject.state.AfterDraw) {
            let pObj = this.getChartObjects();
            let _width = pObj.pTimeline.getItemWidth();
            let _height = pObj.pRange;
            if (Math.abs(x - this.oldx) < _width && Math.abs(y - this.oldy) === 0)
                return true;
            let _old_x = pObj.pTimeline.toIndex(this.oldx);
            let _old_y = pObj.pRange.toValue(this.oldy);
            let _new_x = pObj.pTimeline.toIndex(x);
            let _new_y = pObj.pRange.toValue(y);
            this.oldx = x;
            this.oldy = y;
            let _dif_x = _new_x - _old_x;
            let _dif_y = _new_y - _old_y;
            for (let index in this.points) {
                this.points[index].pos.index += _dif_x;
                this.points[index].pos.value += _dif_y;
            }
        }
        return true;
    }

    acceptMouseUpEvent(x, y) {
        if (this.isValidMouseXY(x, y) === false) {
            return false;
        }
        if (this.state === CToolObject.state.Draw) {
            this.setAfterDrawPos(x, y);
            if (this.step === 0)
                this.setState(CToolObject.state.AfterDraw);
            return true;
        }
        return false;
    }

    setBeforeDrawPos(x, y) {
        for (let index in this.points) {
            this.points[index].setPosXY(x, y);
            this.points[index].setState(CPoint.state.Show);
        }
    }

    setDrawPos(x, y) {
        for (let index in this.points) {
            if (this.points[index].getState() === CPoint.state.Highlight) {
                this.points[index].setPosXY(x, y);
            }
        }
    }

    setAfterDrawPos(x, y) {
        if (this.step !== 0) {
            this.step -= 1;
        }
        for (let index in this.points) {
            this.points[index].setState(CPoint.state.Hide);
        }
        if (this.step === 0) {
            let pObj = this.getChartObjects();
            pObj.pMgr.setNormalMode();
        }
    }

    isSelected(x, y) {
        let isFind = false;
        for (let index in this.points) {
            if (this.points[index].isSelected(x, y)) {
                this.points[index].setState(CPoint.state.Highlight);
                isFind = true;
                break;
            }
        }
        if (isFind === true) {
            this.select();
            return true;
        }
        return false;
    }

    select() {
        for (let index in this.points) {
            if (this.points[index].getState() === CPoint.state.Hide) {
                this.points[index].setState(CPoint.state.Show);
            }
        }
    }

    unselect() {
        for (let index in this.points) {
            if (this.points[index].getState() !== CPoint.state.Hide) {
                this.points[index].setState(CPoint.state.Hide);
            }
        }
    }

    calcDistance(point1, point2, point3) {
        let xa = point1.getPosXY().x;
        let ya = point1.getPosXY().y;
        let xb = point2.getPosXY().x;
        let yb = point2.getPosXY().y;
        let xc = point3.getPosXY().x;
        let yc = point3.getPosXY().y;
        let a1 = xa - xc;
        let a2 = ya - yc;
        let b1 = xb - xc;
        let b2 = yb - yc;
        let area = Math.abs(a1 * b2 - a2 * b1);
        let len = Math.sqrt(Math.pow((xb - xa), 2) + Math.pow((yb - ya), 2));
        return area / len;
    }

    calcGap(r, x, y) {
        let xa = r.sx;
        let ya = r.sy;
        let xb = r.ex;
        let yb = r.ey;
        let xc = x;
        let yc = y;
        let a1 = xa - xc;
        let a2 = ya - yc;
        let b1 = xb - xc;
        let b2 = yb - yc;
        let area = Math.abs(a1 * b2 - a2 * b1);
        let len = Math.sqrt(Math.pow((xb - xa), 2) + Math.pow((yb - ya), 2));
        return area / len;
    }

    isWithRect(point1, point2, point3) {
        let sx = point1.getPosXY().x;
        let sy = point1.getPosXY().y;
        let ex = point2.getPosXY().x;
        let ey = point2.getPosXY().y;
        let x = point3.getPosXY().x;
        let y = point3.getPosXY().y;
        if (sx > ex) {
            sx += 4;
            ex -= 4;
        } else {
            sx -= 4;
            ex += 4;
        }
        if (sy > ey) {
            sy += 4;
            ey -= 4;
        } else {
            sy -= 4;
            ey += 4;
        }
        if (sx <= x && ex >= x && sy <= y && ey >= y) {
            return true;
        }
        if (sx >= x && ex <= x && sy <= y && ey >= y) {
            return true;
        }
        if (sx <= x && ex >= x && sy >= y && ey <= y) {
            return true;
        }
        if (sx >= x && ex <= x && sy >= y && ey <= y) {
            return true;
        }
        return false;
    }

}


export class CBiToolObject extends CToolObject {

    constructor(name) {
        super(name);
        this.addPoint(new CPoint(name));
        this.addPoint(new CPoint(name));
    }

    setBeforeDrawPos(x, y) {
        this.step = 1;
        super.setBeforeDrawPos(x, y);
        this.getPoint(0).setState(CPoint.state.Show);
        this.getPoint(1).setState(CPoint.state.Highlight);
    }

}

export class CTriToolObject extends CToolObject {

    constructor(name) {
        super(name);
        this.addPoint(new CPoint(name));
        this.addPoint(new CPoint(name));
        this.addPoint(new CPoint(name));
    }

    setBeforeDrawPos(x, y) {
        this.step = 2;
        super.setBeforeDrawPos(x, y);
        this.getPoint(0).setState(CPoint.state.Show);
        this.getPoint(1).setState(CPoint.state.Show);
        this.getPoint(2).setState(CPoint.state.Highlight);
    }

    setAfterDrawPos(x, y) {
        if (this.step !== 0)
            this.step -= 1;
        if (this.step === 0) {
            for (let index in this.points) {
                this.points[index].setState(CPoint.state.Hide);
            }
        } else {
            this.getPoint(0).setState(CPoint.state.Show);
            this.getPoint(1).setState(CPoint.state.Highlight);
            this.getPoint(2).setState(CPoint.state.Show);
        }
        if (this.step === 0) {
            let pObj = this.getChartObjects();
            pObj.pMgr.setNormalMode();
        }
    }

}


export class CBandLineObject extends CBiToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawBandLinesPlotter(name, this);
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let c = new CPoint("frame0.k0");
        c.setPosXY(x, y);
        let sx = this.getPoint(0).getPosXY().x;
        let sy = this.getPoint(0).getPosXY().y;
        let ex = this.getPoint(1).getPosXY().x;
        let ey = this.getPoint(1).getPosXY().y;
        let fibSequence = [100.0, 87.5, 75.0, 62.5, 50.0, 37.5, 25.0, 12.5, 0.0];
        for (let i = 0; i < fibSequence.length; i++) {
            let stage_y = sy + (100 - fibSequence[i]) / 100 * (ey - sy);
            if (stage_y < y + 4 && stage_y > y - 4) {
                this.select();
                return true;
            }
        }
        return false;
    }

}


export class CBiParallelLineObject extends CTriToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawBiParallelLinesPlotter(name, this);
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let _0x = this.getPoint(0).getPosXY().x;
        let _0y = this.getPoint(0).getPosXY().y;
        let _1x = this.getPoint(1).getPosXY().x;
        let _1y = this.getPoint(1).getPosXY().y;
        let _2x = this.getPoint(2).getPosXY().x;
        let _2y = this.getPoint(2).getPosXY().y;
        let _a = {x: _0x - _1x, y: _0y - _1y};
        let _b = {x: _0x - _2x, y: _0y - _2y};
        let _c = {x: _a.x + _b.x, y: _a.y + _b.y};
        let _3x = _0x - _c.x;
        let _3y = _0y - _c.y;
        let r1 = {sx: _0x, sy: _0y, ex: _2x, ey: _2y};
        let r2 = {sx: _1x, sy: _1y, ex: _3x, ey: _3y};
        if (this.calcGap(r1, x, y) > 4 && this.calcGap(r2, x, y) > 4) {
            return false;
        }
        return true;
    }

}


export class CBiParallelRayLineObject extends CTriToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawBiParallelRayLinesPlotter(name, this);
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let _0x = this.getPoint(0).getPosXY().x;
        let _0y = this.getPoint(0).getPosXY().y;
        let _1x = this.getPoint(1).getPosXY().x;
        let _1y = this.getPoint(1).getPosXY().y;
        let _2x = this.getPoint(2).getPosXY().x;
        let _2y = this.getPoint(2).getPosXY().y;
        let _a = {x: _0x - _1x, y: _0y - _1y};
        let _b = {x: _0x - _2x, y: _0y - _2y};
        let _c = {x: _a.x + _b.x, y: _a.y + _b.y};
        let _3x = _0x - _c.x;
        let _3y = _0y - _c.y;
        let r1 = {sx: _0x, sy: _0y, ex: _2x, ey: _2y};
        let r2 = {sx: _1x, sy: _1y, ex: _3x, ey: _3y};
        if ((r1.ex > r1.sx && x > r1.sx - 4) || (r1.ex < r1.sx && x < r1.sx + 4) ||
            (r2.ex > r2.sx && x > r2.sx - 4) || (r2.ex < r2.sx && x < r2.sx + 4)) {
            if (this.calcGap(r1, x, y) > 4 && this.calcGap(r2, x, y) > 4) {
                return false;
            }
        } else {
            return false;
        }
        this.select();
        return true;
    }

}


export class CFibFansObject extends CBiToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawFibFansPlotter(name, this);
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let c = new CPoint("frame0.k0");
        c.setPosXY(x, y);
        let sx = this.getPoint(0).getPosXY().x;
        let sy = this.getPoint(0).getPosXY().y;
        let ex = this.getPoint(1).getPosXY().x;
        let ey = this.getPoint(1).getPosXY().y;
        let pObj = this.getChartObjects();
        let areaPos = {
            left: pObj.pArea.getLeft(),
            top: pObj.pArea.getTop(),
            right: pObj.pArea.getRight(),
            bottom: pObj.pArea.getBottom()
        };
        let fibFansSequence = [0, 38.2, 50, 61.8];
        for (let i = 0; i < fibFansSequence.length; i++) {
            let stageY = sy + (100 - fibFansSequence[i]) / 100 * (ey - sy);
            let tempStartPt = {x: sx, y: sy};
            let tempEndPt = {x: ex, y: stageY};
            let crossPt = this.getRectCrossPt(areaPos, tempStartPt, tempEndPt);
            let lenToStartPt = Math.pow((crossPt[0].x - sx), 2) + Math.pow((crossPt[0].y - sy), 2);
            let lenToEndPt = Math.pow((crossPt[0].x - ex), 2) + Math.pow((crossPt[0].y - ey), 2);
            let tempCrossPt = lenToStartPt > lenToEndPt ? {x: crossPt[0].x, y: crossPt[0].y} : {
                x: crossPt[1].x,
                y: crossPt[1].y
            };
            if (tempCrossPt.x > sx && x < sx)
                continue;
            if (tempCrossPt.x < sx && x > sx)
                continue;
            let a = new CPoint("frame0.k0");
            a.setPosXY(sx, sy);
            let b = new CPoint("frame0.k0");
            b.setPosXY(tempCrossPt.x, tempCrossPt.y);
            if (this.calcDistance(a, b, c) > 4) {
                continue;
            }
            this.select();
            return true;
        }
        return false;
    }

}


export class CFibRetraceObject extends CBiToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawFibRetracePlotter(name, this);
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let c = new CPoint("frame0.k0");
        c.setPosXY(x, y);
        let sx = this.getPoint(0).getPosXY().x;
        let sy = this.getPoint(0).getPosXY().y;
        let ex = this.getPoint(1).getPosXY().x;
        let ey = this.getPoint(1).getPosXY().y;
        let fibSequence = [100.0, 78.6, 61.8, 50.0, 38.2, 23.6, 0.0];
        for (let i = 0; i < fibSequence.length; i++) {
            let stage_y = sy + (100 - fibSequence[i]) / 100 * (ey - sy);
            if (stage_y < y + 4 && stage_y > y - 4) {
                this.select();
                return true;
            }
        }
        return false;
    }

}


export class CHoriRayLineObject extends CBiToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawHoriRayLinesPlotter(name, this);
    }

    setDrawPos(x, y) {
        if (this.points[0].getState() === CPoint.state.Highlight) {
            this.points[0].setPosXY(x, y);
            this.points[1].setPosXYNoSnap(this.points[1].getPosXY().x, this.points[0].getPosXY().y);
            return;
        }
        if (this.points[1].getState() === CPoint.state.Highlight) {
            this.points[1].setPosXY(x, y);
            this.points[0].setPosXYNoSnap(this.points[0].getPosXY().x, this.points[1].getPosXY().y);
        }
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let c = new CPoint("frame0.k0");
        c.setPosXY(x, y);
        let sy = this.getPoint(0).getPosXY().y;
        let sx = this.getPoint(0).getPosXY().x;
        let ex = this.getPoint(1).getPosXY().x;
        if (y > sy + 4 || y < sy - 4) {
            return false;
        }
        if (ex > sx && x < sx - 4) {
            return false;
        }
        if (ex < sx && x > sx + 4) {
            return false;
        }
        this.select();
        return true;
    }

}


export class CHoriSegLineObject extends CBiToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawHoriSegLinesPlotter(name, this);
    }

    setDrawPos(x, y) {
        if (this.points[0].getState() === CPoint.state.Highlight) {
            this.points[0].setPosXY(x, y);
            this.points[1].setPosXYNoSnap(this.points[1].getPosXY().x, this.points[0].getPosXY().y);
            return;
        }
        if (this.points[1].getState() === CPoint.state.Highlight) {
            this.points[1].setPosXY(x, y);
            this.points[0].setPosXYNoSnap(this.points[0].getPosXY().x, this.points[1].getPosXY().y);
        }
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let c = new CPoint("frame0.k0");
        c.setPosXY(x, y);
        let sy = this.getPoint(0).getPosXY().y;
        let sx = this.getPoint(0).getPosXY().x;
        let ex = this.getPoint(1).getPosXY().x;
        if (y > sy + 4 || y < sy - 4) {
            return false;
        }
        if (sx > ex && (x > sx + 4 || x < ex - 4)) {
            return false;
        }
        if (sx < ex && (x < sx - 4 || x > ex + 4)) {
            return false;
        }
        this.select();
        return true;
    }

}


export class CHoriStraightLineObject extends CBiToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawHoriStraightLinesPlotter(name, this);
    }

    setDrawPos(x, y) {
        for (let index in this.points) {
            this.points[index].setPosXY(x, y);
        }
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let c = new CPoint("frame0.k0");
        c.setPosXY(x, y);
        let sy = this.getPoint(0).getPosXY().y;
        if (y > sy + 4 || y < sy - 4) {
            return false;
        }
        this.select();
        return true;
    }

}


export class CRayLineObject extends CBiToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawRayLinesPlotter(name, this);
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let c = new CPoint("frame0.k0");
        c.setPosXY(x, y);
        let sx = this.getPoint(0).getPosXY().x;
        let ex = this.getPoint(1).getPosXY().x;
        if (ex > sx && x < sx - 4) {
            return false;
        }
        if (ex < sx && x > sx + 4) {
            return false;
        }
        if (this.calcDistance(this.getPoint(0), this.getPoint(1), c) < 4) {
            this.select();
            return true;
        }
        return false;
    }

}


export class CSegLineObject extends CBiToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawSegLinesPlotter(name, this);
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let c = new CPoint("frame0.k0");
        c.setPosXY(x, y);
        if (this.isWithRect(this.getPoint(0), this.getPoint(1), c) === false) {
            return false;
        }
        if (this.calcDistance(this.getPoint(0), this.getPoint(1), c) < 4) {
            this.select();
            return true;
        }
        return false;
    }

}


export class CStraightLineObject extends CBiToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawStraightLinesPlotter(name, this);
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let c = new CPoint("frame0.k0");
        c.setPosXY(x, y);
        if (this.calcDistance(this.getPoint(0), this.getPoint(1), c) < 4) {
            this.select();
            return true;
        }
        return false;
    }

}


export class CTriParallelLineObject extends CTriToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawTriParallelLinesPlotter(name, this);
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let pObj = this.getChartObjects();
        let _0x = this.getPoint(0).getPosXY().x;
        let _0y = this.getPoint(0).getPosXY().y;
        let _1x = this.getPoint(1).getPosXY().x;
        let _1y = this.getPoint(1).getPosXY().y;
        let _2x = this.getPoint(2).getPosXY().x;
        let _2y = this.getPoint(2).getPosXY().y;
        let _a = {x: _0x - _1x, y: _0y - _1y};
        let _b = {x: _0x - _2x, y: _0y - _2y};
        let _c = {x: _a.x + _b.x, y: _a.y + _b.y};
        let _3x = _0x - _c.x;
        let _3y = _0y - _c.y;
        let r1 = {sx: _0x, sy: _0y, ex: _2x, ey: _2y};
        let r2 = {sx: _1x, sy: _1y, ex: _3x, ey: _3y};
        let _i = {x: _0x - _1x, y: _0y - _1y};
        let _j = {x: _2x - _3x, y: _2y - _3y};
        let _ri = {x: _1x - _0x, y: _1y - _0y};
        let _rj = {x: _3x - _2x, y: _3y - _2y};
        let _4x = Math.abs(_ri.x - _0x);
        let _4y = Math.abs(_ri.y - _0y);
        let _5x = Math.abs(_rj.x - _2x);
        let _5y = Math.abs(_rj.y - _2y);
        let r3 = {sx: _4x, sy: _4y, ex: _5x, ey: _5y};
        if (this.calcGap(r1, x, y) > 4 &&
            this.calcGap(r2, x, y) > 4 &&
            this.calcGap(r3, x, y) > 4) {
            return false;
        }
        this.select();
        return true;
    }

}


export class CVertiStraightLineObject extends CBiToolObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawVertiStraightLinesPlotter(name, this);
    }

    setDrawPos(x, y) {
        for (let index in this.points) {
            this.points[index].setPosXY(x, y);
        }
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let c = new CPoint("frame0.k0");
        c.setPosXY(x, y);
        let sx = this.getPoint(0).getPosXY().x;
        if (x > sx + 4 || x < sx - 4) {
            return false;
        }
        this.select();
        return true;
    }

}


export class CPriceLineObject extends CSegLineObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawPriceLinesPlotter(name, this);
    }

    setDrawPos(x, y) {
        for (let index in this.points) {
            this.points[index].setPosXY(x, y);
        }
    }

    isSelected(x, y) {
        if (super.isSelected(x, y) === true) {
            return true;
        }
        let c = new CPoint("frame0.k0");
        c.setPosXY(x, y);
        let sx = this.getPoint(0).getPosXY().x;
        let sy = this.getPoint(0).getPosXY().y;
        let ex = this.getPoint(1).getPosXY().x;
        let ey = this.getPoint(1).getPosXY().y;
        if (x < sx - 4) {
            return false;
        }
        if (y >= sy + 4 || y <= sy - 4) {
            return false;
        }
        this.select();
        return true;
    }

}


export class CArrowLineObject extends CSegLineObject {

    constructor(name) {
        super(name);
        this.drawer = new plotters.DrawArrowLinesPlotter(name, this);
    }

}

