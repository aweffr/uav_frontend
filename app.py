from flask import Flask, render_template, request
from random import randint
import json
import time
import datetime
from collections import deque
from flask_sqlalchemy import SQLAlchemy

data_queue = deque(maxlen=100)
thread = None

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://aweffr:summer123@aweffr.win:3306/chat"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class FlaskInfo(db.Model):
    __tablename__ = "info"
    id = db.Column(db.Integer, primary_key=True)
    jing_du = db.Column(db.Float)
    wei_du = db.Column(db.Float)
    height = db.Column(db.Float)
    chou_yang = db.Column(db.Float)
    pm25 = db.Column(db.Float)
    wen_du = db.Column(db.Float)
    shi_du = db.Column(db.Float)

    def __repr__(self):
        return "<FlaskInfo id=%d jing_du=%f wei_du=%f height=%f" % (self.id, self.jing_du, self.wei_du, self.height)


xx = [(datetime.datetime.now() + datetime.timedelta(seconds=(x - 60))).strftime("%H:%M:%S") for x in range(60)]
yy = [0, ]
for i in range(59):
    yy.append(yy[-1] + 0.5 * randint(0, 0))


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/receive_data_from_uav", methods=["POST"])
def receive_data_from_uav():
    data = request.data
    data = json.loads(data)
    print("receive_data_from_uav", data)
    return "Succeed", 200


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
    return json.dumps(d)


@app.route('/updatedata')
def update_data():
    global xx, yy
    xx.append(time.strftime("%H:%M:%S"))
    yy.append(yy[-1] + 0.66 * randint(0, 0))
    d = {'x': xx[-1], 'y': yy[-1]}
    return json.dumps(d)


@app.route('/get-ozone-history-data')
def get_ozone_history_data():
    # Test stage
    ozone_xx = [time.strftime(datetime.datetime(2017, 5, i).strftime("%Y-%m-%d")) for i in range(6, 14)]
    # ozone_yy = [52 + 8 * (random() - 0.5) for i in range(len(ozone_xx))]
    ozone_yy = [54.13354220083586,
                54.40904295827208,
                52.837885234874825,
                50.57564263353102,
                48.07532339032751,
                49.794336520820465,
                49.63183682389971,
                49.46190356155412]

    d = {
        "xx": ozone_xx,
        "yy": ozone_yy
    }
    print(d)
    return json.dumps(d)


@app.route('/get-pm25-history-data')
def get_pm25_history_data():
    # Test stage
    pm25_xx = [time.strftime(datetime.datetime(2017, 5, i).strftime("%Y-%m-%d")) for i in range(6, 14)]
    pm25_yy = [72.31210130392026,
               74.36003202003266,
               81.0815528593375,
               85.44115429140395,
               80.97432689427235,
               77.09845096931669,
               69.45107713653275,
               65.97297080702435]

    d = {
        "xx": pm25_xx,
        "yy": pm25_yy
    }
    return json.dumps(d)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
