export class ExprEnv {

     static inst = null;
     _ds = null;
     _firstIndex = null;

    static get () {
        return this.inst;
    }

    static set (env) {
        this.inst = env;
    }

     getDataSource() {
        return this._ds;
    }

     setDataSource(ds) {
        return this._ds = ds;
    }

     getFirstIndex() {
        return this._firstIndex;
    }

     setFirstIndex(n) {
        return this._firstIndex = n;
    }

}


export class Expr {
    constructor() {
        this._rid = 0;
    }

    execute(index) {
    }

    reserve(rid, count) {
    }

    clear() {
    }
}


export class OpenExpr extends Expr {

    execute(index) {
        return ExprEnv.get()._ds.getDataAt(index).open;
    }

}


export class HighExpr extends Expr {

    execute(index) {
        return ExprEnv.get()._ds.getDataAt(index).high;
    }

}


export class LowExpr extends Expr {

    execute(index) {
        return ExprEnv.get()._ds.getDataAt(index).low;
    }

}


export class CloseExpr extends Expr {

    execute(index) {
        return ExprEnv.get()._ds.getDataAt(index).close;
    }

}


export class VolumeExpr extends Expr {

    execute(index) {
        return ExprEnv.get()._ds.getDataAt(index).volume;
    }

}


export class ConstExpr extends Expr {

    constructor(v) {
        super();
        this._value = v;
    }

    execute(index) {
        return this._value;
    }

}


export class ParameterExpr extends Expr {

    constructor(name, minValue, maxValue, defaultValue) {
        super();
        this._name = name;
        this._minValue = minValue;
        this._maxValue = maxValue;
        this._value = this._defaultValue = defaultValue;
    }

    execute(index) {
        return this._value;
    }

    getMinValue() {
        return this._minValue;
    }

    getMaxValue() {
        return this._maxValue;
    }

    getDefaultValue() {
        return this._defaultValue;
    }

    getValue() {
        return this._value;
    }

    setValue(v) {
        if (v === 0)
            this._value = 0;
        else if (v < this._minValue)
            this._value = this._minValue;
        else if (v > this._maxValue)
            this._value = this._maxValue;
        else
            this._value = v;
    }

}


export class OpAExpr extends Expr {

    constructor(a) {
        super();
        this._exprA = a;
    };

    reserve(rid, count) {
        if (this._rid < rid) {
            this._rid = rid;
            this._exprA.reserve(rid, count);
        }
    }

    clear() {
        this._exprA.clear();
    }

}

export class OpABExpr extends Expr {

    constructor(a, b) {
        super();
        this._exprA = a;
        this._exprB = b;
    }

    reserve(rid, count) {
        if (this._rid < rid) {
            this._rid = rid;
            this._exprA.reserve(rid, count);
            this._exprB.reserve(rid, count);
        }
    }

    clear() {
        this._exprA.clear();
        this._exprB.clear();
    }

}


export class OpABCExpr extends Expr {

    constructor(a, b, c) {
        super();
        this._exprA = a;
        this._exprB = b;
        this._exprC = c;
    }


    reserve(rid, count) {
        if (this._rid < rid) {
            this._rid = rid;
            this._exprA.reserve(rid, count);
            this._exprB.reserve(rid, count);
            this._exprC.reserve(rid, count);
        }
    }

    clear() {
        this._exprA.clear();
        this._exprB.clear();
        this._exprC.clear();
    };
}


export class OpABCDExpr extends Expr {

    constructor(a, b, c, d) {
        super();
        this._exprA = a;
        this._exprB = b;
        this._exprC = c;
        this._exprD = d;
    }

    reserve(rid, count) {
        if (this._rid < rid) {
            this._rid = rid;
            this._exprA.reserve(rid, count);
            this._exprB.reserve(rid, count);
            this._exprC.reserve(rid, count);
            this._exprD.reserve(rid, count);
        }
    };

    clear() {
        this._exprA.clear();
        this._exprB.clear();
        this._exprC.clear();
        this._exprD.clear();
    }

}


export class NegExpr extends OpAExpr {

    constructor(a) {
        super(a);
    };

    execute(index) {
        return -(this._exprA.execute(index));
    }

}


export class AddExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        return this._exprA.execute(index) + this._exprB.execute(index);
    }

}


export class SubExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        return this._exprA.execute(index) - this._exprB.execute(index);
    }

}


