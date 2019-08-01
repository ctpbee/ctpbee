export class CName {

    constructor(name) {
        this._names = [];
        this._comps = [];
        if (name instanceof CName) {
            this._names = name._names;
            this._comps = name._comps;
        } else {
            let comps = name.split(".");
            let dotNum = comps.length - 1;
            if (dotNum > 0) {
                this._comps = comps;
                this._names.push(comps[0]);
                for (let i = 1; i <= dotNum; i++) {
                    this._names.push(this._names[i - 1] + "." + comps[i]);
                }
            } else {
                this._comps.push(name);
                this._names.push(name);
            }
        }
    }

    getCompAt(index) {
        if (index >= 0 && index < this._comps.length)
            return this._comps[index];
        return "";
    }

    getName(index) {
        if (index < 0) {
            if (this._names.length > 0)
                return this._names[this._names.length - 1];
        } else if (index < this._names.length) {
            return this._names[index];
        }
        return "";
    }

}
