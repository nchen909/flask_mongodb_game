
## 游戏
简陋的游戏前端链接：[mathskiller909.com/game](https://mathskiller909.com/game) 
（若内容与游戏不同，可以通过[http://47.101.151.73:4999/](http://47.101.151.73:4999/)进入）
上云代码在分支tocloud

mongodb及sql实现游戏
### 游戏内容
考虑以下游戏场景：
1.   每个游戏玩家都有一定数量的金币、宝物。有一个市场供玩家们买卖宝物。玩家可以将宝物放到市场上挂牌，自己确定价格。其他玩家支付足够的金币，可购买宝物。
2.   宝物分为两类：一类为工具，它决定持有玩家的工作能力；一类为配饰，它决定持有玩家的运气。
3.   每位玩家每天可以通过寻宝获得一件宝物，宝物的价值由玩家的运气决定。每位玩家每天可以通过劳动赚取金币，赚得多少由玩家的工作能力决定。（游戏中的一天可以是现实中的1分钟、5分钟、10分钟。自主设定。）
4.   每个宝物都有一个自己的名字（尽量不重复）。每位玩家能够佩戴的宝物是有限的（比如一个玩家只能佩戴一个工具和两个配饰）。多余的宝物被放在存储箱中，不起作用，但可以拿到市场出售。
5.   在市场上挂牌的宝物必须在存储箱中并仍然在存储箱中，直到宝物被卖出。挂牌的宝物可以被收回，并以新的价格重新挂牌。当存储箱装不下时，运气或工作能力值最低的宝物将被系统自动回收。
6.   假设游戏永不停止而玩家的最终目的是获得最好的宝物。
 一个假想的Web游戏，可供多人在线上玩耍。界面尽可能简单。对游戏玩家提供以下几种操作：寻宝（可以自动每天一次）、赚钱（可以自动每天一次）、佩戴宝物、浏览市场、买宝物、挂牌宝物、收回宝物。

### mongodb

报告位于 [数据库游戏实验报告](https://github.com/1012598167/flask_mongodb_game/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93%E6%B8%B8%E6%88%8F%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.md "\数据库游戏实验报告.md")

有用的程序在 [homework2](https://github.com/1012598167/flask_mongodb_game/tree/master/homework2/json_interface_example "\homework2")

运行说明在[README.md](https://github.com/1012598167/flask_mongodb_game/blob/master/homework2/json_interface_example/README.md "\homework2\json_interface_example\README.md")

### postgresql

报告位于 [数据库游戏实验报告](https://github.com/1012598167/flask_mongodb_game/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93%E6%B8%B8%E6%88%8F%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8Asqlgame.md "\数据库游戏实验报告.md")

有用的程序在 [homework_sql](https://github.com/1012598167/flask_mongodb_game/tree/master/homework_sql/json_interface_example "\homework2")

运行说明在[README.md](https://github.com/1012598167/flask_mongodb_game/blob/master/homework2/json_interface_example/README.md "\homework2\json_interface_example\README.md")

## 期末在线bookstore购物系统
项目链接：https://github.com/1012598167/bookstore ,购物链接：[mathskiller909.com/taobao](https://mathskiller909.com/taobao) 
（若内容与购物系统不同，可以通过[http://47.101.151.73:5001/auth/login](http://47.101.151.73:5001/auth/login)进入）

### 项目内容（使用posegresql）
一个提供网上购书功能的网站后端。
网站支持书商在上面开商店，购买者可能通过网站购买。
买家和买家都可以注册自己的账号。
一个买家可以开一个或多个网上商店， 买家可以为自已的账户充值，在任意商店购买图书。
支持下单->付款->发货->收货，流程。
1. 对应接口的功能  
其中包括：  
1)用户权限接口，如注册、登录、登出、注销  
2)买家用户接口，如充值、下单、付款  
3)卖家用户接口，如创建店铺、填加书籍信息及描述、增加库存  
2. 其它功能  
1)实现后续的流程  
发货 -> 收货  
2)搜索图书  
用户可以通过关键字搜索，参数化的搜索方式； 如搜索范围包括，题目，标签，目录，内容；全站搜索或是当前店铺搜索。 如果显示结果较大，需要分页 (使用全文索引优化查找)  
3)订单状态，订单查询和取消定单  
用户可以查自已的历史订单，用户也可以取消订单。  
取消定单，买家主动地取消定单，如果买家下单经过一段时间超时后，如果买家未付款，定单也会自动取消。  

### 存在问题
班上作业存在使用数据库的普遍问题：
1. 在失败路径上不回滚事务，也不关闭连接，事务会一直在idle in transaction状态，数据库的连接很快用光
2. 应用和数据库仅创建一个连接，从头用到尾，数据库没有并发（见connection pool）
3. 仅把写操作放在事务块里，读却没有（无该问题）
4. 格式化用户参数字符串拼SQL，有SQL注入问题（见prepared sql and dynamic sql）

## 课程实验报告
sql及之后所有实验报告位于[见该链接文件夹下的那些“实验报告.md”](https://github.com/1012598167/flask_mongodb_game/tree/master/Database-master)
