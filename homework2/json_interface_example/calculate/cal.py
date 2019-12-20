#!/usr/bin/env python3
# coding:utf-8
import importlib,sys
importlib.reload(sys)
#python2.7用reload(sys)
# 在Python2.x中由于str和byte之间没有明显区别，经常要依赖于defaultencoding来做转换。
# 在python3中有了明确的str和byte类型区别，从一种类型转换成另一种类型要显式指定encoding。
# sys.setdefaultencoding('utf8')#python3.6.3不要
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import redirect,session,render_template
import sys
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING
from random import choice
from .func import *
import hashlib
# import urllib.parse
import urllib
import time
import threading,json
import ssl
bp = Blueprint("mul", __name__, url_prefix="/user")
#client = MongoClient('localhost', 27017)
client=MongoClient('mongodb+srv://mathskiller:11111111qQ@flaskgame-aoyhi.mongodb.net/test?retryWrites=true&w=majority')
user = client.game.user
user.create_index([("name", ASCENDING)], unique=True)
#user name money pocket lucky wear
market = client.game.market
#market.create_index([("goods", ASCENDING)], unique=True)#不能以商品建立索引 因为会有商品重复
treasures = client.game.treasure
info=client.game.info
info.create_index([("username", ASCENDING)], unique=True)#按用户名建立索引
sessiondb=client.game.sessiondb
sessiondb.create_index([("username", ASCENDING)], unique=True)
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
    # print('username' in session)
    print(session.get('username')=='mk')
    # print(session.get('username')=='mk2')
    if session.get('username')!=username:
        return redirect('/user/login')
    else:
        if (work_flag==1):
            work_flag=0
            money0=ana(get_user(username,'money'))
            money=ana(get_user(username,'money'))
            if ana(get_user(username,'wear'))['工具']:
                base=sum(list(map(lambda x:ana(get_treasure(x,'value')),ana(get_user(username,'wear'))['工具'])))*10#基准
                print(base)
                money+=base+get_norm(username,-base/3,base/3,0.7)#钱增加工具价值+（-工具价值至工具价值)/3区间的服从正态分布的随机值
                change_user(username,'money',money)
            else:
                pass#不挂工具拿不到钱
            return render_template('operation.html',username=username,result={'result':'原来有钱{0},现在有钱{1}'.format(money0,money),'ok':1})
        else:
            return render_template('operation.html',username=username,result={'result':'您今天已经工作过','ok':0})
#寻宝
@bp.route("/<string:username>/travel", methods=['GET'])#####得到宝物的level由lucky值决定
def travel(username):
    global travel_flag
    if session.get('username')!=username:
        return redirect('/user/login')
    else:
        if (travel_flag==1):
            travel_flag =0
            #得到宝物的level由lucky值决定 lucky值控制正态分布的期望
            print(get_norm(username,1, 5, 0.7))
            print(get_norm(username, 1, 5, 0.7))
            print(get_norm(username, 1, 5, 0.7))
            print(get_norm(username, 1, 5, 0.7))
            print(get_norm(username, 1, 5, 0.7))
            print(get_norm(username, 1, 5, 0.7))
            level_num=get_norm(username,1, 5, 0.7)#得到武器level的评级
            map_ = {1: '普通', 2: '稀有', 3: '史诗', 4: '传说', 5: '限定'}
            print('level_num',level_num)
            print('map_[level_num]', map_[level_num])
            print(choice([x for x in treasures.find({'property': '工具', 'level':map_[level_num] })])['name'])
            #决定获得配饰还是工具 0是工具1是配饰
            import random
            rd=random.randint(0, 1)
            if (rd==0):#工具
                whatget=choice([x for x in treasures.find({'property': '工具', 'level':map_[level_num] })])['name']#{'$ne':'终极'}不能直接获得能够令游戏胜利的终极目标
                add_pocket(username,whatget)
            else:#配饰
                whatget = choice([x for x in treasures.find({'property': '配饰', 'level':map_[level_num] })])['name']
                add_pocket(username,whatget)
            return render_template('operation.html',username=username,result={'result':whatget,'level': map_[level_num],'ok':1})
        else:
            return render_template('operation.html',username=username,result={'result':'您今天已经寻宝过','ok':0})
#浏览市场
@bp.route("/<string:username>/browse", methods=['GET'])
def browse(username):
    if session.get('username')!=username:
        return redirect('/user/login')
    else:
        return render_template('operation.html',username=username,result={'result':list(get_market()),'ok':1})
#挂牌宝物
@bp.route("/<string:username>/sell", methods=['POST'])
def sell_(username):
    treasure=request.form.get('treasure')
    price = request.form.get('price')
    if session.get('username')!=username:
        return redirect('/user/login')
    else:
        return render_template('operation.html',username=username,result=ana2(sell(username,treasure,price)))
#买宝物
@bp.route("/<string:username>/buy", methods=['POST'])
def buy_(username):
    treasure = request.form.get('treasure')
    price = request.form.get('price')
    sell=request.form.get('sell')
    if session.get('username')!=username:
        return redirect('/user/login')
    else:
        return render_template('operation.html',username=username,result=ana2(buy(username,treasure,price,sell)))
