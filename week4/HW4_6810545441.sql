/* Domain: Sports Betting Website
   Tables: Member(MemberID, MemberName, Email, Balance, JoinDate),
           SportEvent(EventID, EventName, SportType, EventDate, Status),
           BetType(BetTypeID, TypeName),
           Bet(BetID, MemberID[FK], EventID[FK], BetTypeID[FK], BetAmount, Odds, Result) */

CREATE DATABASE hw4_6810545441;
USE hw4_6810545441;

/* ------------------------------------------------------------
   Part A: CREATE TABLE + INSERT
   ------------------------------------------------------------ */

-- 1) Member Table
CREATE TABLE Member (
    MemberID   INT PRIMARY KEY,
    MemberName VARCHAR(50) NOT NULL,
    Email      VARCHAR(80) NOT NULL,
    Balance    DECIMAL(10,2) NOT NULL,
    JoinDate   DATE NOT NULL
);

INSERT INTO Member (MemberID, MemberName, Email, Balance, JoinDate) VALUES
(101, 'Somchai', 'somchai@mail.com', 5000.00, '2024-01-10'),
(102, 'Suda',    'suda@mail.com',    3200.00, '2024-01-15'),
(103, 'Anan',    'anan@mail.com',    1500.00, '2024-02-01'),
(104, 'Ploy',    'ploy@mail.com',    8000.00, '2024-02-10'),
(105, 'Kit',     'kit@mail.com',      200.00, '2024-03-01'),
(106, 'Mai',     'mai@mail.com',    10000.00, '2024-03-15');  -- has never placed a bet (unmatched)

-- 2) SportEvent Table
CREATE TABLE SportEvent (
    EventID   INT PRIMARY KEY,
    EventName VARCHAR(100) NOT NULL,
    SportType VARCHAR(30) NOT NULL,
    EventDate DATE NOT NULL,
    Status    VARCHAR(20) NOT NULL
);

INSERT INTO SportEvent (EventID, EventName, SportType, EventDate, Status) VALUES
(201, 'Liverpool vs Man Utd',        'Football',   '2024-04-01', 'Finished'),
(202, 'Lakers vs Warriors',          'Basketball', '2024-04-03', 'Finished'),
(203, 'Real Madrid vs Barcelona',    'Football',   '2024-04-05', 'Finished'),
(204, 'Thailand vs Vietnam',         'Football',   '2024-04-10', 'Finished'),
(205, 'Djokovic vs Nadal',           'Tennis',     '2024-04-12', 'Finished'),
(206, 'Man City vs Chelsea',         'Football',   '2024-05-01', 'Upcoming'); -- no bets placed yet (unmatched)

-- 3) BetType Table
CREATE TABLE BetType (
    BetTypeID INT PRIMARY KEY,
    TypeName  VARCHAR(50) NOT NULL
);

INSERT INTO BetType (BetTypeID, TypeName) VALUES
(1, '1X2 (Match Result)'),
(2, 'Handicap (Win with different goals)'),
(3, 'Over/Under (Score Over-Under)');

-- 4) Bet Table (main table, links the three tables above)
CREATE TABLE Bet (
    BetID     INT PRIMARY KEY,
    MemberID  INT NOT NULL,
    EventID   INT NOT NULL,
    BetTypeID INT NOT NULL,
    BetAmount DECIMAL(10,2) NOT NULL,
    Odds      DECIMAL(4,2) NOT NULL,
    Result    VARCHAR(10) NOT NULL,

    CONSTRAINT fk_bet_member FOREIGN KEY (MemberID) REFERENCES Member(MemberID),
    CONSTRAINT fk_bet_event  FOREIGN KEY (EventID)  REFERENCES SportEvent(EventID),
    CONSTRAINT fk_bet_type   FOREIGN KEY (BetTypeID) REFERENCES BetType(BetTypeID)
);

