/**
 * Created by ZouLe on 2017/5/14.
 */
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

$(document).ready(function () {
    $.ajax({
        url: "/get-ozone-history-data",
        dataType: "json",
        success: ozonePlot
    })
});