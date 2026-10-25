DROP DATABASE IF EXISTS sql2_practice_STD_ID;
CREATE DATABASE sql2_practice_STD_ID;
USE sql2_practice_STD_ID;

-- ------------------------------------------------------------
-- 1) CUSTOMER DIMENSION
-- ------------------------------------------------------------
CREATE TABLE CustomerDim (
    CustomerKey      INT PRIMARY KEY,
    CustomerID       INT NOT NULL,
    CustomerName     VARCHAR(50) NOT NULL,
    CustomerAge      INT,
    CustomerIncome   DECIMAL(10,2),
    CustomerCredit   VARCHAR(10)
);

INSERT INTO CustomerDim
(CustomerKey, CustomerID, CustomerName, CustomerAge, CustomerIncome, CustomerCredit)
VALUES
(251,  1, 'Maria Anders',       22, 12000.00, 'A'),
(252,  2, 'Ana Trujillo',       32, 32150.00, 'B'),
(253,  3, 'Antonio Moreno',      41, 23200.00, 'C'),
(254,  4, 'Thomas Hardy',        22, 21500.00, 'C'),
(255,  5, 'Christina Berglund',  32, 53635.00, 'A'),
(256,  6, 'Hanna Moos',          45, 32154.00, 'C'),
(257,  7, 'Frederique Citeaux',  62, 22100.00, 'C'),
(258,  8, 'Martin Sommer',       32, 21500.00, 'A'),
(259,  9, 'Laurence Lebihan',    50, 51220.00, 'D'),
(260, 10, 'Elizabeth Lincoln',    43, 51210.00, 'B'),
(261, 11, 'Ann Devon',            45, 44000.00, 'C'),
(262, 12, 'Peter Franken',        58, 61000.00, 'B');

-- ------------------------------------------------------------
-- 2) PRODUCT DIMENSION
-- ------------------------------------------------------------
CREATE TABLE ProductDim (
    ProductKey        INT PRIMARY KEY,
    ProductID         INT NOT NULL,
    ProductName       VARCHAR(80) NOT NULL,
    ProductCategory   VARCHAR(50) NOT NULL,
    SupplierName      VARCHAR(80),
    ProductBrand      VARCHAR(20),
    ProductPrice      DECIMAL(10,2) NOT NULL,
    ProductType       VARCHAR(20),
    ProductPlace_made VARCHAR(50)
);
INSERT INTO ProductDim
(ProductKey, ProductID, ProductName, ProductCategory, SupplierName,
 ProductBrand, ProductPrice, ProductType, ProductPlace_made)
VALUES
(190,  1, 'Chai',                         'Beverages',      'Exotic Liquids',             'PPP', 18.00, 'B', 'THA'),
(191,  2, 'Chang',                        'Beverages',      'Exotic Liquids',             'NPP', 19.00, 'C', 'USA'),
(192,  3, 'Aniseed Syrup',                'Condiments',     'Exotic Liquids',             'XXX', 10.00, 'C', 'THA'),
(193,  4, 'Chef Anton Cajun Seasoning',    'Condiments',     'New Orleans Cajun Delights', 'LLP', 22.00, 'A', 'BRA'),
(194,  5, 'Chef Anton Gumbo Mix',          'Condiments',     'New Orleans Cajun Delights', 'RPO', 21.35, 'D', 'SPN'),
(195,  6, 'Grandma Boysenberry Spread',    'Condiments',     'Grandma Kelly Homestead',    'PPN', 25.00, 'D', 'FRA'),
(196,  7, 'Northwoods Cranberry Sauce',    'Condiments',     'Grandma Kelly Homestead',    'PPP', 40.00, 'B', 'GER'),
(197,  8, 'Queso Cabrales',                'Dairy Products', 'Cooperativa de Quesos',      'NPP', 21.00, 'C', 'THA'),
(198,  9, 'Queso Manchego La Pastora',     'Dairy Products', 'Cooperativa de Quesos',      'XXX', 38.00, 'D', 'USA'),
(199, 10, 'Ikura',                         'Seafood',        'Mayumi Foods',                'LLP', 31.00, 'A', 'JPN'),
(200, 11, 'Pavlova',                       'Confections',    'Pavlova Ltd.',                'POR', 17.45, 'D', 'BRA'),
(201, 12, 'Teatime Chocolate Biscuits',    'Confections',    'Specialty Biscuits Ltd.',     'PNP',  9.20, 'B', 'THA'),
(202, 13, 'Sir Rodney Marmalade',           'Confections',    'Specialty Biscuits Ltd.',     'NOP', 81.00, 'D', 'SPN'),
(203, 14, 'Cote de Blaye',                  'Beverages',      'Aux joyeux ecclesiastiques',  'ABC', 263.50,'A', 'FRA'),
(204, 15, 'Schoggi Schokolade',             'Confections',    'Heli Susswaren',              'DEF', 43.90, 'B', 'SUI');

