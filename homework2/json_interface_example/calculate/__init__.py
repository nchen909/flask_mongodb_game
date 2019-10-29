#!/usr/bin/env python3
#连接数据库
from pymongo import ASCENDING
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo.errors import BulkWriteError

MAXINT=2147483647
# client = MongoClient('localhost', 27017)
#client=MongoClient('mongodb+srv://mathskiller:11111111qQ@flaskgame-aoyhi.mongodb.net/test')
client=MongoClient('mongodb+srv://mathskiller:11111111qQ@flaskgame-aoyhi.mongodb.net/test?retryWrites=true&w=majority')
mydb = client["game"]
mycol = mydb["treasure"]


name=['青龙偃月刀','诸葛连弩','雌雄双股剑','青红剑','丈八蛇矛','贯石斧','方天画戟','麒麟弓','寒冰剑','古锭刀','朱雀羽扇','三尖两刃刀','七宝刀','银月枪','衠钢槊']
name2=['藤甲','白银狮子','八卦阵','仁王盾','束发紫金冠','玲珑狮蛮带','红锦百花袍','木牛流马','烂银甲','护心镜']
value=[35,60,5,20,40,100,9,2,20,45,15,55,25,50,1]
value2=[60,20,30,45,100,70,85,10,1,7]
#普通稀有史诗传说限定
level=[2,4,1,2,3,5,1,1,2,3,1,4,2,4,1]
level2=[4,2,2,3,5,4,4,1,1,1]
map_={1:'普通',2:'稀有',3:'史诗',4:'传说',5:'限定'}
#终极目标获得终极
treasure_list=[]
for i in range(len(name)):
    treasure_list.append({"name":name[i],"property": "工具","value":value[i],"level":map_[level[i]]})
for i in range(len(name2)):
    treasure_list.append({"name": name2[i], "property": "配饰", "value": value2[i], "level": map_[level2[i]]})

mycol.create_index([("name", ASCENDING)], unique=True)#按名字建立索引

try:
    mycol.insert_many(treasure_list)
except BulkWriteError:
    print("已创建过宝物")

#枭雄金印不可通过购买 寻宝等获得，只能最终通过5个束发紫金冠去换 （游戏终极目标）
try:
    mycol.insert_one({"name": '枭雄金印', "property": "配饰", "value": MAXINT, "level": '终极'})
except DuplicateKeyError:
    print("已创建过最强配饰：枭雄金印")