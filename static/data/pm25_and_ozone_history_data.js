/**
 * Created by ZouLe on 2017/5/14.
 */
$(document).ready(function () {
    var pm25HistoryChart = null;
    var pm25Xx = [];
    var pm25Yy = [];
    var pm25Option = null;

    function plot(data) {
        pm25Xx = data['xx'];
        pm25Yy = data['yy'];

        // $("#debug").text(" " + ozoneXx + " " + ozoneYy);

        pm25Option = {
            title: {
                text: 'PM2.5 近日浓度变化',
                left: 'left',
            },
            legend: {
                data: ['PM2.5']
            },
            xAxis: {
                data: pm25Xx,
                type: "category",
                boundaryGap: ['5%', '5%']
            },
            yAxis: {},
            tooltip: {
                trigger: 'axis'
            },
            series: [{
                name: 'PM2.5',
                type: 'line',
                data: pm25Yy,
                smooth: true
            }]
        };

        pm25HistoryChart = echarts.init(document.getElementById('pm25-history-chart'));

        // 使用刚指定的配置项和数据显示图表。
        pm25HistoryChart.setOption(pm25Option);
    }

    $.ajax({
        url: "/get-pm25-history-data",
        dataType: "json",
        success: plot
    })

    var ozoneHistoryChart = null;
    var ozoneXx = [];
    var ozoneYy = [];
    var option = null;

    function ozonePlot(data) {
        ozoneXx = data['xx'];
        ozoneYy = data['yy'];

        // $("#debug").text(" " + ozoneXx + " " + ozoneYy);

        option = {
            title: {
                text: '臭氧近日浓度变化',
                left: 'left'
            },
            legend: {
                data: ['臭氧']
            },
            xAxis: {
                data: ozoneXx,
                type: "category",
                boundaryGap: ['5%', '5%']
            },
            yAxis: {},
            tooltip: {
                trigger: 'axis'
            },
            series: [{
                name: '臭氧',
                type: 'line',
                data: ozoneYy,
                smooth: true
            }]
        };

        ozoneHistoryChart = echarts.init(document.getElementById('ozone-history-chart'));

        // 使用刚指定的配置项和数据显示图表。
        ozoneHistoryChart.setOption(option);
    }

    $.ajax({
        url: "/get-ozone-history-data",
        dataType: "json",
        success: ozonePlot
    })
});