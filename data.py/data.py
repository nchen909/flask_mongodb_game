import pymongo

myclient = pymongo.MongoClient()
mydb = myclient["homework1"]
mycol = mydb['treasure']

userdcict = {"name":"靓仔三号",
        "password":"123",
        "luck":50,
        "ability":50,
        "money":0,
        "ornament":[],
        "kit":[],
        "treasure":[],
        "wearing_orn":"none",
        "wearing_kit":[]}


stuffdict = {"name":"曹汇杰的智慧",
            "owner":"靓仔一号",#内嵌成一个数组
            "on_market":0
            }



marketdict = {"name":"菜闻宇的JAVA",
            "seller":"靓仔一号",
            "price":10000
            }


treasuredict = {"name":"叶晴远的仓鼠",
            "rank":0,
            "type":0,
            "gain":100
            }