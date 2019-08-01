import * as exprs from "./exprs";
import * as themes from "./themes";

export class Indicator {

    constructor() {
        this._exprEnv = new exprs.ExprEnv();
        this._rid = 0;
        this._params = [];
        this._assigns = [];
        this._outputs = [];
    }

    addParameter(expr) {
        this._params.push(expr);
    }

    addAssign(expr) {
        this._assigns.push(expr);
    }

    addOutput(expr) {
        this._outputs.push(expr);
    }

    getParameterCount() {
        return this._params.length;
    }

    getParameterAt(index) {
        return this._params[index];
    }

    getOutputCount() {
        return this._outputs.length;
    }

    getOutputAt(index) {
        return this._outputs[index];
    }

    clear() {
        this._exprEnv.setFirstIndex(-1);
        let i, cnt;
        cnt = this._assigns.length;
        for (i = 0; i < cnt; i++) {
            this._assigns[i].clear();
        }
        cnt = this._outputs.length;
        for (i = 0; i < cnt; i++) {
            this._outputs[i].clear();
        }
    }

    reserve(count) {
        this._rid++;
        let i, cnt;
        cnt = this._assigns.length;
        for (i = 0; i < cnt; i++) {
            this._assigns[i].reserve(this._rid, count);
        }
        cnt = this._outputs.length;
        for (i = 0; i < cnt; i++) {
            this._outputs[i].reserve(this._rid, count);
        }
    }

    execute(ds, index) {
        if (index < 0) {
            return;
        }
        this._exprEnv.setDataSource(ds);
        exprs.ExprEnv.set(this._exprEnv);
        try {
            let i, cnt;
            cnt = this._assigns.length;
            for (i = 0; i < cnt; i++) {
                this._assigns[i].assign(index);
            }
            cnt = this._outputs.length;
            for (i = 0; i < cnt; i++) {
                this._outputs[i].assign(index);
            }
            if (this._exprEnv.getFirstIndex() < 0) {
                this._exprEnv.setFirstIndex(index);
            }
        } catch (e) {
            if (this._exprEnv.getFirstIndex() >= 0) {
                alert(e);
                throw e;
            }
        }
    }

    getParameters() {
        let params = [];
        let i, cnt = this._params.length;
        for (i = 0; i < cnt; i++)
            params.push(this._params[i].getValue());
        return params;
    }

    setParameters(params) {
        if ((params instanceof Array) && params.length === this._params.length) {
            for (let i in this._params)
                this._params[i].setValue(params[i]);
        }
    }
}


export class HLCIndicator extends Indicator {

    constructor() {
        super();
        let M1 = new exprs.ParameterExpr("M1", 2, 1000, 60);
        this.addParameter(M1);
        this.addOutput(new exprs.OutputExpr("HIGH",
            new exprs.HighExpr(),
            exprs.OutputExpr.outputStyle.None
        ));
        this.addOutput(new exprs.OutputExpr("LOW",
            new exprs.LowExpr(),
            exprs.OutputExpr.outputStyle.None
        ));
        this.addOutput(new exprs.OutputExpr("CLOSE",
            new exprs.CloseExpr(),
            exprs.OutputExpr.outputStyle.Line,
            themes.Theme.Color.Indicator0
        ));
        this.addOutput(new exprs.RangeOutputExpr("MA",
            new exprs.MaExpr(new exprs.CloseExpr(), M1),
            exprs.OutputExpr.outputStyle.Line,
            themes.Theme.Color.Indicator1
        ));
    }

    getName() {
        return "CLOSE";
    }

}


export class MAIndicator extends Indicator {

