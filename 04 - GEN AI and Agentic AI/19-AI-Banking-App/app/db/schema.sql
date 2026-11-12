-- Banking analytics schema (MySQL 8 / AWS RDS)

CREATE TABLE IF NOT EXISTS branches (
    branch_id    INT PRIMARY KEY AUTO_INCREMENT,
    branch_name  VARCHAR(100) NOT NULL,
    city         VARCHAR(50)  NOT NULL,
    state        VARCHAR(50)  NOT NULL,
    opened_on    DATE         NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id     INT PRIMARY KEY AUTO_INCREMENT,
    customer_name  VARCHAR(100) NOT NULL,
    branch_id      INT          NOT NULL,
    account_type   VARCHAR(20)  NOT NULL,          -- SAVINGS / CURRENT
    balance        DECIMAL(15,2) NOT NULL DEFAULT 0,
    status         VARCHAR(20)  NOT NULL,          -- ACTIVE / DORMANT / CLOSED
    opened_on      DATE         NOT NULL,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id        INT PRIMARY KEY AUTO_INCREMENT,
    account_id     INT          NOT NULL,
    branch_id      INT          NOT NULL,
    loan_type      VARCHAR(20)  NOT NULL,          -- HOME / PERSONAL / CAR / EDUCATION
    amount         DECIMAL(15,2) NOT NULL,
    interest_rate  DECIMAL(5,2) NOT NULL,
    status         VARCHAR(20)  NOT NULL,          -- APPROVED / REJECTED / PENDING
    applied_on     DATE         NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (branch_id)  REFERENCES branches(branch_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    txn_id      BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_id  INT           NOT NULL,
    branch_id   INT           NOT NULL,
    txn_type    VARCHAR(10)   NOT NULL,            -- CREDIT (incoming) / DEBIT (outgoing)
    category    VARCHAR(20)   NOT NULL,            -- DEPOSIT / WITHDRAWAL / TRANSFER / FEE / INTEREST
    amount      DECIMAL(15,2) NOT NULL,
    txn_date    DATE          NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (branch_id)  REFERENCES branches(branch_id),
    INDEX idx_txn_date (txn_date),
    INDEX idx_txn_branch (branch_id)
);

-- Bank revenue = FEE + INTEREST transactions (money the bank earns)
