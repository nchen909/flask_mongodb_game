#!/usr/bin/env python3
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import redirect,session
import sys
import sqlalchemy
import hashlib
import urllib.parse
from sqlalchemy.exc import  IntegrityError
from sqlalchemy import Column,String,Integer,ForeignKey,create_engine,PrimaryKeyConstraint
from sqlalchemy.orm import  sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  create_engine
from sqlalchemy import  sql,select,func
import psycopg2
bp = Blueprint("mul", __name__, url_prefix="/user")
MAX_POCKET=10#袋子里工具或配饰最多为10个
MAX_WEAR=2 #佩戴宝物最多为2个
MAXINT=2147483647
##################最终目的是合成 枭雄金印 ，return游戏成功


# 创建对象的基类
Base = declarative_base()
# 初始化数据库连接
engine = create_engine('postgresql://postgres:1@localhost:5432/homework_sql')
# 创建DBSession
DBSession = sessionmaker(bind=engine)  # 建立起会话 手机（bind=自己的手机号（mysql号））
# 创建session对象：
session2 = DBSession()  # 用该手机拨打电话（）
#declare a mapping
#定义User对象
class USER(Base):

    __tablename__ = 'user'
    name = Column(String(16),primary_key=True)
    money = Column(Integer, nullable=False)
    lucky = Column(Integer, nullable=False)
    workbase = Column(Integer, nullable=False)
    passwd = Column(String(100), nullable=False)

    def __repr__(self):
        return "name:%s, money:%d, lucky:%d, workbase:%d,passwd:%s" % (
            self.name, self.money, self.lucky, self.workbase,self.passwd)


class TREASURE(Base):
    __tablename__ = 'treasure'
    name = Column(String(5),primary_key=True)
    property = Column(String(2), nullable=False)
    value = Column(Integer, nullable=False)
    level = Column(String(2), nullable=False)

    def __repr__(self):
        return "name:%s, property:%s, value:%d, level:%s" % (
            self.name, self.property, self.value, self.value)

class WEAR(Base):
    __tablename__ = 'wear'
    uid = Column(String(5),ForeignKey('user.name'),primary_key=True)
    tid = Column(String(5),ForeignKey('treasure.name'),primary_key=True)
    num = Column(Integer, primary_key=True)

    def __repr__(self):
        return "name:%s, property:%s, num:%d" % (
            self.uid, self.tid, self.num)

class POCKET(Base):
    __tablename__ = 'pocket'
    uid = Column(String(5),ForeignKey('user.name'),primary_key=True)
    tid = Column(String(5),ForeignKey('treasure.name'), primary_key=True)
    num = Column(Integer, primary_key=True)

    def __repr__(self):
        return "name:%s, property:%s, num:%d" % (
            self.uid, self.tid, self.num)

class MARKET(Base):
    __tablename__ = 'market'
    seller = Column(String(15),ForeignKey('user.name'),primary_key=True)
    tid = Column(String(5), ForeignKey('treasure.name'),primary_key=True)
    price = Column(Integer, nullable=False)
    num = Column(Integer, primary_key=True)

    def __repr__(self):
        return "seller:%s, tid:%s, num:%d, price:%d" % (
            self.seller, self.tid, self.num, self.price)

Base.metadata.create_all(engine)#创建对应的表

