google.charts.load('current', {'packages':['corechart', 'controls']});

var config = {
    api:{
        enable: true,
        interval: 1000 * 1
    },
    candlestick:{
        symbol: 'BTCBUSD',
        duration: '1m',
        limit: 365,
        numViews: 5,
    },
    dataTable: {
        index : 0,
        value: null
    },
    sma: {
        enable: false,
        indexes: [],
        periods: [],
        values: []
    },
    ema: {
        enable: false,
        indexes: [],
        periods: [],
        values: []
    },
    bbands: {
        enable: false,
        indexes: [],
        n: 20,
        k: 2,
        up: [],
        mid: [],
        down: []
    },
    ichimoku: {
        enable: false,
        indexes: [],
        tenkan: [],
        kijun: [],
        senkouA : [],
        senkouB: [],
        chikou: []
    },
    volume: {
        enable: false,
        index: [],
        values: []
    },
    rsi: {
        enable: false,
        indexes: {'up': 0, 'value': 0, 'down': 0},
        period: 14,
        up: 70,
        values: [],
        down: 30
    },
    macd: {
        enable: false,
        indexes: [],
        periods: [],
        values: []
    },
};

function initConfigValues(){
    config.dataTable.index = 0;
    config.sma.indexes = [];
    config.sma.values = [];
    config.ema.indexes = [];
    config.ema.values = [];
    config.bbands.indexes = [];
    config.bbands.up = [];
    config.bbands.mid = [];
    config.bbands.down = [];
    config.ichimoku.indexes = [];
    config.ichimoku.tenkan = [];
    config.ichimoku.kijun = [];
    config.ichimoku.senkouA= [];
    config.ichimoku.senkouB= [];
    config.ichimoku.chikou = [];
    config.volume.index = [];
    config.rsi.indexes = [];
    config.macd.indexes = [];
    config.macd.periods = [];
    config.macd.values = [];
}