    constructor() {
        super();
        let M1 = new exprs.ParameterExpr("M1", 2, 1000, 7);
        let M2 = new exprs.ParameterExpr("M2", 2, 1000, 30);
        let M3 = new exprs.ParameterExpr("M3", 2, 1000, 0);
        let M4 = new exprs.ParameterExpr("M4", 2, 1000, 0);
        let M5 = new exprs.ParameterExpr("M5", 2, 1000, 0);
        let M6 = new exprs.ParameterExpr("M6", 2, 1000, 0);
        this.addParameter(M1);
        this.addParameter(M2);
        this.addParameter(M3);
        this.addParameter(M4);
        this.addParameter(M5);
        this.addParameter(M6);
        this.addOutput(new exprs.RangeOutputExpr("MA",
            new exprs.MaExpr(new exprs.CloseExpr(), M1)
        ));
        this.addOutput(new exprs.RangeOutputExpr("MA",
            new exprs.MaExpr(new exprs.CloseExpr(), M2)
        ));
        this.addOutput(new exprs.RangeOutputExpr("MA",
            new exprs.MaExpr(new exprs.CloseExpr(), M3)
        ));
        this.addOutput(new exprs.RangeOutputExpr("MA",
            new exprs.MaExpr(new exprs.CloseExpr(), M4)
        ));
        this.addOutput(new exprs.RangeOutputExpr("MA",
            new exprs.MaExpr(new exprs.CloseExpr(), M5)
        ));
        this.addOutput(new exprs.RangeOutputExpr("MA",
            new exprs.MaExpr(new exprs.CloseExpr(), M6)
        ));
    }

    getName() {
        return "MA";
    }
}


export class EMAIndicator extends Indicator {

    constructor() {
        super();
        let M1 = new exprs.ParameterExpr("M1", 2, 1000, 7);
        let M2 = new exprs.ParameterExpr("M2", 2, 1000, 30);
        let M3 = new exprs.ParameterExpr("M3", 2, 1000, 0);
        let M4 = new exprs.ParameterExpr("M4", 2, 1000, 0);
        let M5 = new exprs.ParameterExpr("M5", 2, 1000, 0);
        let M6 = new exprs.ParameterExpr("M6", 2, 1000, 0);
        this.addParameter(M1);
        this.addParameter(M2);
        this.addParameter(M3);
        this.addParameter(M4);
        this.addParameter(M5);
        this.addParameter(M6);
        this.addOutput(new exprs.RangeOutputExpr("EMA",
            new exprs.EmaExpr(new exprs.CloseExpr(), M1)
        ));
        this.addOutput(new exprs.RangeOutputExpr("EMA",
            new exprs.EmaExpr(new exprs.CloseExpr(), M2)
        ));
        this.addOutput(new exprs.RangeOutputExpr("EMA",
            new exprs.EmaExpr(new exprs.CloseExpr(), M3)
        ));
        this.addOutput(new exprs.RangeOutputExpr("EMA",
            new exprs.EmaExpr(new exprs.CloseExpr(), M4)
        ));
        this.addOutput(new exprs.RangeOutputExpr("EMA",
            new exprs.EmaExpr(new exprs.CloseExpr(), M5)
        ));
        this.addOutput(new exprs.RangeOutputExpr("EMA",
            new exprs.EmaExpr(new exprs.CloseExpr(), M6)
        ));
    }

    getName() {
        return "EMA";
    }
}


export class VOLUMEIndicator extends Indicator {

    constructor() {
        super();

        let M1 = new exprs.ParameterExpr("M1", 2, 500, 5);
        let M2 = new exprs.ParameterExpr("M2", 2, 500, 10);
        this.addParameter(M1);
        this.addParameter(M2);
        let VOLUME = new exprs.OutputExpr("VOLUME",
            new exprs.VolumeExpr(),
            exprs.OutputExpr.outputStyle.VolumeStick,
            themes.Theme.Color.Text4
        );
        this.addOutput(VOLUME);
        this.addOutput(new exprs.RangeOutputExpr("MA",
            new exprs.MaExpr(VOLUME, M1),
            exprs.OutputExpr.outputStyle.Line,
            themes.Theme.Color.Indicator0
        ));
        this.addOutput(new exprs.RangeOutputExpr("MA",
            new exprs.MaExpr(VOLUME, M2),
            exprs.OutputExpr.outputStyle.Line,
            themes.Theme.Color.Indicator1
        ));
    }

    getName() {
        return "VOLUME";
    }
}


export class MACDIndicator extends Indicator {

