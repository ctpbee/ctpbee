import {NamedObject} from './named_object'
import {ChartManager} from './chart_manager'
import {MEvent} from './mevent'

export class ChartArea extends NamedObject {

    static DockStyle = {
        Left: 0,
        Top: 1,
        Right: 2,
        Bottom: 3,
        Fill: 4
    };

    constructor(name) {
        super(name);
        this._left = 0;
        this._top = 0;
        this._right = 0;
        this._bottom = 0;
        this._changed = false;
        this._highlighted = false;
        this._pressed = false;
        this._selected = false;
        this.Measuring = new MEvent();
    }

    getDockStyle() {
        return this._dockStyle;
    }

    setDockStyle(dockStyle) {
        this._dockStyle = dockStyle;
    }

    getLeft() {
        return this._left;
    }


    getTop() {
        return this._top;
    }


    setTop(v) {
        if (this._top !== v) {
            this._top = v;
            this._changed = true;
        }
    }


    getRight() {
        return this._right;
    }


    getBottom() {
        return this._bottom;
    }

    setBottom(v) {
        if (this._bottom !== v) {
            this._bottom = v;
            this._changed = true;
        }
    }

    getCenter() {
        return (this._left + this._right) >> 1;
    }

    getMiddle() {
        return (this._top + this._bottom) >> 1;
    }

    getWidth() {
        return this._right - this._left;
    }

    getHeight() {
        return this._bottom - this._top;
    }

    getRect() {
        return {
            X: this._left,
            Y: this._top,
            Width: this._right - this._left,
            Height: this._bottom - this._top
        };
    }

    contains(x, y) {
        if (x >= this._left && x < this._right)
            if (y >= this._top && y < this._bottom)
                return [this];
        return null;
    }

    getMeasuredWidth() {
        return this._measuredWidth;
    }

    getMeasuredHeight() {
        return this._measuredHeight;
    }

    setMeasuredDimension(width, height) {
        this._measuredWidth = width;
        this._measuredHeight = height;
    }

    measure(context, width, height) {
        this._measuredWidth = 0;
        this._measuredHeight = 0;
        this.Measuring.raise(this, {Width: width, Height: height});
        if (this._measuredWidth === 0 && this._measuredHeight === 0)
            this.setMeasuredDimension(width, height);
    }

    layout(left, top, right, bottom, forceChange) {
        left <<= 0;
        if (this._left !== left) {
            this._left = left;
            this._changed = true;
        }
        top <<= 0;
        if (this._top !== top) {
            this._top = top;
            this._changed = true;
        }
        right <<= 0;
        if (this._right !== right) {
            this._right = right;
            this._changed = true;
        }
        bottom <<= 0;
        if (this._bottom !== bottom) {
            this._bottom = bottom;
            this._changed = true;
        }
        if (forceChange)
            this._changed = true;
    }

    isChanged() {
        return this._changed;
    }

    setChanged(v) {
        this._changed = v;
    }

    isHighlighted() {
        return this._highlighted;
    }

    getHighlightedArea() {
        return this._highlighted ? this : null;
    }


    highlight(area) {
        this._highlighted = (this === area);
        return this._highlighted ? this : null;
    }

    isPressed() {
        return this._pressed;
    }


    setPressed(v) {
        this._pressed = v;
    }

    isSelected() {
        return this._selected;
    }

    getSelectedArea() {
        return this._selected ? this : null;
    }

    select(area) {
        this._selected = (this === area);
        return this._selected ? this : null;
    }

    onMouseMove(x, y) {
        return null;
    }

    onMouseLeave(x, y) {
    }

    onMouseDown(x, y) {
        return null;
    }

    onMouseUp(x, y) {
        return null;
    }

}


export class MainArea extends ChartArea {

    constructor(name) {
        super(name);
        this._dragStarted = false;
        this._oldX = 0;
        this._oldY = 0;
        this._passMoveEventToToolManager = true;
    }

    onMouseMove(x, y) {
        let mgr = ChartManager.instance;
        if (mgr._capturingMouseArea === this)
            if (this._dragStarted === false)
                if (Math.abs(this._oldX - x) > 1 || Math.abs(this._oldY - y) > 1)
                    this._dragStarted = true;
        if (this._dragStarted) {
            mgr.hideCursor();
            if (mgr.onToolMouseDrag(this.getFrameName(), x, y))
                return this;
            mgr.getTimeline(this.getDataSourceName()).move(x - this._oldX);
            return this;
        }
        if (this._passMoveEventToToolManager && mgr.onToolMouseMove(this.getFrameName(), x, y)) {
            mgr.hideCursor();
            return this;
        }
        switch (mgr._drawingTool) {
            case ChartManager.DrawingTool.Cursor:
                mgr.showCursor();
                break;
            case ChartManager.DrawingTool.CrossCursor:
                if (mgr.showCrossCursor(this, x, y))
                    mgr.hideCursor();
                else
                    mgr.showCursor();
                break;
            default:
                mgr.hideCursor();
                break;
        }
        return this;
    }

    onMouseLeave(x, y) {
        this._dragStarted = false;
        this._passMoveEventToToolManager = true;
    }

