CREATE DATABASE loan_db;

USE loan_db;

CREATE TABLE loan_applications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gender VARCHAR(20),
    married VARCHAR(10),
    dependents VARCHAR(10),
    education VARCHAR(30),
    self_employed VARCHAR(10),
    applicant_income DOUBLE,
    coapplicant_income DOUBLE,
    loan_amount DOUBLE,
    loan_term INT,
    credit_history DOUBLE,
    property_area VARCHAR(30),
    loan_status VARCHAR(5)
);

USE loan_db;

INSERT INTO loan_applications
(
    gender,
    married,
    dependents,
    education,
    self_employed,
    applicant_income,
    coapplicant_income,
    loan_amount,
    loan_term,
    credit_history,
    property_area,
    loan_status
)
VALUES

('Male', 'Yes', '0', 'Graduate', 'No', 5000, 1000, 150, 360, 1, 'Urban', 'Y'),

('Female', 'No', '0', 'Graduate', 'No', 3000, 0, 80, 360, 1, 'Rural', 'Y'),

('Male', 'Yes', '2', 'Graduate', 'No', 4000, 2000, 120, 360, 1, 'Semiurban', 'Y'),

('Male', 'No', '0', 'Not Graduate', 'Yes', 2000, 0, 50, 180, 0, 'Rural', 'N'),

('Female', 'Yes', '1', 'Graduate', 'No', 6000, 1500, 200, 360, 1, 'Urban', 'Y'),

('Male', 'Yes', '3+', 'Graduate', 'No', 2500, 1000, 180, 360, 0, 'Rural', 'N'),

('Female', 'No', '0', 'Not Graduate', 'No', 3500, 500, 100, 360, 1, 'Semiurban', 'Y'),

('Male', 'Yes', '1', 'Graduate', 'Yes', 8000, 2000, 250, 360, 1, 'Urban', 'Y'),

('Male', 'No', '2', 'Graduate', 'No', 1800, 0, 70, 180, 0, 'Rural', 'N'),

('Female', 'Yes', '0', 'Graduate', 'No', 4500, 1000, 130, 360, 1, 'Semiurban', 'Y'),

('Male', 'Yes', '0', 'Not Graduate', 'No', 2200, 500, 90, 360, 0, 'Rural', 'N'),

('Female', 'No', '1', 'Graduate', 'Yes', 7000, 0, 160, 360, 1, 'Urban', 'Y'),

('Male', 'Yes', '2', 'Graduate', 'No', 5500, 1500, 200, 360, 1, 'Semiurban', 'Y'),

('Female', 'No', '0', 'Not Graduate', 'No', 1500, 0, 60, 180, 0, 'Rural', 'N'),

('Male', 'Yes', '1', 'Graduate', 'No', 9000, 2000, 300, 360, 1, 'Urban', 'Y');


-- Check inserted records

SELECT * FROM loan_applications;

-- Count total records

SELECT COUNT(*) FROM loan_applications;