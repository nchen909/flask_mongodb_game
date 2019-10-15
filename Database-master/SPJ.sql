create database SPJ;
\c spj;
create table S
(
	Sno char(2) unique,
	Sname char(6),
	Status char(2),
	City char(4),
	primary key(Sno)
);
	
create table P
(
	Pno char(2) unique,
	Pname char(6),
	color char(2),
	weight int,
	primary key(Pno)
);

create table J
(
	Jno char(2) unique,
	Jname char(8),
	CITY char(4),
	primary key(Jno)
);

create table SPJ
(
	Sno char(2),
	Pno char(2),
	Jno char(2),
	QTY int,
	primary key(Sno,Pno,Jno),
	foreign key(Sno) references S(Sno),
	foreign key(Pno) references P(Pno),
	foreign key(Jno) references J(Jno)
);


insert into S(Sno,Sname,Status,City)
values
('S1','精益','20','天津'),
('S2','盛锡','10','北京'),
('S3','东方红','30','北京'),
('S4','丰泰盛','20','天津'),
('S5','为民','30','上海');


insert into P(Pno,Pname,color,weight)
values
('P1','螺母','红',12),
('P2','螺栓','绿',17),
('P3','螺丝刀','蓝',14),
('P4','螺丝刀','红',14),
('P5','凸轮','蓝',40),
('P6','齿轮','红',30);


insert into J(Jno,Jname,CITY)
values
('J1','三建','北京'),
('J2','一汽','长春'),
('J3','弹簧厂','天津'),
('J4','造船厂','天津'),
('J5','机车厂','唐山'),
('J6','无线电厂','常州'),
('J7','半导体厂','南京');


insert into SPJ(Sno,Pno,Jno,QTY)
values
('S1','P1','J1',200),
('S1','P1','J3',100),
('S1','P1','J4',700),
('S1','P2','J2',100),
('S2','P3','J1',400),
('S2','P3','J2',200),
('S2','P3','J4',500),
('S2','P3','J5',400),
('S2','P5','J1',400),
('S2','P5','J2',100),
('S3','P1','J1',200),
('S3','P3','J1',200),
('S4','P5','J1',100),
('S4','P6','J3',300),
('S4','P6','J4',200),
('S5','P2','J4',100),
('S5','P3','J1',200),
('S5','P6','J2',200),
('S5','P6','J4',500);