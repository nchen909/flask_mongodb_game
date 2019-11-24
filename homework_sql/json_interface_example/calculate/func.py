#!/usr/bin/env python3

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import redirect,session
import sys

import hashlib
import urllib.parse
bp = Blueprint("mul", __name__, url_prefix="/user")
# client = MongoClient('localhost', 27017)
# user = client.game.user
# user.create_index([("name", ASCENDING)], unique=True)
# #user name money pocket lucky wear
# market = client.game.market
# treasures = client.game.treasure
# info=client.game.info
# info.create_index([("username", ASCENDING)], unique=True)#按用户名建立索引

MAX_POCKET=10#袋子里工具或配饰最多为10个
MAX_GJ=1 #佩戴工具最多为1个
MAX_PS=2 #佩戴配饰最多为2个
##################最终目的是合成 枭雄金印 ，return游戏成功

# 解析flask.wrappers.Response中包裹的字典,传入Response及需要的属性 返回对应值
def ana(response_,value='result'):
    return eval(str(response_.data, encoding = "utf-8"))[value]
# 获取用户的某个属性
def get_user(username,attr):
    one=user.find_one({"name": username})
    try:
        return jsonify({"result":one[attr],"ok": 1})
    except KeyError:
        return jsonify({"result":"用户无该属性","ok": 0})

# 修改用户的某个属性
def change_user(username,attr,new_attr):
    if ana(get_user(username,attr),'ok'):
        user.update_one({'name': username}, {'$set': {attr: new_attr}})
        return jsonify({"result":'修改用户属性成功',"ok": 1})
    else:
        return get_user(username,attr)
# 获取宝物的某个属性
def get_treasure(treasure,attr):
    one=treasures.find_one({"name": treasure})
    if one:
        return jsonify({"result":one[attr],"ok": 1})
    else:
        return jsonify({"result":"宝物库中无该属性","ok": 0})

#如果pocket满了就把最便宜的那个先换成钱 然后丢掉 不然不动
def check_pocket(username,the_property):
    pocket=ana(get_user(username,'pocket'))
    bws=pocket[the_property]
    print('check_pocket', bws,len(bws))
    if (len(bws)==MAX_POCKET):
        values=[]
        for i in range(MAX_POCKET):
            values.append(ana(get_treasure(bws[i],'value')))
        money=ana(get_user(username,'money'))
        money+=ana(get_treasure(bws[values.index(min(values))],'value'))*10
        change_user(username,'money',money)#丢掉的要换钱
        pocket[the_property].pop(values.index(min(values)))
        change_user(username,'pocket',pocket)
    return
#如果宝物带满了就把最便宜的那个拆下来 不然不动
def check_wear(username,the_property):
    wear = ana(get_user(username, 'wear'))
    gjs = wear[the_property]
    if the_property=='工具':
        print('check_wear',gjs,len(gjs))
        if (len(gjs) == MAX_GJ):
            values = []
            for i in range(MAX_GJ):
                values.append(ana(get_treasure(gjs[i], 'value')))
            print(wear[the_property])
            add_pocket(username,wear[the_property][values.index(min(values))])
            wear[the_property].pop(values.index(min(values)))
            print(wear[the_property])
            print(wear)
            change_user(username, 'wear', wear)

    elif the_property=='配饰':
        print('check_wear', gjs,len(gjs))
        if (len(gjs) == MAX_PS):
            values = []
            for i in range(MAX_PS):
                values.append(ana(get_treasure(gjs[i], 'value')))
            print(wear[the_property])
            add_pocket(username,wear[the_property][values.index(min(values))])
            wear[the_property].pop(values.index(min(values)))
            print(wear[the_property])
            print(wear)
            change_user(username, 'wear', wear)
    return
# 查看某用户口袋中有无某宝物 有则result为宝物property pocket为该user的口袋{"工具": ["衠钢槊"], "配饰": ["烂银甲"]}
def find_pocket(username,treasure):
    gt=get_treasure(treasure,'property')#获得宝物属性字典
    if ana(gt,'ok'):
        # user_ = user.find_one({"name": username})
        # pocket = user_[0]['pocket']
        # pocket1 = pocket['工具']
        # pocket2 = pocket['配饰']
        # if treasure in pocket1:
        #     return jsonify({"result": '工具','pocket':pocket, "ok": 1})
        # elif treasure in pocket2:
        #     return jsonify({"result": '配饰','pocket':pocket, "ok": 1})
        # else:
        #     return jsonify({"result": '口袋中无该宝物', "ok": 0})
        f=get_user(username,'pocket')
        if ana(f,'ok'):
            the_property = ana(gt)
            pocket=ana(f)[the_property]
            if treasure in pocket:
                return jsonify({"result": '口袋中有该宝物', "ok": 1})
            else:
                return jsonify({"result": '口袋中无该宝物', "ok": 0})
            # return jsonify({"result": treasure,'pocket':pocket, "ok": 1})

        else:
            return f
    else:
        return gt
