-- Create the Employees Table
CREATE TABLE IF NOT EXISTS employees (
    employee_id SERIAL PRIMARY KEY,
    age INT,
    gender TEXT,
    marital_status TEXT,
    job_role TEXT,
    department TEXT,
    business_travel TEXT,
    years_at_company INT,
    total_working_years INT,
    years_in_current_role INT,
    years_since_last_promotion INT,
    monthly_income INT,
    hourly_rate INT,
    stock_option_level INT,
    percent_salary_hike INT,
    job_satisfaction INT,
    work_life_balance INT,
    job_involvement INT,
    environment_satisfaction INT,
    performance_rating INT,
    overtime TEXT
);

-- Create the Predictions Table
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employees(employee_id),
    performance_score FLOAT,
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
