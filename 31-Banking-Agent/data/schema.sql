-- Bank database schema (MySQL 8)
-- Run automatically by:  python -m data.seed_mysql

DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS branches;

CREATE TABLE branches (
    branch_id    VARCHAR(10)  PRIMARY KEY,
    branch_name  VARCHAR(100) NOT NULL,
    city         VARCHAR(50)  NOT NULL
);

CREATE TABLE accounts (
    account_id     VARCHAR(10)  PRIMARY KEY,
    customer_name  VARCHAR(100) NOT NULL,
    branch_id      VARCHAR(10)  NOT NULL,
    account_type   VARCHAR(10)  NOT NULL,          -- SAVINGS / CURRENT
    balance        DECIMAL(15,2) NOT NULL,
    opened_date    DATE         NOT NULL,
    status         VARCHAR(10)  NOT NULL,          -- ACTIVE / DORMANT / CLOSED
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE transactions (
    txn_id      VARCHAR(12)   PRIMARY KEY,
    account_id  VARCHAR(10)   NOT NULL,
    branch_id   VARCHAR(10)   NOT NULL,
    txn_date    DATE          NOT NULL,
    txn_type    VARCHAR(10)   NOT NULL,            -- CREDIT (incoming) / DEBIT (outgoing)
    channel     VARCHAR(10)   NOT NULL,            -- UPI / NEFT / ATM / BRANCH
    amount      DECIMAL(15,2) NOT NULL,
    fee         DECIMAL(12,2) NOT NULL,            -- bank revenue (0.5%)
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (branch_id)  REFERENCES branches(branch_id)
);

CREATE TABLE loans (
    loan_id         VARCHAR(10)   PRIMARY KEY,
    account_id      VARCHAR(10)   NOT NULL,
    branch_id       VARCHAR(10)   NOT NULL,
    loan_type       VARCHAR(20)   NOT NULL,        -- HOME / PERSONAL / CAR / EDUCATION
    amount          DECIMAL(15,2) NOT NULL,
    credit_score    INT           NOT NULL,
    applied_date    DATE          NOT NULL,
    status          VARCHAR(10)   NOT NULL,        -- APPROVED / PENDING / REJECTED
    processing_fee  DECIMAL(12,2) NOT NULL,        -- bank revenue (1% of approved)
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (branch_id)  REFERENCES branches(branch_id)
);

CREATE INDEX idx_txn_date  ON transactions(txn_date);
CREATE INDEX idx_loan_date ON loans(applied_date);