function drawChart(dataTable) {
    var chartDiv = document.getElementById('chart_div');
    var charts = [];
    var dashboard = new google.visualization.Dashboard(chartDiv);
    var mainChart = new google.visualization.ChartWrapper({
        chartType: 'ComboChart',
        containerId: 'chart_div',
        options: {
            hAxis: {'slantedText': false},
            legend: {'position': 'none'},
            candlestick: {
                fallingColor: { strokeWidth: 0, fill: '#a52714' },
                risingColor: { strokeWidth: 0, fill: '#0f9d58' }
            },
            seriesType: "candlesticks",
            series: {}
        },
        view: {
            columns: [
                {
                    calc: function(d, rowIndex) {
                        return d.getFormattedValue(rowIndex, 0);
                    },
                    type: 'string'

                }, 1, 2, 3, 4
            ]

        }

    });
    charts.push(mainChart);

    var options = mainChart.getOptions();
    var view = mainChart.getView();

    if (config.sma.enable == true) {
        for (i = 0; i < config.sma.indexes.length; i++) {
            options.series[config.sma.indexes[i]] = {type: 'line'};
            view.columns.push(config.candlestick.numViews + config.sma.indexes[i]);
        }
    }

    if (config.ema.enable == true) {
        for (i = 0; i < config.ema.indexes.length; i++) {
            options.series[config.ema.indexes[i]] = {type: 'line'};
            view.columns.push(config.candlestick.numViews + config.ema.indexes[i]);
        }
    }

    if (config.bbands.enable == true) {
        for (i = 0; i < config.bbands.indexes.length; i++) {
            options.series[config.bbands.indexes[i]] = {
                type: 'line',
                color: 'blue',
                lineWidth: 1
            };
            view.columns.push(config.candlestick.numViews + config.bbands.indexes[i])
        }
    }

    if (config.ichimoku.enable == true) {
        for (i = 0; i < config.ichimoku.indexes.length; i++) {
            options.series[config.ichimoku.indexes[i]] = {
                type: 'line',
                lineWidth: 1
            };
            view.columns.push(config.candlestick.numViews + config.ichimoku.indexes[i]);
        }
    }

    if (config.volume.enable == true) {
        if ($('#volume_div').length == 0) {
            $('#technical_div').append(
                    "<div id='volume_div' class='bottom_chart'>" +
                    "<span class='technical_title'>Volume</span>" +
                    "<div id='volume_chart'></div>" +
                    "</div>")
        }
        var volumeChart = new google.visualization.ChartWrapper({
            'chartType': 'ColumnChart',
            'containerId': 'volume_chart',
            'options': {
                'hAxis': {'slantedText': false},
                'legend': {'position': 'none'},
                'series': {}
            },
            'view': {
                'columns': [ { 'type': 'string' }, 5]
            }
        });
        charts.push(volumeChart)
    }

    if (config.rsi.enable == true) {
        if ($('#rsi_div').length == 0) {
            $('#technical_div').append(
                    "<div id='rsi_div' class='bottom_chart'>" +
                    "<span class='technical_title'>RSI</span>" +
                    "<div id='rsi_chart'></div>" +
                    "</div>")
        }
        var up = config.candlestick.numViews + config.rsi.indexes['up'];
        var value = config.candlestick.numViews + config.rsi.indexes['value'];
        var down = config.candlestick.numViews + config.rsi.indexes['down'];
        var rsiChart = new google.visualization.ChartWrapper({
            'chartType': 'LineChart',
            'containerId': 'rsi_chart',
            'options': {
                'hAxis': {'slantedText': false},
                'legend': {'position': 'none'},
                'series': {
                    0: {color: 'black', lineWidth: 1},
                    1: {color: '#e2431e'},
                    2: {color: 'black', lineWidth: 1}
                }
            },
            'view': {
                'columns': [ { 'type': 'string' }, up, value, down]
            }
        });
        charts.push(rsiChart)
    }

    if (config.macd.enable == true) {
        if (config.macd.indexes.length == 0) { return }
        if ($('#macd_div').length == 0) {
            $('#technical_div').append(
                    "<div id='macd_div'>" +
                    "<span class='technical_title'>MACD</span>" +
                    "<div id='macd_chart'></div>" +
                    "</div>")
        }
        var macdColumns = [{'type': 'string'}];

        macdColumns.push(config.candlestick.numViews + config.macd.indexes[2]);
        macdColumns.push(config.candlestick.numViews + config.macd.indexes[0]);
        macdColumns.push(config.candlestick.numViews + config.macd.indexes[1]);
        var macdChart = new google.visualization.ChartWrapper({
            'chartType': 'ComboChart',
            'containerId': 'macd_chart',
            'options': {
                legend: {'position': 'none'},
                seriesType: "bars",
                series: {
                    1: {type: 'line', lineWidth: 1 },
                    2: {type: 'line', lineWidth: 1}
                }
            },
            'view': {
                'columns': macdColumns
            }
        });
        charts.push(macdChart)
    }

    var controlWrapper = new google.visualization.ControlWrapper({
        'controlType': 'ChartRangeFilter',
        'containerId': 'filter_div',
        'options': {
            'filterColumnIndex': 0,
            'ui': {
                'chartType': 'LineChart',
                'chartView': {
                    'columns': [0, 4]
                }
            }
        }
    });

    dashboard.bind(controlWrapper, charts);
    dashboard.draw(dataTable);

}

