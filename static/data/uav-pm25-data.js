/**
 * Created by ZouLe on 2017/5/5.
 */
var myChart = null;
var xx = [];
var yy = [];
var option = null;

function plot(data) {
    xx = data['xx'];
    yy = data['yy'];

    // $("#debug").text(" " + ozoneXx + " " + ozoneYy);

    option = {
        title: {
            text: 'PM2.5——时间',
            left: 'left'
        },
        legend: {
            data: ['PM2.5']
        },
        xAxis: {
            data: xx
        },
        yAxis: {},
        tooltip: {
            trigger: 'axis'
        },
        series: [{
            name: 'PM2.5',
            type: 'line',
            data: yy,
            smooth: false
        }]
    };

    myChart = echarts.init(document.getElementById('uav-line-chart'));

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function update_data(data) {
    xx.push(data['x']);
    xx.shift();
    yy.push(data['y']);
    yy.shift();
}

function update_chart() {
    myChart.setOption({
        xAxis: {
            data: xx
        },
        series: [{
            name: 'PM2.5',
            type: 'line',
            data: yy
        }]
    })
}

$(document).ready(function () {
    $.ajax({
        url: "/get_pm25_data",
        dataType: "json",
        success: plot
    });
    setInterval(function () {
        $.ajax({
            url: "/update_pm25_data",
            dataType: "json",
            success: update_data
        })
    }, 1000);
    setInterval(update_chart, 1000);
});