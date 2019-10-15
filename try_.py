from flask import Flask,url_for,request,session
import os
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
# 如果访问 /,返回 Index Page
@app.route('/')#叫做路由
def index():
    return 'Index Page'

# 如果访问 /hello，返回 Hello, World!
@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/user/<username>')
def show_user_profile(username):
    # 显示用户名
    return 'User {}'.format(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # 显示提交整型的用户"id"的结果，注意"int"是将输入的字符串形式转换为整型数据
    return 'Post {}'.format(post_id)#response

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # 显示 /path/ 之后的路径名
    return 'Subpath {}'.format(subpath)

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(username)

@app.route('/sum/<int:a>/<int:b>')
def sum(a,b):
    return '{0} + {1} = {2}'.format(a,b,a+b)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return ('do_the_login()')   # 如果是 POST 方法就执行登录操作
    else:
        return('show_the_login_form()')   # 如果是 GET 方法就展示登录表单


with app.test_request_context():#告诉 Flask 表现得像是在处理一个请求，
    # 即使我们正在通过 Python shell 交互。大家可以仔细分析一下该函数的打印结果。
    print(url_for('index'))
    print(url_for('hello'))
    print(url_for('hello', next='/'))
    print(url_for('profile', username='John Doe'))

app.run()