export class MulExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        return this._exprA.execute(index) * this._exprB.execute(index);
    }

}


export class DivExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        let a = this._exprA.execute(index);
        let b = this._exprB.execute(index);
        if (a === 0)
            return a;
        if (b === 0)
            return (a > 0) ? 1000000 : -1000000;
        return a / b;
    }

}


export class GtExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        return this._exprA.execute(index) > this._exprB.execute(index) ? 1 : 0;
    }

}


export class GeExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        return this._exprA.execute(index) >= this._exprB.execute(index) ? 1 : 0;
    }

}


export class LtExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        return this._exprA.execute(index) < this._exprB.execute(index) ? 1 : 0;
    }

}


export class LeExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        return this._exprA.execute(index) <= this._exprB.execute(index) ? 1 : 0;
    }

}


export class EqExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        return this._exprA.execute(index) === this._exprB.execute(index) ? 1 : 0;
    }

}


export class MaxExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        return Math.max(this._exprA.execute(index), this._exprB.execute(index));
    }

}


export class AbsExpr extends OpAExpr {

    constructor(a) {
        super(a);
    }

    execute(index) {
        return Math.abs(this._exprA.execute(index));
    }

}


export class RefExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        if (this._offset === undefined || this._offset < 0) {
            this._offset = this._exprB.execute(index);
            if (this._offset < 0) {
                throw "offset < 0";
            }
        }
        index -= this._offset;
        if (index < 0) {
            throw "index < 0";
        }
        let result = this._exprA.execute(index);
        if (isNaN(result)) {
            throw "NaN";
        }
        return result;
    }

}


export class AndExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        return (this._exprA.execute(index) !== 0) && (this._exprB.execute(index) !== 0) ? 1 : 0;
    }

}


export class OrExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
    }

    execute(index) {
        return (this._exprA.execute(index) !== 0) || (this._exprB.execute(index) !== 0) ? 1 : 0;
    }

}


export class IfExpr extends OpABCExpr {

    constructor(a, b, c) {
        super(a, b, c);
    }

    execute(index) {
        return this._exprA.execute(index) !== 0 ? this._exprB.execute(index) : this._exprC.execute(index);
    }

}


export class AssignExpr extends OpAExpr {

    constructor(name, a) {
        super(a);
        this._name = name;
        this._buf = [];
    }

    getName() {
        return this._name;
    }

    execute(index) {
        return this._buf[index];
    }

    assign(index) {
        this._buf[index] = this._exprA.execute(index);
        if (ExprEnv.get()._firstIndex >= 0) {
            if (isNaN(this._buf[index]) && !isNaN(this._buf[index - 1])) {
                throw this._name + ".assign(" + index + "): NaN";
            }
        }
    }

    reserve(rid, count) {
        if (this._rid < rid) {
            for (let c = count; c > 0; c--) {
                this._buf.push(NaN);
            }
        }
        super.reserve(rid, count);
    }

    clear() {
        super.clear();
        this._buf = [];
    }

}


export class OutputExpr extends AssignExpr {

    static outputStyle = {
        None: 0,
        Line: 1,
        VolumeStick: 2,
        MACDStick: 3,
        SARPoint: 4
    };

    constructor(name, a, style, color) {
        super(name, a);
        this._style = (style === undefined) ? OutputExpr.outputStyle.Line : style;
        this._color = color;
    }


    getStyle() {
        return this._style;
    }

    getColor() {
        return this._color;
    }

}


export class RangeOutputExpr extends OutputExpr {

    constructor(name, a, style, color) {
        super(name, a, style, color);
    }

    getName() {
        return this._name + this._exprA.getRange();
    }

}


export class RangeExpr extends OpABExpr {

    constructor(a, b) {
        super(a, b);
        this._range = -1;
        this._buf = [];
    }

    getRange() {
        return this._range;
    }

    initRange() {
        this._range = this._exprB.execute(0);
    }

    execute(index) {
        if (this._range < 0) {
            this.initRange();
        }
        let rA = this._buf[index].resultA = this._exprA.execute(index);
        return this._buf[index].result = this.calcResult(index, rA);
    }

    reserve(rid, count) {
        if (this._rid < rid) {
            for (let c = count; c > 0; c--) {
                this._buf.push({resultA: NaN, result: NaN});
            }
        }
        super.reserve(rid, count);
    }

