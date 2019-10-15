import sys
from flask import Blueprint
from flask import jsonify
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import pymongo
from flask import request

bp = Blueprint("opt", __name__, url_prefix="/opt")
client = MongoClient('localhost', 27017)
players = client.web.players
players.create_index([("name", pymongo.ASCENDING)], unique=True)
markets = client.web.markets
treasures = client.web.treasures


@bp.route("/login/<string:username>", methods=['GET'])
def login(username):
    try:
       post_id = players.insert_one({"name": username, "money": 1000,
                                  "treasure": {"T": "宝刀", "A": "黄玉"},
                                  "box": []}).inserted_id
    except DuplicateKeyError:
        return "用户名已存在"
    return players.find_one({"_id": post_id})


@bp.route("/json", methods=["POST"])
def opt_post():
    return 0


@bp.route("/<string:username>/wear/<string:treasure>", methods=['GET'])
def wear(username, treasure):
    trea_class = treasures.find_one({"name": treasure})['property']
    ori = players.find_one({"name": username})["treasure"][trea_class]

    flag = 0
    box = players.find_one({'name': username})['box']
    player_treasure = players.find_one({"name": username})["treasure"]
    for trea in box:
        if trea == treasure:
            box.remove(trea)
            box.append(ori)
            player_treasure[trea_class] = treasure
            players.update_one({"name":username}, {"$set": {treasure: player_treasure}})
            flag = 1
    if flag == 0:
        return "存储箱没有该宝物"


@bp.route("/market", methods=['GET'])
def look_market():
    res = ''
    for treasure in markets.find():
        res += str(treasure)
        res += '\n'
    return jsonify(res)


@bp.route("/<string:username>/buy/<string:treasure>", methods=['GET'])
def buy(username, treasure):
    player = players.find_one({"name": username})
    # 宝物到位
    box1 = player['box']
    if len(box1) >= 10:
        recovery_treasure(username)
    box = player['box']
    box.append(treasure)
    players.update_one({"name": username}, {"$set", {"box": box}})
    # 买家钱到位
    treasure_money = treasures.find_one({"name":treasure})['price']
    money1 = player['money'] - treasure_money
    players.update_one({"name": username}, {"$set", {"money": money1}})
    # 卖家钱到位
    of = markets.find_one({"name": treasure})['of']
    money2 = players.find_one({"name": of})['money'] + treasure_money
    players.update_one({"name": of}, {"$set", {"money": money2}})
    # 市场删除该宝物
    markets.delete_one({"name": treasure})
    return "购买成功，金币余额 %d" % money1


@bp.route("/<string:username>/sell/<string:treasure>/<int:price>", methods=['GET'])
def sell(username, treasure, price):
    player = players.find_one({"name": username})
    # 卖家宝物到位
    box = player['box']
    for trea in box:
        if trea == treasure:
            box.remove(trea)
            break
    # 市场宝物到位
    markets.insert_one({"name": treasure, "price": price, "of": username})
    return "挂牌"







def recovery_treasure(name):
    box = players.find_one({"name": name})['box']
    treasure_name = box[0]
    level = treasures.find_one({"name": box[0]})['level']
    for treasure in box[1:]:
        temp = treasures.find_one({"name": treasure})['level']
        if temp < level:
            level = temp
            treasure_name = treasure
    for treasure in box:
        if treasure == treasure_name:
            box.remove(treasure)
            break
    players.update_one({'name': name}, {"$set": {"box": box}})
    print("回收成功")