name=['青龙偃月刀','诸葛连弩','雌雄双股剑','青红剑','丈八蛇矛','贯石斧','方天画戟','麒麟弓','寒冰剑','古锭刀','朱雀羽扇','三尖两刃刀','七宝刀','银月枪','衠钢槊']
name2=['藤甲','白银狮子','八卦阵','仁王盾','束发紫金冠','玲珑狮蛮带','红锦百花袍','木牛流马','烂银甲','护心镜']
value=[35,60,5,20,40,100,9,2,20,45,15,55,25,50,1]
value2=[60,20,30,45,100,70,85,10,1,7]
#普通稀有史诗传说限定
level=[2,4,1,2,3,5,1,1,2,3,1,4,2,4,1]
level2=[4,2,2,3,5,4,4,1,1,1]
map_={1:'普通',2:'稀有',3:'史诗',4:'传说',5:'限定'}
#终极目标获得终极
#
# def dbadd():
#     #######################增
#     # try:
#     for i in range(len(name)):
#         treasure1 = TREASURE(name=name[i], property= "工具", value=value[i], level= map_[level[i]])
#         session2.add(treasure1)
#     for i in range(len(name2)):
#         treasure2 = TREASURE(name=name2[i], property= "配饰", value=value[i], level= map_[level[i]])
#         session2.add(treasure2)
#     # except:
#     #     print("已创建过宝物")
#     # 枭雄金印不可通过购买 寻宝等获得，只能最终通过5个束发紫金冠去换 （游戏终极目标）
#     # try:
#     treasure3 = TREASURE(name='枭雄金印', property="配饰", value=MAXINT, level='终极')
#     session2.add(treasure3)
#     # except IntegrityError:
#     #     print("已创建过最强配饰：枭雄金印")
#
#
# def dbfind():
#     ########################查
#     zgs = session2.query(TREASURE).filter(TREASURE.name=="衠钢槊").one()
#     print(zgs.value)
#
# def dbchange():
#     ########################改
#     zgs = session2.query(TREASURE).filter(TREASURE.name=="衠钢槊").one()#查
#     zgs.value = 1
#     # a.books.append(Book(id=10001,book_name='yzynb2',user_name=1243))#增
#     session2.add(zgs)
# # def dbdelete():
# #     #######################删
# #     a = session2.query(User).get(1)#查
# #     session2.delete(a)
# def dbselect():
# ########################直接命令行
#     users = session2.execute("SELECT value FROM treasure WHERE name='衠钢槊'").fetchall()#能找到对象
#     print(type(users[0]))
#     for auser in users:
#         print(f"value：{auser.value}")

# 解析flask.wrappers.Response中包裹的字典,传入Response及需要的属性 返回对应值
def ana(response_,value='result'):
    # return eval(str(response_.data, encoding = "utf-8"))[value]
    return response_[value]

# def get_try():
#     student_=session2.query(Student).order_by(Student.sage.desc()).all()
#     # print(select(['*']).select_from(Student))
#     print(session2.execute(select([Student])).fetchall())
# 获取用户的某个属性
def get_user(username,attr='name'):
    one = session2.query(USER).filter(USER.name == username).first()#.first 或者.all返回列表 如果没有返回空
    if not (one):
        return {"result": "无该用户", "ok": 2}
    if attr=='name':
        return {"result": one.name, "one":one,"ok": 1}
    elif attr=='money':
        return {"result": one.money,"one":one, "ok": 1}
    elif attr == 'lucky':
        return {"result": one.lucky, "one":one,"ok": 1}
    elif attr=='workbase':
        return {"result": one.workbase,"one":one, "ok": 1}
    elif attr=='passwd':
        return {"result": one.passwd,"one":one, "ok": 1}
    else:
        return {"result": "用户无该属性", "ok": 0}



    # try:
    #     return jsonify({"result":one[attr],"ok": 1})
    # except KeyError:
    #     return jsonify({"result":"用户无该属性","ok": 0})

# 修改用户的某个属性
def change_user(username,attr,new_attr):
    if ana(get_user(username,attr),'ok'):
        one=ana(get_user(username,attr),'one')
        if attr == 'name':
            one.name=new_attr
        elif attr == 'money':
            one.money=new_attr
        elif attr == 'lucky':
            one.lucky=new_attr
        elif attr == 'workbase':
            one.workbase=new_attr
        elif attr == 'passwd':
            one.passwd=new_attr
        return {"result":'修改用户属性成功',"ok": 1}
    else:
        return get_user(username,attr)

#密码是否正确
def is_passwd_correct(username,pwd):
    if ana(get_user(username),'ok')==2:
        auser = USER(name=username, money=200, lucky=0, workbase=0,passwd=pwd)

        session2.add(auser)
        add_pocket(username, "衠钢槊")
        add_pocket(username,"烂银甲")
        return {"result": "新建玩家成功，您的初始配置为", "name": username, "money": 200,
                        "pocket": ["衠钢槊","烂银甲"]
                           , 'lucky': 0,'wear':[],'market':[],"ok":1}
    elif ana(get_user(username,'passwd'))!=pwd:
        return {"result": "密码错误，请重新login再post密码", "ok": 0}
    else:
        return {"result":"登录成功,请进行游戏","ok":1}
# 获取宝物的某个属性
def get_treasure(treasure,attr='property'):
    one = session2.query(TREASURE).filter(TREASURE.name == treasure).first()
    if not (one):
        return {"result": "无该宝物", "ok": 0}
    if attr=='name':
        return {"result": one.name, "one":one,"ok": 1}
    elif attr=='property':
        return {"result": one.property,"one":one, "ok": 1}
    elif attr == 'value':
        return {"result": one.value, "one":one,"ok": 1}
    elif attr=='level':
        return {"result": one.level,"one":one, "ok": 1}
    else:
        return {"result": "宝物库中无该属性", "ok": 0}