    constructor() {
        super();
        let SHORT = new exprs.ParameterExpr("SHORT", 2, 200, 12);
        let LONG = new exprs.ParameterExpr("LONG", 2, 200, 26);
        let MID = new exprs.ParameterExpr("MID", 2, 200, 9);
        this.addParameter(SHORT);
        this.addParameter(LONG);
        this.addParameter(MID);
        let DIF = new exprs.OutputExpr("DIF",
            new exprs.SubExpr(
                new exprs.EmaExpr(new exprs.CloseExpr(), SHORT),
                new exprs.EmaExpr(new exprs.CloseExpr(), LONG)
            )
        );
        this.addOutput(DIF);
        let DEA = new exprs.OutputExpr("DEA",
            new exprs.EmaExpr(DIF, MID)
        );
        this.addOutput(DEA);
        let MACD = new exprs.OutputExpr("MACD",
            new exprs.MulExpr(
                new exprs.SubExpr(DIF, DEA),
                new exprs.ConstExpr(2)
            ),
            exprs.OutputExpr.outputStyle.MACDStick
        );
        this.addOutput(MACD);
    }

    getName() {
        return "MACD";
    }
}


export class DMIIndicator extends Indicator {

    constructor() {
        super();
        let N = new exprs.ParameterExpr("N", 2, 90, 14);
        let MM = new exprs.ParameterExpr("MM", 2, 60, 6);
        this.addParameter(N);
        this.addParameter(MM);
        let MTR = new exprs.AssignExpr("MTR",
            new exprs.ExpmemaExpr(
                new exprs.MaxExpr(
                    new exprs.MaxExpr(
                        new exprs.SubExpr(new exprs.HighExpr(), new exprs.LowExpr()),
                        new exprs.AbsExpr(
                            new exprs.SubExpr(
                                new exprs.HighExpr(),
                                new exprs.RefExpr(new exprs.CloseExpr(), new exprs.ConstExpr(1))
                            )
                        )
                    ),
                    new exprs.AbsExpr(
                        new exprs.SubExpr(
                            new exprs.RefExpr(new exprs.CloseExpr(), new exprs.ConstExpr(1)),
                            new exprs.LowExpr()
                        )
                    )
                ),
                N
            )
        );
        this.addAssign(MTR);
        let HD = new exprs.AssignExpr("HD",
            new exprs.SubExpr(
                new exprs.HighExpr(),
                new exprs.RefExpr(new exprs.HighExpr(), new exprs.ConstExpr(1))
            )
        );
        this.addAssign(HD);
        let LD = new exprs.AssignExpr("LD",
            new exprs.SubExpr(
                new exprs.RefExpr(new exprs.LowExpr(), new exprs.ConstExpr(1)),
                new exprs.LowExpr()
            )
        );
        this.addAssign(LD);
        let DMP = new exprs.AssignExpr("DMP",
            new exprs.ExpmemaExpr(
                new exprs.IfExpr(
                    new exprs.AndExpr(
                        new exprs.GtExpr(HD, new exprs.ConstExpr(0)),
                        new exprs.GtExpr(HD, LD)
                    ),
                    HD,
                    new exprs.ConstExpr(0)
                ),
                N
            )
        );
        this.addAssign(DMP);
        let DMM = new exprs.AssignExpr("DMM",
            new exprs.ExpmemaExpr(
                new exprs.IfExpr(
                    new exprs.AndExpr(
                        new exprs.GtExpr(LD, new exprs.ConstExpr(0)),
                        new exprs.GtExpr(LD, HD)
                    ),
                    LD,
                    new exprs.ConstExpr(0)
                ),
                N
            )
        );
        this.addAssign(DMM);
        let PDI = new exprs.OutputExpr("PDI",
            new exprs.MulExpr(
                new exprs.DivExpr(DMP, MTR),
                new exprs.ConstExpr(100)
            )
        );
        this.addOutput(PDI);
        let MDI = new exprs.OutputExpr("MDI",
            new exprs.MulExpr(
                new exprs.DivExpr(DMM, MTR),
                new exprs.ConstExpr(100)
            )
        );
        this.addOutput(MDI);
        let ADX = new exprs.OutputExpr("ADX",
            new exprs.ExpmemaExpr(
                new exprs.MulExpr(
                    new exprs.DivExpr(
                        new exprs.AbsExpr(
                            new exprs.SubExpr(MDI, PDI)
                        ),
                        new exprs.AddExpr(MDI, PDI)
                    ),
                    new exprs.ConstExpr(100)
                ),
                MM
            )
        );
        this.addOutput(ADX);
        let ADXR = new exprs.OutputExpr("ADXR",
            new exprs.ExpmemaExpr(ADX, MM)
        );
        this.addOutput(ADXR);
    }

