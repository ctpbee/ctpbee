import {CName} from './cname'

export class NamedObject {

    constructor(name) {
        this._name = name;
        this._nameObj = new CName(name);
    }

    getFrameName() {
        return this._nameObj.getName(0);
    }

    getDataSourceName() {
        return this._nameObj.getName(1);
    }

    getAreaName() {
        return this._nameObj.getName(2);
    }

    getName() {
        return this._nameObj.getName(-1);
    }

    getNameObject() {
        return this._nameObj;
    }

    getRectCrossPt(rect, startPt, endPt) {
        let crossPt;
        let firstPt = {x: -1, y: -1};
        let secondPt = {x: -1, y: -1};
        let xdiff = endPt.x - startPt.x;
        let ydiff = endPt.y - startPt.y;
        if (Math.abs(xdiff) < 2) {
            firstPt = {x: startPt.x, y: rect.top};
            secondPt = {x: endPt.x, y: rect.bottom};
            crossPt = [firstPt, secondPt];
            return crossPt;
        }
        let k = ydiff / xdiff;
        secondPt.x = rect.right;
        secondPt.y = startPt.y + (rect.right - startPt.x) * k;
        firstPt.x = rect.left;
        firstPt.y = startPt.y + (rect.left - startPt.x) * k;
        crossPt = [firstPt, secondPt];
        return crossPt;
    }

}
