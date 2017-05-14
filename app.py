from flask import Flask, render_template
from random import shuffle, randint
from json import dumps
from recevie_data import revice_data_service
import threading
import time
import psutil
from subprocess import PIPE

app = Flask(__name__)

xx = [time.strftime("%HH-%MM-%SS") for x in range(100)]
yy = [75, ]
for i in range(99):
    yy.append(yy[-1] + randint(-3, 3))


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
    d = {'xx': [x for x in xx],
         'yy': yy}
    return dumps(d)


@app.route('/updatedata')
def update_data():
    global xx, yy
    xx.append(time.strftime("%HH-%MM-%SS"))
    yy.append(yy[-1] + randint(-4, 4))
    d = {'x': xx[-1], 'y': yy[-1]}
    return dumps(d)


if __name__ == '__main__':
    # proc = psutil.Popen(["python", "D:/NetworkProgramming/dynamic_chart/core/recevie_data.py"], stdin=PIPE, stdout=PIPE)
    app.run(host="0.0.0.0", port=12000)