INSERT INTO Bet (BetID, MemberID, EventID, BetTypeID, BetAmount, Odds, Result) VALUES
(1,  101, 201, 1,  500.00, 1.80, 'Win'),
(2,  101, 202, 2,  300.00, 1.95, 'Lose'),
(3,  101, 203, 3,  200.00, 2.10, 'Win'),
(4,  102, 201, 2, 1000.00, 1.75, 'Win'),
(5,  102, 204, 1,  150.00, 2.50, 'Lose'),
(6,  102, 205, 3,  400.00, 1.90, 'Win'),
(7,  103, 202, 1,  100.00, 3.00, 'Lose'),
(8,  103, 203, 2,  250.00, 1.85, 'Win'),
(9,  104, 201, 3, 2000.00, 1.70, 'Win'),
(10, 104, 204, 2,  800.00, 2.00, 'Win'),
(11, 104, 205, 1,  600.00, 2.20, 'Lose'),
(12, 105, 202, 3,   50.00, 2.05, 'Lose'),
(13, 105, 203, 1,  100.00, 1.95, 'Win'),
(14, 101, 204, 2,  350.00, 1.88, 'Win'),
(15, 102, 203, 3,  450.00, 2.15, 'Lose');

/* ------------------------------------------------------------
   Part B: Queries (10 Queries)
   ------------------------------------------------------------ */

/* Query 1 - INNER JOIN
   My question: Show member names, event names, bet amounts, and results — only for bets that actually occurred) */
SELECT m.MemberName, se.EventName, b.BetAmount, b.Result
FROM Member m
INNER JOIN Bet b ON m.MemberID = b.MemberID
INNER JOIN SportEvent se ON b.EventID = se.EventID
ORDER BY m.MemberName;

/* Query 2 - LEFT JOIN
   My question: Show all members with their bets, including members who have never placed a bet (keeps every row from Member even without a match in Bet -> Mai appears with NULL) */
SELECT m.MemberID, m.MemberName, b.BetID, b.BetAmount
FROM Member m
LEFT JOIN Bet b ON m.MemberID = b.MemberID
ORDER BY m.MemberID;

/* Query 3 - RIGHT JOIN
   My question: Show all events with their bet data, including events with no bets yet (keeps every row from SportEvent even without a match in Bet -> Man City vs Chelsea appears with NULL) */
SELECT se.EventID, se.EventName, b.BetID, b.BetAmount
FROM Bet b
RIGHT JOIN SportEvent se ON b.EventID = se.EventID
ORDER BY se.EventID;

/* Query 4 - JOIN + GROUP BY + Aggregate
   My question: Show the number of bets, total amount, and average amount each member has bet, ordered from highest to lowest total */
SELECT m.MemberName,
       COUNT(b.BetID)   AS TotalBets,
       SUM(b.BetAmount) AS TotalAmount,
       AVG(b.BetAmount) AS AvgAmount
FROM Member m
JOIN Bet b ON m.MemberID = b.MemberID
GROUP BY m.MemberID, m.MemberName
ORDER BY TotalAmount DESC;

/* Query 5 - Scalar Subquery
   My question: Find members whose balance is greater than the average balance of all members */
SELECT MemberName, Balance
FROM Member
WHERE Balance > (SELECT AVG(Balance) FROM Member);

/* Query 6 - IN Subquery
   My question: Show the name and email of members who have placed a bet on a Football event */
SELECT MemberName, Email
FROM Member
WHERE MemberID IN (
    SELECT b.MemberID
    FROM Bet b
    JOIN SportEvent se ON b.EventID = se.EventID
    WHERE se.SportType = 'Football'
);

/* Query 7 - NOT IN Subquery
   My question: Show the names of members who have never placed a bet on a Tennis event */
SELECT MemberName
FROM Member
WHERE MemberID NOT IN (
    SELECT b.MemberID
    FROM Bet b
    JOIN SportEvent se ON b.EventID = se.EventID
    WHERE se.SportType = 'Tennis'
);

/* Query 8 - ANY or ALL Subquery (chose ALL)
   My question: Show bets with an amount greater than ALL of member Anan's bet amounts (uses ALL to compare against the highest value returned by the subquery) */
SELECT BetID, MemberID, BetAmount
FROM Bet
WHERE BetAmount > ALL (
    SELECT BetAmount FROM Bet WHERE MemberID = 103
);

/* Query 9 - EXISTS Subquery
   My question: Show the names of events that have at least one bet placed on them */
SELECT se.EventName
FROM SportEvent se
WHERE EXISTS (
    SELECT 1 FROM Bet b WHERE b.EventID = se.EventID
);

/* Query 10 - NOT EXISTS Subquery
   My question: Show the names of events that have no bets placed on them */
SELECT se.EventName
FROM SportEvent se
WHERE NOT EXISTS (
    SELECT 1 FROM Bet b WHERE b.EventID = se.EventID
);