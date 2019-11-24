from sqlalchemy import Column,String,Integer,ForeignKey,create_engine,PrimaryKeyConstraint
from sqlalchemy.orm import  sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  create_engine
import psycopg2

# 创建对象的基类
Base = declarative_base()
# 初始化数据库连接
engine = create_engine('postgresql://postgres:1@localhost:5432/postgres')
# 创建DBSession
DBSession = sessionmaker(bind=engine)  # 建立起会话 手机（bind=自己的手机号（mysql号））
# 创建session对象：
session = DBSession()  # 用该手机拨打电话（）
#declare a mapping
#定义User对象
class User(Base):

    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, index=True)
    books = relationship('Book',backref='author')#一本书对一用户 一用户对多本书 （书指用户写的书）
    #如果是一对一 加上uselist=False
    #relationship:存在关系，但是该关系在user中不存在 其为ForeignKey服务 也就是说
    #当你插入
    #外键对连表查询有一定的优化，那就是relationship字段，其配合外键一起使用 查询时不需要分两步走（先定位到两张表都有的属性 再查领一张表） 一步上天

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, nullable=False)
    book_name = Column(String(64), primary_key=True)
    # “多”的一方的book表是通过外键关联到user表的:
    user_name = Column(Integer,ForeignKey('users.id'),index=True)
    #目的：对于某些访问频繁（where中用的多）的数据加快访问速度
    #优点：加快数据访问 缺点：占用空间，树维护代价 o(n)到o(logn)
    #update次数比较少 树维护也是需要代价的 改的不多经常用就能建索引
    #author=relationship(User)

    def __repr__(self):#定义 __repr__ 是为了方便调试，你可以不定义，也可以定义的更详细一些。
        return '%s(%r)' % (self.__class__.__name__, self.user_name)#有时候报错可能只是因为__repr__没写对或者写了东西

Base.metadata.create_all(engine)#创建对应的表
def dbadd():
    #######################增
    user1 = User(id=123,username='mk',password='1',email='chennuo909@163.com')
    session.add(user1)
    user1 = User(id=1,username='mk2',password='1',email='chennuo909@163.com')
    session.add(user1)
    book1 = Book(id=3,book_name='yzynb',user_name=123)
    session.add_all([book1])
def dbfind():
    ########################查
    user = session.query(User).filter(User.id==123).one()
    print(user.books[0].user_name)####这就是relationship的好处 主表查从表 user.books有多本 查第一本
    #正向查询 通过查users得到book里的字段 起作用的是relationship中的Book字段（因为外码）
    #用户 id，就可以用 get 方法， filter_by 用于按某一个字段过滤，而 filter 可以让我们按多个字段过滤，all 则是获取所有
    abook = session.query(Book).filter_by(book_name='yzynb2').first()
    #反向查询 因为定义了,backref='author'所以不要倒过来再写一遍
    print(abook.author.email)
    # 打印类型和对象的name属性:
    print('type:', type(user))#直接就变成一个对象
    print('name:', user.username)
def dbchange():
    ########################改
    a = session.query(User).get(1)#查
    a.password = '3'
    # a.books.append(Book(id=10001,book_name='yzynb2',user_name=1243))#增
    session.add(a)
def dbdelete():
    #######################删
    a = session.query(User).get(1)#查
    session.delete(a)
def dbselect():
########################直接命令行
    # users = session.execute("SELECT id,username,password,email FROM users").fetchall()#能找到对象
    # print(type(users[0]))
    # for auser in users:
    #     print(f"id：{auser.id},username：{auser.username},password={auser.password},email={auser.email}")
    users = session.execute("SELECT count(password) FROM users").fetchall()#能找到对象
    print(type(users[0]))
    # for auser in users:
    #     print(f"id：{auser.count(password)},username：{auser.username},password={auser.password},email={auser.email}")


dbselect()
#提交即保存到数据库
session.commit()
#关闭session
session.close()