    onMouseDown(x, y) {
        let mgr = ChartManager.instance;
        mgr.getTimeline(this.getDataSourceName()).startMove();
        this._oldX = x;
        this._oldY = y;
        this._dragStarted = false;
        if (mgr.onToolMouseDown(this.getFrameName(), x, y))
            this._passMoveEventToToolManager = false;
        return this;
    }

    onMouseUp(x, y) {
        let mgr = ChartManager.instance;
        let ret = null;
        if (this._dragStarted) {
            this._dragStarted = false;
            ret = this;
        }
        if (mgr.onToolMouseUp(this.getFrameName(), x, y))
            ret = this;
        this._passMoveEventToToolManager = true;
        return ret;
    }
}


export class IndicatorArea extends ChartArea {

    constructor(name) {
        super(name);
        this._dragStarted = false;
        this._oldX = 0;
        this._oldY = 0;
    }

    onMouseMove(x, y) {
        let mgr = ChartManager.instance;
        if (mgr._capturingMouseArea === this) {
            if (this._dragStarted === false) {
                if (this._oldX !== x || this._oldY !== y) {
                    this._dragStarted = true;
                }
            }
        }
        if (this._dragStarted) {
            mgr.hideCursor();
            mgr.getTimeline(this.getDataSourceName()).move(x - this._oldX);
            return this;
        }
        switch (mgr._drawingTool) {
            case ChartManager.DrawingTool.CrossCursor:
                if (mgr.showCrossCursor(this, x, y))
                    mgr.hideCursor();
                else
                    mgr.showCursor();
                break;
            default:
                mgr.showCursor();
                break;
        }
        return this;
    }

    onMouseLeave(x, y) {
        this._dragStarted = false;
    }


    onMouseDown(x, y) {
        let mgr = ChartManager.instance;
        mgr.getTimeline(this.getDataSourceName()).startMove();
        this._oldX = x;
        this._oldY = y;
        this._dragStarted = false;
        return this;
    }

    onMouseUp(x, y) {
        if (this._dragStarted) {
            this._dragStarted = false;
            return this;
        }
        return null;
    }

}


export class MainRangeArea extends ChartArea {

    constructor(name) {
        super(name);
    }

    onMouseMove(x, y) {
        ChartManager.instance.showCursor();
        return this;
    }

}


export class IndicatorRangeArea extends ChartArea {

    constructor(name) {
        super(name);
    }

    onMouseMove(x, y) {
        ChartManager.instance.showCursor();
        return this;
    }

}


export class TimelineArea extends ChartArea {

    constructor(name) {
        super(name);
    }

    onMouseMove(x, y) {
        ChartManager.instance.showCursor();
        return this;
    }

}


export class ChartAreaGroup extends ChartArea {

    constructor(name) {
        super(name);
        this._areas = [];
        this._highlightedArea = null;
        this._selectedArea = null;
    }

    contains(x, y) {
        let areas;
        let a, i, cnt = this._areas.length;
        for (i = 0; i < cnt; i++) {
            a = this._areas[i];
            areas = a.contains(x, y);
            if (areas !== null) {
                areas.push(this);
                return areas;
            }
        }
        return super.contains(x, y);
    }

    getAreaCount() {
        return this._areas.length;
    }

    getAreaAt(index) {
        if (index < 0 || index >= this._areas.length) {
            return null;
        }
        return this._areas[index];
    }


    addArea(area) {
        this._areas.push(area);
    }

    removeArea(area) {
        let i, cnt = this._areas.length;
        for (i = 0; i < cnt; i++) {
            if (area === this._areas[i]) {
                this._areas.splice(i);
                this.setChanged(true);
                break;
            }
        }
    }

    getGridColor() {
        return this._gridColor;
    }

    setGridColor(c) {
        this._gridColor = c;
    }

    getHighlightedArea() {
        if (this._highlightedArea !== null) {
            return this._highlightedArea.getHighlightedArea();
        }
        return null;
    }

    highlight(area) {
        this._highlightedArea = null;
        let e, i, cnt = this._areas.length;
        for (i = 0; i < cnt; i++) {
            e = this._areas[i].highlight(area);
            if (e !== null) {
                this._highlightedArea = e;
                return this;
            }
        }
        return null;
    }

    getSelectedArea() {
        if (this._selectedArea !== null) {
            return this._selectedArea.getSelectedArea();
        }
        return null;
    }

    select(area) {
        this._selectedArea = null;
        let e, i, cnt = this._areas.length;
        for (i = 0; i < cnt; i++) {
            e = this._areas[i].select(area);
            if (e !== null) {
                this._selectedArea = e;
                return this;
            }
        }
        return null;
    }

    onMouseLeave(x, y) {
        let i, cnt = this._areas.length;
        for (i = 0; i < cnt; i++)
            this._areas[i].onMouseLeave(x, y);
    }

    onMouseUp(x, y) {
        let a, i, cnt = this._areas.length;
        for (i = 0; i < cnt; i++) {
            a = this._areas[i].onMouseUp(x, y);
            if (a !== null)
                return a;
        }
        return null;
    }

}

