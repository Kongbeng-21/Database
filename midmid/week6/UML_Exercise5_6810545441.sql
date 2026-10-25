CREATE DATABASE uml_exercise5;
USE uml_exercise5;

drop table if exists Serviceby; 
drop table if exists Auto;
drop table if exists Person;
drop table if exists Dealer;
drop table if exists State;

create table Person (
	PersonID int primary key,
    Pname VARCHAR(100) NOT NULL
);

create table State (
	StateID int primary key,
    SName VARCHAR(100) not null
);

create table Auto (
	AutoID int primary key,
    AName VARCHAR(100),
    AModel VARCHAR(100),
    AYear int,
	PersonID int not null,
    StateID int not null,
    foreign key (PersonID) references Person(PersonID),
    foreign key (StateID) references State(StateID)
);

create table Dealer (
	DealerID int primary key,
    DName varchar(100)
);

create table Serviceby (
	AutoID int not null,
    DealerID int not null,
    primary key (AutoID,DealerID),
    foreign key (AutoID) references Auto(AutoID),
    foreign key (DealerID) references Dealer(DealerID)
);


INSERT INTO Person (PersonID, Pname) VALUES
(1, 'Gay Khaw'),
(2, 'Bung Gus'),
(3, 'Kongbeng Handsome'),
(4, 'Sun Gay'),
(5, 'Grade Adatabase');

INSERT INTO State (StateID, SName) VALUES
(1, 'Bangkok'),
(2, 'Chiang Mai'),
(3, 'Nonthaburi'),
(4, 'Chonburi'),
(5, 'Khon Kaen');

INSERT INTO Dealer (DealerID, DName) VALUES
(1, 'Toyota Sukhumvit'),
(2, 'Honda Ratchada'),
(3, 'Isuzu Bangna'),
(4, 'Mazda Ladprao'),
(5, 'Nissan Pinklao');

INSERT INTO Auto (AutoID, AName, AModel, AYear, PersonID, StateId) VALUES
(1, 'Toyota', 'Camry', 2022, 1, 1),
(2, 'Honda', 'Civic', 2021, 2, 2),
(3, 'Isuzu', 'D-Max', 2023, 3, 3),
(4, 'Mazda', 'CX-5', 2020, 4, 4),
(5, 'Nissan', 'Almera', 2022, 5, 5);

INSERT INTO Serviceby (AutoID, DealerID) VALUES
(1, 1),
(1, 2),
(2, 2),
(3, 3),
(4, 4),
(5, 5);
	