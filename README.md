简陋的游戏前端链接：[noname.asia](noname.asia) (ssl证书暂有些问题,不过http可以访问，请见谅)
上云代码在分支tocloud

mongodb及sql实现游戏

考虑以下游戏场景：

\1.   每个游戏玩家都有一定数量的金币、宝物。有一个市场供玩家们买卖宝物。玩家可以将宝物放到市场上挂牌，自己确定价格。其他玩家支付足够的金币，可购买宝物。

\2.   宝物分为两类：一类为工具，它决定持有玩家的工作能力；一类为配饰，它决定持有玩家的运气。

\3.   每位玩家每天可以通过寻宝获得一件宝物，宝物的价值由玩家的运气决定。每位玩家每天可以通过劳动赚取金币，赚得多少由玩家的工作能力决定。（游戏中的一天可以是现实中的1分钟、5分钟、10分钟。自主设定。）

\4.   每个宝物都有一个自己的名字（尽量不重复）。每位玩家能够佩戴的宝物是有限的（比如一个玩家只能佩戴一个工具和两个配饰）。多余的宝物被放在存储箱中，不起作用，但可以拿到市场出售。

\5.   在市场上挂牌的宝物必须在存储箱中并仍然在存储箱中，直到宝物被卖出。挂牌的宝物可以被收回，并以新的价格重新挂牌。当存储箱装不下时，运气或工作能力值最低的宝物将被系统自动回收。

\6.   假设游戏永不停止而玩家的最终目的是获得最好的宝物。

 一个假想的Web游戏，可供多人在线上玩耍。界面尽可能简单（简单文字和链接即可，不需要style）。对游戏玩家提供以下几种操作：寻宝（可以自动每天一次）、赚钱（可以自动每天一次）、佩戴宝物、浏览市场、买宝物、挂牌宝物、收回宝物。



mongodb

报告位于 [数据库游戏实验报告](https://github.com/1012598167/flask_mongodb_game/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93%E6%B8%B8%E6%88%8F%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.md "\数据库游戏实验报告.md")

有用的程序在 [homework2](https://github.com/1012598167/flask_mongodb_game/tree/master/homework2/json_interface_example "\homework2")

运行说明在[README.md](https://github.com/1012598167/flask_mongodb_game/blob/master/homework2/json_interface_example/README.md "\homework2\json_interface_example\README.md")

postgresql

报告位于 [数据库游戏实验报告](https://github.com/1012598167/flask_mongodb_game/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93%E6%B8%B8%E6%88%8F%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8Asqlgame.md "\数据库游戏实验报告.md")

有用的程序在 [homework_sql](https://github.com/1012598167/flask_mongodb_game/tree/master/homework_sql/json_interface_example "\homework2")

运行说明在[README.md](https://github.com/1012598167/flask_mongodb_game/blob/master/homework2/json_interface_example/README.md "\homework2\json_interface_example\README.md")

sql及之后所有实验报告位于[见该链接文件夹下的那些“实验报告.md”](https://github.com/1012598167/flask_mongodb_game/tree/master/Database-master)

别的都是没用的
