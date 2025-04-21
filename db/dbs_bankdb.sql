-- Create Database with proper character set and collation
CREATE DATABASE IF NOT EXISTS DBS_CreditCard
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE DBS_CreditCard;

-- Drop tables if they exist (for clean re-runs)
DROP TABLE IF EXISTS Rewards;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Accounts;
DROP TABLE IF EXISTS Customers;

-- Create schema with proper data types, constraints, and indexes
-- Table for Customers with additional fields and constraints
CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    date_of_birth DATE,
    join_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    status ENUM('Active', 'Inactive', 'Suspended') NOT NULL DEFAULT 'Active',
    preferred_language VARCHAR(10) DEFAULT 'en',
    INDEX idx_customer_name (last_name, first_name),
    INDEX idx_customer_email (email)
) ENGINE=InnoDB;

-- Table for Credit Card Accounts with improved structure
CREATE TABLE Accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    account_type ENUM('Standard', 'Gold', 'Platinum', 'Business') NOT NULL DEFAULT 'Standard',
    card_number VARCHAR(16) NOT NULL UNIQUE,
    expiry_date DATE NOT NULL,
    credit_limit DECIMAL(12, 2) NOT NULL DEFAULT 1000.00,
    available_credit DECIMAL(12, 2) NOT NULL DEFAULT 1000.00,
    annual_fee DECIMAL(10, 2) DEFAULT 0.00,
    interest_rate DECIMAL(5, 2) NOT NULL DEFAULT 12.99,
    statement_date INT NOT NULL DEFAULT 1, -- Day of month
    payment_due_date INT NOT NULL DEFAULT 15, -- Day of month
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    INDEX idx_account_customer (customer_id)
) ENGINE=InnoDB;

-- Table for Transactions with improved categorization and tracking
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    settlement_date DATETIME,
    merchant_name VARCHAR(255) NOT NULL,
    merchant_id VARCHAR(50),
    merchant_category_code VARCHAR(4),
    category VARCHAR(100),
    transaction_amount DECIMAL(12, 2) NOT NULL,
    transaction_type ENUM('Purchase', 'Payment', 'Fee', 'Credit', 'Refund', 'Adjustment', 'Cash Advance') NOT NULL,
    transaction_reference VARCHAR(100),
    transaction_status ENUM('Pending', 'Completed', 'Declined', 'Disputed') NOT NULL DEFAULT 'Completed',
    currency VARCHAR(3) DEFAULT 'SGD',
    exchange_rate DECIMAL(10, 6) DEFAULT 1.000000,
    description TEXT,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE,
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_transaction_account (account_id),
    INDEX idx_transaction_type (transaction_type),
    INDEX idx_transaction_category (category)
) ENGINE=InnoDB;

-- Table for Rewards and Loyalty points
CREATE TABLE Rewards (
    reward_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    reward_points INT NOT NULL DEFAULT 0,
    tier_level ENUM('Standard', 'Silver', 'Gold', 'Platinum') NOT NULL DEFAULT 'Standard',
    points_expiry_date DATE,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE,
    INDEX idx_reward_account (account_id)
) ENGINE=InnoDB;

-- Insert sample data - Diverse set of customers
INSERT INTO Customers (first_name, last_name, email, phone, address, city, country, postal_code, date_of_birth, join_date, preferred_language)
VALUES 
-- Singapore customers
('John', 'Tan', 'john.tan@example.com', '+65 9123 4567', '123 Orchard Road, #05-01', 'Singapore', 'Singapore', '238839', '1985-07-15', '2022-01-10', 'en'),
('Wei Lin', 'Chen', 'weilin.chen@example.com', '+65 8765 4321', '56 Toa Payoh Lorong 4, #12-45', 'Singapore', 'Singapore', '310056', '1990-04-25', '2023-02-18', 'zh'),
('Aisha', 'Begum', 'aisha.b@example.com', '+65 9876 5432', '789 Tampines Ave 3, #08-123', 'Singapore', 'Singapore', '520789', '1992-11-30', '2023-05-20', 'ms'),
('Radhika', 'Sharma', 'radhika.s@example.com', '+65 8432 1098', '23 Serangoon Road', 'Singapore', 'Singapore', '218081', '1988-09-12', '2022-08-15', 'ta'),
('Michael', 'Wong', 'michael.wong@example.com', '+65 9345 6789', '45 Bukit Timah Road', 'Singapore', 'Singapore', '229842', '1979-03-05', '2021-11-22', 'en'),

-- Malaysia customers
('Siti', 'Aminah', 'siti.a@example.com', '+60 12-345 6789', '15 Jalan Bukit Bintang', 'Kuala Lumpur', 'Malaysia', '55100', '1995-06-18', '2023-07-30', 'ms'),
('David', 'Lee', 'david.lee@example.com', '+60 19-876 5432', '88 Persiaran KLCC', 'Kuala Lumpur', 'Malaysia', '50088', '1983-12-01', '2022-04-15', 'en'),

-- Hong Kong customers
('Wing', 'Chow', 'wing.chow@example.com', '+852 9123 4567', '123 Nathan Road', 'Kowloon', 'Hong Kong', '', '1975-08-22', '2022-03-10', 'zh'),
('Sarah', 'Johnson', 'sarah.j@example.com', '+852 6789 0123', '45 Queens Road Central', 'Central', 'Hong Kong', '', '1991-05-17', '2023-01-05', 'en'),