#如果pocket满了就把最便宜的那个先换成钱 然后丢掉 不然不动
def check_pocket(username):
    num1 = session2.query(func.sum(POCKET.num)).filter(POCKET.uid == username).all()
    if num1[0][0]==MAX_POCKET:
        thelist=session2.query(POCKET.tid).filter(POCKET.uid == username).all()#所有该用户的POCKET信息
        values=[]
        for i in range(MAX_POCKET):
            values.append(ana(get_treasure(thelist[i].tid,'value')))
        ana(get_user(username, 'money'),'one').money+=ana(get_treasure(thelist[values.index(min(values))].tid, 'value')) * 10
        un_pocket(username,thelist[values.index(min(values))].tid)
    return

#如果宝物带满了就把最便宜的那个拆下来 不然不动
def check_wear(username):
    num1 = session2.query(func.sum(WEAR.num)).filter(POCKET.uid == username).all()
    if num1[0][0]==MAX_WEAR:
        thelist=session2.query(WEAR.tid).filter(WEAR.uid == username).all()#所有该用户的WEAR信息
        values=[]
        for i in range(MAX_WEAR):
            values.append(ana(get_treasure(thelist[i].tid,'value')))
        add_pocket(username, thelist[values.index(min(values))].tid)
        un_wear(username, thelist[values.index(min(values))].tid)
    return

# 查看某用户口袋中有无某宝物 有则result为宝物property pocket为该user的口袋{"工具": ["衠钢槊"], "配饰": ["烂银甲"]}
def find_pocket(username,treasure):
    isok = get_treasure(treasure)#判断是否存在该treasure
    if ana(isok, 'ok'):
        one = session2.query(POCKET).filter(POCKET.tid == treasure and POCKET.uid == username).first()
        if one:
            return {"result": '宝物已在口袋中','one':one, "ok": 1}
        else:
            return {"result": '宝物未在口袋中', "ok": 0}
    else:
        return isok

# 删除某用户口袋中某宝物
def un_pocket(username,treasure):
    isok=get_treasure(treasure)#判断是否存在该treasure
    if ana(isok,'ok'):
        exist=find_pocket(username,treasure)#判断user是否有该treasure
        if ana(exist,'ok'):
            ana(exist,'one').num-=1
            if(ana(exist, 'one').num ==0):
                session2.delete(ana(exist, 'one'))
            return {"result": '口袋中宝物数量-1', "ok": 1}
        else:
            return {"result": '口袋中无该宝物，不能删除', "ok": 0}
    else:
        return isok


# 增加某用户口袋中某宝物
def add_pocket(username,treasure):
    isok=get_treasure(treasure)#判断是否存在该treasure
    if ana(isok,'ok'):
        check_pocket(username)
        exist=find_pocket(username,treasure)#判断user是否有该treasure
        if ana(exist,'ok'):
            ana(exist,'one').num+=1
        else:
            pocket1 = POCKET(uid=username, tid=treasure, num=1)
            session2.add(pocket1)
        return {"result": '宝物已进入口袋', "ok": 1}
    else:
        return isok

# 查看某用户佩戴中有无某宝物
def find_wear(username,treasure):
    isok = get_treasure(treasure)#判断是否存在该treasure
    if ana(isok, 'ok'):
        one = session2.query(WEAR).filter(WEAR.tid == treasure and WEAR.uid == username).first()
        if one:
            return {"result": '宝物佩戴着','one':one, "ok": 1}
        else:
            return {"result": '宝物没佩戴着', "ok": 0}
    else:
        return isok

# 撤回某用户佩戴中某宝物至口袋
def un_wear(username,treasure):
    isok=get_treasure(treasure,'property')#种类
    if ana(isok,'ok'):
        exist=find_wear(username,treasure)#判断user是否有该treasure
        if ana(exist,'ok'):
            gt =ana(isok)
            if(gt=='配饰'):
                ana(get_user(username,'lucky'),'one').lucky-=ana(get_treasure(treasure,'value'))
            elif(gt=='工具'):
                ana(get_user(username, 'workbase'), 'one').workbase -= ana(get_treasure(treasure, 'value'))*10
            ana(exist,'one').num-=1
            if(ana(exist, 'one').num ==0):
                session2.delete(ana(exist, 'one'))
            add_pocket(username, treasure)
            return {"result": '佩戴中宝物数量-1', "ok": 1}
        else:
            return {"result": '佩戴中无该宝物，不能删除', "ok": 0}
    else:
        return isok