    getName() {
        return "DMI";
    }

}


export class DMAIndicator extends Indicator {

    constructor() {
        super();
        let N1 = new exprs.ParameterExpr("N1", 2, 60, 10);
        let N2 = new exprs.ParameterExpr("N2", 2, 250, 50);
        let M = new exprs.ParameterExpr("M", 2, 100, 10);
        this.addParameter(N1);
        this.addParameter(N2);
        this.addParameter(M);
        let DIF = new exprs.OutputExpr("DIF",
            new exprs.SubExpr(
                new exprs.MaExpr(new exprs.CloseExpr(), N1),
                new exprs.MaExpr(new exprs.CloseExpr(), N2)
            )
        );
        this.addOutput(DIF);
        let DIFMA = new exprs.OutputExpr("DIFMA",
            new exprs.MaExpr(DIF, M)
        );
        this.addOutput(DIFMA);
    }

    getName() {
        return "DMA";
    }

}


export class TRIXIndicator extends Indicator {

    constructor() {
        super();
        let N = new exprs.ParameterExpr("N", 2, 100, 12);
        let M = new exprs.ParameterExpr("M", 2, 100, 9);
        this.addParameter(N);
        this.addParameter(M);
        let MTR = new exprs.AssignExpr("MTR",
            new exprs.EmaExpr(
                new exprs.EmaExpr(
                    new exprs.EmaExpr(new exprs.CloseExpr(), N), N), N)
        );
        this.addAssign(MTR);
        let TRIX = new exprs.OutputExpr("TRIX",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SubExpr(
                        MTR,
                        new exprs.RefExpr(
                            MTR,
                            new exprs.ConstExpr(1)
                        )
                    ),
                    new exprs.RefExpr(
                        MTR,
                        new exprs.ConstExpr(1)
                    )
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addOutput(TRIX);
        let MATRIX = new exprs.OutputExpr("MATRIX",
            new exprs.MaExpr(TRIX, M)
        );
        this.addOutput(MATRIX);
    }

    getName() {
        return "TRIX";
    }

}


export class BRARIndicator extends Indicator {