    clear() {
        super.clear();
        this._range = -1;
        this._buf = [];
    }

}


export class HhvExpr extends RangeExpr {

    constructor(a, b) {
        super(a, b);
    }

    calcResult(index, resultA) {
        if (this._range === 0) {
            return NaN;
        }
        let first = ExprEnv.get()._firstIndex;
        if (first < 0) {
            return resultA;
        }
        if (index > first) {
            let n = this._range;
            let result = resultA;
            let start = index - n + 1;
            let i = Math.max(first, start);
            for (; i < index; i++) {
                let p = this._buf[i];
                if (result < p.resultA) {
                    result = p.resultA;
                }
            }
            return result;
        } else {
            return resultA;
        }
    }

}


export class LlvExpr extends RangeExpr {

    constructor(a, b) {
        super(a, b);
    }

    calcResult(index, resultA) {
        if (this._range === 0)
            return NaN;
        let first = ExprEnv.get()._firstIndex;
        if (first < 0)
            return resultA;
        if (index > first) {
            let n = this._range;
            let result = resultA;
            let start = index - n + 1;
            let i = Math.max(first, start);
            for (; i < index; i++) {
                let p = this._buf[i];
                if (result > p.resultA)
                    result = p.resultA;
            }
            return result;
        } else {
            return resultA;
        }
    }
}


export class CountExpr extends RangeExpr {

    constructor(a, b) {
        super(a, b);
    }

    calcResult(index, resultA) {
        if (this._range === 0)
            return NaN;
        let first = ExprEnv.get()._firstIndex;
        if (first < 0)
            return 0;
        if (index >= first) {
            let n = this._range - 1;
            if (n > index - first)
                n = index - first;
            let count = 0;
            for (; n >= 0; n--) {
                if (this._buf[index - n].resultA !== 0.0)
                    count++;
            }
            return count;
        } else {
            return 0;
        }
    }

}


export class SumExpr extends RangeExpr {

    constructor(a, b) {
        super(a, b);
    }

    calcResult(index, resultA) {
        let first = ExprEnv.get()._firstIndex;
        if (first < 0)
            return resultA;
        if (index > first) {
            let n = this._range;
            if (n === 0 || n >= index + 1 - first) {
                return this._buf[index - 1].result + resultA;
            }
            return this._buf[index - 1].result + resultA - this._buf[index - n].resultA;
        } else {
            return resultA;
        }
    }

}


export class StdExpr extends RangeExpr {

    constructor(a, b) {
        super(a, b);
    }

    calcResult(index, resultA) {
        if (this._range === 0)
            return NaN;
        let stdData = this._stdBuf[index];
        let first = ExprEnv.get()._firstIndex;
        if (first < 0) {
            stdData.resultMA = resultA;
            return 0.0;
        }
        if (index > first) {
            let n = this._range;
            if (n >= index + 1 - first) {
                n = index + 1 - first;
                stdData.resultMA = this._stdBuf[index - 1].resultMA * (1.0 - 1.0 / n) + (resultA / n);
            } else {
                stdData.resultMA = this._stdBuf[index - 1].resultMA + (resultA - this._buf[index - n].resultA) / n;
            }
            let sum = 0;
            for (let i = index - n + 1; i <= index; i++)
                sum += Math.pow(this._buf[i].resultA - stdData.resultMA, 2);
            return Math.sqrt(sum / n);
        }
        stdData.resultMA = resultA;
        return 0.0;
    }

    reserve(rid, count) {
        if (this._rid < rid) {
            for (let c = count; c > 0; c--)
                this._stdBuf.push({resultMA: NaN});
        }
        super.reserve(rid, count);
    }

    clear() {
        super.clear();
        this._stdBuf = [];
    }

}


export class MaExpr extends RangeExpr {

    constructor(a, b) {
        super(a, b);
    }

    calcResult(index, resultA) {
        if (this._range === 0)
            return NaN;
        let first = ExprEnv.get()._firstIndex;
        if (first < 0)
            return resultA;
        if (index > first) {
            let n = this._range;
            if (n >= index + 1 - first) {
                n = index + 1 - first;
                return this._buf[index - 1].result * (1.0 - 1.0 / n) + (resultA / n);
            }
            return this._buf[index - 1].result + (resultA - this._buf[index - n].resultA) / n;
        } else {
            return resultA;
        }
    }

}


export class EmaExpr extends RangeExpr {