# 从某用户口袋中佩戴某宝物
def add_wear(username,treasure):
    isok=get_treasure(treasure,'property')#种类
    if ana(isok,'ok'):
        f = un_pocket(username, treasure)
        if ana(f,'ok'):
            exist=find_wear(username,treasure)
            if ana(exist, 'ok'):
                check_wear(username,treasure)
                gt =ana(isok)
                if(gt=='配饰'):
                    ana(get_user(username,'lucky'),'one').lucky+=ana(get_treasure(treasure,'value'))
                elif(gt=='工具'):
                    ana(get_user(username, 'workbase'), 'one').workbase += ana(get_treasure(treasure, 'value'))*10
                ana(exist,'one').num+=1

            else:
                wear1 = WEAR(uid=username, tid=treasure, num=1)
                session2.add(wear1)
            return {"result": '佩戴中宝物数量+1', "ok": 1}
        else:
            return f
    else:
        return isok
    #lucky值为宝物value之和，在0-200之间，由于大多宝物value不高 所以寻宝不会很容易给找到好的 但是也必然有概率能爆到最好装备
    #lucky值用来调整（或说决定）正态分布的期望

#返回market当前信息
def get_market():#返回的直接是market列表！没有jsonify！
    for x in session2.query(MARKET).all():
        yield (x.seller,x.tid,x.price,x.num)
    # market=market.find_one({"name": treasure})
    # if one:
    #     return jsonify({"result":one[0][attr],"ok": 1})
    # else:
    #     return jsonify({"result":"宝物库中无该属性","ok": 0})
# #如果有返回最便宜的那个的_id 没有ok=0
# def check_market(goods):####买要买最便宜的 符合思想
#     the_find=market.find({"goods":goods})
#     try:
#         nouse=the_find[0]
#     except IndexError:
#         return jsonify({"result":"market无该goods","ok": 0})
#     else:
#         values=[]
#         for x in the_find:
#             values.append(x['value'])
#
#         get_id=the_find[values.index(min(values))]['_id']
#         return jsonify({"result":get_id,"ok": 1})#返回最便宜的那条的id

#看市场上到底有没有这条记录
def check_market_full(goods,price,sell):
    the_find=session2.query(MARKET).filter(MARKET.seller==sell and MARKET.tid==goods and MARKET.price==price).first()
    if not the_find:
        return {"result":"market无该商品记录","market":list(get_market()),'one':the_find,"ok": 0}
    else:
        return {"result":"market有该商品记录","market":list(get_market()),'one':the_find,"ok": 1}#返回最便宜的那条的id（不设计此功能了 因为会有玩家专门挑贵的买）
# 给market加一条信息
def add_market(goods,price,sell):
    one=check_market_full(goods,price,sell)
    if ana(one,'ok'):
        ana(one,'one').num+=1
    else:
        market1=MARKET(seller=sell,tid=goods,price=price,num=1)
        session2.add(market1)
    return {"result":'插入成功',"ok": 1}
# 给market删一条指定信息
def del_market(goods,price,sell):
    one=check_market_full(goods,price,sell)
    if ana(one,'ok'):
        ana(one,'one').num-=1
        if (ana(one,'one').num==0):
            session2.delete(ana(one,'one'))
        return {"result": "已从market中移除一条记录", "market": list(get_market()), "ok": 1}
    else:
        return {"result":'market无该商品记录',"market":list(get_market()),"ok": 0}
# 将一样物品从包中挂到市场
def sell(username,treasure,price):
    f = un_pocket(username, treasure)
    if ana(f, 'ok'):
        # wear = f['wear']
        # wear[ana(get_treasure(treasure,'property'))].append(treasure)
        # user.update_one({'name': username}, {'$set': wear})
        add_market(treasure, price, username)
        return {"result": '已将其挂到市场',
                        "market": list(get_market()), "ok": 1}
    else:
        return f

# 将一样物品从市场上收回回到包中
def back(username,treasure,price,sell):
    if(username==sell):
        gt = get_treasure(treasure, 'property')
        if ana(gt,'ok'):
            f=check_market_full(treasure,price,sell)
            if ana(f,'ok'):#市场上有没有这东西
                del_market(treasure,price,sell)
                add_pocket(username,treasure)
                return {"result": '已从市场上收回到包中',
                                    "market": list(get_market()), "ok": 1}
            else:
                return f
        else:
            return gt
    else:
        return {"result":'东西不是你的，不能撤回！' , "ok": 0}