-- ------------------------------------------------------------
-- 3) DATE DIMENSION
-- ------------------------------------------------------------
CREATE TABLE DateDim (
    DateKey  INT PRIMARY KEY,
    Day      INT NOT NULL,
    Month    VARCHAR(20) NOT NULL,
    Year     VARCHAR(4) NOT NULL,
    TheDate  DATE NOT NULL
);

INSERT INTO DateDim (DateKey, Day, Month, Year, TheDate)
VALUES
(76,  5, 'December', '2003', '2003-12-05'),
(77,  6, 'December', '2003', '2003-12-06'),
(78,  7, 'December', '2003', '2003-12-07'),
(79,  8, 'December', '2003', '2003-12-08'),
(80,  9, 'December', '2003', '2003-12-09'),
(81,  3, 'January',  '2004', '2004-01-03'),
(82, 12, 'February', '2004', '2004-02-12'),
(83, 16, 'February', '2004', '2004-02-16'),
(84,  6, 'March',    '2004', '2004-03-06'),
(85, 18, 'March',    '2004', '2004-03-18'),
(86, 25, 'March',    '2004', '2004-03-25'),
(87,  2, 'April',    '2004', '2004-04-02');

-- ------------------------------------------------------------
-- 4) ELECTRONIC SALES FACT
-- ------------------------------------------------------------
CREATE TABLE ElectFact (
    ProductKey  INT NOT NULL,
    CustomerKey INT NOT NULL,
    DateKey     INT NOT NULL,
    unit_sold   INT NOT NULL,
    total       DECIMAL(10,2) NOT NULL,

    PRIMARY KEY (ProductKey, CustomerKey, DateKey),

    CONSTRAINT fk_fact_product
        FOREIGN KEY (ProductKey) REFERENCES ProductDim(ProductKey),

    CONSTRAINT fk_fact_customer
        FOREIGN KEY (CustomerKey) REFERENCES CustomerDim(CustomerKey),

    CONSTRAINT fk_fact_date
        FOREIGN KEY (DateKey) REFERENCES DateDim(DateKey)
);

-- total = unit_sold * ProductPrice

INSERT INTO ElectFact
(ProductKey, CustomerKey, DateKey, unit_sold, total)
VALUES
-- Maria Anders (251)
(190, 251, 81, 30,  540.00),
(203, 251, 82,  4, 1054.00),
(197, 251, 84,  8,  168.00),

-- Ana Trujillo (252)
(190, 252, 76,  2,   36.00),
(191, 252, 79, 10,  190.00),
(203, 252, 83,  5, 1317.50),
(201, 252, 86, 12,  110.40),

-- Antonio Moreno (253)
(192, 253, 77, 15,  150.00),
(193, 253, 82,  6,  132.00),
(198, 253, 85,  7,  266.00),

-- Thomas Hardy (254)
(194, 254, 78, 12,  256.20),
(196, 254, 83, 10,  400.00),
(202, 254, 87,  3,  243.00),

-- Christina Berglund (255)
(191, 255, 77,  1,   19.00),
(203, 255, 80,  6, 1581.00),
(204, 255, 85,  7,  307.30),

-- Hanna Moos (256)
(195, 256, 79,  9,  225.00),
(197, 256, 82, 11,  231.00),
(200, 256, 86, 20,  349.00),

