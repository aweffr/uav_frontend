from flask import Flask, render_template
from random import shuffle, randint
from json import dumps
from random import random
import time
import datetime

app = Flask(__name__)

xx = [(datetime.datetime.now() + datetime.timedelta(seconds=(x-60))).strftime("%H:%M:%S") for x in range(60)]
yy = [0, ]
for i in range(59):
    yy.append(yy[-1] + 0.5 * randint(0, 0))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/testindex')
def test_index():
    return render_template("/pages/myindex.html")


@app.route('/testchart')
def test_chart():
    return render_template("/pages/ozonelive.html")


@app.route('/pages/<page_name>')
def pages(page_name):
    return render_template('/pages/%s' % page_name)


@app.route('/getdata')
def getdata():
    global xx, yy
    d = {'xx': xx,
         'yy': yy}
    return dumps(d)


@app.route('/updatedata')
def update_data():
    global xx, yy
    xx.append(time.strftime("%H:%M:%S"))
    yy.append(yy[-1] + 0.66 * randint(0, 0))
    d = {'x': xx[-1], 'y': yy[-1]}
    return dumps(d)


@app.route('/get-ozone-history-data')
def get_ozone_history_data():
    # Test stage
    ozone_xx = [time.strftime(datetime.datetime(2017, 5, i).strftime("%Y-%m-%d")) for i in range(6, 14)]
    ozone_yy = [52 + 8 * (random() - 0.5) for i in range(len(ozone_xx))]
    d = {
        "xx": ozone_xx,
        "yy": ozone_yy
    }
    print(d)
    return dumps(d)


@app.route('/get-pm25-history-data')
def get_pm25_history_data():
    # Test stage
    pm25_xx = [time.strftime(datetime.datetime(2017, 5, i).strftime("%Y-%m-%d")) for i in range(6, 14)]
    pm25_yy = [78 + 40 * (random() - 0.5) for i in range(len(pm25_xx))]
    d = {
        "xx": pm25_xx,
        "yy": pm25_yy
    }
    return dumps(d)


if __name__ == '__main__':
    # proc = psutil.Popen(["python", "D:/NetworkProgramming/dynamic_chart/core/recevie_data.py"], stdin=PIPE, stdout=PIPE)
    app.run(host="0.0.0.0", port=12000)