    constructor() {
        super();
        let N = new exprs.ParameterExpr("N", 2, 120, 26);
        this.addParameter(N);
        let REF_CLOSE_1 = new exprs.AssignExpr("REF_CLOSE_1",
            new exprs.RefExpr(new exprs.CloseExpr(), new exprs.ConstExpr(1))
        );
        this.addAssign(REF_CLOSE_1);
        let BR = new exprs.OutputExpr("BR",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SumExpr(
                        new exprs.MaxExpr(
                            new exprs.ConstExpr(0),
                            new exprs.SubExpr(
                                new exprs.HighExpr(),
                                REF_CLOSE_1
                            )
                        ),
                        N
                    ),
                    new exprs.SumExpr(
                        new exprs.MaxExpr(
                            new exprs.ConstExpr(0),
                            new exprs.SubExpr(
                                REF_CLOSE_1,
                                new exprs.LowExpr()
                            )
                        ),
                        N
                    )
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addOutput(BR);
        let AR = new exprs.OutputExpr("AR",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SumExpr(
                        new exprs.SubExpr(
                            new exprs.HighExpr(),
                            new exprs.OpenExpr()
                        ),
                        N
                    ),
                    new exprs.SumExpr(
                        new exprs.SubExpr(
                            new exprs.OpenExpr(),
                            new exprs.LowExpr()
                        ),
                        N
                    )
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addOutput(AR);
    }

    getName() {
        return "BRAR";
    }

}


export class VRIndicator extends Indicator {

    constructor() {
        super();
        let N = new exprs.ParameterExpr("N", 2, 100, 26);
        let M = new exprs.ParameterExpr("M", 2, 100, 6);
        this.addParameter(N);
        this.addParameter(M);
        let REF_CLOSE_1 = new exprs.AssignExpr("REF_CLOSE_1",
            new exprs.RefExpr(new exprs.CloseExpr(), new exprs.ConstExpr(1))
        );
        this.addAssign(REF_CLOSE_1);
        let TH = new exprs.AssignExpr("TH",
            new exprs.SumExpr(
                new exprs.IfExpr(
                    new exprs.GtExpr(
                        new exprs.CloseExpr(),
                        REF_CLOSE_1
                    ),
                    new exprs.VolumeExpr(),
                    new exprs.ConstExpr(0)
                ),
                N
            )
        );
        this.addAssign(TH);
        let TL = new exprs.AssignExpr("TL",
            new exprs.SumExpr(
                new exprs.IfExpr(
                    new exprs.LtExpr(
                        new exprs.CloseExpr(),
                        REF_CLOSE_1
                    ),
                    new exprs.VolumeExpr(),
                    new exprs.ConstExpr(0)
                ),
                N
            )
        );
        this.addAssign(TL);
        let TQ = new exprs.AssignExpr("TQ",
            new exprs.SumExpr(
                new exprs.IfExpr(
                    new exprs.EqExpr(
                        new exprs.CloseExpr(),
                        REF_CLOSE_1
                    ),
                    new exprs.VolumeExpr(),
                    new exprs.ConstExpr(0)
                ),
                N
            )
        );
        this.addAssign(TQ);
        let VR = new exprs.OutputExpr("VR",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.AddExpr(
                        new exprs.MulExpr(
                            TH,
                            new exprs.ConstExpr(2)
                        ),
                        TQ
                    ),
                    new exprs.AddExpr(
                        new exprs.MulExpr(
                            TL,
                            new exprs.ConstExpr(2)
                        ),
                        TQ
                    )
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addOutput(VR);
        let MAVR = new exprs.OutputExpr("MAVR",
            new exprs.MaExpr(VR, M)
        );
        this.addOutput(MAVR);
    }

    getName() {
        return "VR";
    }

}


export class OBVIndicator extends Indicator {

    constructor() {
        super();
        let M = new exprs.ParameterExpr("M", 2, 100, 30);
        this.addParameter(M);
        let REF_CLOSE_1 = new exprs.AssignExpr("REF_CLOSE_1",
            new exprs.RefExpr(new exprs.CloseExpr(), new exprs.ConstExpr(1))
        );
        this.addAssign(REF_CLOSE_1);
        let VA = new exprs.AssignExpr("VA",
            new exprs.IfExpr(
                new exprs.GtExpr(new exprs.CloseExpr(), REF_CLOSE_1),
                new exprs.VolumeExpr(),
                new exprs.NegExpr(new exprs.VolumeExpr())
            )
        );
        this.addAssign(VA);
        let OBV = new exprs.OutputExpr("OBV",
            new exprs.SumExpr(
                new exprs.IfExpr(
                    new exprs.EqExpr(new exprs.CloseExpr(), REF_CLOSE_1),
                    new exprs.ConstExpr(0),
                    VA
                ),
                new exprs.ConstExpr(0)
            )
        );
        this.addOutput(OBV);
        let MAOBV = new exprs.OutputExpr("MAOBV",
            new exprs.MaExpr(OBV, M)
        );
        this.addOutput(MAOBV);
    }

    getName() {
        return "OBV";
    }

}


export class EMVIndicator extends Indicator {

    constructor() {
        super();
        let N = new exprs.ParameterExpr("N", 2, 90, 14);
        let M = new exprs.ParameterExpr("M", 2, 60, 9);
        this.addParameter(N);
        this.addParameter(M);
        let VOLUME = new exprs.AssignExpr("VOLUME",
            new exprs.DivExpr(
                new exprs.MaExpr(new exprs.VolumeExpr(), N),
                new exprs.VolumeExpr()
            )
        );
        this.addAssign(VOLUME);
        let MID = new exprs.AssignExpr("MID",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SubExpr(
                        new exprs.AddExpr(new exprs.HighExpr(), new exprs.LowExpr()),
                        new exprs.RefExpr(
                            new exprs.AddExpr(new exprs.HighExpr(), new exprs.LowExpr()),
                            new exprs.ConstExpr(1)
                        )
                    ),
                    new exprs.AddExpr(new exprs.HighExpr(), new exprs.LowExpr())
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addAssign(MID);
        let EMV = new exprs.OutputExpr("EMV",
            new exprs.MaExpr(
                new exprs.DivExpr(
                    new exprs.MulExpr(
                        MID,
                        new exprs.MulExpr(
                            VOLUME,
                            new exprs.SubExpr(new exprs.HighExpr(), new exprs.LowExpr())
                        )
                    ),
                    new exprs.MaExpr(
                        new exprs.SubExpr(new exprs.HighExpr(), new exprs.LowExpr()),
                        N
                    )
                ),
                N
            )
        );
        this.addOutput(EMV);
        let MAEMV = new exprs.OutputExpr("MAEMV",
            new exprs.MaExpr(EMV, M)
        );
        this.addOutput(MAEMV);
    }

    getName() {
        return "EMV";
    }

}


export class RSIIndicator extends Indicator {

    constructor() {
        super();
        let N1 = new exprs.ParameterExpr("N1", 2, 120, 6);
        let N2 = new exprs.ParameterExpr("N2", 2, 250, 12);
        let N3 = new exprs.ParameterExpr("N3", 2, 500, 24);
        this.addParameter(N1);
        this.addParameter(N2);
        this.addParameter(N3);
        let LC = new exprs.AssignExpr("LC",
            new exprs.RefExpr(new exprs.CloseExpr(), new exprs.ConstExpr(1))
        );
        this.addAssign(LC);
        let CLOSE_LC = new exprs.AssignExpr("CLOSE_LC",
            new exprs.SubExpr(new exprs.CloseExpr(), LC)
        );
        this.addAssign(CLOSE_LC);
        this.addOutput(new exprs.OutputExpr("RSI1",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SmaExpr(new exprs.MaxExpr(CLOSE_LC, new exprs.ConstExpr(0)), N1, new exprs.ConstExpr(1)),
                    new exprs.SmaExpr(new exprs.AbsExpr(CLOSE_LC), N1, new exprs.ConstExpr(1))
                ),
                new exprs.ConstExpr(100)
            )
        ));
        this.addOutput(new exprs.OutputExpr("RSI2",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SmaExpr(new exprs.MaxExpr(CLOSE_LC, new exprs.ConstExpr(0)), N2, new exprs.ConstExpr(1)),
                    new exprs.SmaExpr(new exprs.AbsExpr(CLOSE_LC), N2, new exprs.ConstExpr(1))
                ),
                new exprs.ConstExpr(100)
            )
        ));
        this.addOutput(new exprs.OutputExpr("RSI3",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SmaExpr(new exprs.MaxExpr(CLOSE_LC, new exprs.ConstExpr(0)), N3, new exprs.ConstExpr(1)),
                    new exprs.SmaExpr(new exprs.AbsExpr(CLOSE_LC), N3, new exprs.ConstExpr(1))
                ),
                new exprs.ConstExpr(100)
            )
        ));
    }

    getName() {
        return "RSI";
    }

}


