CREATE DATABASE IF NOT EXISTS banking_ai;
USE banking_ai;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(120),
    city VARCHAR(80)
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    account_type ENUM('SAVINGS','CURRENT','FIXED_DEPOSIT') NOT NULL,
    balance DECIMAL(14,2) NOT NULL DEFAULT 0,
    status ENUM('ACTIVE','INACTIVE','CLOSED') NOT NULL DEFAULT 'ACTIVE',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    transaction_type ENUM('DEPOSIT','WITHDRAWAL') NOT NULL,
    amount DECIMAL(14,2) NOT NULL,
    transaction_date DATETIME NOT NULL,
    status ENUM('SUCCESS','FAILED','PENDING') NOT NULL DEFAULT 'SUCCESS',
    description VARCHAR(255),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

INSERT INTO customers VALUES
(1,'Ananya Rao','ananya@example.com','Hyderabad'),
(2,'Rahul Sharma','rahul@example.com','Bengaluru'),
(3,'Priya Reddy','priya@example.com','Hyderabad'),
(4,'Kiran Kumar','kiran@example.com','Chennai');

INSERT INTO accounts VALUES
(1,1,'1000001001','SAVINGS',125000,'ACTIVE'),
(2,2,'1000001002','CURRENT',550000,'ACTIVE'),
(3,3,'1000001003','SAVINGS',78000,'ACTIVE'),
(4,4,'1000001004','FIXED_DEPOSIT',300000,'ACTIVE');

INSERT INTO transactions VALUES
(1,1,'DEPOSIT',25000,'2026-11-02 10:15:00','SUCCESS','Salary credit'),
(2,1,'WITHDRAWAL',5000,'2026-11-03 12:30:00','SUCCESS','ATM withdrawal'),
(3,2,'DEPOSIT',150000,'2026-11-05 09:00:00','SUCCESS','Business payment'),
(4,3,'WITHDRAWAL',2500,'2026-11-06 16:45:00','FAILED','UPI payment'),
(5,4,'DEPOSIT',100000,'2026-11-08 11:00:00','SUCCESS','FD investment');