# 查看某用户on_market中有无某宝物 有则result为宝物property pocket为该user的口袋{"工具": ["衠钢槊"], "配饰": ["烂银甲"]}
def find_onmarket(username,treasure):
    gt = get_treasure(treasure, 'property')  # 获得宝物属性字典
    if ana(gt,'ok'):
        if ana(get_user(username, 'onmarket'),'ok'):
            the_property = ana(gt)
            onmarket = ana(get_user(username, 'onmarket'))[the_property]
            if treasure in onmarket:
                return jsonify({"result": '有该物品挂于市场', "ok": 1})
            else:
                return jsonify({"result": '无该物品挂于市场', "ok": 0})
            # return jsonify({"result": treasure,'pocket':pocket, "ok": 1})
        else:
            return get_user(username, 'onmarket')
    else:
        return gt
# 删除某用户口袋中某宝物
def un_pocket(username,treasure):
    gt=get_treasure(treasure,'property')
    if ana(gt,'ok'):
        f = find_pocket(username, treasure)
        if ana(f,'ok'):
            # pocket = f['pocket']
            # pocket[ana(f)].remove(treasure)
            # user.update_one({'name': username}, {'$set': {'pocket':pocket}})
            # return jsonify({"result": '宝物已从口袋中删除', "ok": 1})
            the_property = ana(gt)
            print('the_property',the_property)
            pocket=ana(get_user(username,'pocket'))
            print('pocket', pocket)
            pocket[the_property].remove(treasure)
            print('pocket', pocket)
            change_user(username,'pocket',pocket)
            return jsonify({"result": '宝物已从口袋中删除', "ok": 1})
        else:
            return f
    else:
        return gt
# 删除某用户onmarket中某宝物
def un_onmarket(username,treasure):
    gt=get_treasure(treasure,'property')
    if ana(gt,'ok'):
        f = find_onmarket(username, treasure)
        if ana(f,'ok'):
            # pocket = f['pocket']
            # pocket[ana(f)].remove(treasure)
            # user.update_one({'name': username}, {'$set': {'pocket':pocket}})
            # return jsonify({"result": '宝物已从口袋中删除', "ok": 1})
            the_property = ana(gt)
            onmarket=ana(get_user(username,'onmarket'))
            onmarket[the_property].remove(treasure)
            change_user(username,'onmarket',onmarket)
            return jsonify({"result": '宝物已从onmarket中删除', "ok": 1})
        else:
            return f
    else:
        return gt
# 增加某用户口袋中某宝物
def add_pocket(username,treasure):
    gt=get_treasure(treasure,'property')
    if ana(gt,'ok'):
        # user_ = user.find_one({"name": username})
        # pocket = user_[0]['pocket']
        # the_property=ana(get_treasure(treasure,'property'))
        # pocket[the_property].append(treasure)
        # user.update_one({'name': username}, {'$set': {'pocket':pocket}})
        the_property = ana(gt)

        check_pocket(username,the_property)#满了得删一个再放到袋子
        pocket = ana(get_user(username, 'pocket'))
        pocket[the_property].append(treasure)
        change_user(username, 'pocket', pocket)
        return jsonify({"result": '宝物已进入口袋', "ok": 1})
    else:
        return gt
# 增加某用户on_market中某宝物
def add_onmarket(username,treasure):
    gt=get_treasure(treasure,'property')
    if ana(gt,'ok'):
        # user_ = user.find_one({"name": username})
        # pocket = user_[0]['pocket']
        # the_property=ana(get_treasure(treasure,'property'))
        # pocket[the_property].append(treasure)
        # user.update_one({'name': username}, {'$set': {'pocket':pocket}})
        the_property = ana(gt)
        onmarket = ana(get_user(username, 'onmarket'))
        onmarket[the_property].append(treasure)
        change_user(username, 'onmarket', onmarket)
        return jsonify({"result": '宝物已进入onmarket', "ok": 1})
    else:
        return gt
