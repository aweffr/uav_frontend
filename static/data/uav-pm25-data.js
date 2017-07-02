/**
 * Created by ZouLe on 2017/5/5.
 */
var myChart = null;
var heightChart = null;
var xx = [];
var yy = [];
var xx_height = [];
var yy_height = [];
var option = null;
var option_height = null;

function plot(data) {
    xx = data['xx'];
    yy = data['yy'];
    xx_height = data["xx_height"];
    yy_height = data["yy_height"];
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

    option_height = {
        title: {
            text: '高度--PM2.5',
            left: 'left'
        },
        legend: {
            data: ['PM2.5']
        },
        xAxis: {
            data: yy_height
        },
        yAxis: {},
        tooltip: {
            trigger: 'axis'
        },
        series: [{
            name: 'PM2.5',
            type: 'line',
            data: xx_height,
            smooth: false
        }]
    };

    heightChart = echarts.init(document.getElementById("uav-height-chart"));
    heightChart.setOption(option_height);
}

function update_data(data) {
    xx.push(data['x']);
    xx.shift();
    yy.push(data['y']);
    yy.shift();

    xx_height = data['xx_height'];
    yy_height = data['yy_height'];
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
    });
    heightChart.setOption({
        xAxis: {
            data: yy_height
        },
        series: [{
            name: 'PM2.5',
            type: 'line',
            data: xx_height
        }]
    });
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