export class WRIndicator extends Indicator {

    constructor() {
        super();
        let N = new exprs.ParameterExpr("N", 2, 100, 10);
        let N1 = new exprs.ParameterExpr("N1", 2, 100, 6);
        this.addParameter(N);
        this.addParameter(N1);
        let HHV = new exprs.AssignExpr("HHV",
            new exprs.HhvExpr(new exprs.HighExpr(), N)
        );
        this.addAssign(HHV);
        let HHV1 = new exprs.AssignExpr("HHV1",
            new exprs.HhvExpr(new exprs.HighExpr(), N1)
        );
        this.addAssign(HHV1);
        let LLV = new exprs.AssignExpr("LLV",
            new exprs.LlvExpr(new exprs.LowExpr(), N)
        );
        this.addAssign(LLV);
        let LLV1 = new exprs.AssignExpr("LLV1",
            new exprs.LlvExpr(new exprs.LowExpr(), N1)
        );
        this.addAssign(LLV1);
        let WR1 = new exprs.OutputExpr("WR1",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SubExpr(
                        HHV,
                        new exprs.CloseExpr()
                    ),
                    new exprs.SubExpr(
                        HHV,
                        LLV
                    )
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addOutput(WR1);
        let WR2 = new exprs.OutputExpr("WR2",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SubExpr(
                        HHV1,
                        new exprs.CloseExpr()
                    ),
                    new exprs.SubExpr(
                        HHV1,
                        LLV1
                    )
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addOutput(WR2);
    }

    getName() {
        return "WR";
    }

}


export class SARIndicator extends Indicator {

    constructor() {
        super();
        let N = new exprs.ConstExpr(4);
        let MIN = new exprs.ConstExpr(2);
        let STEP = new exprs.ConstExpr(2);
        let MAX = new exprs.ConstExpr(20);
        this.addOutput(new exprs.OutputExpr("SAR",
            new exprs.SarExpr(N, MIN, STEP, MAX),
            exprs.OutputExpr.outputStyle.SARPoint
        ));
    }

    getName() {
        return "SAR";
    }

}


export class KDJIndicator extends Indicator {

    constructor() {
        super();
        let N = new exprs.ParameterExpr("N", 2, 90, 9);
        let M1 = new exprs.ParameterExpr("M1", 2, 30, 3);
        let M2 = new exprs.ParameterExpr("M2", 2, 30, 3);
        this.addParameter(N);
        this.addParameter(M1);
        this.addParameter(M2);
        let HHV = new exprs.AssignExpr("HHV",
            new exprs.HhvExpr(new exprs.HighExpr(), N)
        );
        this.addAssign(HHV);
        let LLV = new exprs.AssignExpr("LLV",
            new exprs.LlvExpr(new exprs.LowExpr(), N)
        );
        this.addAssign(LLV);
        let RSV = new exprs.AssignExpr("RSV",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SubExpr(
                        new exprs.CloseExpr(),
                        LLV
                    ),
                    new exprs.SubExpr(
                        HHV,
                        LLV
                    )
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addAssign(RSV);
        let K = new exprs.OutputExpr("K",
            new exprs.SmaExpr(RSV, M1, new exprs.ConstExpr(1))
        );
        this.addOutput(K);
        let D = new exprs.OutputExpr("D",
            new exprs.SmaExpr(K, M2, new exprs.ConstExpr(1))
        );
        this.addOutput(D);
        let J = new exprs.OutputExpr("J",
            new exprs.SubExpr(
                new exprs.MulExpr(
                    K,
                    new exprs.ConstExpr(3)
                ),
                new exprs.MulExpr(
                    D,
                    new exprs.ConstExpr(2)
                )
            )
        );
        this.addOutput(J);
    }

    getName() {
        return "KDJ";
    }

}


export class ROCIndicator extends Indicator {

    constructor() {
        super();

        let N = new exprs.ParameterExpr("N", 2, 120, 12);
        let M = new exprs.ParameterExpr("M", 2, 60, 6);
        this.addParameter(N);
        this.addParameter(M);
        let REF_CLOSE_N = new exprs.AssignExpr("REF_CLOSE_N",
            new exprs.RefExpr(new exprs.CloseExpr(), N)
        );
        this.addAssign(REF_CLOSE_N);
        let ROC = new exprs.OutputExpr("ROC",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SubExpr(
                        new exprs.CloseExpr(),
                        REF_CLOSE_N
                    ),
                    REF_CLOSE_N
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addOutput(ROC);
        let MAROC = new exprs.OutputExpr("MAROC",
            new exprs.MaExpr(ROC, M)
        );
        this.addOutput(MAROC);
    }

    getName() {
        return "ROC";
    }

}


export class MTMIndicator extends Indicator {

    constructor() {
        super();
        let N = new exprs.ParameterExpr("N", 2, 120, 12);
        let M = new exprs.ParameterExpr("M", 2, 60, 6);
        this.addParameter(N);
        this.addParameter(M);
        let MTM = new exprs.OutputExpr("MTM",
            new exprs.SubExpr(
                new exprs.CloseExpr(),
                new exprs.RefExpr(new exprs.CloseExpr(), N)
            )
        );
        this.addOutput(MTM);
        let MTMMA = new exprs.OutputExpr("MTMMA",
            new exprs.MaExpr(MTM, M)
        );
        this.addOutput(MTMMA);
    }

    getName() {
        return "MTM";
    }

}


export class BOLLIndicator extends Indicator {

    constructor() {
        super();

        let N = new exprs.ParameterExpr("N", 2, 120, 20);
        this.addParameter(N);
        let STD_CLOSE_N = new exprs.AssignExpr("STD_CLOSE_N",
            new exprs.StdExpr(new exprs.CloseExpr(), N)
        );
        this.addAssign(STD_CLOSE_N);
        let BOLL = new exprs.OutputExpr("BOLL",
            new exprs.MaExpr(new exprs.CloseExpr(), N)
        );
        this.addOutput(BOLL);
        let UB = new exprs.OutputExpr("UB",
            new exprs.AddExpr(
                BOLL,
                new exprs.MulExpr(
                    new exprs.ConstExpr(2),
                    STD_CLOSE_N
                )
            )
        );
        this.addOutput(UB);
        let LB = new exprs.OutputExpr("LB",
            new exprs.SubExpr(
                BOLL,
                new exprs.MulExpr(
                    new exprs.ConstExpr(2),
                    STD_CLOSE_N
                )
            )
        );
        this.addOutput(LB);
    }

    getName() {
        return "BOLL";
    }

}


export class PSYIndicator extends Indicator {

    constructor() {
        super();

        let N = new exprs.ParameterExpr("N", 2, 100, 12);
        let M = new exprs.ParameterExpr("M", 2, 100, 6);
        this.addParameter(N);
        this.addParameter(M);
        let PSY = new exprs.OutputExpr("PSY",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.CountExpr(
                        new exprs.GtExpr(
                            new exprs.CloseExpr(),
                            new exprs.RefExpr(new exprs.CloseExpr(), new exprs.ConstExpr(1))
                        ),
                        N
                    ),
                    N
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addOutput(PSY);
        let PSYMA = new exprs.OutputExpr("PSYMA",
            new exprs.MaExpr(PSY, M)
        );
        this.addOutput(PSYMA);
    }

    getName() {
        return "PSY";
    }

}


export class STOCHRSIIndicator extends Indicator {

    constructor() {
        super();

        let N = new exprs.ParameterExpr("N", 3, 100, 14);
        let M = new exprs.ParameterExpr("M", 3, 100, 14);
        let P1 = new exprs.ParameterExpr("P1", 2, 50, 3);
        let P2 = new exprs.ParameterExpr("P2", 2, 50, 3);
        this.addParameter(N);
        this.addParameter(M);
        this.addParameter(P1);
        this.addParameter(P2);
        let LC = new exprs.AssignExpr("LC",
            new exprs.RefExpr(new exprs.CloseExpr(), new exprs.ConstExpr(1))
        );
        this.addAssign(LC);
        let CLOSE_LC = new exprs.AssignExpr("CLOSE_LC",
            new exprs.SubExpr(new exprs.CloseExpr(), LC)
        );
        this.addAssign(CLOSE_LC);
        let RSI = new exprs.AssignExpr("RSI",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.SmaExpr(new exprs.MaxExpr(CLOSE_LC, new exprs.ConstExpr(0)), N, new exprs.ConstExpr(1)),
                    new exprs.SmaExpr(new exprs.AbsExpr(CLOSE_LC), N, new exprs.ConstExpr(1))
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addAssign(RSI);
        let STOCHRSI = new exprs.OutputExpr("STOCHRSI",
            new exprs.MulExpr(
                new exprs.DivExpr(
                    new exprs.MaExpr(
                        new exprs.SubExpr(
                            RSI,
                            new exprs.LlvExpr(RSI, M)
                        ),
                        P1
                    ),
                    new exprs.MaExpr(
                        new exprs.SubExpr(
                            new exprs.HhvExpr(RSI, M),
                            new exprs.LlvExpr(RSI, M)
                        ),
                        P1
                    )
                ),
                new exprs.ConstExpr(100)
            )
        );
        this.addOutput(STOCHRSI);
        this.addOutput(new exprs.RangeOutputExpr("MA",
            new exprs.MaExpr(STOCHRSI, P2)
        ));
    }

    getName = function () {
        return "StochRSI";
    }

}

