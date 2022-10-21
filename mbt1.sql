set sql_safe_updates=0;

create database IF NOT EXISTS mbt1;
use mbt1;
alter database mbt1 default character set utf8mb4;

set foreign_key_checks = 0;
drop table IF EXISTS User cascade; 
drop table IF EXISTS Center cascade;
drop table IF EXISTS Record cascade;  
drop table IF EXISTS Challenge cascade; 
set foreign_key_checks = 1;


create table Center (
CCODE INT NOT NULL,
Cname varchar(20) NOT NULL,
Caddress varchar(20) NOT NULL,
primary key(CCODE));


create table User (
UID varchar(20) NOT NULL,
UPW varchar(20) NOT NULL,
primary key(UID));
    

create table Record (
REvent varchar(10) NOT NULL,
RDate varchar(10) NOT NULL,
R1rm INT default 0,
UID varchar(10) NOT NULL,
primary key(REvent, RDate, UID),
foreign key (UID) references User(UID));

create table Challenge (
CEvent varchar(10) NOT NULL,
CWeight INT default 0,
UID varchar(10) NOT NULL,
CCODE INT NOT NULL,
primary key(CEvent, UID, CCODE),
foreign key (UID) references User(UID),
foreign key (CCODE) references Center(CCODE));

insert into Center
values(0000, 'A GYM', '홍익대 체육관');
insert into Center
values(1111, 'B GYM', '마포구 상수동');

insert into User
values('kms', '1234');
insert into User
values('psy', '1234');

insert into Record
values('Squat', '22-05-01', 80, 'kms');
insert into Record
values('Squat', '22-05-02', 60, 'kms');
insert into Record
values('Squat', '22-05-03', 70, 'kms');
insert into Record
values('Squat', '22-05-05', 90, 'kms');

insert into Record
values('BenchPress', '22-05-01', 60, 'kms');
insert into Record
values('BenchPress', '22-05-02', 80, 'kms');
insert into Record
values('BenchPress', '22-05-03', 100, 'kms');
insert into Record
values('BenchPress', '22-05-05', 80, 'kms');

insert into Record
values('Deadlift', '22-05-01', 100, 'kms');
insert into Record
values('Deadlift', '22-05-02', 110, 'kms');
insert into Record
values('Deadlift', '22-05-03', 100, 'kms');
insert into Record
values('Deadlift', '22-05-05', 110, 'kms');

insert into Record
values('Squat', '22-05-05', 120, 'psy');
insert into Record
values('BenchPress', '22-05-05', 200, 'psy');
insert into Record
values('Deadlift', '22-05-05', 80, 'psy');


-- 1
select * from Center;
select * from User;
select * from Record;

select * from Record where REvent = 'Deadlift' and UID = 'kms' order by RDate desc LIMIT 7;
select * from Record where REvent = 'Squat' and UID = 'kms' order by RDate desc LIMIT 7;
select * from Record where REvent = 'BenchPress' and UID = 'kms' order by RDate desc LIMIT 7;



select UID, MAX(R1rm)
from Record
where REvent = 'Squat'
group by UID;





select * from User where UID = 'kms' and UPW = '1234';
select * from User;


select MAX(R1rm) from Record where REvent = 'Squat' and UID = 'kms';

select * from Record where UID = 'kms' and REvent = 'Squat';

select RDate, R1rm from Record where UID = 'kms' and REvent = 'Squat' order by RDate desc LIMIT 5;



insert into Record
values('Deadlift', '22-09-02', 200, 'kms');
insert into Record
values('Squat', '22-09-02', 300, 'kms');
insert into Record
values('BenchPress', '22-09-02', 400, 'kms');

insert into Record 
values('BenchPress', '22-10-21', 300, 'kms');
select * from Record where UID = 'kms' and REvent = 'BenchPress';
update Record 
set R1rm = 700 where UID = 'kms' and REvent = 'BenchPress' and RDate = '22-10-21';

select * from Record where UID = 'kms' and REvent = 'BenchPress';
