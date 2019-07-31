import {NamedObject} from './named_object'
import {ChartManager} from './chart_manager'
import {DataSource} from './data_sources'

export class Timeline extends NamedObject {

    static itemWidth = [1, 3, 3, 5, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29];

    static spaceWidth = [1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 7, 7, 7];

    static PADDING_LEFT = 4;

    static PADDING_RIGHT = 8;

    constructor(name) {
        super(name);
        this._updated = false;
        this._innerLeft = 0;
        this._innerWidth = 0;
        this._firstColumnLeft = 0;
        this._scale = 3;
        this._lastScale = -1;
        this._maxItemCount = 0;
        this._maxIndex = 0;
        this._firstIndex = -1;
        this._selectedIndex = -1;
        this._savedFirstIndex = -1;
    }


    isLatestShown() {
        return this.getLastIndex() === this._maxIndex;
    }

    isUpdated() {
        return this._updated;
    }

    setUpdated(v) {
        this._updated = v;
    }

    getItemWidth() {
        return Timeline.itemWidth[this._scale];
    }

    getSpaceWidth() {
        return Timeline.spaceWidth[this._scale];
    }

    getColumnWidth() {
        return this.getSpaceWidth() + this.getItemWidth();
    }

    getInnerWidth() {
        return this._innerWidth;
    }

    getItemLeftOffset() {
        return this.getSpaceWidth();
    }

    getItemCenterOffset() {
        return this.getSpaceWidth() + (this.getItemWidth() >> 1);
    }

    getFirstColumnLeft() {
        return this._firstColumnLeft;
    }

    getMaxItemCount() {
        return this._maxItemCount;
    }

    getFirstIndex() {
        return this._firstIndex;
    }

    getLastIndex() {
        return Math.min(this._firstIndex + this._maxItemCount, this._maxIndex);
    }

    getSelectedIndex() {
        return this._selectedIndex;
    }

    getMaxIndex() {
        return this._maxIndex;
    }

    calcColumnCount(w) {
        return Math.floor(w / this.getColumnWidth()) << 0;
    }

    calcFirstColumnLeft(maxItemCount) {
        return this._innerLeft + this._innerWidth - (this.getColumnWidth() * maxItemCount);
    }

    calcFirstIndexAlignRight(oldFirstIndex, oldMaxItemCount, newMaxItemCount) {
        return Math.max(0, oldFirstIndex + Math.max(oldMaxItemCount, 1) - Math.max(newMaxItemCount, 1));
    }

    calcFirstIndex(newMaxItemCount) {
        return this.validateFirstIndex(
            this.calcFirstIndexAlignRight(this._firstIndex, this._maxItemCount,
                newMaxItemCount), newMaxItemCount);
    }

    updateMaxItemCount() {
        let newMaxItemCount = this.calcColumnCount(this._innerWidth);
        let newFirstIndex;
        if (this._maxItemCount < 1) {
            newFirstIndex = this.calcFirstIndex(newMaxItemCount);
        } else if (this._lastScale === this._scale) {
            newFirstIndex = this.validateFirstIndex(this._firstIndex - (newMaxItemCount - this._maxItemCount));
        } else {
            let focusedIndex = (this._selectedIndex >= 0) ? this._selectedIndex : this.getLastIndex() - 1;
            newFirstIndex = this.validateFirstIndex(focusedIndex -
                Math.round((focusedIndex - this._firstIndex) * newMaxItemCount / this._maxItemCount));
        }
        this._lastScale = this._scale;
        if (this._firstIndex !== newFirstIndex) {
            if (this._selectedIndex === this._firstIndex)
                this._selectedIndex = newFirstIndex;
            this._firstIndex = newFirstIndex;
            this._updated = true;
        }
        if (this._maxItemCount !== newMaxItemCount) {
            this._maxItemCount = newMaxItemCount;
            this._updated = true;
        }
        this._firstColumnLeft = this.calcFirstColumnLeft(newMaxItemCount);
    }