-- Frederique Citeaux (257)
(198, 257, 80, 13,  494.00),
(199, 257, 83,  8,  248.00),
(202, 257, 87,  5,  405.00),

-- Martin Sommer (258)
(190, 258, 78, 20,  360.00),
(196, 258, 81, 18,  720.00),
(203, 258, 84,  2,  527.00),

-- Laurence Lebihan (259)
(191, 259, 76, 25,  475.00),
(200, 259, 82, 15,  261.75),
(204, 259, 86,  9,  395.10);

-- Q1
SELECT ProductCategory, COUNT(*) AS NumberOfProducts
FROM ProductDim
GROUP BY ProductCategory
ORDER BY ProductCategory;

-- Q2
SELECT DISTINCT c.CustomerName, c.CustomerAge
FROM CustomerDim c
JOIN ElectFact f ON c.CustomerKey = f.CustomerKey
ORDER BY c.CustomerName;

-- Q3
SELECT c.CustomerName, p.ProductName, f.unit_sold, f.total
FROM ElectFact f
JOIN CustomerDim c ON f.CustomerKey = c.CustomerKey
JOIN ProductDim p ON f.ProductKey = p.ProductKey
ORDER BY f.total DESC;

-- Q4
SELECT p.ProductCategory,
       SUM(f.total) AS TotalSales,
       SUM(f.unit_sold) AS TotalUnitsSold
FROM ElectFact f
JOIN ProductDim p ON f.ProductKey = p.ProductKey
GROUP BY p.ProductCategory
ORDER BY TotalSales DESC;

-- Q5
SELECT p.ProductName,
       SUM(f.unit_sold) AS TotalUnitsSold,
       SUM(f.total) AS TotalRevenue
FROM ElectFact f
JOIN ProductDim p ON f.ProductKey = p.ProductKey
GROUP BY p.ProductKey, p.ProductName
ORDER BY TotalRevenue DESC;

-- Q6
SELECT c.CustomerName, COALESCE(SUM(f.total), 0) AS TotalSpent
FROM CustomerDim c
LEFT JOIN ElectFact f ON c.CustomerKey = f.CustomerKey
GROUP BY c.CustomerKey, c.CustomerName
ORDER BY c.CustomerName;

-- Q7
SELECT c.CustomerName, c.CustomerCredit,
       SUM(f.total) AS TotalSpent
FROM CustomerDim c
JOIN ElectFact f ON c.CustomerKey = f.CustomerKey
GROUP BY c.CustomerKey, c.CustomerName, c.CustomerCredit
HAVING SUM(f.total) > 1000
ORDER BY TotalSpent DESC;

-- Q8
SELECT ProductName, ProductPrice
FROM ProductDim
WHERE ProductPrice > (SELECT AVG(ProductPrice) FROM ProductDim)
ORDER BY ProductPrice DESC;

-- Q9
SELECT DISTINCT c.CustomerName
FROM CustomerDim c
WHERE c.CustomerKey IN (
    SELECT f.CustomerKey
    FROM ElectFact f
    JOIN ProductDim p ON f.ProductKey = p.ProductKey
    WHERE p.ProductCategory = 'Beverages'
)
ORDER BY c.CustomerName;

-- Q10
SELECT c.CustomerName, p.ProductName, d.TheDate, f.unit_sold, f.total
FROM ElectFact f
JOIN CustomerDim c ON f.CustomerKey = c.CustomerKey
JOIN ProductDim p ON f.ProductKey = p.ProductKey
JOIN DateDim d ON f.DateKey = d.DateKey
ORDER BY d.TheDate;

-- Extra
SELECT c.CustomerName,
       SUM(f.total) AS TotalSpent,
       MAX(d.TheDate) AS LastPurchaseDate
FROM CustomerDim c
JOIN ElectFact f ON c.CustomerKey = f.CustomerKey
JOIN DateDim d ON f.DateKey = d.DateKey
GROUP BY c.CustomerKey, c.CustomerName
HAVING SUM(f.total) > 1000
ORDER BY TotalSpent DESC;