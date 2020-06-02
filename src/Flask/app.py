# 导入Flask类
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import sys
import click
from flask import request, url_for, redirect, flash
# 引入 算法代码
from src.queryX.AnsForQ_v1 import ansForQuery_V1
# 数据库可视化代码
from src.codeIO_MySql.selectFromMySql.allPaperInfo import get_Modify_PaperInfoFromMySql
from src.codeIO_MySql.selectFromMySql.allMainInfo import get_Modify_MainInfoFromMySql


# 实例化，可视为固定格式
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'

# 全局变量区域
USER_ROOT = 'root'
USER_ROOT_PASSWORD = 'root'
# 查询的返回结果 HTTP POST 数据格式
Query = ''
AnsForQ = []

# -------------------------------------------------------------------------------------------
# 数据库 部分
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
#
#
# class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
#     id = db.Column(db.Integer, primary_key=True)  # 主键
#     name = db.Column(db.String(20))  # 名字
#
#
# class Movie(db.Model):  # 表名将会是 movie
#     id = db.Column(db.Integer, primary_key=True)  # 主键
#     title = db.Column(db.String(60))  # 电影标题
#     year = db.Column(db.String(4))  # 电影年份
#
# # 数据库数据灌入  增量灌入形式
# @app.cli.command()
# def forge():
#     """Generate fake data."""
#     db.create_all()
#
#     # 全局的两个变量移动到这个函数内
#     name = 'Grey Li'
#     movies = [
#         {'title': 'My Neighbor Totoro', 'year': '1988'},
#         {'title': 'Dead Poets Society', 'year': '1989'},
#         {'title': 'A Perfect World', 'year': '1993'},
#     ]
#
#     user = User(name=name)
#     db.session.add(user)
#     for m in movies:
#         movie = Movie(title=m['title'], year=m['year'])
#         db.session.add(movie)
#
#     db.session.commit()
#     click.echo('Done.')
# -------------------------------------------------------------------------------------------


# 客户端（例如Web浏览器）把请求发送给Web服务器，Web服务器再把请求发送给Flask程序实例。
# 程序实例需要知道对每个URL请求运行哪些代码，所以保存了一个URL到python函数的映射关系。处理URL和函数之间关系的程序称为路由。
# route() 方法用于设定路由 称为 装饰器
# 绑定一个 web 地址  和 一个 def 方法
# 使用 app.route() 装饰器来为这个函数绑定对应的 URL
# 当用户在浏览器访问这个 URL 的时候，就会触发这个函数，获取返回值，并把返回值显示到浏览器窗口：
@app.route('/helloflask')
def hello_world():
    return '<h1>Hello Flask!</h1><img src="http://helloflask.com/totoro.gif">'


# 这里的<name>是个变量 同时也可以在函数里 获取到 name 的值
@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name


# 模板上下文处理函数
# 这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用。
@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = 'root_user'
    return dict(user=user)  # 需要返回字典，等同于return {'user': user}






# todo 要不要把主页面和登入界面换一下？ 好像也不用 默认游客登入  登入在主页面的右上角
# 主页面
# 使用 render_template() 函数可以把模板渲染出来，必须传入的参数为模板文件名（相对于 templates 根目录的文件路径）
# render_template() 函数在调用时会识别并执行 index.html 里所有的 Jinja2 语句，返回渲染好的模板内容。在
@app.route('/', methods=['GET', 'POST'])
def index():
    global Query
    global AnsForQ
    # 如果收到请求
    if request.method == 'POST':  # 判断是否是 POST 请求
        print("POST IF IN")
        # 获取表单数据
        Query = request.form.get('title')  # 传入表单对应输入字段的 name 值

        # 得到的 Query
        print("Query : ", Query)
        print("Ans : ....................")

        # 验证输入查询语句
        if len(Query) > 100:
            print('Invalid input.')
            flash('Invalid input.')  # 显示错误提示    报错Internal Server Error 需要设置签名所需的密钥
            return redirect(url_for('index'))  # 重定向回主页

        # 在这里根据 query 来更改 数据  AnsForQ 然后重定向后会自动渲染  AnsForQ的格式 需要和 html 统一 数据格式
        # AnsForQ [{'id': , 'title': , 'score':}]
        AnsForQ = ansForQuery_V1(Query)
        print('Query Searched ! .')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('index.html', movies=AnsForQ)


# 1. form 表单 method='post'    2. link 改为 flask 加载 CSS 模式
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    global USER_ROOT
    global USER_ROOT_PASSWORD

    if request.method == 'POST':
        print("in POST")
        # 获取表单数据 # 传入表单对应输入字段的 name 值
        username = request.form.get('username')
        userpassword = request.form.get('userpassword')
        print("输入的用户名和密码为：", username, userpassword)
        if username == USER_ROOT and userpassword == USER_ROOT_PASSWORD:
            print("User info is right")
            # 重定向会主页 查询页
            return redirect(url_for('index'))

    # 返回登入页
    return render_template("sign-in.html")


# 肥仔界面
@app.route('/database/Overview', methods=['GET', 'POST'])
def batabaseOverview():
    # 文件上传 界面 和 最近上传者数据 （暂且不管）
    print('in database/Overview.html')
    if request.method == 'POST':
        uploaded_files = request.files.getlist("myFile[]")
        print(len(uploaded_files))
        print(uploaded_files)

        # 当前文件所在路径
        basepath = os.path.dirname(__file__)

        for file in uploaded_files:
            if not file.filename.endswith(".pdf"):
                print("文件格式非PDF")
                return
            upload_path = os.path.join(basepath, 'RecvFile', secure_filename(file.filename))
            file.save(upload_path)
        print("For 循环结束 发送文件上传提示")

    return render_template("database.html")


@app.route('/database/PaperInfo')
def batabasePaperInfo():
    print("in paperInfo.html")
    ans = get_Modify_PaperInfoFromMySql()
    return render_template("paperInfo.html", items=ans)


@app.route('/database/MainInfo')
def batabaseMainInfo():
    print("in MainInfo.html")
    ans = get_Modify_MainInfoFromMySql()
    return render_template("mainInfo.html", items=ans)







# 错误处理页面和函数 404 即 URL 不存在与于templates中
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码


# 编辑条目
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


# 删除条目
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页


if __name__ == '__main__':

    # 本地调试
    app.run(debug=True)

    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    # NATAPP.cn 内网穿透 本地端口 8383
    # app.run(host="0.0.0.0", port=8383, debug=True)
