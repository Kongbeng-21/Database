drop database Admission_6810545441;
create database Admission_6810545441;
use Admission_6810545441;
create table College
    (cname varchar(255),
    state varchar(255),
    enrollment int,
    primary key(cname));
    
create table student
    (sid int,
    sname varchar(255),
    GPA real,
    sizeHS int,
    primary key(sid));
create table apply
    (sid int,
    cname varchar(255),
    major varchar(255),
    decision varchar(255),
    primary key(sid,cname,major));
    
insert into College values ('Stanford', 'CA', 15000);
insert into College values ('Berkeley', 'CA', 36000);
insert into College values ('MIT', 'MA', 10000);
insert into College values ('Cornell', 'NY', 21000);
insert into Student values (123, 'Amy', 3.9, 1000);
insert into Student values (234, 'Bob', 3.6, 1500);
insert into Apply values (123, 'Stanford', 'CS', 'Y');
insert into Student values (345, 'Craig', 3.5, 500);
insert into Student values (456, 'Doris', 3.9, 1000);
insert into Student values (567, 'Edward', 2.9, 2000);
insert into Student values (678, 'Fay', 3.8, 200);
insert into Student values (789, 'Gary', 3.4, 800);
insert into Student values (987, 'Helen', 3.7, 800);
insert into Student values (876, 'Irene', 3.9, 400);
insert into Student values (765, 'Jay', 2.9, 1500);
insert into Student values (654, 'Amy', 3.9, 1000);
insert into Student values (543, 'Craig', 3.4, 2000);
insert into Apply values (123, 'Stanford', 'EE', 'N');
insert into Apply values (123, 'Berkeley', 'CS', 'Y');
insert into Apply values (123, 'Cornell', 'EE', 'Y');
insert into Apply values (234, 'Berkeley', 'biology', 'N');
insert into Apply values (345, 'MIT', 'bioengineering', 'Y');
insert into Apply values (345, 'Cornell', 'bioengineering', 'N');
insert into Apply values (345, 'Cornell', 'CS', 'Y');
insert into Apply values (345, 'Cornell', 'EE', 'N');
insert into Apply values (678, 'Stanford', 'history', 'Y');
insert into Apply values (987, 'Stanford', 'CS', 'Y');
insert into Apply values (987, 'Berkeley', 'CS', 'Y');
insert into Apply values (876, 'Stanford', 'CS', 'N');
insert into Apply values (876, 'MIT', 'biology', 'Y');
insert into Apply values (876, 'MIT', 'marine biology', 'N');
insert into Apply values (765, 'Stanford', 'history', 'Y');
insert into Apply values (765, 'Cornell', 'history', 'N');
insert into Apply values (765, 'Cornell', 'psychology', 'Y');
insert into Apply values (543, 'MIT', 'CS', 'N');

select count(*) from College;  
select count(*) from Student;  
select count(*) from Apply;

select cname, count(*) as nb_of_applications from Apply group by cname;

select *
from Student;

select sID,sName,GPA
from Student
where GPA>3.6;

select count(*)
from Student,Apply;

select distinct sname,major
from Student,Apply
where Student.sID = Apply.sID;

select max(gpa) as max_gpa
from student;

select *
from College
where enrollment > 15000;

select Student.sName ,Student.GPA , Apply.decision
from student,Apply
where Student.sID = Apply.sID
and Student.sizeHS < 1000
and Apply.cName = 'Stanford'
and Apply.major = 'CS';

select distinct College.cName
from College, Apply
where College.cName = Apply.cName
and College.enrollment > 20000
and Apply.major = 'CS';

select min(Student.GPA) as Smallest_GPA
from Student, Apply
where Student.sID = Apply.sID
and Apply.major = 'CS';

select Student.sName, Student.GPA
from College,Student,Apply
where student.sID = apply.sID
and college.cName = apply.cName
and apply.major = 'CS'
and apply.decision = 'N'
and College.enrollment > 20000;



select cname, count(*)
from Apply
group by cname;

select cName,major, min(GPA),max(GPA),count(*)
from apply,student
where student.sID = apply.sID
group by cName,major;

select student,sID,cName
from student,apply
where student.sID = apply.sID
order by srudent.sID;