function send () {
    if (config.api.enable == false){
        return
    }
    var params = {
        symbol: config.candlestick.symbol,
        limit: config.candlestick.limit,
        duration: config.candlestick.duration,
    };

    if (config.sma.enable == true) {
        params["sma"] = true;
        params["smaPeriod1"] = config.sma.periods[0];
        params["smaPeriod2"] = config.sma.periods[1];
        params["smaPeriod3"] = config.sma.periods[2];
    }

    if (config.ema.enable == true) {
        params["ema"] = true;
        params["emaPeriod1"] = config.ema.periods[0];
        params["emaPeriod2"] = config.ema.periods[1];
        params["emaPeriod3"] = config.ema.periods[2];
    }

    if (config.bbands.enable == true) {
        params["bbands"] = true;
        params["bbandsN"] = config.bbands.n;
        params["bbandsK"] = config.bbands.k;
    }

    if (config.ichimoku.enable == true) {
        params["ichimoku"] = true;
    }

    if (config.rsi.enable == true) {
        params["rsi"] = true;
        params["rsiPeriod"] = config.rsi.period;
    }

    if (config.macd.enable == true) {
        params["macd"] = true;
        params["macdPeriod1"] = config.macd.periods[0];
        params["macdPeriod2"] = config.macd.periods[1];
        params["macdPeriod3"] = config.macd.periods[2];
    }

    $.get("/api/candle/", params).done(function (data) {
        initConfigValues();
        var dataTable = new google.visualization.DataTable();
        dataTable.addColumn('date', 'Date');
        dataTable.addColumn('number', 'Low');
        dataTable.addColumn('number', 'Open');
        dataTable.addColumn('number', 'Close');
        dataTable.addColumn('number', 'High');
        dataTable.addColumn('number', 'Volume');

        if (data["smas"] != undefined) {
            for (i = 0; i < data['smas'].length; i++){
                var smaData = data['smas'][i];
                if (smaData.length == 0){ continue; }
                config.dataTable.index += 1;
                config.sma.indexes[i] = config.dataTable.index;
                dataTable.addColumn('number', 'SMA' + smaData["period"].toString());
                config.sma.values[i] = smaData["values"]
            }
        }

        if (data["emas"] != undefined) {
            for (i = 0; i < data['emas'].length; i++){
                var emaData = data['emas'][i];
                if (emaData.length == 0){ continue; }
                config.dataTable.index += 1;
                config.ema.indexes[i] = config.dataTable.index;
                dataTable.addColumn('number', 'EMA' + emaData["period"].toString());
                config.ema.values[i] = emaData["values"]
            }
        }

        if (data['bbands'] != undefined) {
            var n = data['bbands']['n'];
            var k = data['bbands']['k'];
            var up = data['bbands']['up'];
            var mid = data['bbands']['mid'];
            var down = data['bbands']['down'];
            config.dataTable.index += 1;
            config.bbands.indexes[0] = config.dataTable.index;
            config.dataTable.index += 1;
            config.bbands.indexes[1] = config.dataTable.index;
            config.dataTable.index += 1;
            config.bbands.indexes[2] = config.dataTable.index;
            dataTable.addColumn('number', 'BBands Up(' + n + ',' + k + ')');
            dataTable.addColumn('number', 'BBands Mid(' + n + ',' + k + ')');
            dataTable.addColumn('number', 'BBands Down(' + n + ',' + k + ')');
            config.bbands.up = up;
            config.bbands.mid = mid;
            config.bbands.down = down;
        }

        if (data['ichimoku'] != undefined) {
            var tenkan = data['ichimoku']['tenkan'];
            var kijun = data['ichimoku']['kijun'];
            var senkouA = data['ichimoku']['senkou_a'];
            var senkouB = data['ichimoku']['senkou_b'];
            var chikou = data['ichimoku']['chikou'];

            config.dataTable.index += 1;
            config.ichimoku.indexes[0] = config.dataTable.index;
            config.dataTable.index += 1;
            config.ichimoku.indexes[1] = config.dataTable.index;
            config.dataTable.index += 1;
            config.ichimoku.indexes[2] = config.dataTable.index;
            config.dataTable.index += 1;
            config.ichimoku.indexes[3] = config.dataTable.index;
            config.dataTable.index += 1;
            config.ichimoku.indexes[4] = config.dataTable.index;

            config.ichimoku.tenkan = tenkan;
            config.ichimoku.kijun = kijun;
            config.ichimoku.senkouA = senkouA;
            config.ichimoku.senkouB = senkouB;
            config.ichimoku.chikou = chikou;

            dataTable.addColumn('number', 'Tenkan');
            dataTable.addColumn('number', 'Kijun');
            dataTable.addColumn('number', 'SenkouA');
            dataTable.addColumn('number', 'SenkouB');
            dataTable.addColumn('number', 'Chikou');
        }

        if (data['rsi'] != undefined ){
            config.dataTable.index += 1;
            config.rsi.indexes['up'] = config.dataTable.index;
            config.dataTable.index += 1;
            config.rsi.indexes['value'] = config.dataTable.index;
            config.dataTable.index += 1;
            config.rsi.indexes['down'] = config.dataTable.index;
            config.rsi.period = data['rsi']['period'];
            config.rsi.values = data['rsi']['values'];
            dataTable.addColumn('number', 'RSI Thread');
            dataTable.addColumn('number', 'RSI(' + config.rsi.period + ')');
            dataTable.addColumn('number', 'RSI Thread');
        }

        if (data['macd'] != undefined) {
            var macdData = data['macd'];
            var fast_period = macdData["fast_period"].toString();
            var slow_period = macdData["slow_period"].toString();
            var signal_period = macdData["signal_period"].toString();
            var macd = macdData["macd"];
            var macd_signal = macdData["macd_signal"];
            var macd_hist = macdData["macd_hist"];

            config.dataTable.index += 1;
            config.macd.indexes[0] = config.dataTable.index;
            config.dataTable.index += 1;
            config.macd.indexes[1] = config.dataTable.index;
            config.dataTable.index += 1;
            config.macd.indexes[2] = config.dataTable.index;
            var speriods = '(' + fast_period + ',' + slow_period + ',' + signal_period +')';
            dataTable.addColumn('number', 'MD' + speriods);
            dataTable.addColumn('number', 'MS' + speriods);
            dataTable.addColumn('number', 'HT' + speriods);
            config.macd.values[0] = macd;
            config.macd.values[1] = macd_signal;
            config.macd.values[2] = macd_hist;
            config.macd.periods[0] = fast_period;
            config.macd.periods[1] = slow_period;
            config.macd.periods[2] = signal_period;
        }

        var googleChartData = [];
        var candles = data["candles"];

        for(var i=0; i < candles.length; i++){
            var candle = candles[i];
            var date = new Date(candle.time);
            var datas = [date, candle.low, candle.open, candle.close, candle.high, candle.volume];

            if (data["smas"] != undefined) {
                for (j = 0; j < config.sma.values.length; j++) {
                    if (config.sma.values[j][i] == 0) {
                        datas.push(null);
                    } else {
                        datas.push(config.sma.values[j][i]);
                    }
                }
            }

            if (data["emas"] != undefined) {
                for (j = 0; j < config.ema.values.length; j++) {
                    if (config.ema.values[j][i] == 0) {
                        datas.push(null);
                    } else {
                        datas.push(config.ema.values[j][i]);
                    }
                }
            }

            if (data["bbands"] != undefined) {
                if (config.bbands.up[i] == 0) {
                    datas.push(null);
                } else {
                    datas.push(config.bbands.up[i]);
                }
                if (config.bbands.mid[i] == 0) {
                    datas.push(null);
                } else {
                    datas.push(config.bbands.mid[i]);
                }
                if (config.bbands.down[i] == 0) {
                    datas.push(null);
                } else {
                    datas.push(config.bbands.down[i]);
                }
            }

            if (data["ichimoku"] != undefined) {
                if (config.ichimoku.tenkan[i] == 0) {
                    datas.push(null);
                } else {
                    datas.push(config.ichimoku.tenkan[i]);
                }
                if (config.ichimoku.kijun[i] == 0) {
                    datas.push(null);
                } else {
                    datas.push(config.ichimoku.kijun[i]);
                }
                if (config.ichimoku.senkouA[i] == 0) {
                    datas.push(null);
                } else {
                    datas.push(config.ichimoku.senkouA[i]);
                }
                if (config.ichimoku.senkouB[i] == 0) {
                    datas.push(null);
                } else {
                    datas.push(config.ichimoku.senkouB[i]);
                }
                if (config.ichimoku.chikou[i] == 0) {
                    datas.push(null);
                } else {
                    datas.push(config.ichimoku.chikou[i]);
                }
            }

            if (data["rsi"] != undefined){
                datas.push(config.rsi.up);
                if (config.rsi.values[i] == 0) {
                    datas.push(null);
                }else{
                    datas.push(config.rsi.values[i]);
                }
                datas.push(config.rsi.down);
            }

            if (data["macd"] != undefined) {
                for (j = 0; j < config.macd.values.length; j++) {
                    if (config.macd.values[j][i] == 0) {
                        datas.push(null);
                    } else {
                        datas.push(config.macd.values[j][i]);
                    }
                }
            }

            googleChartData.push(datas)
        }

        dataTable.addRows(googleChartData);
        drawChart(dataTable);
    })
}