# 买（金币会变）
def buy(username,treasure,price,sell):
    if(username!=sell):
        gt = get_treasure(treasure, 'property')
        if ana(gt,'ok'):
            f = check_market_full(treasure, price, sell)
            if ana(f,'ok'):#市场上有没有这东西
                theuser=ana(get_user(username, 'one'))
                theuser.money-=price
                if theuser.money>=0:
                    del_market(treasure,price,sell)
                    theseller = ana(get_user(sell, 'one'))
                    theseller.money += price
                    add_pocket(username,treasure)
                    return jsonify({"result": '购买成功', "market": list(get_market()), "ok": 1})
                else:
                    return jsonify({"result": '钱不够', "ok": 0})
            else:
                return f
        else:
            return gt
    else:
        x=back(username,treasure,price,sell)
        if ana(x,'ok'):
            return {"result":'撤回了自己的商品！' , "ok": 1}#买自己就是撤回商品
        else:
            return x
#看能不能换得枭雄金印，获得游戏胜利
def final(username):
    one=find_pocket(username,'束发紫金冠')
    if ana(one,'ok'):
        count=ana(one,'num')
        if (count >= 5):
            un_pocket(username,'束发紫金冠')
            un_pocket(username, '束发紫金冠')
            un_pocket(username, '束发紫金冠')
            un_pocket(username, '束发紫金冠')
            un_pocket(username, '束发紫金冠')
            add_pocket(username,'枭雄金印')
            return {"result": '恭喜您获得枭雄金印，游戏胜利！', "ok": 1}
        else:
            return {"result": '您只有'+str(count)+'个束发紫金冠，要五个才能换枭雄金印', "ok": 0}
    else:
        return {"result": '您没有束发紫金冠！', "ok": 0}
#工作
def to_work(username,work_flag):
    if (work_flag == 1):
        money0 = ana(get_user(username, 'money'))
        money = ana(get_user(username, 'money'))
        base=ana(get_user(username,'workbase'))
        if base!=0:
            print(base)
            ana(get_user(username),'one').money+= base + get_norm(username, -base / 3, base / 3, 0.7)  # 钱增加工具价值+（-工具价值至工具价值)/3区间的服从正态分布的随机值
        else:
            pass  # 不挂工具拿不到钱
        return {'result': '原来有钱{0},现在有钱{1}'.format(money0, money), 'ok': 1}
    else:
        return {'result': '您今天已经工作过', 'ok': 0}
#寻宝
def to_travel(username,travel_flag):
    from random import choice
    if (travel_flag == 1):
        # 得到宝物的level由lucky值决定 lucky值控制正态分布的期望
        level_num = get_norm(username, 1, 5, 0.7)  # 得到武器level的评级
        map_ = {1: '普通', 2: '稀有', 3: '史诗', 4: '传说', 5: '限定'}
        print('level_num', level_num)
        print('map_[level_num]', map_[level_num])
        # 决定获得配饰还是工具 0是工具1是配饰
        import random
        rd = random.randint(0, 1)
        if (rd == 0):  # 工具
            whatget=choice([x for x in session2.query(TREASURE.name).filter(TREASURE.property=='工具' and TREASURE.level==map_[level_num]).all()]).name
            add_pocket(username, whatget)
        else:  # 配饰
            whatget=choice([x for x in session2.query(TREASURE.name).filter(TREASURE.property=='配饰' and TREASURE.level==map_[level_num]).all()]).name
            add_pocket(username, whatget)
        return {'result': whatget, 'level': map_[level_num], 'ok': 1}
    else:
        return {'result': '您今天已经寻宝过', 'ok': 0}
def change_mu(username,lower,upper):#lucky值用来调整（或说决定）正态分布的期望
    lucky=ana(get_user(username,'lucky'))
    return lower+float(lucky)/200*(upper-lower)
#最小，最大，期望，标准差 生成近似在某区间内正态的整数值
def get_norm(username,lower, upper, sigma=0.7):
    mu=change_mu(username,lower,upper)
    import scipy.stats as stats
    x=lower-1
    while not((x>lower) & (x<upper)):#由于正态分布其实是朝着无穷延伸的 所以难免有越界的地方 去了就是
        #上面不加括号你试试
        X = stats.truncnorm(
        (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
        N = stats.norm(loc=mu, scale=sigma)
        x=N.rvs(1)[0]
    return(round(x))

###

#查看属性
#修改属性
#




# dbadd()
# dbfind()
# dbchange()
# dbselect()
# print(change_user('mk','money','200'))
#提交即保存到数据库
session2.commit()
#关闭session
session2.close()