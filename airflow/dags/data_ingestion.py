from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import pandas as pd
import random
import great_expectations as ge
from sqlalchemy import create_engine

# Database connection (Update credentials)
DB_CONN = "postgresql://user:password@db:5432/employees_db"

# Folders
RAW_DATA_DIR = "/opt/airflow/raw-data"
GOOD_DATA_DIR = "/opt/airflow/good-data"
BAD_DATA_DIR = "/opt/airflow/bad-data"

# Ensure folders exist
os.makedirs(GOOD_DATA_DIR, exist_ok=True)
os.makedirs(BAD_DATA_DIR, exist_ok=True)

def read_random_file():
    """Pick a random file from raw-data"""
    files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".csv")]
    if not files:
        print("⚠️ No files found for ingestion")
        return None
    return os.path.join(RAW_DATA_DIR, random.choice(files))

def validate_data(**kwargs):
    """Validate data using Great Expectations"""
    file_path = kwargs['ti'].xcom_pull(task_ids='read_data')
    
    if not file_path:
        return "no_file"

    df = pd.read_csv(file_path)
    ge_df = ge.from_pandas(df)

    # Define Expectations
    expectations = [
        ge_df.expect_column_to_exist("Age"),
        ge_df.expect_column_values_to_be_between("Age", 18, 65),
        ge_df.expect_column_values_to_not_be_null("Salary"),
        ge_df.expect_column_values_to_be_in_set("Country", ["China", "India", "Lebanon"]),
    ]

    # Count failures
    failures = sum(1 for exp in expectations if not exp["success"])
    
    # Save validation report to DB
    engine = create_engine(DB_CONN)
    report_df = pd.DataFrame({
        "file_name": [os.path.basename(file_path)],
        "total_rows": [len(df)],
        "errors": [failures],
        "timestamp": [datetime.now()]
    })
    report_df.to_sql("data_quality_issues", engine, if_exists="append", index=False)

    return "valid" if failures == 0 else "invalid"

def move_file(**kwargs):
    """Move file to good-data or bad-data based on validation"""
    file_path = kwargs['ti'].xcom_pull(task_ids='read_data')
    validation_status = kwargs['ti'].xcom_pull(task_ids='validate_data')

    if not file_path or validation_status == "no_file":
        return

    dest_dir = GOOD_DATA_DIR if validation_status == "valid" else BAD_DATA_DIR
    os.rename(file_path, os.path.join(dest_dir, os.path.basename(file_path)))

# Define DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "data_ingestion",
    default_args=default_args,
    schedule_interval="*/1 * * * *",  # Run every minute
    catchup=False,
)

read_task = PythonOperator(
    task_id="read_data",
    python_callable=read_random_file,
    dag=dag,
)

validate_task = PythonOperator(
    task_id="validate_data",
    python_callable=validate_data,
    provide_context=True,
    dag=dag,
)

move_task = PythonOperator(
    task_id="move_file",
    python_callable=move_file,
    provide_context=True,
    dag=dag,
)

read_task >> validate_task >> move_task
