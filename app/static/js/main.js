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
};

function initConfigValues(){
    config.dataTable.index = 0;
    config.sma.indexes = [];
    config.sma.values = [];
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
}