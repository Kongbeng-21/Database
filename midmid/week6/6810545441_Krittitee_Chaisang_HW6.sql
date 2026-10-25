drop database if exists gamestoresystem;
create database gamestoresystem;
use gamestoresystem;

CREATE TABLE Publisher (
    PublisherID     INT,
    PublisherName   VARCHAR(100) NOT NULL,
    Country         VARCHAR(50)  NOT NULL,
    YearFounded     INT,
    TargetGroup     VARCHAR(50),
    PRIMARY KEY (PublisherID)
);

CREATE TABLE Game (
    GameID       INT,
    GameName     VARCHAR(100) NOT NULL,
    RentPrice    DECIMAL(10,2) NOT NULL,
    PublisherID  INT NOT NULL,
    PRIMARY KEY (GameID),
    FOREIGN KEY (PublisherID) REFERENCES Publisher(PublisherID),
    CHECK (RentPrice > 0)
);

CREATE TABLE Member (
    MemberID     INT,
    MemberName   VARCHAR(100) NOT NULL,
    PhoneNum     VARCHAR(50) NOT NULL UNIQUE,
    Membership   VARCHAR(20) NOT NULL DEFAULT 'Bronze',
    JoinDate     DATE NOT NULL DEFAULT (CURRENT_DATE),
    ReferredBy   INT NULL,
    PRIMARY KEY (MemberID),
    FOREIGN KEY (ReferredBy) REFERENCES Member(MemberID)
);

CREATE TABLE IndividualMember (
    MemberID       INT,
    IDCardNumber   VARCHAR(20) NOT NULL UNIQUE,
    PRIMARY KEY (MemberID),
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
);

CREATE TABLE CorporateMember (
    MemberID       INT,
    CompanyName    VARCHAR(100) NOT NULL,
    TaxID          VARCHAR(20) NOT NULL UNIQUE,
    PRIMARY KEY (MemberID),
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
);

CREATE TABLE Rental (
    RentalID       INT,
    MemberID       INT NOT NULL,
    GameID         INT NOT NULL,
    DateRent       DATE NOT NULL,
    DateGiveBack   DATE NULL,
    PRIMARY KEY (RentalID),
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID),
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
);

INSERT INTO Publisher (PublisherID, PublisherName, Country, YearFounded, TargetGroup) VALUES
(1, 'Rockstar Games', 'USA', 1998, 'Adult'),
(2, 'Roblox Corporation', 'USA', 2004, 'Kids'),
(3, 'EA Sports', 'USA', 1982, 'Adult'),
(4, 'Nintendo', 'Japan', 1889, 'Kids'),
(5, 'Ubisoft', 'France', 1986, 'Adult'),
(6, 'Capcom', 'Japan', 1979, 'Adult'),
(7, 'Square Enix', 'Japan', 2003, 'Teen'),
(8, 'Activision', 'USA', 1979, 'Adult'),
(9, 'Bandai Namco', 'Japan', 2006, 'Teen'),
(10, 'CD Projekt', 'Poland', 1994, 'Adult');

INSERT INTO Game (GameID, GameName, RentPrice, PublisherID) VALUES
(1, 'GTA5', 1000.00, 1),
(2, 'RedDead Redemption 2', 750.00, 1),
(3, 'GTA6', 2000.00, 1),
(4, 'Roblox', 67.00, 2),
(5, 'Fifa24', 500.00, 3),
(6, 'Mario Kart 8', 600.00, 4),
(7, 'Assassins Creed Mirage', 850.00, 5),
(8, 'Resident Evil 4', 900.00, 6),
(9, 'Final Fantasy XVI', 1200.00, 7),
(10, 'Call of Duty MW3', 1100.00, 8),
(11, 'Tekken 8', 850.00, 9),
(12, 'Cyberpunk2077', 950.00, 10);

-- Member: 1-10 = Individual, 11-20 = Corporate
INSERT INTO Member (MemberID, MemberName, PhoneNum, Membership, JoinDate, ReferredBy) VALUES
(1, 'Nattapong Srisuk', '0891234567', 'Gold', '2023-01-15', NULL),
(2, 'Waraporn Jindarat', '0862345678', 'Silver', '2023-03-22', NULL),
(3, 'Chaiwat Petch', '0813456789', 'Gold', '2023-06-10', 1),
(4, 'Siriporn Boonrod', '0924567890', 'Bronze', '2024-01-05', 1),
(5, 'Thanakorn Meesuk', '0955678901', 'Silver', '2024-02-18', 2),
(6, 'Ploy Wongsuwan', '0866123456', 'Gold', '2024-03-01', NULL),
(7, 'Kittipong Saelim', '0877234567', 'Bronze', '2024-03-15', 6),
(8, 'Ananya Ruangrit', '0888345678', 'Silver', '2024-04-02', NULL),
(9, 'Somsak Intharak', '0899456789', 'Gold', '2024-04-20', 8),
(10, 'Napat Charoensuk', '0900567890', 'Bronze', '2024-05-05', NULL),
(11, 'Bangkok Esports Co., Ltd.', '021234567', 'Gold', '2023-02-01', NULL),
(12, 'Thai Game Cafe Network', '022345678', 'Gold', '2023-04-15', NULL),
(13, 'Chiang Mai Gaming Hub', '023456789', 'Silver', '2023-07-20', NULL),
(14, 'Siam Digital Events', '024567890', 'Gold', '2023-09-10', NULL),
(15, 'Pattaya LAN Center', '025678901', 'Bronze', '2024-01-18', NULL),
(16, 'Phuket Arcade Co.', '026789012', 'Silver', '2024-02-25', NULL),
(17, 'Isan Game Zone', '027890123', 'Bronze', '2024-03-30', NULL),
(18, 'Rangsit Cyber Club', '028901234', 'Gold', '2024-04-14', NULL),
(19, 'Ekkamai Play House', '029012345', 'Silver', '2024-05-22', NULL),
(20, 'Nonthaburi Game Studio', '020123456', 'Gold', '2024-06-01', NULL);

