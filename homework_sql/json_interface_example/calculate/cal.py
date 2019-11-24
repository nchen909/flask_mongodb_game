#!/usr/bin/env python3

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import redirect,session
import sys
# from pymongo import MongoClient
# from pymongo.errors import DuplicateKeyError
# from pymongo import ASCENDING
from random import choice
from .__init__ import *
import hashlib
import urllib.parse
import time
import threading,json
bp = Blueprint("mul", __name__, url_prefix="/user")
#client = MongoClient('localhost', 27017)
# client=MongoClient('mongodb+srv://mathskiller:11111111qQ@flaskgame-aoyhi.mongodb.net/test?retryWrites=true&w=majority')
# user = client.game.user
# user.create_index([("name", ASCENDING)], unique=True)
# #user name money pocket lucky wear
# market = client.game.market
# #market.create_index([("goods", ASCENDING)], unique=True)#不能以商品建立索引 因为会有商品重复
# treasures = client.game.treasure
# info=client.game.info
# info.create_index([("username", ASCENDING)], unique=True)#按用户名建立索引
# sessiondb=client.game.sessiondb
# sessiondb.create_index([("username", ASCENDING)], unique=True)
###python中设置成这样（外面）需要在函数中调用且改变的全局变量需要在函数中写成global

#设置信号量work_flag,travel_flag
work_flag=1
travel_flag=1
#并发执行
def oneday():#flask会运行运行的那个文件中所有被import到的有路由的整个py文件
    global work_flag,travel_flag
    while 1:
        time.sleep(60)#60s为一天
        work_flag = 1#每个人work_flag不一样
        travel_flag = 1

timer=threading.Timer(0,oneday)
timer.start()
#工作
@bp.route("/<string:username>/work", methods=['GET'])#####工作能力直接由工具价值决定
def work(username):
    global work_flag
    #print('username' in session)
    print(session.get('username'))
    if not session.get('username'):
        return redirect('/user/login')
    else:
        tojson=to_work(username,work_flag)
        work_flag = 0
        return jsonify(tojson)
#寻宝
@bp.route("/<string:username>/travel", methods=['GET'])#####得到宝物的level由lucky值决定
def travel(username):
    global travel_flag
    if not session.get('username'):
        return redirect('/user/login')
    else:
        tojson=to_travel(username,travel_flag)
        travel_flag = 0
        return jsonify(tojson)
#浏览市场
@bp.route("/<string:username>/browse", methods=['GET'])
def browse(username):
    if not session.get('username'):
        return redirect('/user/login')
    else:
        return jsonify({'result':list(get_market()),'ok':1})
#挂牌宝物
@bp.route("/<string:username>/sell/<string:treasure>/<int:price>", methods=['GET'])
def sell_(username,treasure,price):
    if not session.get('username'):
        return redirect('/user/login')
    else:
        return jsonify(sell(username,treasure,price))
#买宝物
@bp.route("/<string:username>/buy/<string:treasure>/<int:price>/<string:sell>", methods=['GET'])
def buy_(username,treasure,price,sell):
    if not session.get('username'):
        return redirect('/user/login')
    else:
        return jsonify(buy(username,treasure,price,sell))
#收回宝物
@bp.route("/<string:username>/back/<string:treasure>/<int:price>/<string:sell>", methods=['GET'])
def back_(username,treasure,price,sell):
    if not session.get('username'):
        return redirect('/user/login')
    else:
        return jsonify(back(username,treasure,price,sell))
#获得枭雄金印
@bp.route("/<string:username>/final", methods=['GET'])
def final_(username):
    if not session.get('username'):
        return redirect('/user/login')
    else:
        return jsonify(final(username))
