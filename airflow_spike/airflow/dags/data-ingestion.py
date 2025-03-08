from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os
import shutil
import pandas as pd
import random
from sqlalchemy import create_engine
import great_expectations as ge

# Constants
RAW_DATA_FOLDER = "/opt/airflow/input-data/raw-data"
GOOD_DATA_FOLDER = "/opt/airflow/input-data/good-data"
DATABASE_URL = "postgresql+psycopg2://postgres:password@postgres:5432/employee_db"

# DAG definition
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "catchup": False,
}

dag = DAG(
    "data_ingestion",
    default_args=default_args,
    schedule_interval="*/5 * * * *",  # Runs every 5 minutes
    description="Reads, validates, and moves new data",
    tags=["ingestion"],
)

# Function to pick a random file
def read_data(**kwargs):
    files = [f for f in os.listdir(RAW_DATA_FOLDER) if f.endswith(".csv")]
    if not files:
        raise ValueError("No files available in raw-data")

    selected_file = random.choice(files)
    file_path = os.path.join(RAW_DATA_FOLDER, selected_file)
    kwargs["ti"].xcom_push(key="selected_file", value=selected_file)
    return file_path

# Function to validate and move file
def validate_and_save_file(**kwargs):
    ti = kwargs["ti"]
    selected_file = ti.xcom_pull(task_ids="read_data", key="selected_file")

    if not selected_file:
        raise ValueError("No file received from read_data task")

    file_path = os.path.join(RAW_DATA_FOLDER, selected_file)
    df = pd.read_csv(file_path)

    # Great Expectations Validation
    expectations = ge.dataset.PandasDataset(df)
    
    validation_issues = []
    
    # Check for missing values
    for column in df.columns:
        result = expectations.expect_column_values_to_not_be_null(column)
        if not result["success"]:
            validation_issues.append({"column": column, "issue": "missing values"})

    # Check for negative values in numeric columns
    for col in df.select_dtypes(include=["number"]).columns:
        if (df[col] < 0).sum() > 0:
            validation_issues.append({"column": col, "issue": "negative values"})

    # Log issues to PostgreSQL if any exist
    if validation_issues:
        engine = create_engine(DATABASE_URL)
        validation_df = pd.DataFrame(validation_issues)
        validation_df.to_sql("data_quality_issues", engine, if_exists="append", index=False)

    # Move file to good_data
    shutil.move(file_path, os.path.join(GOOD_DATA_FOLDER, selected_file))

# Tasks
read_data_task = PythonOperator(
    task_id="read_data",
    python_callable=read_data,
    provide_context=True,
    dag=dag,
)

validate_and_save_task = PythonOperator(
    task_id="validate_and_save_file",
    python_callable=validate_and_save_file,
    provide_context=True,
    dag=dag,
)

read_data_task >> validate_and_save_task  # Task dependency