-- Indonesia customers
('Budi', 'Santoso', 'budi.s@example.com', '+62 812-3456-7890', 'Jl. Sudirman Kav. 52-53', 'Jakarta', 'Indonesia', '12190', '1987-02-28', '2022-09-08', 'en'),
('Dewi', 'Lestari', 'dewi.l@example.com', '+62 878-9012-3456', 'Jl. Thamrin No. 10', 'Jakarta', 'Indonesia', '10230', '1993-10-15', '2023-04-12', 'en'),

-- India customers
('Raj', 'Patel', 'raj.patel@example.com', '+91 98765 43210', '42 Marine Drive', 'Mumbai', 'India', '400020', '1982-11-07', '2022-06-25', 'en'),
('Priya', 'Singh', 'priya.s@example.com', '+91 87654 32109', '15 M.G. Road', 'Bangalore', 'India', '560001', '1994-07-19', '2023-03-18', 'en'),

-- Thai customers
('Somchai', 'Wattana', 'somchai.w@example.com', '+66 81 234 5678', '123 Sukhumvit Road', 'Bangkok', 'Thailand', '10110', '1980-01-30', '2022-07-14', 'en'),
('Nuan', 'Charoenporn', 'nuan.c@example.com', '+66 89 876 5432', '45 Silom Road', 'Bangkok', 'Thailand', '10500', '1989-06-12', '2023-08-22', 'en');

-- Insert sample accounts with varying credit limits and types
INSERT INTO Accounts (customer_id, account_number, account_type, card_number, expiry_date, credit_limit, available_credit, annual_fee, interest_rate, statement_date, payment_due_date)
VALUES
-- Singapore customers
(1, 'AC100054389', 'Platinum', '5489123412341234', '2027-09-30', 25000.00, 15675.50, 300.00, 12.99, 25, 15),
(2, 'AC100054390', 'Gold', '5489123412345678', '2026-11-30', 15000.00, 9785.25, 150.00, 15.99, 3, 20),
(3, 'AC100054391', 'Standard', '5489123412349876', '2026-08-31', 5000.00, 2350.00, 0.00, 18.99, 10, 25),
(4, 'AC100054392', 'Standard', '5489123412345432', '2025-12-31', 8000.00, 3200.75, 0.00, 18.99, 15, 30),
(5, 'AC100054393', 'Business', '5489123412347777', '2028-02-28', 50000.00, 23456.78, 500.00, 10.99, 20, 10),

-- Malaysia customers
(6, 'AC100054394', 'Gold', '5489123412348888', '2027-05-31', 12000.00, 8976.50, 120.00, 16.99, 5, 22),
(7, 'AC100054395', 'Platinum', '5489123412349999', '2026-07-31', 30000.00, 18500.25, 280.00, 13.99, 12, 28),

-- Hong Kong customers
(8, 'AC100054396', 'Business', '5489123456781234', '2028-01-31', 45000.00, 30250.45, 450.00, 11.50, 18, 5),
(9, 'AC100054397', 'Platinum', '5489123456785678', '2027-10-31', 20000.00, 12450.75, 250.00, 13.50, 22, 12),

-- Indonesia customers
(10, 'AC100054398', 'Gold', '5489123456789012', '2026-06-30', 10000.00, 6785.25, 100.00, 17.50, 8, 24),
(11, 'AC100054399', 'Standard', '5489123456783456', '2025-11-30', 7500.00, 4325.50, 0.00, 19.50, 13, 29),

-- India customers
(12, 'AC100054400', 'Platinum', '5489123456787890', '2027-08-31', 18000.00, 10245.75, 220.00, 14.50, 7, 23),
(13, 'AC100054401', 'Standard', '5489123456786543', '2026-03-31', 6000.00, 3576.80, 0.00, 19.99, 17, 2),

-- Thai customers
(14, 'AC100054402', 'Gold', '5489123456785555', '2027-04-30', 14000.00, 9875.45, 130.00, 16.50, 9, 25),
(15, 'AC100054403', 'Business', '5489123456784444', '2028-03-31', 40000.00, 27834.90, 400.00, 12.50, 24, 14);