INSERT INTO IndividualMember (MemberID, IDCardNumber) VALUES
(1, 'ID1234567890123'),
(2, 'ID2345678901234'),
(3, 'ID3456789012345'),
(4, 'ID4567890123456'),
(5, 'ID5678901234567'),
(6, 'ID6789012345678'),
(7, 'ID7890123456789'),
(8, 'ID8901234567890'),
(9, 'ID9012345678901'),
(10, 'ID0123456789012');

INSERT INTO CorporateMember (MemberID, CompanyName, TaxID) VALUES
(11, 'Bangkok Esports Co., Ltd.', 'TAX1122334455'),
(12, 'Thai Game Cafe Network', 'TAX2233445566'),
(13, 'Chiang Mai Gaming Hub', 'TAX3344556677'),
(14, 'Siam Digital Events', 'TAX4455667788'),
(15, 'Pattaya LAN Center', 'TAX5566778899'),
(16, 'Phuket Arcade Co.', 'TAX6677889900'),
(17, 'Isan Game Zone', 'TAX7788990011'),
(18, 'Rangsit Cyber Club', 'TAX8899001122'),
(19, 'Ekkamai Play House', 'TAX9900112233'),
(20, 'Nonthaburi Game Studio', 'TAX0011223344');

INSERT INTO Rental (RentalID, MemberID, GameID, DateRent, DateGiveBack) VALUES
(1, 1, 5, '2024-01-10', '2024-01-15'),
(2, 2, 1, '2024-02-05', '2024-02-10'),
(3, 3, 2, '2024-03-01', NULL),
(4, 4, 4, '2024-03-15', '2024-03-20'),
(5, 5, 3, '2024-04-01', '2024-04-05'),
(6, 1, 1, '2024-04-10', '2024-04-14'),
(7, 6, 6, '2024-04-12', '2024-04-16'),
(8, 7, 8, '2024-05-01', NULL),
(9, 8, 10, '2024-05-05', '2024-05-09'),
(10, 2, 12, '2024-05-10', '2024-05-15'),
(11, 9, 9, '2024-05-20', '2024-05-25'),
(12, 10, 11, '2024-06-01', '2024-06-05'),
(13, 3, 7, '2024-06-10', NULL),
(14, 5, 1, '2024-06-15', '2024-06-20'),
(15, 1, 3, '2024-07-01', '2024-07-07'),
(16, 11, 5, '2024-07-05', '2024-07-10'),
(17, 12, 6, '2024-07-08', '2024-07-12'),
(18, 13, 8, '2024-07-15', NULL),
(19, 14, 10, '2024-07-20', '2024-07-25'),
(20, 15, 2, '2024-08-01', '2024-08-05');

-- Q1: JOIN — currently rented out games (not yet returned)
SELECT m.MemberName, g.GameName, r.DateRent
FROM Rental r
JOIN Member m ON r.MemberID = m.MemberID
JOIN Game g ON r.GameID = g.GameID
WHERE r.DateGiveBack IS NULL;

-- Q2: GROUP BY + aggregate — total revenue per publisher
SELECT p.PublisherName, COUNT(r.RentalID) AS TotalRentals, SUM(g.RentPrice) AS TotalRevenue
FROM Rental r
JOIN Game g ON r.GameID = g.GameID
JOIN Publisher p ON g.PublisherID = p.PublisherID
GROUP BY p.PublisherName
ORDER BY TotalRevenue DESC;

-- Q3: HAVING — members who rented more than once (repeat customers)
SELECT m.MemberName, COUNT(*) AS TotalRentals
FROM Rental r
JOIN Member m ON r.MemberID = m.MemberID
GROUP BY m.MemberName
HAVING COUNT(*) > 1;

-- Q4: CASE + date function (SQL-III concept) — rental status and duration
SELECT r.RentalID, m.MemberName, g.GameName,
       DATEDIFF(IFNULL(r.DateGiveBack, CURDATE()), r.DateRent) AS DaysRented,
       CASE WHEN r.DateGiveBack IS NULL THEN 'Still Rented' ELSE 'Returned' END AS RentalStatus
FROM Rental r
JOIN Member m ON r.MemberID = m.MemberID
JOIN Game g ON r.GameID = g.GameID
ORDER BY DaysRented DESC;

-- Q5: Own design — compare rental activity between Individual and Corporate members
SELECT 'Individual' AS MemberType, COUNT(DISTINCT r.MemberID) AS ActiveRenters, COUNT(r.RentalID) AS TotalRentals
FROM Rental r
JOIN IndividualMember im ON r.MemberID = im.MemberID
UNION
SELECT 'Corporate' AS MemberType, COUNT(DISTINCT r.MemberID), COUNT(r.RentalID)
FROM Rental r
JOIN CorporateMember cm ON r.MemberID = cm.MemberID;