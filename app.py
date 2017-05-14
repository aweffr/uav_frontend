from flask import Flask, render_template
from random import shuffle, randint
from json import dumps

# http://blog.csdn.net/u014030117/article/details/46508901
# Flask对Jinja2模版引擎支持很好，但无奈其所有静态文件都要放在static文件夹中（URL路由得加/static/...）
# 实例化Flask类的时候做一个小设置static_url_path=''即可，
# 把static_url_path设置为空字符串相当于设置把所有根目录下URL的访问都关联到/static/目录下，
# 所以静态HTML模版中直接可以引用/js/something.js而不是/static/js/something.js
app = Flask(__name__)

xx = [x for x in range(100)]
yy = [75, ]
for i in range(99):
    yy.append(yy[-1] + randint(-3, 4))


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
    return render_template('/pages/%s.html' % page_name)


@app.route('/getdata')
def getdata():
    yy = [85, ]
    for i in range(99):
        yy.append(yy[-1] + randint(-2, 5))
    d = {'xx': [x for x in range(100)],
         'yy': yy}
    return dumps(d)


@app.route('/updatedata')
def update_data():
    global xx, yy
    xx.append(xx[-1] + 1)
    yy.append(yy[-1] + randint(-9, 15))
    d = {'x': xx[-1], 'y': yy[-1]}
    return dumps(d)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=12225)