#登录
@bp.route("/login", methods=['GET','POST'])
def login():
    print(request.method)
    print(request.path)
    # if request.path == '/user/login':
    #     return '重复跳转'
    if request.method == 'POST':
        username = request.form.get('username')
        print(username)
        pwd = request.form.get('pwd')
        session['username'] = username
        print(request.cookies.get('session'))
        # if sessiondb.find_one({'username':username}):
        #     sessiondb.delete_one({'username':username})
        # sessiondb.insert_one({'username':username,'session':request.cookies.get('session')})
        #print(session.get('username'))
        return redirect('/user/test?username={0}&pwd={1}'.format(username,str(urllib.parse.quote(str(hashlib.md5(pwd.encode("utf-8")).digest()))))) # 如果是 POST 方法就执行登录操作
    elif request.method == 'GET':
        return('PLEASE USE POST TO LOGIN!')   # 如果是 GET 方法就展示登录表单

###########################写pytest时发现 如果是这么写 return就返回一个303的界面不走下去
###########################所以如果redirect的界面人访问不到 那就是
# @bp.route('/nopwd')
# # def nopwd():
# #     return()
#查看用户名密码是否正确
@bp.route('/test')#/<string:username>/<string:pwd>')
def index():

    username = request.args.get('username')
    pwd = request.args.get('pwd')
    print(pwd)
    return jsonify(is_passwd_correct(username, pwd))

##查看自己的某个属性
@bp.route("/<string:username>/see/<string:attr>", methods=['GET'])
def attr_(username,attr):
    if not session.get('username'):
        return redirect('/user/login')
    else:
        return jsonify(get_user(username,attr))

##查看宝物的某个属性
@bp.route("/<string:username>/see/<string:treasure>/<string:attr>", methods=['GET'])
def see_attr_(username,treasure,attr):
    if not session.get('username'):
        return redirect('/user/login')
    else:
        return jsonify(get_treasure(treasure,attr))

##穿戴
@bp.route("/<string:username>/wear/<string:treasure>", methods=['GET'])
def wear(username,treasure):
    if not session.get('username'):
        return redirect('/user/login')
    else:
        return jsonify(add_wear(username,treasure))

##脱掉
@bp.route("/<string:username>/unwear/<string:treasure>", methods=['GET'])
def unwear(username,treasure):
    if not session.get('username'):
        return redirect('/user/login')
    else:
        return jsonify(un_wear(username,treasure))


# @bp.route("/<string:username>/buy/<string:treasure>", methods=['GET'])
#     # def buy(username, treasure):
#     #     # if session.get('username'):
#     #
#     #     return players.find_one({"_id": post_id})
#     # else:
#     #     return redirect('/user/login')
#     player = players.find_one({"name": username})
#     # 宝物到位
#     box1 = player['box']
#     if len(box1) >= 10:
#         recovery_treasure(username)
#     box = player['box']
#     box.append(treasure)
#     players.update_one({"name": username}, {"$set", {"box": box}})
#     # 买家钱到位
#     treasure_money = treasures.find_one({"name":treasure})['price']
#     money1 = player['money'] - treasure_money
#     players.update_one({"name": username}, {"$set", {"money": money1}})
#     # 卖家钱到位
#     of = markets.find_one({"name": treasure})['of']
#     money2 = players.find_one({"name": of})['money'] + treasure_money
#     players.update_one({"name": of}, {"$set", {"money": money2}})
#     # 市场删除该宝物
#     markets.delete_one({"name": treasure})
#     return "购买成功，金币余额 %d" % money1

@bp.route("/<string:cmd>/<int:x>/<int:y>", methods=['GET'])
def cal_get(cmd, x, y):
    result, ok = cal_gut(cmd, x, y)
    return jsonify({"result": result, "ok": ok})


@bp.route("/json", methods=["POST"])
def cal_post():
    result, ok = cal_gut(request.json["cmd"], request.json["op1"], request.json["op2"])
    return jsonify({"result": result, "ok": ok})


def cal_gut(cmd, x, y):
    if cmd == "add":
        return x + y, True
    elif cmd == "sub":
        return x - y, True
    elif cmd == "mul":
        return x * y, True
    elif cmd == "div":
        return int(x / y), True
    else:
        return 0, False