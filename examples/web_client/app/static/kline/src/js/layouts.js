import * as areas from './areas'
import {ChartManager} from './chart_manager'
import * as themes from './themes'
import {ChartSettings} from './chart_settings'

export class TableLayout extends areas.ChartAreaGroup {

    constructor(name) {
        super(name);
        this._nextRowId = 0;
        this._focusedRowIndex = -1;
    }

    getNextRowId() {
        return this._nextRowId++;
    }

    measure(context, width, height) {
        this.setMeasuredDimension(width, height);
        let rowH, prevH = 0,
            totalH = 0;
        let h, rows;
        let rh = [];
        let i, cnt = this._areas.length;
        for (i = 0; i < cnt; i += 2) {
            rowH = this._areas[i].getHeight();
            if (rowH === 0) {
                if (i === 0) {
                    rows = (cnt + 1) >> 1;
                    let n = (rows * 2) + 5;
                    let nh = ((height / n) * 2) << 0;
                    h = height;
                    for (i = rows - 1; i > 0; i--) {
                        rh.unshift(nh);
                        h -= nh;
                    }
                    rh.unshift(h);
                    break;
                } else if (i === 2) {
                    rowH = prevH / 3;
                } else {
                    rowH = prevH;
                }
            }
            totalH += rowH;
            prevH = rowH;
            rh.push(rowH);
        }
        if (totalH > 0) {
            let rate = height / totalH;
            rows = (cnt + 1) >> 1;
            h = height;
            for (i = rows - 1; i > 0; i--) {
                rh[i] *= rate;
                h -= rh[i];
            }
            rh[0] = h;
        }
        let nw = 8;
        // chart depths sidebar (深度图侧边栏宽度)
        let minRW = 76;
        let maxRW = Math.min(240, width >> 1);
        let rw = minRW;
        let mgr = ChartManager.instance;
        let timeline = mgr.getTimeline(this.getDataSourceName());
        if (timeline.getFirstIndex() >= 0) {
            let firstIndexes = [];
            for (rw = minRW; rw < maxRW; rw += nw) {
                firstIndexes.push(timeline.calcFirstIndex(timeline.calcColumnCount(width - rw)));
            }
            let lastIndex = timeline.getLastIndex();
            let dpNames = [".main", ".secondary"];
            let minmaxes = new Array(firstIndexes.length);
            let iArea, iIndex;
            for (iArea = 0, iIndex = 0, rw = minRW; iArea < this._areas.length && iIndex < firstIndexes.length; iArea += 2) {
                let area = this._areas[iArea];
                let plotter = mgr.getPlotter(area.getName() + "Range.main");
                for (let iDp in dpNames) {
                    let dp = mgr.getDataProvider(area.getName() + dpNames[iDp]);
                    if (dp === undefined) {
                        continue;
                    }
                    dp.calcRange(firstIndexes, lastIndex, minmaxes, null);
                    while (iIndex < firstIndexes.length) {
                        let minW = plotter.getRequiredWidth(context, minmaxes[iIndex].min);
                        let maxW = plotter.getRequiredWidth(context, minmaxes[iIndex].max);
                        if (Math.max(minW, maxW) < rw) {
                            break;
                        }
                        iIndex++;
                        rw += nw;
                    }
                }
            }
        }
        for (i = 1; i < this._areas.length; i += 2) {
            this._areas[i].measure(context, rw, rh[i >> 1]);
        }
        let lw = width - rw;
        for (i = 0; i < this._areas.length; i += 2) {
            this._areas[i].measure(context, lw, rh[i >> 1]);
        }
    }

    layout(left, top, right, bottom, forceChange) {
        super.layout(left, top, right, bottom, forceChange);
        if (this._areas.length < 1)
            return;
        let area;
        let center = left + this._areas[0].getMeasuredWidth();
        let t = top,
            b;
        if (!forceChange)
            forceChange = this.isChanged();
        let i, cnt = this._areas.length;
        for (i = 0; i < cnt; i++) {
            area = this._areas[i];
            b = t + area.getMeasuredHeight();
            area.layout(left, t, center, b, forceChange);
            i++;
            area = this._areas[i];
            area.layout(center, t, this.getRight(), b, forceChange);
            t = b;
        }
        this.setChanged(false);
    }

    drawGrid(context) {
        if (this._areas.length < 1) {
            return;
        }
        let mgr = ChartManager.instance;
        let theme = mgr.getTheme(this.getFrameName());
        context.fillStyle = theme.getColor(themes.Theme.Color.Grid1);
        context.fillRect(this._areas[0].getRight(), this.getTop(), 1, this.getHeight());
        let i, cnt = this._areas.length - 2;
        for (i = 0; i < cnt; i += 2)
            context.fillRect(this.getLeft(), this._areas[i].getBottom(), this.getWidth(), 1);
        if (!mgr.getCaptureMouseWheelDirectly()) {
            for (i = 0, cnt += 2; i < cnt; i += 2) {
                if (this._areas[i].isSelected()) {
                    context.strokeStyle = theme.getColor(themes.Theme.Color.Indicator1);
                    context.strokeRect(
                        this.getLeft() + 0.5, this.getTop() + 0.5,
                        this.getWidth() - 1, this.getHeight() - 1);
                    break;
                }
            }
        }
    }

    highlight(area) {
        this._highlightedArea = null;
        let e, i, cnt = this._areas.length;
        for (i = 0; i < cnt; i++) {
            e = this._areas[i];
            if (e === area) {
                i &= ~1;
                e = this._areas[i];
                e.highlight(e);
                this._highlightedArea = e;
                i++;
                e = this._areas[i];
                e.highlight(null);
                e.highlight(e);
            } else {
                e.highlight(null);
            }
        }
        return this._highlightedArea !== null ? this : null;
    }

