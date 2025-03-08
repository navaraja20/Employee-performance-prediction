-- Drop existing tables if they exist
DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS data_quality_issues;

-- Table for storing predictions
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    prediction TEXT NOT NULL,
    features JSONB NOT NULL,
    source VARCHAR(50) CHECK (source IN ('webapp', 'scheduled')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for storing data quality issues
CREATE TABLE data_quality_issues (
    id SERIAL PRIMARY KEY,
    missing_values JSONB NOT NULL,
    negative_values JSONB NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster queries on predictions
CREATE INDEX idx_predictions_timestamp ON predictions(timestamp);

-- Index for retrieving recent data quality issues
CREATE INDEX idx_data_quality_issues_detected_at ON data_quality_issues(detected_at);
