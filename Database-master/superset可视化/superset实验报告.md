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

打开路径E:\superset\env

启动虚拟环境env\Scripts\activate

E:\superset\env\Lib\site-packages\superset\bin

python superset run

![image-20191211194553442](C:\Users\chenn\AppData\Roaming\Typora\typora-user-images\image-20191211194553442.png)

![image-20191211194603740](C:\Users\chenn\AppData\Roaming\Typora\typora-user-images\image-20191211194603740.png)

可视化等功能在charts里去开。