    select(area) {
        this._selectedArea = null;
        let e, i, cnt = this._areas.length;
        for (i = 0; i < cnt; i++) {
            e = this._areas[i];
            if (e === area) {
                i &= ~1;
                e = this._areas[i];
                e.select(e);
                this._selectedArea = e;
                i++;
                e = this._areas[i];
                e.select(e);
            } else {
                e.select(null);
            }
        }
        return this._selectedArea !== null ? this : null;
    }

    onMouseMove(x, y) {
        if (this._focusedRowIndex >= 0) {
            let upper = this._areas[this._focusedRowIndex];
            let lower = this._areas[this._focusedRowIndex + 2];
            let d = y - this._oldY;
            if (d === 0)
                return this;
            let upperBottom = this._oldUpperBottom + d;
            let lowerTop = this._oldLowerTop + d;
            if (upperBottom - upper.getTop() >= 60 && lower.getBottom() - lowerTop >= 60) {
                upper.setBottom(upperBottom);
                lower.setTop(lowerTop);
            }
            return this;
        }
        let i, cnt = this._areas.length - 2;
        for (i = 0; i < cnt; i += 2) {
            let b = this._areas[i].getBottom();
            if (y >= b - 4 && y < b + 4) {
                ChartManager.instance.showCursor('n-resize');
                return this;
            }
        }
        return null;
    }

    onMouseLeave(x, y) {
        this._focusedRowIndex = -1;
    }

    onMouseDown(x, y) {
        let i, cnt = this._areas.length - 2;
        for (i = 0; i < cnt; i += 2) {
            let b = this._areas[i].getBottom();
            if (y >= b - 4 && y < b + 4) {
                this._focusedRowIndex = i;
                this._oldY = y;
                this._oldUpperBottom = b;
                this._oldLowerTop = this._areas[i + 2].getTop();
                return this;
            }
        }
        return null;
    }

    onMouseUp(x, y) {
        if (this._focusedRowIndex >= 0) {
            this._focusedRowIndex = -1;
            let i, cnt = this._areas.length;
            let height = [];
            for (i = 0; i < cnt; i += 2) {
                height.push(this._areas[i].getHeight());
            }
            ChartSettings.get().charts.areaHeight = height;
            ChartSettings.save();
        }
        return this;
    }

}


export class DockableLayout extends areas.ChartAreaGroup {

    constructor(name) {
        super(name);
    }

    measure(context, width, height) {
        super.measure(context, width, height);
        width = this.getMeasuredWidth();
        height = this.getMeasuredHeight();
        for (let i in this._areas) {
            let area = this._areas[i];
            area.measure(context, width, height);
            switch (area.getDockStyle()) {
                case areas.ChartArea.DockStyle.left:
                case areas.ChartArea.DockStyle.Right:
                    width -= area.getMeasuredWidth();
                    break;
                case areas.ChartArea.DockStyle.Top:
                case areas.ChartArea.DockStyle.Bottom:
                    height -= area.getMeasuredHeight();
                    break;
                case areas.ChartArea.DockStyle.Fill:
                    width = 0;
                    height = 0;
                    break;
            }
        }
    }

    layout(left, top, right, bottom, forceChange) {
        super.layout(left, top, right, bottom, forceChange);
        left = this.getLeft();
        top = this.getTop();
        right = this.getRight();
        bottom = this.getBottom();
        let w, h;
        if (!forceChange) {
            forceChange = this.isChanged();
        }
        for (let i in this._areas) {
            let area = this._areas[i];
            switch (area.getDockStyle()) {
                case areas.ChartArea.DockStyle.left:
                    w = area.getMeasuredWidth();
                    area.layout(left, top, left + w, bottom, forceChange);
                    left += w;
                    break;
                case areas.ChartArea.DockStyle.Top:
                    h = area.getMeasuredHeight();
                    area.layout(left, top, right, top + h, forceChange);
                    top += h;
                    break;
                case areas.ChartArea.DockStyle.Right:
                    w = area.getMeasuredWidth();
                    area.layout(right - w, top, right, bottom, forceChange);
                    right -= w;
                    break;
                case areas.ChartArea.DockStyle.Bottom:
                    h = area.getMeasuredHeight();
                    area.layout(left, bottom - h, right, bottom, forceChange);
                    bottom -= h;
                    break;
                case areas.ChartArea.DockStyle.Fill:
                    area.layout(left, top, right, bottom, forceChange);
                    left = right;
                    top = bottom;
                    break;
            }
        }
        this.setChanged(false);
    }

    drawGrid(context) {
        let mgr = ChartManager.instance;
        let theme = mgr.getTheme(this.getFrameName());
        let left = this.getLeft();
        let top = this.getTop();
        let right = this.getRight();
        let bottom = this.getBottom();
        context.fillStyle = theme.getColor(this._gridColor);
        for (let i in this._areas) {
            let area = this._areas[i];
            switch (area.getDockStyle()) {
                case areas.ChartArea.DockStyle.Left:
                    context.fillRect(area.getRight(), top, 1, bottom - top);
                    left += area.getWidth();
                    break;
                case areas.ChartArea.DockStyle.Top:
                    context.fillRect(left, area.getBottom(), right - left, 1);
                    top += area.getHeight();
                    break;
                case areas.ChartArea.DockStyle.Right:
                    context.fillRect(area.getLeft(), top, 1, bottom - top);
                    right -= area.getWidth();
                    break;
                case areas.ChartArea.DockStyle.Bottom:
                    context.fillRect(left, area.getTop(), right - left, 1);
                    bottom -= area.getHeight();
                    break;
            }
        }
    }

}
