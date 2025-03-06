-- Create the new database
CREATE DATABASE IF NOT EXISTS employee_performance;

-- Connect to the new database
\c employee_performance

-- Create the Employee Predictions Table
CREATE TABLE IF NOT EXISTS employee_predictions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age INT NOT NULL,
    gender TEXT NOT NULL,
    marital_status TEXT,
    job_role TEXT NOT NULL,
    department TEXT NOT NULL,
    business_travel TEXT,
    years_at_company INT NOT NULL,
    total_working_years INT NOT NULL,
    years_in_current_role INT NOT NULL,
    years_since_last_promotion INT NOT NULL,
    monthly_income FLOAT NOT NULL,
    hourly_rate FLOAT NOT NULL,
    stock_option_level INT NOT NULL,
    percent_salary_hike FLOAT NOT NULL,
    job_satisfaction INT NOT NULL,
    work_life_balance INT NOT NULL,
    job_involvement INT NOT NULL,
    environment_satisfaction INT NOT NULL,
    performance_rating INT NOT NULL,
    overtime TEXT NOT NULL,
    prediction_score FLOAT
);

-- Create the Predictions Table
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employee_predictions(id) ON DELETE CASCADE,
    performance_score FLOAT NOT NULL,
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table to store model metadata
CREATE TABLE IF NOT EXISTS model_metadata (
    id SERIAL PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    trained_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accuracy FLOAT NOT NULL
);

-- Create table to log training executions
CREATE TABLE IF NOT EXISTS training_logs (
    id SERIAL PRIMARY KEY,
    dag_name TEXT NOT NULL,
    execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for commonly queried fields
CREATE INDEX idx_department ON employee_predictions(department);
CREATE INDEX idx_job_role ON employee_predictions(job_role);
CREATE INDEX idx_performance_rating ON employee_predictions(performance_rating);
CREATE INDEX idx_years_at_company ON employee_predictions(years_at_company);
CREATE INDEX idx_overtime ON employee_predictions(overtime);

-- Create partitioned table for employees
CREATE TABLE IF NOT EXISTS employee_predictions_partitioned (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age INT NOT NULL,
    gender TEXT NOT NULL,
    marital_status TEXT,
    job_role TEXT NOT NULL,
    department TEXT NOT NULL,
    years_at_company INT NOT NULL,
    monthly_income FLOAT NOT NULL,
    performance_rating INT NOT NULL
) PARTITION BY LIST (department);

-- Create partitions
CREATE TABLE employee_predictions_it PARTITION OF employee_predictions_partitioned FOR VALUES IN ('IT');
CREATE TABLE employee_predictions_hr PARTITION OF employee_predictions_partitioned FOR VALUES IN ('HR');
CREATE TABLE employee_predictions_sales PARTITION OF employee_predictions_partitioned FOR VALUES IN ('Sales');
