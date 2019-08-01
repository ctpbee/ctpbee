import {ChartManager} from './chart_manager'

export class ChartSettings {

    static checkVersion() {
        if (ChartSettings._data.ver < 2) {
            ChartSettings._data.ver = 2;
            let charts = ChartSettings._data.charts;
            charts.period_weight = {};
            charts.period_weight['line'] = 8;
            charts.period_weight['1min'] = 7;
            charts.period_weight['5min'] = 6;
            charts.period_weight['15min'] = 5;
            charts.period_weight['30min'] = 4;
            charts.period_weight['1hour'] = 3;
            charts.period_weight['1day'] = 2;
            charts.period_weight['1week'] = 1;
            charts.period_weight['3min'] = 0;
            charts.period_weight['2hour'] = 0;
            charts.period_weight['4hour'] = 0;
            charts.period_weight['6hour'] = 0;
            charts.period_weight['12hour'] = 0;
            charts.period_weight['3day'] = 0;
        }
        if (ChartSettings._data.ver < 3) {
            ChartSettings._data.ver = 3;
            let charts = ChartSettings._data.charts;
            charts.areaHeight = [];
        }
    }

    static get () {
        if (ChartSettings._data === undefined) {
            ChartSettings.init();
            ChartSettings.load();
            ChartSettings.checkVersion();
        }
        return ChartSettings._data;
    };

    static init() {
        let _indic_param = {};
        let _name = ['MA', 'EMA', 'VOLUME', 'MACD', 'KDJ', 'StochRSI', 'RSI', 'DMI', 'OBV', 'BOLL', 'DMA', 'TRIX', 'BRAR', 'VR', 'EMV', 'WR', 'ROC', 'MTM', 'PSY'];
        for (let i = 0; i < _name.length; i++) {
            let _value = ChartManager.instance.createIndicatorAndRange('', _name[i], true);
            if (_value === null) continue;
            _indic_param[_name[i]] = [];
            let param = _value.indic.getParameters();
            for (let j = 0; j < param.length; j++) {
                _indic_param[_name[i]].push(param[j]);
            }
        }
        let _chart_style = 'CandleStick';
        let _m_indic = 'MA';
        let _indic = ['VOLUME', 'MACD'];
        let _range = '15m';
        let _frame = {};
        _frame.chartStyle = _chart_style;
        _frame.mIndic = _m_indic;
        _frame.indics = _indic;
        _frame.indicsStatus = 'open';
        _frame.period = _range;
        ChartSettings._data = {
            ver: 1,
            charts: _frame,
            indics: _indic_param,
            theme: "Dark"
        };
        ChartSettings.checkVersion();
    }

    static load() {
        if (document.cookie.length <= 0)
            return;
        let start = document.cookie.indexOf("chartSettings=");
        if (start < 0)
            return;
        start += "chartSettings=".length;
        let end = document.cookie.indexOf(";", start);
        if (end < 0)
            end = document.cookie.length;
        let json = unescape(document.cookie.substring(start, end));
        ChartSettings._data = JSON.parse(json);
    }

    static save() {
        let exdate = new Date();
        exdate.setDate(exdate.getDate() + 2);
        document.cookie = "chartSettings=" + escape(JSON.stringify(ChartSettings._data)) +
            ";expires=" + exdate.toGMTString();
    }
}