function changeDuration(s){
    config.candlestick.duration = s;
    send();
}

setInterval(send, 1000 * 3);
window.onload = function () {
    send();

    $('#dashboard_div').mouseenter(function() {
        config.api.enable = false;
    }).mouseleave(function() {
        config.api.enable = true;
    });

    $('#inputSma').change(function() {
        if (this.checked === true) {
            config.sma.enable = true;
        } else {
            config.sma.enable = false;
        }
        send();
    });

    $("#inputSmaPeriod1").change(function() {
        config.sma.periods[0] = this.value;
        send();
    });
    $("#inputSmaPeriod2").change(function() {
        config.sma.periods[1] = this.value;
        send();
    });
    $("#inputSmaPeriod3").change(function() {
        config.sma.periods[2] = this.value;
        send();
    });

    $('#inputEma').change(function() {
        if (this.checked === true) {
            config.ema.enable = true;
        } else {
            config.ema.enable = false;
        }
        send();
    });
    $("#inputEmaPeriod1").change(function() {
        config.ema.periods[0] = this.value;
        send();
    });
    $("#inputEmaPeriod2").change(function() {
        config.ema.periods[1] = this.value;
        send();
    });
    $("#inputEmaPeriod3").change(function() {
        config.ema.periods[2] = this.value;
        send();
    });

    $('#inputBBands').change(function() {
        if (this.checked === true) {
            config.bbands.enable = true;
        } else {
            config.bbands.enable = false;
        }
        send();
    });
    $("#inputBBandsN").change(function() {
        config.bbands.n = this.value;
        send();
    });
    $("#inputBBandsK").change(function() {
        config.bbands.k = this.value;
        send();
    });

    $('#inputIchimoku').change(function() {
        if (this.checked === true) {
            config.ichimoku.enable = true;
        } else {
            config.ichimoku.enable = false;
        }
        send();
    });

    $('#inputVolume').change(function() {
        if (this.checked === true) {
            config.volume.enable = true;
            drawChart(config.dataTable.value);
        } else {
            config.volume.enable = false;
            $('#volume_div').remove();
        }
    });

    $('#inputRsi').change(function() {
        if (this.checked === true) {
            config.rsi.enable = true;
        } else {
            config.rsi.enable = false;
            $('#rsi_div').remove();
        }
        send();
    });
    $("#inputRsiPeriod").change(function() {
        config.rsi.period = this.value;
        send();
    });

    $('#inputMacd').change(function() {
        if (this.checked === true) {
            config.macd.enable = true;
        } else {
            $('#macd_div').remove();
            config.macd.enable = false;
        }
        send();
    });
    $("#inputMacdPeriod1").change(function() {
        config.macd.periods[0] = this.value;
        send();
    });
    $("#inputMacdPeriod2").change(function() {
        config.macd.periods[1] = this.value;
        send();
    });
    $("#inputMacdPeriod3").change(function() {
        config.macd.periods[2] = this.value;
        send();
    });

}