#收回宝物
@bp.route("/<string:username>/back", methods=['POST'])
def back_(username):
    treasure = request.form.get('treasure')
    price = request.form.get('price')
    sell=request.form.get('sell')
    if session.get('username')!=username:
        return redirect('/user/login')
    else:
        return render_template('operation.html',username=username,result=ana2(back(username,treasure,price,sell)))
#获得枭雄金印
@bp.route("/<string:username>/final", methods=['GET'])
def final_(username):
    if session.get('username')!=username:
        return redirect('/user/login')
    else:
        return render_template('operation.html',username=username,result=ana2(final(username)))

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@bp.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

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
        print('POSTgetsession:   ',request.cookies.get('session'))
        # if sessiondb.find_one({'username':username}):
        #     sessiondb.delete_one({'username':username})
        # sessiondb.insert_one({'username':username,'session':request.cookies.get('session')})
        print('POSTgetusername:   ',session.get('username'))
        from urllib.request import pathname2url
        return redirect('/user/test?username={0}&pwd={1}'.format(username,str(urllib.request.pathname2url(str(hashlib.md5(pwd.encode("utf-8")).digest()))))) # 如果是 POST 方法就执行登录操作
    elif request.method == 'GET':
        print('GETgetusername:   ',session.get('username'))
        return render_template('login.html')   # 如果是 GET 方法就展示登录表单

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
    print('/test pwd:',pwd)
    try:
        info.insert_one({'username':username,'pwd':pwd})

    except DuplicateKeyError:
        if (info.find_one({ "username": username,'pwd':pwd })):#以name建立索引找起来就快
            return render_template('loginskip.html',username=username,pwd=pwd,result=str({"result":"登录成功,请进行游戏","ok":1}))
        else:
            return render_template('login.html',result=str({"result":"密码错误，请重新login再post密码","ok":0}))
    else:
        user.insert_one({"name": username, "money": 200,
                         "pocket": {"工具": ["衠钢槊"], "配饰": ["烂银甲"]}
                            ,'lucky':0,'wear':{"工具": [], "配饰": []},
                         'onmarket':{"工具": [], "配饰": []}})
        return render_template('loginskip.html',username=username,pwd=pwd,result=str({"result":"新建玩家成功，您的初始配置为","name": username, "money": 200,
                         "pocket": {"工具": ["衠钢槊"], "配饰": ["烂银甲"]}
                            ,'lucky':0,'wear':{"工具": [], "配饰": []},
                        'onmarket':{"工具": [], "配饰": []}}))

##查看自己的某个属性
@bp.route("/<string:username>/see", methods=['POST'])
def attr_(username):
    treasure=request.form.get('treasure')
    attr = request.form.get('attr')
    print(treasure)
    print(attr)
    if not treasure:
        if session.get('username')!=username:
            return redirect('/user/login')
        else:
            return render_template('operation.html',username=username,result=ana2(get_user(username,attr)))
    else:
        if session.get('username') != username:
            return redirect('/user/login')
        else:
            return render_template('operation.html',username=username,result=ana2(get_treasure(treasure, attr)))


##穿戴
@bp.route("/<string:username>/wear", methods=['POST'])
def wear(username):
    treasure = request.form.get('treasure')
    if session.get('username')!=username:
        return redirect('/user/login')
    else:
        return render_template('operation.html',username=username,result=ana2(add_wear(username,treasure)))
    #print(session.get('username'))
    #return find_pocket(username,treasure)

    # if session.get('username'):
    #     user_=user.find_one({"name": username})
    #     pocket=user_[0]['pocket']
    #     pocket1=pocket['工具']
    #     pocket2 = pocket['配饰']
    #     if treasure in pocket1:
    #         pocket1.pop(treasure)
    #
    #     elif treasure in pocket2:
    #     else:
    #         return jsonify({"result": '穿戴失败，无该宝物', "ok": 0})
    # else:
    #     return redirect('/user/login')

##脱掉
@bp.route("/<string:username>/unwear", methods=['POST'])
def unwear(username):
    treasure = request.form.get('treasure')
    if session.get('username')!=username:
        return redirect('/user/login')
    else:
        return render_template('operation.html',username=username,result=ana2(un_wear(username,treasure)))

##游戏操作界面
@bp.route("/operation/<string:username>", methods=['GET'])
def operation(username):
    return render_template('operation.html',username=username)

from flask import request
def shutdown_server():
    func2 = request.environ.get('werkzeug.server.shutdown')
    if func2 is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func2()
@bp.route('/shutdown', methods=['GET'])
def shutdown2():
    shutdown_server()
    return 'Server shutting down...'
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

# @bp.route("/<string:cmd>/<int:x>/<int:y>", methods=['GET'])
# def cal_get(cmd, x, y):
#     result, ok = cal_gut(cmd, x, y)
#     return jsonify({"result": result, "ok": ok})
#
#
# @bp.route("/json", methods=["POST"])
# def cal_post():
#     result, ok = cal_gut(request.json["cmd"], request.json["op1"], request.json["op2"])
#     return jsonify({"result": result, "ok": ok})
#
#
# def cal_gut(cmd, x, y):
#     if cmd == "add":
#         return x + y, True
#     elif cmd == "sub":
#         return x - y, True
#     elif cmd == "mul":
#         return x * y, True
#     elif cmd == "div":
#         return int(x / y), True
#     else:
#         return 0, False