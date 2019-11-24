create table student(id int primary key not null,name char(10) not null,age int not null,sex int);
create table course(id int primary key not null,cname char(30) not null,period int not null,credit int not null);
create table sc(sid int,cid int,grade smallint,primary key (sid,cid), foreign key(sid) references student(id),foreign key(cid) references course(id));