# 查看某用户佩戴中有无某宝物
def find_wear(username,treasure):
    gt = get_treasure(treasure, 'property')
    if ana(gt,'ok'):
        # user_ = user.find_one({"name": username})
        # wear = user_[0]['wear']
        # wear1 = wear['工具']
        # wear2 = wear['配饰']
        # if treasure in wear1:
        #     return jsonify({"result": '工具', 'pocket': wear, "ok": 1})
        # elif treasure in wear2:
        #     return jsonify({"result": '配饰', 'pocket': wear, "ok": 1})
        # else:
        #     return jsonify({"result": '佩戴中无该宝物', "ok": 0})
        if ana(get_user(username,'wear'),'ok'):
            # pocket=ana(get_user(username, 'pocket'))
            # treasure=ana(gt)
            # return jsonify({"result": treasure,'pocket':pocket, "ok": 1})
            if treasure in ana(get_user(username,'wear'))[ana(gt)]:
                return jsonify({"result": '有佩戴该宝物',"wear":ana(get_user(username, 'wear')),"pocket":ana(get_user(username, 'pocket')), "ok": 1})
            else:
                return jsonify({"result": '没有佩戴该宝物', "wear": ana(get_user(username, 'wear')),
                                "pocket": ana(get_user(username, 'pocket')), "ok": 0})
        else:
            return get_user(username,'wear')
    else:
        return gt

# 撤回某用户佩戴中某宝物至口袋
def un_wear(username,treasure):
    gt = get_treasure(treasure, 'property')
    if ana(gt,'ok'):
        f = find_wear(username, treasure)
        if ana(f,'ok'):
            # wear = f['wear']
            # wear[ana(f)].remove(treasure)
            # user.update_one({'name': username}, {'$set': {'wear':'wear'}})
            the_property=ana(gt)
            wear=ana(get_user(username,'wear'))
            wear[the_property].remove(treasure)
            if the_property=='配饰':
                lucky=ana(get_user(username,'lucky'))
                lucky-=ana(get_treasure(treasure,'value'))
                change_user(username, 'lucky', lucky)
            change_user(username,'wear',wear)
            check_pocket(username, the_property)  # 满了得删一个再放到袋子
            add_pocket(username, treasure)
            if the_property == '工具':
                return jsonify({"result": '撤回成功，宝物已从佩戴中回到口袋',"wear":ana(get_user(username, 'wear')),"pocket":ana(get_user(username, 'pocket')) ,
                            "ability":"工作能力基准下降至{0}".format(sum(list(map(lambda x:ana(get_treasure(x,'value')),ana(get_user(username,'wear'))['工具'])))*10),"ok": 1})
            elif the_property=='配饰':
                return jsonify({"result": '撤回成功，宝物已从佩戴中回到口袋',"wear":ana(get_user(username, 'wear')),"pocket":ana(get_user(username, 'pocket')) ,
                            "lucky":"运气下降至{0}".format(ana(get_user(username,'lucky'))),"ok": 1})
            #return jsonify({"result": '撤回成功，宝物已从佩戴中回到口袋',"wear":ana(get_user(username, 'wear')),"pocket":ana(get_user(username, 'pocket')), "ok": 1})
        else:
            return f
    else:
        return gt


# 从某用户口袋中佩戴某宝物
def add_wear(username,treasure):
    #lucky值为宝物value之和，在0-200之间，由于大多宝物value不高 所以寻宝不会很容易给找到好的 但是也必然有概率能爆到最好装备
    #lucky值用来调整（或说决定）正态分布的期望
    gt = get_treasure(treasure, 'property')
    if ana(gt,'ok'):
        f = un_pocket(username, treasure)
        if ana(f,'ok'):
            # wear = f['wear']
            # wear[ana(get_treasure(treasure,'property'))].append(treasure)
            # user.update_one({'name': username}, {'$set': wear})
            the_property = ana(gt)

            if the_property=='配饰':
                lucky=ana(get_user(username,'lucky'))
                lucky+=ana(get_treasure(treasure,'value'))
                change_user(username, 'lucky', lucky)
            check_wear(username, the_property)  # 满了得删一个再装
            wear = ana(get_user(username, 'wear'))
            wear[the_property].append(treasure)
            change_user(username, 'wear', wear)
            if the_property == '工具':
                return jsonify({"result": '已从口袋中佩戴上',"wear":ana(get_user(username, 'wear')),"pocket":ana(get_user(username, 'pocket')) ,
                            "ability":"工作能力基准提升至{0}".format(sum(list(map(lambda x:ana(get_treasure(x,'value')),ana(get_user(username,'wear'))['工具'])))*10),"ok": 1})
            elif the_property=='配饰':
                return jsonify({"result": '已从口袋中佩戴上',"wear":ana(get_user(username, 'wear')),"pocket":ana(get_user(username, 'pocket')) ,
                            "lucky":"运气提升至{0}".format(ana(get_user(username,'lucky'))),"ok": 1})
        else:
            return f
    else:
        return gt
