/* Domain: Sports Betting Website
   Reused from HW#4 */
USE hw4_6810545441;

/* Task 1 - Subquery in SELECT
   My question: Show each member's balance alongside the average balance of all members */
SELECT MemberName, Balance,
       (SELECT AVG(Balance) FROM Member) AS AvgBalance
FROM Member;

/* Task 2 - Correlated Subquery
   My question: For each member, show how many bets they have placed */
SELECT m.MemberName,
       (SELECT COUNT(*) FROM Bet b WHERE b.MemberID = m.MemberID) AS TotalBets
FROM Member m
ORDER BY m.MemberName;

/* Task 3 - Subquery in FROM
   My question: Show sport types whose total bet amount exceeds 1000 */
SELECT SportType, TotalBetAmount
FROM (
    SELECT se.SportType, SUM(b.BetAmount) AS TotalBetAmount
    FROM Bet b
    JOIN SportEvent se ON b.EventID = se.EventID
    GROUP BY se.SportType
) AS SportTotals
WHERE TotalBetAmount > 1000
ORDER BY TotalBetAmount DESC;

/* Task 4 - CASE Expression
   My question: Classify each member's balance level as High/Medium/Low */
SELECT MemberName, Balance,
       CASE
           WHEN Balance >= 5000 THEN 'High'
           WHEN Balance >= 1500 THEN 'Medium'
           ELSE 'Low'
       END AS BalanceLevel
FROM Member;

/* Task 5 - CASE + Aggregate
   My question: For each member, count how many bets they Won vs Lost */
SELECT m.MemberName,
       SUM(CASE WHEN b.Result = 'Win'  THEN 1 ELSE 0 END) AS WinCount,
       SUM(CASE WHEN b.Result = 'Lose' THEN 1 ELSE 0 END) AS LoseCount
FROM Member m
JOIN Bet b ON m.MemberID = b.MemberID
GROUP BY m.MemberID, m.MemberName
ORDER BY WinCount DESC;

/* Task 6 - Common Table Expression (CTE)
   My question: Using a CTE, find members whose total bet amount exceeds 1000 */
WITH MemberBetTotal AS (
    SELECT m.MemberID, m.MemberName, SUM(b.BetAmount) AS TotalBetAmount
    FROM Member m
    JOIN Bet b ON m.MemberID = b.MemberID
    GROUP BY m.MemberID, m.MemberName
)
SELECT MemberName, TotalBetAmount
FROM MemberBetTotal
WHERE TotalBetAmount > 1000
ORDER BY TotalBetAmount DESC;

/* Task 7 - VIEW
   My question: Create a reusable view showing each member's total betting summary */
CREATE VIEW MemberBetSummary AS
SELECT m.MemberID, m.MemberName, 
       COUNT(b.BetID) AS TotalBets, 
       SUM(b.BetAmount) AS TotalAmount
FROM Member m
JOIN Bet b ON m.MemberID = b.MemberID
GROUP BY m.MemberID, m.MemberName;

SELECT * FROM MemberBetSummary
WHERE TotalAmount > 1000
ORDER BY TotalAmount DESC;

/* Task 8 - Date/DateTime Functions
   My question: Show each member's join date, how many days they have been a member, 
   and the month they joined */
SELECT MemberName, JoinDate,
       DATEDIFF(CURRENT_DATE, JoinDate) AS DaysAsMember,
       MONTH(JoinDate) AS JoinMonth,
       YEAR(JoinDate) AS JoinYear
FROM Member
ORDER BY JoinDate;

/* Task 9 - Constraints
   My question: Add a Promotion table demonstrating NOT NULL, UNIQUE, CHECK, DEFAULT, 
   and FOREIGN KEY together */
CREATE TABLE Promotion (
    PromoID     INT PRIMARY KEY,
    PromoCode   VARCHAR(20) NOT NULL UNIQUE,
    MemberID    INT,
    DiscountPct DECIMAL(5,2) NOT NULL CHECK (DiscountPct BETWEEN 0 AND 100),
    Status      VARCHAR(20) NOT NULL DEFAULT 'Active',
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

INSERT INTO Promotion (PromoID, PromoCode, MemberID, DiscountPct, Status)
VALUES
(1, 'WELCOME10', 101, 10.00, 'Active'),
(2, 'VIP20',     104, 20.00, 'Active'),
(3, 'SPRING5',   102,  5.00, 'Expired');

/* Task 10 - Index
   My question: We frequently filter bets by EventID (e.g., to show all bets on a 
   specific match). This index speeds up that lookup instead of scanning the whole Bet table. */
SELECT * FROM Bet WHERE EventID = 201;

CREATE INDEX idx_bet_eventid ON Bet (EventID);