DROP DATABASE IF EXISTS Gym_6810545441;
CREATE DATABASE Gym_6810545441;
USE Gym_6810545441;

CREATE TABLE Trainer (
    trainerID       INT PRIMARY KEY,
    trainerName     VARCHAR(100) NOT NULL,
    specialty       VARCHAR(50),
    yearsExperience INT,
    phone           VARCHAR(20)
);

CREATE TABLE Member (
    memberID        INT PRIMARY KEY,
    memberName      VARCHAR(100) NOT NULL,
    email           VARCHAR(100),
    city            VARCHAR(50),
    membershipType  VARCHAR(20),
    joinDate        DATE
);

CREATE TABLE Class (
    classID      INT PRIMARY KEY,
    className    VARCHAR(100) NOT NULL,
    classType    VARCHAR(50),
    trainerID    INT,
    duration     INT,            
    price        DECIMAL(8,2),
    maxCapacity  INT,
    FOREIGN KEY (trainerID) REFERENCES Trainer(trainerID)
);

CREATE TABLE Booking (
    memberID     INT,
    classID      INT,
    bookingDate  DATE,
    attended     VARCHAR(3),      
    PRIMARY KEY (memberID, classID, bookingDate),
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (classID)  REFERENCES Class(classID)
);



INSERT INTO Trainer VALUES
(1, 'Somchai Prasert', 'Yoga', 8, '081-111-1111'),
(2, 'Nattapong Wong', 'Cardio', 5, '081-222-2222'),
(3, 'Kanya Suksri', 'Pilates', 10, '081-333-3333'),
(4, 'Wichai Boonmee', 'Weight Training', 12, '081-444-4444'),
(5, 'Ploy Chaiyaporn', 'Yoga', 3, '081-555-5555'),
(6, 'Anucha Tanaka', 'Cardio', 7, '081-666-6666');

INSERT INTO Member VALUES
(101, 'Krittitee Chaisang', 'krittitee@gmail.com', 'Bangkok', 'Premium', '2024-01-15'),
(102, 'Wanida Srisuk', 'wanida@gmail.com', 'Bangkok', 'Basic', '2024-02-10'),
(103, 'Panuwat Meechai', 'panuwat@hotmail.com', 'Nonthaburi', 'Premium', '2024-01-20'),
(104, 'Suda Kongkiat', 'suda@gmail.com', 'Bangkok', 'Basic', '2024-03-05'),
(105, 'Thanawat Rakpong', 'thanawat@yahoo.com', 'Pathum Thani', 'Premium', '2024-02-25'),
(106, 'Areeya Sompong', 'areeya@gmail.com', 'Bangkok', 'Basic', '2024-04-01'),
(107, 'Chatchai Intra', 'chatchai@hotmail.com', 'Nonthaburi', 'Premium', '2024-03-18'),
(108, 'Malee Thongdee', 'malee@gmail.com', 'Bangkok', 'Basic', '2024-04-12');

INSERT INTO Class VALUES
(201, 'Morning Yoga', 'Yoga', 1, 60, 400.00, 20),
(202, 'Power Yoga', 'Yoga', 5, 45, 350.00, 15),
(203, 'HIIT Cardio', 'Cardio', 2, 30, 300.00, 25),
(204, 'Cardio Blast', 'Cardio', 6, 45, 350.00, 20),
(205, 'Reformer Pilates', 'Pilates', 3, 50, 600.00, 10),
(206, 'Mat Pilates', 'Pilates', 3, 40, 450.00, 15),
(207, 'Strength Training', 'Weight Training', 4, 60, 500.00, 12),
(208, 'Advanced Weight Lifting', 'Weight Training', 4, 75, 700.00, 8);

INSERT INTO Booking VALUES
(101, 201, '2025-06-01', 'Yes'),
(101, 205, '2025-06-03', 'Yes'),
(101, 201, '2025-06-08', 'No'),
(102, 203, '2025-06-02', 'Yes'),
(102, 204, '2025-06-05', 'Yes'),
(103, 207, '2025-06-01', 'Yes'),
(103, 208, '2025-06-10', 'Yes'),
(104, 201, '2025-06-04', 'Yes'),
(104, 202, '2025-06-09', 'No'),
(105, 205, '2025-06-06', 'Yes'),
(105, 206, '2025-06-07', 'Yes'),
(106, 203, '2025-06-02', 'Yes'),
(107, 207, '2025-06-03', 'Yes'),
(108, 202, '2025-06-05', 'Yes');


/* ============================================================
   1.3) BUSINESS INTELLIGENCE QUERIES
   ============================================================ */

/* Q1: Find classes that cost more than 400 baht */
SELECT className, classType, price
FROM Class
WHERE price > 400;


/* Q2: Show all possible combinations between members and classes */
SELECT *
FROM Member, Class;


/* Q3: Show all possible combinations between trainers and classes */
SELECT *
FROM Trainer, Class;


/* Q4: Find the average price of all classes */
SELECT AVG(price) AS avg_price
FROM Class;


/* Q5: Count how many members have Premium membership */
SELECT COUNT(*) AS num_premium_members
FROM Member
WHERE membershipType = 'Premium';


/* Q6: Find classes that have been booked more than once */
SELECT classID, COUNT(*) AS num_bookings
FROM Booking
GROUP BY classID
HAVING COUNT(*) > 1;


/* Q7: Find members who booked both Yoga and Pilates */
SELECT B.memberID
FROM Booking B, Class C
WHERE B.classID = C.classID
  AND C.classType IN ('Yoga', 'Pilates')
GROUP BY B.memberID
HAVING COUNT(DISTINCT C.classType) = 2;


/* Q8: Show member name, class name, and booking date for each booking */
SELECT M.memberName, C.className, B.bookingDate
FROM Member M, Class C, Booking B
WHERE M.memberID = B.memberID AND C.classID = B.classID
ORDER BY B.bookingDate;


/* Q9: Find trainers with more experience than at least one Yoga trainer */
SELECT DISTINCT T1.trainerName, T1.yearsExperience
FROM Trainer T1, Trainer T2
WHERE T1.yearsExperience > T2.yearsExperience
  AND T2.specialty = 'Yoga';


/* Q10: Sort classes by type first, then by price */
SELECT className, classType, price
FROM Class
ORDER BY classType ASC, price DESC;


/* Q11: Find members who use a Gmail email address */
SELECT memberName, email
FROM Member
WHERE email LIKE '%gmail%';


/* Q12: Show classes, their trainers, and booking counts
   for classes booked more than once */
SELECT C.className, T.trainerName, COUNT(*) AS num_bookings
FROM Class C, Trainer T, Booking B
WHERE C.trainerID = T.trainerID AND C.classID = B.classID
GROUP BY C.className, T.trainerName
HAVING COUNT(*) > 1
ORDER BY num_bookings DESC;


/* Q13: Find members who booked either Yoga or Cardio classes (Set Operations - UNION) */
SELECT B.memberID
FROM Booking B, Class C
WHERE B.classID = C.classID AND C.classType = 'Yoga'
UNION
SELECT B.memberID
FROM Booking B, Class C
WHERE B.classID = C.classID AND C.classType = 'Cardio';