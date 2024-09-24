CREATE DATABASE hospital_db;
USE hospital_db;
CREATE TABLE hospitals (
    reg_no VARCHAR(10) PRIMARY KEY,      -- Registration number of the hospital
    name VARCHAR(100),                   -- Hospital name
    rating DECIMAL(2, 1),                -- Hospital rating (e.g., 4.5)
    bed_capacity INT,                    -- Number of beds available in the hospital
    num_doctors INT                      -- Number of doctors in the hospital
);
INSERT INTO hospitals (reg_no, name, rating, bed_capacity, num_doctors)
VALUES ('H001', 'City Hospital', 4.5, 100, 20);
DELETE FROM hospitals WHERE reg_no = 'H001';
SELECT * FROM hospitals 
WHERE reg_no LIKE '%H%' 
   OR name LIKE '%City%' 
   OR rating LIKE '4.5' 
   OR bed_capacity LIKE '100' 
   OR num_doctors LIKE '20';

UPDATE hospitals 
SET name = 'Updated Hospital', rating = 4.6, bed_capacity = 150, num_doctors = 25 
WHERE reg_no = 'H001';