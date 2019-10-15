import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo.errors import BulkWriteError

client = MongoClient('localhost', 27017)
treasures = client.web.treasures


treasure_test = [{"name": "青龙偃月刀", "property": "T", "level": 10, "price": 500},
                {"name": "斩蛇剑", "property": "T", "level": 9, "price": 450},
                {"name": "干将剑", "property": "T", "level": 8, "price": 400},
                {"name": "倚天剑", "property": "T", "level": 7, "price": 350},
                {"name": "莫邪剑", "property": "T", "level": 6, "price": 300},
                {"name": "七星宝剑", "property": "T", "level": 5, "price": 250},
                {"name": "青虹剑", "property": "T", "level": 4, "price": 200},
                {"name": "雌雄一对剑", "property": "T", "level": 3, "price": 150},
                {"name": "宝剑", "property": "T", "level": 2, "price": 100},
                {"name": "宝刀", "property": "T", "level": 1, "price": 50},
                {"name": "黄玉", "property": "A", "level": 10, "price": 500},
                {"name": "碧玉", "property": "A", "level": 9, "price": 450},
                {"name": "青玉", "property": "A", "level": 8, "price": 400},
                {"name": "红玉", "property": "A", "level": 7, "price": 350},
                {"name": "玛瑙", "property": "A", "level": 6, "price": 300},
                {"name": "翡翠", "property": "A", "level": 5, "price": 250},
                {"name": "珍珠", "property": "A", "level": 4, "price": 200},
                {"name": "衽露", "property": "A", "level": 3, "price": 150},
                {"name": "金耳环", "property": "A", "level": 2, "price": 100},
                {"name": "罗伊香囊", "property": "A", "level": 1, "price": 50},
                 ]
treasures.create_index([("name", pymongo.ASCENDING)], unique=True)
try:
    treasures.insert_many(treasure_test)
except BulkWriteError:
    print("重复初始化")
