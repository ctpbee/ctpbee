export class MEvent {

    constructor() {
        this._handlers = [];
    }

    addHandler(o, f) {
        if (this.indexOf(o, f) < 0)
            this._handlers.push({obj: o, func: f});
    }

    removeHandler(o, f) {
        let i = this.indexOf(o, f);
        if (i >= 0)
            this._handlers.splice(i, 1);
    }

    raise(s, g) {
        let a = this._handlers;
        let e, i, c = a.length;
        for (i = 0; i < c; i++) {
            e = a[i];
            e.func(s, g);
        }
    }

    indexOf(o, f) {
        let a = this._handlers;
        let e, i, c = a.length;
        for (i = 0; i < c; i++) {
            e = a[i];
            if (o === e.obj && f === e.func)
                return i;
        }
        return -1;
    }

}
