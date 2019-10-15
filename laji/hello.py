from flask import Flask
app = Flask(__name__)



# @app.route('/user/yzy')#输url是什么就是什么
#
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello, World'


if __name__ == '__main__':
    app.run()
# def show_user_profile(username):
#     # show the user profile for that user
#     return 'User %s' % escape(username)
#
# @app.route('/post/7')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id
#
# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return 'Subpath %s' % escape(subpath)