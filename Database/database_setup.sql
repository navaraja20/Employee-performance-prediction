-- 1. Login to PostgreSQL
psql -U postgres

-- 2. List databases
\l

-- 3. Create your database (if not done already)
CREATE DATABASE employee_prediction;

-- 4. Connect to your database
\c employee_prediction

-- 5. Create the table (run this script after connecting)
-- (copy/paste the above CREATE TABLE block)

-- 6. List tables
\dt

-- 7. Describe structure of table
\d public.predictions

-- 8. View predictions
SELECT * FROM public.predictions LIMIT 10;

-- 9. Exit
\q

-- Create the predictions table for employee performance prediction
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    gender VARCHAR(50),
    age INTEGER,
    job_role VARCHAR(100),
    monthly_income FLOAT,
    job_satisfaction VARCHAR(50),
    performance_prediction VARCHAR(20),
    prediction_confidence FLOAT,
    source VARCHAR(50),
    prediction_date TIMESTAMP,
    actual_label VARCHAR(20)
);

-- Create validation statistics table
CREATE TABLE IF NOT EXISTS validation_statistics (
    id SERIAL PRIMARY KEY,
    filepath TEXT,
    total_rows INTEGER,
    valid_rows INTEGER,
    invalid_rows INTEGER,
    criticality VARCHAR(20),
    errors_summary TEXT,
    error_counts JSONB,
    created_on TIMESTAMP,
    bad_row_indices TEXT
);

CREATE TABLE IF NOT EXISTS processed_files (
    file_name TEXT PRIMARY KEY,
    processed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Training data table (for Grafana drift analysis)
CREATE TABLE IF NOT EXISTS training_data (
    id SERIAL PRIMARY KEY,
    age INTEGER,
    gender VARCHAR(50),
    job_role VARCHAR(100),
    monthly_income FLOAT,
    job_satisfaction VARCHAR(50),
    performance_rating VARCHAR(20),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

