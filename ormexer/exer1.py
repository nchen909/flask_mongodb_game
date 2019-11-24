from sqlalchemy import Column,String,Integer,ForeignKey,create_engine,PrimaryKeyConstraint
from sqlalchemy.orm import  sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  create_engine,sql,select,func
import psycopg2

# 创建对象的基类
Base = declarative_base()
# 初始化数据库连接
engine = create_engine('postgresql://postgres:1@localhost:5432/sc')
# 创建DBSession
DBSession = sessionmaker(bind=engine)  # 建立起会话 手机（bind=自己的手机号（mysql号））
# 创建session对象：
session = DBSession()  # 用该手机拨打电话（）
#declare a mapping
# #定义User对象
# class User(Base):
#
#     __tablename__ = 'users'
#     id = Column(Integer,primary_key=True)
#     username = Column(String(64), nullable=False, index=True)
#     password = Column(String(64), nullable=False)
#     email = Column(String(64), nullable=False, index=True)
#     books = relationship('Book',backref='author')#一本书对一用户 一用户对多本书 （书指用户写的书）
#     #如果是一对一 加上uselist=False
#     #relationship:存在关系，但是该关系在user中不存在 其为ForeignKey服务 也就是说
#     #当你插入
#     #外键对连表查询有一定的优化，那就是relationship字段，其配合外键一起使用 查询时不需要分两步走（先定位到两张表都有的属性 再查领一张表） 一步上天
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.username)
#
#
# class Book(Base):
#     __tablename__ = 'book'
#     id = Column(Integer, nullable=False)
#     book_name = Column(String(64), primary_key=True)
#     # “多”的一方的book表是通过外键关联到user表的:
#     user_name = Column(Integer,ForeignKey('users.id'),index=True)
#     #目的：对于某些访问频繁（where中用的多）的数据加快访问速度
#     #优点：加快数据访问 缺点：占用空间，树维护代价 o(n)到o(logn)
#     #update次数比较少 树维护也是需要代价的 改的不多经常用就能建索引
#     #author=relationship(User)
#
#     def __repr__(self):#定义 __repr__ 是为了方便调试，你可以不定义，也可以定义的更详细一些。
#         return '%s(%r)' % (self.__class__.__name__, self.user_name)#有时候报错可能只是因为__repr__没写对或者写了东西
class Student(Base):
    __tablename__ = 'student'
    sno = Column(Integer,primary_key= True)
    sname = Column(String(20))
    sage = Column(Integer)
    ssex = Column(String(20))
    sdept = Column(String(20))
class Course(Base):
    __tablename__ = 'course'
    cno = Column(Integer,primary_key=True)
    cname = Column(String(20))
    cpno = Column(Integer)
    ccredit = Column(Integer)
class SC(Base):
    __tablename__ = 'sc'
    sno = Column(Integer,ForeignKey('student.sno'))
    cno = Column(Integer,ForeignKey('course.cno'))
    grade = Column(Integer)
    __table_args__=(
    PrimaryKeyConstraint('sno', 'cno'),
    {},
    )
Base.metadata.create_all(engine)#创建对应的表


def db1():
# 1）按学生年龄升序查询Student表的所有记录
    student=session.query(Student).order_by(Student.sage.desc()).all()
    for s in student:
        print(s.sname)#sql.select('*').select_from(student))

    # # student = session.query(Student.sname).order_by(Student.sage.desc()).all()
    # # print(student)
    #
    # student_=session.query(Student).order_by(Student.sage.desc()).all()
    # # print(select(['*']).select_from(Student))
    # print(session.execute(select([Student])).fetchall())

def db2():
# 2）按课程名称分组查询课程表的记录
    #print(session.query(Student.sno).count())
    #course_=session.query(Course.cname,Course.ccredit).group_by(Course.cname).all()


    # course_=session.query(func.avg(SC.grade), func.count(
    #     Course.cname)).group_by(Course.cname).join(Course).all()
    #
    # print(course_)
    # for c in course_:
    #     print(c[0])

    course_=session.query(func.count(Course.cno)).group_by(Course.cname).all()

def db3():
# 3）对学生表按年龄分组，统计每组的人数
    student_=session.query(func.count(Student.sno),Student.sage).group_by(Student.sage).all()
    print(student_)
def db4():
    # 4）查询有成绩低于60的学生的姓名
    student_=session.query(Student.sname,SC.grade).join(SC).filter(SC.grade<60).all()
    print(student_)

def db5():
    # 5）查询选择了课程名为数据库的学生的学号
    student_=session.query(SC.sno.distinct()).join(Course).filter(Course.cname=="数据库").all()

    print(student_)
def db6():
    # 6）查询存在有85分以上成绩的课程的课程号
    course_=session.query(SC.sno.distinct()).filter(SC.grade>85).all()
    print(course_)
def db7():
    # 7）查询数据库课程分数最高的男同学的成绩
    student_=session.query(func.max(SC.grade)).join(Course).join(Student).filter(Course.cname=="数据库").filter(Student.ssex=='男').all()
    print(student_)
def db8():
    # 8）查询选择了课程名为操作系统的学生姓名和成绩
    student_=session.query(Student.sname,SC.grade).join(SC).join(Course).filter(Course.cname=='操作系统').all()
    print(student_)
def db9():
    student_=session.query(func.sum(SC.grade)).filter(SC.grade>85).all()
    print(student_[0][0])
def db9():
    student_=session.query(SC.sno).filter(SC.grade>85).all()
    for students in student_:
        print(students.sno)
# def dbadd():
#     #######################增
#     user1 = User(id=123,username='mk',password='1',email='chennuo909@163.com')
#     session.add(user1)
#     user1 = User(id=1,username='mk2',password='1',email='chennuo909@163.com')
#     session.add(user1)
#     book1 = Book(id=3,book_name='yzynb',user_name=123)
#     session.add_all([book1])
# def dbfind():
#     ########################查
#     user = session.query(User).filter(User.id==123).one()
#     print(user.books[0].user_name)####这就是relationship的好处 主表查从表 user.books有多本 查第一本
#     #正向查询 通过查users得到book里的字段 起作用的是relationship中的Book字段（因为外码）
#     #用户 id，就可以用 get 方法， filter_by 用于按某一个字段过滤，而 filter 可以让我们按多个字段过滤，all 则是获取所有
#     abook = session.query(Book).filter_by(book_name='yzynb2').first()
#     #反向查询 因为定义了,backref='author'所以不要倒过来再写一遍
#     print(abook.author.email)
#     # 打印类型和对象的name属性:
#     print('type:', type(user))#直接就变成一个对象
#     print('name:', user.username)
# def dbchange():
#     ########################改
#     a = session.query(User).get(1)#查
#     a.password = '3'
#     # a.books.append(Book(id=10001,book_name='yzynb2',user_name=1243))#增
#     session.add(a)
# def dbdelete():
#     #######################删
#     a = session.query(User).get(1)#查
#     session.delete(a)
# def dbselect():
# ########################直接命令行
#     users = session.execute("SELECT id,username,password,email FROM users").fetchall()#能找到对象
#     for auser in users:
#         print(f"id：{auser.id},username：{auser.username},password={auser.password},email={auser.email}")

db9()
#提交即保存到数据库
session.commit()
#关闭session
session.close()