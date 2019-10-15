import os
import random
import sys
from flask import Flask
from flask_apscheduler import APScheduler
from pymongo import MongoClient
from action.opt import bp
from action.opt import recovery_treasure



file_dir = os.path.dirname(__file__)    #
sys.path.append(file_dir)   #

client = MongoClient('localhost', 27017)
players = client.web.players
markets = client.web.markets
treasures = client.web.treasures


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:hunt',
            'trigger': 'cron',
            'second': 5,
        },
        {
            'id': 'job2',
            'func': '__main__:labour',
            'trigger': 'cron',
            'second': 5,
        }
    ]


def hunt():
    for player in players.find():
        name = player["name"]
        box = player['box']
        if len(box) >= 10:
            print("存储箱已满,执行系统回收")
            recovery_treasure(name)
        wear_treasure_name = player['treasure']['A']
        wear_treasure_level = treasures.find_one({"name": wear_treasure_name})['level']
        hunted = list(treasures.find({"level": {"&lt":wear_treasure_level+2, "&mt":wear_treasure_level-2}}))[0]['name']   # 寻宝随机性
        box.append(hunted)
        players.update_one({"name": name}, {"$set": {"box": box}})
        print("寻找到宝物 %s" % hunted['name'])

def labour():

    print("劳动时间")


if __name__ == "__main__":
    app = Flask(__name__)
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.register_blueprint(bp)
    app.run(debug=True)