-- Insert varied transaction history with different categories and transaction types
INSERT INTO Transactions (account_id, transaction_date, settlement_date, merchant_name, merchant_id, merchant_category_code, category, transaction_amount, transaction_type, transaction_reference, currency)
VALUES
-- John Tan (SG)
(1, '2025-03-15 08:23:15', '2025-03-16 00:00:00', 'Singapore Airlines', 'SGAIR123', '3056', 'Travel', 2450.75, 'Purchase', 'T123456789', 'SGD'),
(1, '2025-03-17 12:45:30', '2025-03-18 00:00:00', 'Marina Bay Sands Hotel', 'MBS456', '7011', 'Accommodation', 1850.00, 'Purchase', 'T123456790', 'SGD'),
(1, '2025-03-20 19:12:45', '2025-03-21 00:00:00', 'Din Tai Fung', 'DTF789', '5812', 'Dining', 135.50, 'Purchase', 'T123456791', 'SGD'),
(1, '2025-03-25 14:30:00', '2025-03-26 00:00:00', 'Apple Store', 'APPLE001', '5732', 'Electronics', 3200.00, 'Purchase', 'T123456792', 'SGD'),
(1, '2025-04-01 10:15:22', '2025-04-01 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 2000.00, 'Payment', 'P123456789', 'SGD'),
(1, '2025-04-05 16:45:33', '2025-04-06 00:00:00', 'Annual Fee', NULL, NULL, 'Fee', 300.00, 'Fee', 'F123456789', 'SGD'),

-- Wei Lin Chen (SG)
(2, '2025-03-10 09:45:12', '2025-03-11 00:00:00', 'NTUC FairPrice', 'NTUC123', '5411', 'Groceries', 258.35, 'Purchase', 'T223456789', 'SGD'),
(2, '2025-03-16 13:20:45', '2025-03-17 00:00:00', 'Uniqlo Orchard', 'UNIQ456', '5651', 'Shopping', 345.90, 'Purchase', 'T223456790', 'SGD'),
(2, '2025-03-22 20:15:33', '2025-03-23 00:00:00', 'Golden Village', 'GV789', '7832', 'Entertainment', 56.00, 'Purchase', 'T223456791', 'SGD'),
(2, '2025-03-28 18:30:15', '2025-03-29 00:00:00', 'Grab Transport', 'GRAB001', '4121', 'Transportation', 32.50, 'Purchase', 'T223456792', 'SGD'),
(2, '2025-04-02 11:05:45', '2025-04-03 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 500.00, 'Payment', 'P223456789', 'SGD'),

-- Aisha Begum (SG)
(3, '2025-03-12 10:30:22', '2025-03-13 00:00:00', 'Sephora', 'SEPH123', '5977', 'Beauty', 189.75, 'Purchase', 'T323456789', 'SGD'),
(3, '2025-03-18 14:15:45', '2025-03-19 00:00:00', 'Watsons', 'WATS456', '5912', 'Health', 67.80, 'Purchase', 'T323456790', 'SGD'),
(3, '2025-03-24 16:45:12', '2025-03-25 00:00:00', 'Starbucks', 'STAR789', '5814', 'Cafes', 24.50, 'Purchase', 'T323456791', 'SGD'),
(3, '2025-03-30 09:20:33', '2025-03-31 00:00:00', 'Guardian Pharmacy', 'GUARD001', '5912', 'Health', 115.25, 'Purchase', 'T323456792', 'SGD'),
(3, '2025-04-04 13:10:15', '2025-04-05 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 300.00, 'Payment', 'P323456789', 'SGD'),

-- Add sample transactions for all other accounts with diverse merchants and categories
-- Michael Wong (SG)
(5, '2025-03-08 11:30:20', '2025-03-09 00:00:00', 'Microsoft Store', 'MSFT123', '5734', 'Software', 1999.99, 'Purchase', 'T523456789', 'SGD'),
(5, '2025-03-15 09:45:33', '2025-03-16 00:00:00', 'Shell Petroleum', 'SHELL456', '5541', 'Fuel', 125.80, 'Purchase', 'T523456790', 'SGD'),
(5, '2025-03-20 14:22:45', '2025-03-21 00:00:00', 'Marriott Hotel', 'MARR789', '7011', 'Accommodation', 3500.00, 'Purchase', 'T523456791', 'SGD'),
(5, '2025-03-25 16:15:12', '2025-03-26 00:00:00', 'Singapore Airlines', 'SGAIR001', '3056', 'Travel', 5420.75, 'Purchase', 'T523456792', 'SGD'),
(5, '2025-03-28 10:30:45', '2025-03-29 00:00:00', 'Harvey Norman', 'HARV002', '5722', 'Electronics', 2345.60, 'Purchase', 'T523456793', 'SGD'),
(5, '2025-04-02 15:45:33', '2025-04-03 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 8000.00, 'Payment', 'P523456789', 'SGD'),
(5, '2025-04-05 13:20:15', '2025-04-06 00:00:00', 'Annual Fee', NULL, NULL, 'Fee', 500.00, 'Fee', 'F523456789', 'SGD'),

-- Siti Aminah (MY)
(6, '2025-03-10 12:45:15', '2025-03-11 00:00:00', 'Pavilion KL', 'PKL123', '5311', 'Shopping', 562.50, 'Purchase', 'T623456789', 'MYR'),
(6, '2025-03-17 15:30:22', '2025-03-18 00:00:00', 'Jaya Grocer', 'JAYA456', '5411', 'Groceries', 328.45, 'Purchase', 'T623456790', 'MYR'),
(6, '2025-03-24 18:15:33', '2025-03-25 00:00:00', 'Maxis', 'MAXI789', '4812', 'Telecommunications', 188.00, 'Purchase', 'T623456791', 'MYR'),
(6, '2025-03-30 14:45:12', '2025-03-31 00:00:00', 'Guardian', 'GUARD001', '5912', 'Health', 78.90, 'Purchase', 'T623456792', 'MYR'),
(6, '2025-04-05 10:30:45', '2025-04-06 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 600.00, 'Payment', 'P623456789', 'MYR'),

-- Wing Chow (HK)
(8, '2025-03-05 09:15:22', '2025-03-06 00:00:00', 'Cathay Pacific', 'CATHY123', '3056', 'Travel', 12500.00, 'Purchase', 'T823456789', 'HKD'),
(8, '2025-03-12 13:45:33', '2025-03-13 00:00:00', 'Four Seasons Hotel', 'FOUR456', '7011', 'Accommodation', 8750.00, 'Purchase', 'T823456790', 'HKD'),
(8, '2025-03-18 16:30:15', '2025-03-19 00:00:00', 'Apple Store', 'APPLE789', '5732', 'Electronics', 9999.00, 'Purchase', 'T823456791', 'HKD'),
(8, '2025-03-25 11:20:45', '2025-03-26 00:00:00', 'HSBC Insurance', 'HSBC001', '6300', 'Insurance', 4500.00, 'Purchase', 'T823456792', 'HKD'),
(8, '2025-04-01 14:15:33', '2025-04-02 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 15000.00, 'Payment', 'P823456789', 'HKD'),
(8, '2025-04-10 10:45:15', '2025-04-11 00:00:00', 'Annual Fee', NULL, NULL, 'Fee', 450.00, 'Fee', 'F823456789', 'HKD'),

-- Sample of international transactions (currency conversion)
(9, '2025-03-20 15:30:22', '2025-03-21 00:00:00', 'Amazon US', 'AMZN123', '5942', 'Online Shopping', 425.75, 'Purchase', 'T923456789', 'USD'),
(9, '2025-03-26 17:45:33', '2025-03-27 00:00:00', 'Hilton Tokyo', 'HILT456', '7011', 'Accommodation', 3250.00, 'Purchase', 'T923456790', 'JPY'),
(9, '2025-04-03 12:15:45', '2025-04-04 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 2000.00, 'Payment', 'P923456789', 'HKD'),

-- Raj Patel (IN)
(12, '2025-03-15 14:20:15', '2025-03-16 00:00:00', 'Air India', 'AIRIN123', '3056', 'Travel', 45000.00, 'Purchase', 'T123456793', 'INR'),
(12, '2025-03-22 16:45:22', '2025-03-23 00:00:00', 'Taj Hotel', 'TAJ456', '7011', 'Accommodation', 35000.00, 'Purchase', 'T123456794', 'INR'),
(12, '2025-03-29 10:30:33', '2025-03-30 00:00:00', 'Crossword Books', 'CROSS789', '5942', 'Books', 3500.00, 'Purchase', 'T123456795', 'INR'),
(12, '2025-04-05 13:15:45', '2025-04-06 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 50000.00, 'Payment', 'P123456790', 'INR'),

-- Add some declined transactions for testing
(3, '2025-04-05 18:45:22', '2025-04-05 18:45:22', 'Louis Vuitton', 'LV123', '5631', 'Luxury', 4500.00, 'Purchase', 'T323456793', 'SGD'),
(13, '2025-04-02 15:30:33', '2025-04-02 15:30:33', 'Apple Online', 'APPLE789', '5732', 'Electronics', 85000.00, 'Purchase', 'T133456789', 'INR');

-- Update transaction status for declined transactions
UPDATE Transactions SET transaction_status = 'Declined' WHERE transaction_reference IN ('T323456793', 'T133456789');

-- Sample refunds and credits
INSERT INTO Transactions (account_id, transaction_date, settlement_date, merchant_name, merchant_id, merchant_category_code, category, transaction_amount, transaction_type, transaction_reference, currency)
VALUES
(1, '2025-04-02 09:30:15', '2025-04-03 00:00:00', 'Apple Store Refund', 'APPLE001', '5732', 'Electronics', 500.00, 'Refund', 'R123456789', 'SGD'),
(5, '2025-04-06 10:45:22', '2025-04-07 00:00:00', 'Cashback Reward', NULL, NULL, 'Rewards', 250.00, 'Credit', 'C523456789', 'SGD'),
(8, '2025-04-05 11:15:33', '2025-04-06 00:00:00', 'Disputed Charge Reversal', NULL, NULL, 'Adjustment', 1200.00, 'Credit', 'C823456789', 'HKD');

-- Insert reward points data
INSERT INTO Rewards (account_id, reward_points, tier_level, points_expiry_date)
VALUES
(1, 12500, 'Platinum', '2026-04-15'),
(2, 5800, 'Gold', '2026-04-30'),
(3, 1200, 'Standard', '2026-03-31'),
(4, 3500, 'Silver', '2026-05-31'),
(5, 25000, 'Platinum', '2026-04-30'),
(6, 7800, 'Gold', '2026-03-31'),
(7, 18500, 'Platinum', '2026-05-31'),
(8, 30000, 'Platinum', '2026-06-30'),
(9, 9500, 'Gold', '2026-04-15'),
(10, 6200, 'Silver', '2026-03-31'),
(11, 2800, 'Standard', '2026-04-30'),
(12, 8700, 'Gold', '2026-05-31'),
(13, 1500, 'Standard', '2026-03-31'),
(14, 7200, 'Gold', '2026-04-15'),
(15, 22000, 'Platinum', '2026-06-30');

-- Create View for statement generation 
CREATE OR REPLACE VIEW vw_customer_statements AS
SELECT 
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    c.phone,
    CONCAT_WS(', ', c.address, c.city, c.country, c.postal_code) AS full_address,
    a.account_id,
    a.account_number,
    a.card_number,
    a.credit_limit,
    a.available_credit,
    t.transaction_id,
    t.transaction_date,
    t.merchant_name,
    t.category,
    t.transaction_amount,
    t.transaction_type,
    t.transaction_status,
    t.currency
FROM 
    Customers c
JOIN 
    Accounts a ON c.customer_id = a.customer_id
LEFT JOIN 
    Transactions t ON a.account_id = t.account_id
WHERE
    t.transaction_status = 'Completed' OR t.transaction_status IS NULL;

-- Create Stored Procedure for calculating account summary
DELIMITER //
CREATE PROCEDURE sp_calculate_account_summary(IN p_account_id INT)
BEGIN
    SELECT
        a.account_id,
        a.account_number,
        a.card_number,
        a.credit_limit,
        a.available_credit,
        (SELECT COALESCE(SUM(transaction_amount), 0) FROM Transactions 
         WHERE account_id = p_account_id AND transaction_type = 'Purchase' AND transaction_status = 'Completed') AS total_purchases,
        (SELECT COALESCE(SUM(transaction_amount), 0) FROM Transactions 
         WHERE account_id = p_account_id AND transaction_type = 'Payment' AND transaction_status = 'Completed') AS total_payments,
        (SELECT COALESCE(SUM(transaction_amount), 0) FROM Transactions 
         WHERE account_id = p_account_id AND transaction_type = 'Fee' AND transaction_status = 'Completed') AS total_fees,
        (SELECT COALESCE(SUM(transaction_amount), 0) FROM Transactions 
         WHERE account_id = p_account_id AND (transaction_type = 'Credit' OR transaction_type = 'Refund') 
         AND transaction_status = 'Completed') AS total_credits,
        r.reward_points,
        r.tier_level
    FROM
        Accounts a
    LEFT JOIN
        Rewards r ON a.account_id = r.account_id
    WHERE
        a.account_id = p_account_id;
END //
DELIMITER ;


INSERT INTO Transactions (account_id, transaction_date, settlement_date, merchant_name, merchant_id, merchant_category_code, category, transaction_amount, transaction_type, transaction_reference, currency)
VALUES (8, '2025-03-05 09:15:22', '2025-03-06 00:00:00', 'Cathay Pacific', 'CATHY123', '3056', 'Travel', 12500.00, 'Purchase', 'T823456789', 'HKD'),
(8, '2025-03-12 13:45:33', '2025-03-13 00:00:00', 'Four Seasons Hotel', 'FOUR456', '7011', 'Accommodation', 8750.00, 'Purchase', 'T823456790', 'HKD'),
(8, '2025-03-18 16:30:15', '2025-03-19 00:00:00', 'Apple Store', 'APPLE789', '5732', 'Electronics', 9999.00, 'Purchase', 'T823456791', 'HKD'),
(8, '2025-03-25 11:20:45', '2025-03-26 00:00:00', 'HSBC Insurance', 'HSBC001', '6300', 'Insurance', 4500.00, 'Purchase', 'T823456792', 'HKD'),
(8, '2025-04-01 14:15:33', '2025-04-02 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 15000.00, 'Payment', 'P823456789', 'HKD'),
(8, '2025-04-10 10:45:15', '2025-04-11 00:00:00', 'Annual Fee', NULL, NULL, 'Fee', 450.00, 'Fee', 'F823456789', 'HKD'),
(8, '2025-04-15 12:30:22', '2025-04-16 00:00:00', 'ZARA', 'ZARA567', '5651', 'Clothing', 2450.00, 'Purchase', 'T823456793', 'HKD'),
(8, '2025-04-17 18:45:33', '2025-04-18 00:00:00', 'City Super', 'CITY890', '5411', 'Groceries', 1250.00, 'Purchase', 'T823456794', 'HKD'),
(8, '2025-04-20 09:15:45', '2025-04-21 00:00:00', 'ParknShop', 'PARK123', '5411', 'Groceries', 750.00, 'Purchase', 'T823456795', 'HKD'),
(8, '2025-04-22 14:30:15', '2025-04-23 00:00:00', 'Netflix', 'NFLX456', '4899', 'Entertainment', 120.00, 'Purchase', 'T823456796', 'HKD'),
(8, '2025-04-25 11:20:45', '2025-04-26 00:00:00', 'Spotify', 'SPOT789', '4899', 'Entertainment', 98.00, 'Purchase', 'T823456797', 'HKD'),
(8, '2025-04-28 16:15:33', '2025-04-29 00:00:00', 'Wellcome', 'WELL001', '5411', 'Groceries', 650.00, 'Purchase', 'T823456798', 'HKD'),
(8, '2025-05-01 14:15:33', '2025-05-02 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 20000.00, 'Payment', 'P823456790', 'HKD'),
(8, '2025-05-05 09:15:22', '2025-05-06 00:00:00', 'Hong Kong Airlines', 'HKAIR123', '3056', 'Travel', 5600.00, 'Purchase', 'T823456799', 'HKD'),
(8, '2025-05-08 13:45:33', '2025-05-09 00:00:00', 'InterContinental', 'INTC456', '7011', 'Accommodation', 6300.00, 'Purchase', 'T823456800', 'HKD'),
(8, '2025-05-12 16:30:15', '2025-05-13 00:00:00', 'Samsung', 'SAMS789', '5732', 'Electronics', 7500.00, 'Purchase', 'T823456801', 'HKD'),
(8, '2025-05-15 11:20:45', '2025-05-16 00:00:00', 'AIA Insurance', 'AIA001', '6300', 'Insurance', 3250.00, 'Purchase', 'T823456802', 'HKD'),
(8, '2025-05-18 14:30:15', '2025-05-19 00:00:00', 'H&M', 'HM456', '5651', 'Clothing', 1350.00, 'Purchase', 'T823456803', 'HKD'),
(8, '2025-05-22 09:15:45', '2025-05-23 00:00:00', 'AEON', 'AEON789', '5411', 'Groceries', 950.00, 'Purchase', 'T823456804', 'HKD'),
(8, '2025-05-25 18:45:33', '2025-05-26 00:00:00', 'UNIQLO', 'UNI001', '5651', 'Clothing', 1650.00, 'Purchase', 'T823456805', 'HKD'),
(8, '2025-05-28 12:30:22', '2025-05-29 00:00:00', 'Maxim Cakes', 'MAX123', '5812', 'Dining', 450.00, 'Purchase', 'T823456806', 'HKD'),
(8, '2025-06-01 14:15:33', '2025-06-02 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 18000.00, 'Payment', 'P823456791', 'HKD'),
(8, '2025-06-03 11:20:45', '2025-06-04 00:00:00', 'Apple Music', 'APPM456', '4899', 'Entertainment', 75.00, 'Purchase', 'T823456807', 'HKD'),
(8, '2025-06-05 16:15:33', '2025-06-06 00:00:00', 'HKT', 'HKT789', '4814', 'Telecommunications', 550.00, 'Purchase', 'T823456808', 'HKD'),
(8, '2025-06-08 09:15:22', '2025-06-09 00:00:00', 'China Mobile', 'CMOB001', '4814', 'Telecommunications', 350.00, 'Purchase', 'T823456809', 'HKD'),
(8, '2025-06-12 13:45:33', '2025-06-13 00:00:00', 'Amazon', 'AMZN123', '5942', 'Retail', 1250.00, 'Purchase', 'T823456810', 'HKD'),
(8, '2025-06-15 16:30:15', '2025-06-16 00:00:00', 'Fortress', 'FORT456', '5732', 'Electronics', 3600.00, 'Purchase', 'T823456811', 'HKD'),
(8, '2025-06-18 11:20:45', '2025-06-19 00:00:00', 'Starbucks', 'STAR789', '5814', 'Dining', 85.00, 'Purchase', 'T823456812', 'HKD'),
(8, '2025-06-22 14:30:15', '2025-06-23 00:00:00', 'Pacific Coffee', 'PCOF001', '5814', 'Dining', 75.00, 'Purchase', 'T823456813', 'HKD'),
(8, '2025-06-25 09:15:45', '2025-06-26 00:00:00', 'Mannings', 'MANN123', '5912', 'Healthcare', 650.00, 'Purchase', 'T823456814', 'HKD'),
(8, '2025-06-28 18:45:33', '2025-06-29 00:00:00', 'Watson', 'WATS456', '5912', 'Healthcare', 480.00, 'Purchase', 'T823456815', 'HKD'),
(8, '2025-07-01 14:15:33', '2025-07-02 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 12000.00, 'Payment', 'P823456792', 'HKD'),
(8, '2025-07-03 12:30:22', '2025-07-04 00:00:00', 'MTR', 'MTR789', '4111', 'Transportation', 550.00, 'Purchase', 'T823456816', 'HKD'),
(8, '2025-07-05 11:20:45', '2025-07-06 00:00:00', 'Octopus', 'OCTO001', '4111', 'Transportation', 500.00, 'Purchase', 'T823456817', 'HKD'),
(8, '2025-07-08 16:15:33', '2025-07-09 00:00:00', 'CSL', 'CSL123', '4814', 'Telecommunications', 450.00, 'Purchase', 'T823456818', 'HKD'),
(8, '2025-07-12 09:15:22', '2025-07-13 00:00:00', 'Emirates', 'EMIR456', '3056', 'Travel', 15600.00, 'Purchase', 'T823456819', 'HKD'),
(8, '2025-07-15 13:45:33', '2025-07-16 00:00:00', 'Mandarin Oriental', 'MAND789', '7011', 'Accommodation', 12450.00, 'Purchase', 'T823456820', 'HKD'),
(8, '2025-07-18 16:30:15', '2025-07-19 00:00:00', 'Sony', 'SONY001', '5732', 'Electronics', 6250.00, 'Purchase', 'T823456821', 'HKD'),
(8, '2025-07-22 11:20:45', '2025-07-23 00:00:00', 'Pruudential', 'PRUD123', '6300', 'Insurance', 2750.00, 'Purchase', 'T823456822', 'HKD'),
(8, '2025-07-25 14:30:15', '2025-07-26 00:00:00', 'Gap', 'GAP456', '5651', 'Clothing', 1550.00, 'Purchase', 'T823456823', 'HKD'),
(8, '2025-07-28 09:15:45', '2025-07-29 00:00:00', 'Taste', 'TAST789', '5411', 'Groceries', 1150.00, 'Purchase', 'T823456824', 'HKD'),
(8, '2025-08-01 14:15:33', '2025-08-02 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 25000.00, 'Payment', 'P823456793', 'HKD'),
(8, '2025-08-03 18:45:33', '2025-08-04 00:00:00', 'Muji', 'MUJI001', '5651', 'Clothing', 2350.00, 'Purchase', 'T823456825', 'HKD'),
(8, '2025-08-05 12:30:22', '2025-08-06 00:00:00', 'Cafe de Coral', 'CDC123', '5812', 'Dining', 175.00, 'Purchase', 'T823456826', 'HKD'),
(8, '2025-08-08 11:20:45', '2025-08-09 00:00:00', 'Disney+', 'DIS456', '4899', 'Entertainment', 88.00, 'Purchase', 'T823456827', 'HKD'),
(8, '2025-08-12 16:15:33', '2025-08-13 00:00:00', '3HK', '3HK789', '4814', 'Telecommunications', 380.00, 'Purchase', 'T823456828', 'HKD'),
(8, '2025-08-15 09:15:22', '2025-08-16 00:00:00', 'Singapore Airlines', 'SIA001', '3056', 'Travel', 9800.00, 'Purchase', 'T823456829', 'HKD'),
(8, '2025-08-18 13:45:33', '2025-08-19 00:00:00', 'Hilton', 'HILT123', '7011', 'Accommodation', 7650.00, 'Purchase', 'T823456830', 'HKD'),
(8, '2025-08-22 16:30:15', '2025-08-23 00:00:00', 'Huawei', 'HUAW456', '5732', 'Electronics', 5450.00, 'Purchase', 'T823456831', 'HKD'),
(8, '2025-08-25 11:20:45', '2025-08-26 00:00:00', 'FWD Insurance', 'FWD789', '6300', 'Insurance', 3150.00, 'Purchase', 'T823456832', 'HKD'),
(8, '2025-08-28 14:30:15', '2025-08-29 00:00:00', 'Adidas', 'ADID001', '5651', 'Clothing', 2250.00, 'Purchase', 'T823456833', 'HKD'),
(8, '2025-09-01 14:15:33', '2025-09-02 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 23000.00, 'Payment', 'P823456794', 'HKD'),
(8, '2025-09-03 09:15:45', '2025-09-04 00:00:00', 'Market Place', 'MRKP123', '5411', 'Groceries', 1450.00, 'Purchase', 'T823456834', 'HKD'),
(8, '2025-09-05 18:45:33', '2025-09-06 00:00:00', 'Nike', 'NIKE456', '5651', 'Clothing', 2750.00, 'Purchase', 'T823456835', 'HKD'),
(8, '2025-09-08 12:30:22', '2025-09-09 00:00:00', 'KFC', 'KFC789', '5812', 'Dining', 210.00, 'Purchase', 'T823456836', 'HKD'),
(8, '2025-09-12 11:20:45', '2025-09-13 00:00:00', 'YouTube Premium', 'YT001', '4899', 'Entertainment', 98.00, 'Purchase', 'T823456837', 'HKD'),
(8, '2025-09-15 16:15:33', '2025-09-16 00:00:00', 'SmarTone', 'SMRT123', '4814', 'Telecommunications', 480.00, 'Purchase', 'T823456838', 'HKD'),
(8, '2025-09-18 09:15:22', '2025-09-19 00:00:00', 'Japan Airlines', 'JAL456', '3056', 'Travel', 8500.00, 'Purchase', 'T823456839', 'HKD'),
(8, '2025-09-22 13:45:33', '2025-09-23 00:00:00', 'Sheraton', 'SHER789', '7011', 'Accommodation', 9350.00, 'Purchase', 'T823456840', 'HKD'),
(8, '2025-09-25 16:30:15', '2025-09-26 00:00:00', 'Lenovo', 'LENV001', '5732', 'Electronics', 8750.00, 'Purchase', 'T823456841', 'HKD'),
(8, '2025-09-28 11:20:45', '2025-09-29 00:00:00', 'AXA Insurance', 'AXA123', '6300', 'Insurance', 3650.00, 'Purchase', 'T823456842', 'HKD'),
(8, '2025-10-01 14:15:33', '2025-10-02 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 27000.00, 'Payment', 'P823456795', 'HKD'),
(8, '2025-10-03 14:30:15', '2025-10-04 00:00:00', 'Puma', 'PUMA456', '5651', 'Clothing', 1850.00, 'Purchase', 'T823456843', 'HKD'),
(8, '2025-10-05 09:15:45', '2025-10-06 00:00:00', 'Fusion', 'FUSI789', '5411', 'Groceries', 950.00, 'Purchase', 'T823456844', 'HKD'),
(8, '2025-10-08 18:45:33', '2025-10-09 00:00:00', 'Uniqlo', 'UNIQ001', '5651', 'Clothing', 1950.00, 'Purchase', 'T823456845', 'HKD'),
(8, '2025-10-10 10:45:15', '2025-10-11 00:00:00', 'Annual Fee', NULL, NULL, 'Fee', 450.00, 'Fee', 'F823456790', 'HKD'),
(8, '2025-10-12 12:30:22', '2025-10-13 00:00:00', 'McDonald', 'MCD123', '5812', 'Dining', 165.00, 'Purchase', 'T823456846', 'HKD'),
(8, '2025-10-15 11:20:45', '2025-10-16 00:00:00', 'HBO GO', 'HBO456', '4899', 'Entertainment', 108.00, 'Purchase', 'T823456847', 'HKD'),
(8, '2025-10-18 16:15:33', '2025-10-19 00:00:00', 'PCCW', 'PCCW789', '4814', 'Telecommunications', 620.00, 'Purchase', 'T823456848', 'HKD'),
(8, '2025-10-22 09:15:22', '2025-10-23 00:00:00', 'Korean Air', 'KAL001', '3056', 'Travel', 7800.00, 'Purchase', 'T823456849', 'HKD'),
(8, '2025-10-25 13:45:33', '2025-10-26 00:00:00', 'Conrad', 'CONR123', '7011', 'Accommodation', 10250.00, 'Purchase', 'T823456850', 'HKD'),
(8, '2025-10-28 16:30:15', '2025-10-29 00:00:00', 'Dell', 'DELL456', '5732', 'Electronics', 12350.00, 'Purchase', 'T823456851', 'HKD'),
(8, '2025-11-01 14:15:33', '2025-11-02 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 23000.00, 'Payment', 'P823456796', 'HKD'),
(8, '2025-11-03 11:20:45', '2025-11-04 00:00:00', 'Manulife', 'MANU789', '6300', 'Insurance', 4250.00, 'Purchase', 'T823456852', 'HKD'),
(8, '2025-11-05 14:30:15', '2025-11-06 00:00:00', 'Giordano', 'GIOR001', '5651', 'Clothing', 850.00, 'Purchase', 'T823456853', 'HKD'),
(8, '2025-11-08 09:15:45', '2025-11-09 00:00:00', 'YATA', 'YATA123', '5411', 'Groceries', 1650.00, 'Purchase', 'T823456854', 'HKD'),
(8, '2025-11-12 18:45:33', '2025-11-13 00:00:00', 'Bossini', 'BOSS456', '5651', 'Clothing', 1350.00, 'Purchase', 'T823456855', 'HKD'),
(8, '2025-11-15 12:30:22', '2025-11-16 00:00:00', 'Pizza Hut', 'PIZZ789', '5812', 'Dining', 320.00, 'Purchase', 'T823456856', 'HKD'),
(8, '2025-11-18 11:20:45', '2025-11-19 00:00:00', 'Amazon Prime', 'AMZP001', '4899', 'Entertainment', 88.00, 'Purchase', 'T823456857', 'HKD'),
(8, '2025-11-22 16:15:33', '2025-11-23 00:00:00', 'i-Cable', 'ICAB123', '4814', 'Telecommunications', 350.00, 'Purchase', 'T823456858', 'HKD'),
(8, '2025-11-25 09:15:22', '2025-11-26 00:00:00', 'Air China', 'AIRC456', '3056', 'Travel', 6400.00, 'Purchase', 'T823456859', 'HKD'),
(8, '2025-11-28 13:45:33', '2025-11-29 00:00:00', 'Holiday Inn', 'HOLI789', '7011', 'Accommodation', 5650.00, 'Purchase', 'T823456860', 'HKD'),
(8, '2025-12-01 14:15:33', '2025-12-02 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 21000.00, 'Payment', 'P823456797', 'HKD'),
(8, '2025-12-03 16:30:15', '2025-12-04 00:00:00', 'Xiaomi', 'XIAO001', '5732', 'Electronics', 4350.00, 'Purchase', 'T823456861', 'HKD'),
(8, '2025-12-05 11:20:45', '2025-12-06 00:00:00', 'Zurich Insurance', 'ZURI123', '6300', 'Insurance', 2950.00, 'Purchase', 'T823456862', 'HKD'),
(8, '2025-12-08 14:30:15', '2025-12-09 00:00:00', 'Balenciaga', 'BALE456', '5651', 'Clothing', 15350.00, 'Purchase', 'T823456863', 'HKD'),
(8, '2025-12-12 09:15:45', '2025-12-13 00:00:00', 'JUSCO', 'JUSC789', '5411', 'Groceries', 2150.00, 'Purchase', 'T823456864', 'HKD'),
(8, '2025-12-15 18:45:33', '2025-12-16 00:00:00', 'Tommy Hilfiger', 'TOMM001', '5651', 'Clothing', 3650.00, 'Purchase', 'T823456865', 'HKD'),
(8, '2025-12-18 12:30:22', '2025-12-19 00:00:00', 'Tsui Wah', 'TSUI123', '5812', 'Dining', 450.00, 'Purchase', 'T823456866', 'HKD'),
(8, '2025-12-22 11:20:45', '2025-12-23 00:00:00', 'Viu TV', 'VIU456', '4899', 'Entertainment', 68.00, 'Purchase', 'T823456867', 'HKD'),
(8, '2025-12-25 16:15:33', '2025-12-26 00:00:00', 'Hutchison', 'HUTC789', '4814', 'Telecommunications', 480.00, 'Purchase', 'T823456868', 'HKD'),
(8, '2025-12-28 09:15:22', '2025-12-29 00:00:00', 'Eva Air', 'EVA001', '3056', 'Travel', 9200.00, 'Purchase', 'T823456869', 'HKD'),
(8, '2026-01-01 14:15:33', '2026-01-02 00:00:00', 'Payment Thank You', NULL, NULL, 'Payment', 32000.00, 'Payment', 'P823456798', 'HKD'),
(8, '2026-01-03 13:45:33', '2026-01-04 00:00:00', 'JW Marriott', 'JWM123', '7011', 'Accommodation', 11450.00, 'Purchase', 'T823456870', 'HKD'),
(8, '2026-01-05 16:30:15', '2026-01-06 00:00:00', 'LG', 'LG456', '5732', 'Electronics', 6750.00, 'Purchase', 'T823456871', 'HKD'),
(8, '2026-01-08 11:20:45', '2026-01-09 00:00:00', 'MetLife', 'METL789', '6300', 'Insurance', 3850.00, 'Purchase', 'T823456872', 'HKD'),
(8, '2026-01-10 10:45:15', '2026-01-11 00:00:00', 'Late Payment Fee', NULL, NULL, 'Fee', 300.00, 'Fee', 'F823456791', 'HKD'),
(8, '2026-01-12 14:30:15', '2026-01-13 00:00:00', 'CK', 'CK001', '5651', 'Clothing', 4250.00, 'Purchase', 'T823456873', 'HKD'),
(8, '2026-01-15 09:15:45', '2026-01-16 00:00:00', 'DON DON DONKI', 'DONK123', '5411', 'Groceries', 2350.00, 'Purchase', 'T823456874', 'HKD'),
(8, '2026-01-18 18:45:33', '2026-01-19 00:00:00', 'Levi', 'LEVI456', '5651', 'Clothing', 1950.00, 'Purchase', 'T823456875', 'HKD'),
(8, '2026-01-22 12:30:22', '2026-01-23 00:00:00', 'Subway', 'SUB789', '5812', 'Dining', 95.00, 'Purchase', 'T823456876', 'HKD'),
(8, '2026-01-25 11:20:45', '2026-01-26 00:00:00', 'Apple TV+', 'APTV001', '4899', 'Entertainment', 58.00, 'Purchase', 'T823456877', 'HKD'),
(8, '2026-01-28 16:15:33', '2026-01-29 00:00:00', 'HKBN', 'HKBN123', '4814', 'Telecommunications', 280.00, 'Purchase', 'T823456878', 'HKD');