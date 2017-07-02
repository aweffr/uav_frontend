from flask import Flask, render_template, request
import json
import time
from datetime import datetime, timedelta
from collections import deque
from flask_sqlalchemy import SQLAlchemy
from operator import itemgetter

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
    pm25 = db.Column(db.Float)
    chou_yang = db.Column(db.Float)
    wen_du = db.Column(db.Float)
    shi_du = db.Column(db.Float)
    recv_time = db.Column(db.DateTime, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __repr__(self):
        return "<FlaskInfo> pm25=%f" % self.pm25


xx = [(datetime.now() + timedelta(seconds=(x - 60))).strftime("%H:%M:%S") for x in range(60)]
xx = deque(xx, maxlen=len(xx))
yy = deque()


def init():
    global xx, yy
    xx = [(datetime.now() + timedelta(seconds=(x - 60))).strftime("%H:%M:%S") for x in range(60)]
    xx = deque(xx, maxlen=len(xx))
    yy = deque(maxlen=(len(xx)))
    data_list = FlaskInfo.query.order_by(FlaskInfo.id.asc()).all()
    for info in data_list:
        yy.append((info.jing_du, info.wei_du, info.height, info.pm25, info.chou_yang, info.wen_du, info.shi_du))
    while len(yy) < len(xx):
        yy.appendleft((0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

    print(yy)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/receive_data_from_uav", methods=["POST"])
def receive_data_from_uav():
    data = request.data
    data = json.loads(data)
    print("receive_data_from_uav", type(data), data)

    if isinstance(data, str):
        data = eval(data)
        print(repr(data))

    info = FlaskInfo(jing_du=data["jing_du"],
                     wei_du=data["wei_du"],
                     height=data["height"],
                     pm25=data["pm25"],
                     chou_yang=data["chou_yang"],
                     wen_du=data["wen_du"],
                     shi_du=data["shi_du"])
    db.session.add(info)
    x_now = datetime.now().strftime("%H:%M:%S")
    y_now = (data["jing_du"],
             data["wei_du"],
             data["height"],
             data["pm25"],
             data["chou_yang"],
             data["wen_du"],
             data["shi_du"])
    if len(xx) == 0 or (len(xx) > 0 and x_now != xx[-1]):
        xx.append(datetime.now().strftime("%H:%M:%S"))
        yy.append(y_now)
    else:
        yy[-1] = y_now
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


@app.route('/get_ozone_data')
def get_ozone_data():
    global xx, yy
    out_xx = []
    out_yy = []
    for x, y in zip(xx, yy):
        out_xx.append(x)
        out_yy.append(y[4])
    d = {'xx': out_xx,
         'yy': out_yy}
    height_yy, _, chou_yang_xx = get_heigth_data()
    d["xx_height"] = chou_yang_xx
    d["yy_height"] = height_yy
    return json.dumps(d)


#  0             1            2             3         4               5            6
# (info.jing_du, info.wei_du, info.height, info.pm25, info.chou_yang, info.wen_du, info.shi_du)
def get_heigth_data():
    global xx, yy
    lst = []
    for data in yy:
        lst.append((data[2], data[3], data[4]))  # (height, pm25, chou_yang)
    lst = sorted(lst, key=itemgetter(0, 1, 2))
    height_out, pm25_out, chou_yang_out = [], [], []
    for height, pm25, chou_yang in lst:
        height_out.append(height)
        pm25_out.append(pm25)
        chou_yang_out.append(chou_yang)
    return height_out, pm25_out, chou_yang_out


@app.route('/update_ozone_data')
def update_data():
    global xx, yy
    out = yy[-1][4]
    d = {'x': xx[-1], 'y': out}

    height_yy, _, chou_yang_xx = get_heigth_data()
    d["xx_height"] = chou_yang_xx
    d["yy_height"] = height_yy

    return json.dumps(d)


@app.route('/get_pm25_data')
def get_pm25_data():
    global xx, yy
    out_xx = []
    out_yy = []
    for x, y in zip(xx, yy):
        out_xx.append(x)
        out_yy.append(y[3])
    d = {'xx': out_xx,
         'yy': out_yy}

    height_yy, pm25_xx, chou_yang_xx = get_heigth_data()
    d["xx_height"] = pm25_xx
    d["yy_height"] = height_yy

    return json.dumps(d)


@app.route('/update_pm25_data')
def update_pm25_data():
    global xx, yy
    out = yy[-1][3]
    d = {'x': xx[-1], 'y': out}

    height_yy, pm25_xx, chou_yang_xx = get_heigth_data()
    d["xx_height"] = pm25_xx
    d["yy_height"] = height_yy

    return json.dumps(d)


@app.route('/get-ozone-history-data')
def get_ozone_history_data():
    # Test stage
    ozone_xx = [time.strftime(datetime(2017, 5, i).strftime("%Y-%m-%d")) for i in range(6, 14)]
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
    pm25_xx = [time.strftime(datetime(2017, 5, i).strftime("%Y-%m-%d")) for i in range(6, 14)]
    pm25_yy = [72.31210130392026,
               74.36003202003266,
               81.0815528593375,
               85.44115429140395,
               83.97432689427235,
               79.09845096931669,
               73.45107713653275,
               65.97297080702435]

    d = {
        "xx": pm25_xx,
        "yy": pm25_yy
    }
    return json.dumps(d)


if __name__ == '__main__':
    init()
    app.run(host="0.0.0.0", port=5000)
