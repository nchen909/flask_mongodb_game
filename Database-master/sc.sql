create database sc;
\c sc;
create table Student(
    Sno char(9) primary key,
	Sname char(20) unique,
	Ssex char(2),
	Sage smallint,
	Sdept char(20)
	);
create table Course(
    Cno char(10) primary key,
	Cname char(40) NOT NULL,
	Cpno char(4),
	Ccredit smallint);
create table SC(
	Sno char(9),
	Cno char(4),
	Grade smallint);
insert into Student(Sno,Sname,Ssex,Sage,Sdept) values('200215121','李勇','男',20,'CS');
insert into Student(Sno,Sname,Ssex,Sage,Sdept) values('200215122','刘勇','女',19,'CS');
insert into Student(Sno,Sname,Ssex,Sage,Sdept) values('200215123','王敏','女',18,'MA');
insert into Student(Sno,Sname,Ssex,Sage,Sdept) values('200215125','张立','男',19,'IS');

insert into Course(Cno,Cname,Cpno,Ccredit) values('1','数据库','5','4');
insert into Course(Cno,Cname,Cpno,Ccredit) values('2','数学',null,'2');
insert into Course(Cno,Cname,Cpno,Ccredit) values('6','数据处理',null,'2');
insert into Course(Cno,Cname,Cpno,Ccredit) values('4','操作系统','6','3');
insert into Course(Cno,Cname,Cpno,Ccredit) values('7','PASCAL语言','6','4');
insert into Course(Cno,Cname,Cpno,Ccredit) values('5','数据结构','7','4');
insert into Course(Cno,Cname,Cpno,Ccredit) values('3','信息系统','1','4');

insert into SC(Sno,Cno,Grade) values('200215121','1',92);
insert into SC(Sno,Cno,Grade) values('200215121','2',85);
insert into SC(Sno,Cno,Grade) values('200215121','3',88);
insert into SC(Sno,Cno,Grade) values('200215122','2',90);
insert into SC(Sno,Cno,Grade) values('200215122','3',80);