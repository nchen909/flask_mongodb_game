# 12/11 下载安装

内容存于 E:/superset

请使用阿里源安装pip install -i https://mirrors.aliyun.com/pypi/simple superset

记得http加s 不然会因为没证书而访问不了

Failed building wheel for python-geohash

https://blog.csdn.net/weixin_41838105/article/details/88623794

下载不了对应whl文件

python --version 检查 cpxx是否和version一致

若

![image-20191211185206822](C:\Users\chenn\AppData\Roaming\Typora\typora-user-images\image-20191211185206822.png)

```
(env) (base) E:\superset>fabmanager create-admin --app superset
fabmanager is going to be deprecated in 2.2.X, you can use the same commands on the improved 'flask fab <command>'
Username [admin]: mathskiller
User first name [admin]: nuo
User last name [user]: chen
Email [admin@fab.org]: chennuo909@163.com
Password:
Repeat for confirmation:
2019-12-11 18:51:28,219:INFO:root:Configured event logger of type <class 'superset.utils.log.DBEventLogger'>
Recognized Database Authentications.
Admin User mathskiller created.
```

之后命令请进入xxx\superset\bin安装



以后每次启动

打开路径E:\superset

启动虚拟环境env\Scripts\activate

E:\superset\env\Lib\site-packages\superset\bin

python superset run

![image-20191211194553442](C:\Users\chenn\AppData\Roaming\Typora\typora-user-images\image-20191211194553442.png)

![image-20191211194603740](C:\Users\chenn\AppData\Roaming\Typora\typora-user-images\image-20191211194603740.png)

可视化等功能在charts里去开。

# 12/18 一些类型图

## Line chart

时间的种类选date

![image-20191218191116144](superset实验报告.assets/image-20191218191116144.png)

![image-20191218191240699](superset实验报告.assets/image-20191218191240699.png)

![image-20191218191321261](superset实验报告.assets/image-20191218191321261.png)

## Word Cloud

series出现字段

metric度量标准

![image-20191218191648705](superset实验报告.assets/image-20191218191648705.png)

![image-20191218191716057](superset实验报告.assets/image-20191218191716057.png)

保存请用save 并填写表名和dashboard名并点击保存到dashboard

## Filter box 和wordcloud一起使用

![image-20191218192308966](superset实验报告.assets/image-20191218192308966.png)

![image-20191218192428844](superset实验报告.assets/image-20191218192428844.png)

**条件选择某个图比方wordcloud中要筛选的东西比如区域**

![image-20191218192437149](superset实验报告.assets/image-20191218192437149.png)

![image-20191218192745159](superset实验报告.assets/image-20191218192745159.png)

![image-20191218192753853](superset实验报告.assets/image-20191218192753853.png)

选择表拖进来 save changes

然后就可以根据筛选条件去筛选词云

![image-20191218192843347](superset实验报告.assets/image-20191218192843347.png)