    constructor(a, b) {
        super(a, b);
    }

    initRange() {
        super.initRange();
        this._alpha = 2.0 / (this._range + 1);
    }

    calcResult(index, resultA) {
        if (this._range === 0)
            return NaN;
        let first = ExprEnv.get()._firstIndex;
        if (first < 0)
            return resultA;
        if (index > first) {
            let prev = this._buf[index - 1];
            return this._alpha * (resultA - prev.result) + prev.result;
        }
        return resultA;
    }

}


export class ExpmemaExpr extends EmaExpr {

    constructor(a, b) {
        super(a, b);
    };

    calcResult(index, resultA) {
        let first = ExprEnv.get()._firstIndex;
        if (first < 0)
            return resultA;
        if (index > first) {
            let n = this._range;
            let prev = this._buf[index - 1];
            if (n >= index + 1 - first) {
                n = index + 1 - first;
                return prev.result * (1.0 - 1.0 / n) + (resultA / n);
            }
            return this._alpha * (resultA - prev.result) + prev.result;
        }
        return resultA;
    }

}


export class SmaExpr extends RangeExpr {

    constructor(a, b, c) {
        super(a, b);
        this._exprC = c;
        this._mul = null;
    }

    initRange() {
        super.initRange();
        this._mul = this._exprC.execute(0);
    }

    calcResult(index, resultA) {
        if (this._range === 0)
            return NaN;
        let first = ExprEnv.get()._firstIndex;
        if (first < 0)
            return resultA;
        if (index > first) {
            let n = this._range;
            if (n > index + 1 - first)
                n = index + 1 - first;
            return ((n - 1) * this._buf[index - 1].result + resultA * this._mul) / n;
        }
        return resultA;
    }
}


export class SarExpr extends OpABCDExpr {

    constructor(a, b, c, d) {
        super(a, b, c, d);
        this._buf = [];
        this._range = -1;
        this._min = null;
        this._step = null;
        this._max = null;
    }

    execute(index) {
        if (this._range < 0) {
            this._range = this._exprA.execute(0);
            this._min = this._exprB.execute(0) / 100.0;
            this._step = this._exprC.execute(0) / 100.0;
            this._max = this._exprD.execute(0) / 100.0;
        }
        let data = this._buf[index];
        let exprEnv = ExprEnv.get();
        let first = exprEnv._firstIndex;
        if (first < 0) {
            data.longPos = true;
            data.sar = exprEnv._ds.getDataAt(index).low;
            data.ep = exprEnv._ds.getDataAt(index).high;
            data.af = 0.02;
        } else {
            let high = exprEnv._ds.getDataAt(index).high;
            let low = exprEnv._ds.getDataAt(index).low;
            let prev = this._buf[index - 1];
            data.sar = prev.sar + prev.af * (prev.ep - prev.sar);
            if (prev.longPos) {
                data.longPos = true;
                if (high > prev.ep) {
                    data.ep = high;
                    data.af = Math.min(prev.af + this._step, this._max);
                } else {
                    data.ep = prev.ep;
                    data.af = prev.af;
                }
                if (data.sar > low) {
                    data.longPos = false;
                    let i = index - this._range + 1;
                    for (i = Math.max(i, first); i < index; i++) {
                        let h = exprEnv._ds.getDataAt(i).high;
                        if (high < h) high = h;
                    }
                    data.sar = high;
                    data.ep = low;
                    data.af = 0.02;
                }
            } else {
                data.longPos = false;
                if (low < prev.ep) {
                    data.ep = low;
                    data.af = Math.min(prev.af + this._step, this._max);
                } else {
                    data.ep = prev.ep;
                    data.af = prev.af;
                }
                if (data.sar < high) {
                    data.longPos = true;
                    let i = index - this._range + 1;
                    for (i = Math.max(i, first); i < index; i++) {
                        let l = exprEnv._ds.getDataAt(i).low;
                        if (low > l) low = l;
                    }
                    data.sar = low;
                    data.ep = high;
                    data.af = 0.02;
                }
            }
        }
        return data.sar;
    }

    reserve(rid, count) {
        if (this._rid < rid) {
            for (let c = count; c > 0; c--)
                this._buf.push({longPos: true, sar: NaN, ep: NaN, af: NaN});
        }
        super.reserve(rid, count);
    }

    clear() {
        super.clear();
        this._range = -1;
    }

}
