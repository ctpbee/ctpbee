import {NamedObject} from './named_object'
import {CPoint} from './cpoint'
import * as ctools from './ctools'

export class CToolManager extends NamedObject {

    constructor(name) {
        super(name);
        this.selectedObject = -1;
        this.toolObjects = [];
    }

    getToolObjectCount() {
        return this.toolObjects.length;
    }

    addToolObject(o) {
        this.toolObjects.push(o);
    }

    getToolObject(i) {
        if (i < this.toolObjects.length && i >= 0) {
            return this.toolObjects[i];
        }
        return null;
    }

    getCurrentObject() {
        return this.getToolObject(this.getToolObjectCount() - 1);
    }

    getSelectedObject() {
        return this.getToolObject(this.selectedObject);
    }

    delCurrentObject() {
        this.toolObjects.splice(this.getToolObjectCount() - 1, 1);
    }

    delSelectedObject() {
        this.toolObjects.splice(this.selectedObject, 1);
        this.selectedObject = -1;
    }

    acceptMouseMoveEvent(x, y) {
        if (this.selectedObject === -1) {
            let curr = this.toolObjects[this.getToolObjectCount() - 1];
            if (curr !== null && curr !== undefined && curr.getState() !== ctools.CToolObject.state.AfterDraw)
                return curr.acceptMouseMoveEvent(x, y);
        } else {
            let sel = this.toolObjects[this.selectedObject];
            if (sel.getState() === ctools.CToolObject.state.Draw) {
                return sel.acceptMouseMoveEvent(x, y);
            }
            sel.unselect();
            this.selectedObject = -1;
        }
        for (let index in this.toolObjects) {
            if (this.toolObjects[index].isSelected(x, y)) {
                this.selectedObject = index;
                return false;
            }
        }
        return false;
    }

    acceptMouseDownEvent(x, y) {
        this.mouseDownMove = false;
        if (this.selectedObject === -1) {
            let curr = this.toolObjects[this.getToolObjectCount() - 1];
            if (curr !== null && curr !== undefined && curr.getState() !== ctools.CToolObject.state.AfterDraw)
                return curr.acceptMouseDownEvent(x, y);
        } else {
            let sel = this.toolObjects[this.selectedObject];
            if (sel.getState() !== ctools.CToolObject.state.BeforeDraw)
                return sel.acceptMouseDownEvent(x, y);
        }
        return false;
    }

    acceptMouseDownMoveEvent(x, y) {
        this.mouseDownMove = true;
        if (this.selectedObject === -1) {
            let curr = this.toolObjects[this.getToolObjectCount() - 1];
            if (curr !== null && curr !== undefined && curr.getState() === ctools.CToolObject.state.Draw)
                return curr.acceptMouseDownMoveEvent(x, y);
            return false;
        } else {
            let sel = this.toolObjects[this.selectedObject];
            if (sel.getState() !== ctools.CToolObject.state.BeforeDraw) {
                if (sel.acceptMouseDownMoveEvent(x, y) === true) {
                    let point = this.toolObjects[this.selectedObject].points;
                    for (let i = 0; i < point.length; i++) {
                        if (point[i].state === CPoint.state.Highlight || point[i].state === CPoint.state.Show) {
                            return true;
                        }
                    }
                }
                return true;
            }
        }
    }

    acceptMouseUpEvent(x, y) {
        if (this.mouseDownMove === true) {
            if (this.selectedObject === -1) {
                let curr = this.toolObjects[this.getToolObjectCount() - 1];
                if (curr !== null && curr !== undefined && curr.getState() === ctools.CToolObject.state.Draw)
                    return curr.acceptMouseUpEvent(x, y);
                return true;
            } else {
                let sel = this.toolObjects[this.selectedObject];
                if (sel.getState() !== ctools.CToolObject.state.BeforeDraw)
                    return sel.acceptMouseUpEvent(x, y);
            }
        }
        if (this.selectedObject !== -1) {
            return true;
        }
        let curr = this.toolObjects[this.getToolObjectCount() - 1];
        if (curr !== null && curr !== undefined) {
            if (curr.getState() === ctools.CToolObject.state.Draw)
                return true;
            if (!curr.isValidMouseXY(x, y)) {
                return false;
            }
            if (curr.isSelected(x, y)) {
                return true;
            }
        }
        return false;
    }

}