    validateFirstIndex(firstIndex, maxItemCount) {
        if (this._maxIndex < 1) {
            return -1;
        }
        if (firstIndex < 0) {
            return 0;
        }
        let lastFirst = Math.max(0, this._maxIndex - 1 /*maxItemCount*/);
        if (firstIndex > lastFirst) {
            return lastFirst;
        }
        return firstIndex;
    }

    validateSelectedIndex() {
        if (this._selectedIndex < this._firstIndex)
            this._selectedIndex = -1;
        else if (this._selectedIndex >= this.getLastIndex())
            this._selectedIndex = -1;
    }

    onLayout() {
        let mgr = ChartManager.instance;
        let area = mgr.getArea(this.getDataSourceName() + ".main");
        if (area !== null) {
            this._innerLeft = area.getLeft() + Timeline.PADDING_LEFT;
            let w = Math.max(0, area.getWidth() - (Timeline.PADDING_LEFT + Timeline.PADDING_RIGHT));
            if (this._innerWidth !== w) {
                this._innerWidth = w;
                this.updateMaxItemCount();
            }
        }
    }

    toIndex(x) {
        return this._firstIndex + this.calcColumnCount(x - this._firstColumnLeft);
    }

    toColumnLeft(index) {
        return this._firstColumnLeft + (this.getColumnWidth() * (index - this._firstIndex));
    }

    toItemLeft(index) {
        return this.toColumnLeft(index) + this.getItemLeftOffset();
    }

    toItemCenter(index) {
        return this.toColumnLeft(index) + this.getItemCenterOffset();
    }

    selectAt(x) {
        this._selectedIndex = this.toIndex(x);
        this.validateSelectedIndex();
        return (this._selectedIndex >= 0);
    }

    unselect() {
        this._selectedIndex = -1;
    }

    update() {
        let mgr = ChartManager.instance;
        let ds = mgr.getDataSource(this.getDataSourceName());
        let oldMaxIndex = this._maxIndex;
        this._maxIndex = ds.getDataCount();
        switch (ds.getUpdateMode()) {
            case DataSource.UpdateMode.Refresh:
                if (this._maxIndex < 1)
                    this._firstIndex = -1;
                else
                    this._firstIndex = Math.max(this._maxIndex - this._maxItemCount, 0);
                this._selectedIndex = -1;
                this._updated = true;
                break;
            case DataSource.UpdateMode.Append:
                let lastIndex = this.getLastIndex();
                let erasedCount = ds.getErasedCount();
                if (lastIndex < oldMaxIndex) {
                    if (erasedCount > 0) {
                        this._firstIndex = Math.max(this._firstIndex - erasedCount, 0);
                        if (this._selectedIndex >= 0) {
                            this._selectedIndex -= erasedCount;
                            this.validateSelectedIndex();
                        }
                        this._updated = true;
                    }
                } else if (lastIndex === oldMaxIndex) {
                    this._firstIndex += (this._maxIndex - oldMaxIndex);
                    if (this._selectedIndex >= 0) {
                        this._selectedIndex -= erasedCount;
                        this.validateSelectedIndex();
                    }
                    this._updated = true;
                }
                break;
        }
    }

    move(x) {
        if (this.isLatestShown()) {
            ChartManager.instance.getArea(this.getDataSourceName() + ".mainRange").setChanged(true);
        }
        this._firstIndex = this.validateFirstIndex(
            this._savedFirstIndex - this.calcColumnCount(x), this._maxItemCount);
        this._updated = true;
        if (this._selectedIndex >= 0)
            this.validateSelectedIndex();
    }

    startMove() {
        this._savedFirstIndex = this._firstIndex;
    }

    scale(s) {
        this._scale += s;
        if (this._scale < 0) {
            this._scale = 0;
        } else if (this._scale >= Timeline.itemWidth.length) {
            this._scale = Timeline.itemWidth.length - 1;
        }
        this.updateMaxItemCount();
        if (this._selectedIndex >= 0) {
            this.validateSelectedIndex();
        }
    }

}
