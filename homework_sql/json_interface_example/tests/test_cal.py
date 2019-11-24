#!/usr/bin/env python3
import random
# from .conftest import client
from flask.testing import FlaskClient
#from flask import  request
import pytest
import random
from random import choice
import hashlib
import urllib.parse
import time
import threading,json
import string
from pymongo import MongoClient
from homework2.json_interface_example.calculate.func import ana
from flask import  session
from flask import Flask
from flask.testing import FlaskClient

# from calculate.cal import bp
# from python_flask.action.opt import bp
from homework2.json_interface_example.calculate.cal import bp
import os
#clientmg = MongoClient('localhost', 27017)
clientmg=MongoClient('mongodb+srv://mathskiller:11111111qQ@flaskgame-aoyhi.mongodb.net/test?retryWrites=true&w=majority')
user = clientmg.game.user
#user name money pocket lucky wear
market = clientmg.game.market
#market.create_index([("goods", ASCENDING)], unique=True)#不能以商品建立索引 因为会有商品重复
treasures = clientmg.game.treasure
info=clientmg.game.info
sessiondb=clientmg.game.sessiondb
commands = ["add", "sub", "mul", "div", "no"]
# session={}#"wotm pytest is too hard to use in pytest when flask use session"

app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(bp)
# def client:
#     app: Flask = Flask(__name__)
#     app.config['SECRET_KEY'] = os.urandom(24)
#     app.register_blueprint(bp)
#     client= app.test_client(use_cookies=True)
#     return client
with app.test_client(use_cookies=True) as client:
    @pytest.mark.parametrize(('username','pwd','message'),(
            [('mk','1a23',["登录成功,请进行游戏","密码错误，请重新login再post密码"]),
             ('mk2','a',["登录成功,请进行游戏","密码错误，请重新login再post密码"]),
             ('mk','1a2',["登录成功,请进行游戏","密码错误，请重新login再post密码"]),
             ('mk','1a23',["登录成功,请进行游戏","密码错误，请重新login再post密码"]),
             (''.join(random.sample(string.ascii_letters + string.digits, random.randint(1,8))),''.join(random.sample(string.ascii_letters + string.digits, random.randint(1,8))),['新建玩家成功，您的初始配置为'])]

    ))
    def test_login_get(username,pwd,message):
        rand= random.randint(0,3)
        if rand==0:#get
            response = client.get('/user/login')
            assert b'PLEASE USE POST TO LOGIN!' in response.data
        else:
            #由于代码中使用了302跳转，所以没办法只能这样写test
            #return redirect('/user/test?username={0}&pwd={1}'.format(username,str(urllib.parse.quote(str(hashlib.md5(pwd.encode("utf-8")).digest())))))
            #由于有上面这句话若还从/user/login入口进去 /user/test必然覆盖不到
            response = client.post('/user/login', data={'username':username,'pwd':pwd})
            print(response.status_code)
            assert response.status_code == 302

            #session['username'] = username
            response=client.get('/user/test?username={0}&pwd={1}'.format(username,str(urllib.parse.quote(str(hashlib.md5(pwd.encode("utf-8")).digest())))))
            json=response.get_json()
            # cookies = response.headers.getlist('Cookie')
            # print('##########',response.headers,'############')
            # print(cookies)
            # global session
            # session[username]=cookies[8:]
            # print(session)
            # print(1/0)
            # client.set_cookie('localhost', 'session', session)
            # if not(info.find_one({ "username": username})):#以name建立索引找起来就快
            #     assert json["cue"]==message
            # else:
            assert json["result"] in message

    @pytest.mark.parametrize(('username','message'),(
            [('mk',1),
             ('mk',0)]

    ))#由于money由随机方法生成，故不能猜测
    #第二次由于一天内不能第二次夺宝 所以ok=0
    def test_work(username,message):
        # aclient=client
        # print(sessiondb.find_one({'username':username})['session'])
        # aclient.set_cookie('localhost', 'session', sessiondb.find_one({'username':username})['session'])
        response = client.get('/user/{0}/work'.format(username))
        # print(response)
        # print(response.get_json())
        # print(response.data)
        # print(response.get_cookies())
        json=response.get_json()
        assert json["ok"]==message

    @pytest.mark.parametrize(('username','message'),(
            [('mk',1),
             ('mk',0)]
    ))#也有随机 所以只能判断ok与否
    def test_travel(username, message):
        response = client.get('/user/{0}/travel'.format(username))
        json=response.get_json()
        assert json["ok"]==message

    @pytest.mark.parametrize(('username','message'),(
            [('mk',1),
             ('mk2',0)]
    ))#也有随机 所以只能判断ok与否
    def test_travel(username, message):
        response = client.get('/user/{0}/travel'.format(username))
        json=response.get_json()
        assert json["ok"]==message

    @pytest.mark.parametrize(('username','message'),(
            [('mk',1),
             ('mk2',1)]
    ))
    def test_browse(username, message):
        response = client.get('/user/{0}/browse'.format(username))
        json=response.get_json()
        assert json["ok"]==message

    @pytest.mark.parametrize(('username','treasure','price','message'),(
            [('mk','衠钢槊',20,1),
             ('mk', '衠钢槊', 1, 1),
             ('mk2','衠钢槊',30,1),
             ('mk2', '衠钢槊', 30, 1),
             ('mk2', '衠钢槊', 100000, 1),
             ('mk','枭雄金印',20,0),#不能卖口袋里没有的
             ('mk','没有此物',20,0)]#不能卖没这东西的
    ))
    def test_sell(username,treasure,price,message):
        response = client.get('/user/{0}/sell/{1}/{2}'.format(username,treasure,price))
        json=response.get_json()
        assert json["ok"]==message

    @pytest.mark.parametrize(('username','treasure','price','sell','message'),(
            [('mk','衠钢槊',20,'mk',1),
             ('mk2','衠钢槊',30,'mk',0),#不能收别人的
             ('mk2', '衠钢槊', 30, 'mk2', 1),
             ('mk','枭雄金印',20,'mk',0),#不能收没有的
             ('mk','没有此物',20,'mk',0)]#不能收没有记录的
    ))
    def test_back(username,treasure,price,sell,message):
        response = client.get('/user/{0}/back/{1}/{2}/{3}'.format(username,treasure,price,sell))
        json=response.get_json()
        assert json["ok"]==message

    @pytest.mark.parametrize(('username','treasure','price','sell','message'),(
            [
             ('mk2', '衠钢槊', 1,'mk', 1),#mk和mk2互相买卖（由于mk已经满了仓库 所以会被check到并把最不值钱的丢了）
             ('mk', '衠钢槊', 30, 'mk2', 1),
             ('mk2','衠钢槊',30,'mk',0),#不能买市场上没有的
             ('mk', '衠钢槊', 100000, 'mk2', 0),#钱不够不能买
             ('mk2','衠钢槊',100000,'mk2',1),#可以买自己的
             ('mk','没有此物',20,'mk',0)]#不能收没有记录的
    ))
    def test_buy(username,treasure,price,sell,message):
        response = client.get('/user/{0}/buy/{1}/{2}/{3}'.format(username,treasure,price,sell))
        json=response.get_json()
        assert json["ok"]==message


    @pytest.mark.parametrize(('username', 'message'), (
            [
                ('mk2',0),
                ('mk',0)]#由于这俩人都没有5个束发紫金冠 换不了最终的枭雄金印
    ))
    # 获得枭雄金印
    def test_final(username, message):
        response = client.get('/user/{0}/final'.format(username))
        json=response.get_json()
        assert json["ok"]==message

    @pytest.mark.parametrize(('username', 'attr','message'), (
            [
                ('mk2','wear',1),#查看穿戴
                ('mk','yzynb',0)]#不能看没有的属性
    ))
    def test_see(username, attr,message):
        response = client.get('/user/{0}/see/{1}'.format(username,attr))
        json=response.get_json()
        assert json["ok"]==message

    @pytest.mark.parametrize(('username', 'treasure','message'), (
            [
                ('mk2','衠钢槊',1),
                ('mk2','枭雄金印',0),#不能穿没有的
            ('mk2','无此宝物',0)]#不能穿没该宝物的
    ))
    def test_wear(username, treasure,message):
        response = client.get('/user/{0}/wear/{1}'.format(username,treasure))
        json=response.get_json()
        assert json["ok"]==message

    @pytest.mark.parametrize(('username', 'treasure','message'), (
            [
                ('mk2','衠钢槊',1),
                ('mk2','枭雄金印',0),#不能脱没有的
            ('mk2','无此宝物',0)]#不能脱没该宝物的
    ))
    def test_unwear(username, treasure,message):
        response = client.get('/user/{0}/unwear/{1}'.format(username,treasure))
        json=response.get_json()
        assert json["ok"]==message

    # def verify_json(json, cmd: str, x: int, y: int):
    #     result = 0
    #     ok = True
    #     if cmd == "add":
    #         result = x + y
    #     elif cmd == "sub":
    #         result = x - y
    #     elif cmd == "mul":
    #         result = x * y
    #     elif cmd == "div":
    #         result = int(x / y)
    #     else:
    #         ok = False
    #     assert json["ok"] is ok
    #     assert json["result"] == result
    #
    #
    # def test_cal_get():
    #     for cmd in commands:
    #         op1 = random.randint(0, 100)
    #         op2 = random.randint(1, 100)
    #         response = client.get("/user/%s/%d/%d" % (cmd, op1, op2))
    #         json = response.get_json()
    #         print('json', json)
    #         verify_json(json, cmd, op1, op2)
    #
    #
    # def test_cal_post():
    #     for cmd in commands:
    #         op1 = random.randint(0, 100)
    #         op2 = random.randint(1, 100)
    #         response = client.post('/user/json', json=dict(
    #             cmd=cmd,
    #             op1=op1,
    #             op2=op2))
    #
    #         json = response.get_json()
    #         print('json', json)
    #         verify_json(json, cmd, op1, op2)
