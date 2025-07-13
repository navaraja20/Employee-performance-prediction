-- Grafana Monitoring SQL Queries
-- For Data Ingestion Quality, Drift, and Prediction Monitoring (Employee Performance)

-- ===============================
-- Ingested Data Monitoring Dashboard
-- ===============================

-- 🔘 Invalid Rows Percentage Gauge (Last 10 Minutes)
SELECT
  MAX(created_on) AS "time",
  CASE 
    WHEN COUNT(*) = 0 THEN 0
    ELSE (SUM(invalid_rows)::float / NULLIF(SUM(total_rows), 0)) * 100 
  END AS invalid_percentage
FROM validation_statistics
WHERE created_on >= NOW() - INTERVAL '10 minutes'
  AND criticality = 'critical';

-- 🔸 Valid vs Invalid (Mocked using counts) - Last 10 records
SELECT
  created_on AS "time",
  valid_rows,
  invalid_rows
FROM validation_statistics
ORDER BY created_on DESC
LIMIT 10;

-- 🔺 Missing Values Drift Over Time (simulate via regex on issue string)
SELECT
  date_trunc('minute', created_on) 
    - INTERVAL '1 minute' * (EXTRACT(MINUTE FROM created_on)::int % 10) AS time,
  COUNT(*) FILTER (WHERE errors_summary ILIKE '%missing%') * 100.0 / NULLIF(COUNT(*), 0) AS missing_percentage
FROM validation_statistics
WHERE created_on >= NOW() - INTERVAL '24 hours'
GROUP BY time
ORDER BY time;

-- ❗ Error Category Breakdown (Last 1 Hour)
SELECT 'Missing Values' AS error_type, COUNT(*) FROM validation_statistics
WHERE created_on >= NOW() - INTERVAL '1 hour' AND errors_summary ILIKE '%missing%'

UNION ALL

SELECT 'Invalid Categories', COUNT(*) FROM validation_statistics
WHERE created_on >= NOW() - INTERVAL '1 hour' AND errors_summary ILIKE '%invalid%'

UNION ALL

SELECT 'Out of Range', COUNT(*) FROM validation_statistics
WHERE created_on >= NOW() - INTERVAL '1 hour' AND errors_summary ILIKE '%out_of_range%'

UNION ALL

SELECT 'Wrong Types', COUNT(*) FROM validation_statistics
WHERE created_on >= NOW() - INTERVAL '1 hour' AND errors_summary ILIKE '%type%'

UNION ALL

SELECT 'Format Errors', COUNT(*) FROM validation_statistics
WHERE created_on >= NOW() - INTERVAL '1 hour' AND errors_summary ILIKE '%format%'

UNION ALL

SELECT 'Missing Columns', COUNT(*) FROM validation_statistics
WHERE created_on >= NOW() - INTERVAL '1 hour' AND errors_summary ILIKE '%missing_job_role_column%';

-- ❓ Distribution of Error Types (Last 30 mins)
SELECT error_type, COUNT(*) AS total_errors
FROM (
  SELECT 
    created_on,
    CASE
      WHEN errors_summary ILIKE '%missing_age%' THEN 'missing_age'
      WHEN errors_summary ILIKE '%missing_gender%' THEN 'missing_gender'
      WHEN errors_summary ILIKE '%missing_monthly_income%' THEN 'missing_monthly_income'
      WHEN errors_summary ILIKE '%missing_job_satisfaction%' THEN 'missing_job_satisfaction'
      WHEN errors_summary ILIKE '%missing_job_role_column%' THEN 'missing_job_role_column'
      ELSE 'other'
    END AS error_type
  FROM validation_statistics
  WHERE created_on >= NOW() - INTERVAL '30 minutes'
) err_group
GROUP BY error_type
ORDER BY total_errors DESC;

-- ===============================
-- Data Drift and Prediction Monitoring Dashboard
-- ===============================

-- 🎯 Prediction Class Distribution (Last 1 Hour)
SELECT
  performance_prediction AS prediction_class,
  COUNT(*) AS count
FROM predictions
WHERE prediction_date >= NOW() - INTERVAL '1 hour'
GROUP BY performance_prediction;

-- 📉 Model Confidence Over Time (Last 24 Hours)
SELECT
  date_trunc('minute', prediction_date) 
    + INTERVAL '30 minutes' * FLOOR(EXTRACT(MINUTE FROM prediction_date) / 30) AS "time",
  AVG(prediction_confidence) AS avg_confidence
FROM predictions
WHERE prediction_date >= NOW() - INTERVAL '24 hours'
  AND prediction_confidence IS NOT NULL
GROUP BY 1
ORDER BY 1;

-- 📊 Age Drift vs Training Data (Assumes training_data exists)
WITH training_avg AS (
  SELECT AVG(age) AS base_age FROM training_data
),
pred_half_hourly AS (
  SELECT 
    date_trunc('hour', prediction_date) + 
      INTERVAL '30 minutes' * FLOOR(EXTRACT(MINUTE FROM prediction_date) / 30) AS time,
    AVG(age) AS pred_age
  FROM predictions
  WHERE prediction_date >= NOW() - INTERVAL '24 hours'
  GROUP BY time
)
SELECT 
  time,
  pred_age,
  training_avg.base_age,
  ABS(pred_age - training_avg.base_age) AS drift_amount
FROM pred_half_hourly, training_avg
ORDER BY time;

-- 🟢 Model Accuracy Over Time (requires ground truth data)
-- This is a placeholder - needs actual labeled data to calculate accuracy
SELECT 
  date_trunc('hour', prediction_date) AS time,
  COUNT(*) AS predictions_made,
  AVG(prediction_confidence) AS avg_confidence
FROM predictions
WHERE prediction_date >= NOW() - INTERVAL '24 hours'
GROUP BY time
ORDER BY time;

-- Note: The following query is commented out since there's no actual_label column
-- To calculate real accuracy, you would need:
/*
SELECT
  date_trunc('hour', prediction_date) AS hour,
  AVG(CASE WHEN performance_prediction = actual_label THEN 1 ELSE 0 END)::float AS accuracy
FROM predictions
WHERE actual_label IS NOT NULL
GROUP BY hour
ORDER BY hour;
*/
ORDER BY hour;