#返回market当前信息
def get_market():#返回的直接是market列表！没有jsonify！
    for x in market.find({},{'_id':0}):
        yield str(x)
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
    the_find=market.find({"goods": goods,"price":price,"sell":sell})
    try:
        print(the_find[0]['goods'])
    except IndexError:
        return jsonify({"result":"market无该商品记录","market":list(get_market()),"ok": 0})
    else:
        return jsonify({"result":"market有该商品记录","market":list(get_market()),"ok": 1})#返回最便宜的那条的id（不设计此功能了 因为会有玩家专门挑贵的买）
# 给market加一条信息
def add_market(goods,price,sell):
    market.insert_one({"goods":goods, "price":price, "sell": sell})
    return jsonify({"result":'插入成功',"ok": 1})
# 给market删一条指定信息
def del_market(goods,price,sell):
    the_find=market.find({"goods": goods, "price":price, "sell": sell})
    try:
        nouse=the_find[0]
    except IndexError:
        return jsonify({"result":"market无该商品记录","market":list(get_market()),"ok": 0})#找不到得让用户看一眼market
    else:
        market.delete_one({"goods":goods, "price":price, "sell": sell})
        return jsonify({"result": "该商品已从market中移除","market":list(get_market()), "ok": 1})
# 将一样物品从包中挂到市场
def sell(username,treasure,price):
    gt = get_treasure(treasure, 'property')
    if ana(gt,'ok'):
        f = un_pocket(username, treasure)
        if ana(f,'ok'):
            # wear = f['wear']
            # wear[ana(get_treasure(treasure,'property'))].append(treasure)
            # user.update_one({'name': username}, {'$set': wear})
            add_onmarket(username,treasure)
            add_market(treasure,price,username)
            return jsonify({"result": '已将其挂到市场', "pocket": ana(get_user(username, 'pocket')),
                            "market": list(get_market()), "ok": 1})
        else:
            return f
    else:
        return gt
# 将一样物品从市场上收回回到包中
def back(username,treasure,price,sell):
    if(username==sell):
        gt = get_treasure(treasure, 'property')
        if ana(gt,'ok'):
            f=check_market_full(treasure,price,sell)
            if ana(f,'ok'):#市场上有没有这东西
                del_market(treasure,price,sell)
                un_onmarket(username,treasure)
                add_pocket(username,treasure)
                return jsonify({"result": '已从市场上收回到包中', "pocket": ana(get_user(username, 'pocket')),
                                "onmarket": ana(get_user(username, 'onmarket')),
                                    "market": list(get_market()), "ok": 1})
            else:
                return f
        else:
            return gt
    else:
        return jsonify({"result":'东西不是你的，不能撤回！' , "ok": 0})
# 买（金币会变）
def buy(username,treasure,price,sell):
    if(username!=sell):
        gt = get_treasure(treasure, 'property')
        if ana(gt,'ok'):
            f = check_market_full(treasure, price, sell)
            if ana(f,'ok'):#市场上有没有这东西
                money_buy = ana(get_user(username, 'money'))
                money_buy -= price
                if money_buy>=0:
                    del_market(treasure,price,sell)
                    un_onmarket(sell,treasure)
                    money_sell=ana(get_user(sell,'money'))
                    money_sell+=price
                    change_user(sell,'money',money_sell)
                    add_pocket(username,treasure)
                    change_user(username, 'money', money_buy)
                    return jsonify({"result": '购买成功', "pocket": ana(get_user(username, 'pocket')),
                                        "market": list(get_market()), "ok": 1})
                else:
                    return jsonify({"result": '钱不够', "money": ana(get_user(username, 'pocket')), "ok": 0})
            else:
                return f
        else:
            return gt
    else:
        x=back(username,treasure,price,sell)
        if ana(x,'ok'):
            return jsonify({"result":'撤回了自己的商品！' , "ok": 1})#买自己就是撤回商品
        else:
            return x
#看能不能换得枭雄金印，获得游戏胜利
def final(username):
    gp=get_user(username, 'pocket')
    if ana(gp,'ok'):
        x=ana(get_user(username, 'pocket'))
        ps=x['配饰']
        count=ps.count('束发紫金冠')
        if (count>=5):
            un_pocket(username,'束发紫金冠')
            un_pocket(username, '束发紫金冠')
            un_pocket(username, '束发紫金冠')
            un_pocket(username, '束发紫金冠')
            un_pocket(username, '束发紫金冠')
            add_pocket(username,'枭雄金印')
            return jsonify({"result":'恭喜您获得枭雄金印，游戏胜利！' , "ok": 1})
        else:
            return jsonify({"result": '您只有'+str(count)+'个束发紫金冠，要五个才能换枭雄金印', "ok": 0})
    else:
        return get_user(username,'pocket')
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