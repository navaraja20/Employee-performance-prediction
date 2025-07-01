# airflow/dags/data_ingestion_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import random
import shutil

RAW_DATA_PATH = '/opt/airflow/raw-data'
GOOD_DATA_PATH = '/opt/airflow/good_data'
BAD_DATA_PATH = '/opt/airflow/bad_data'

DEFAULT_ARGS = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(seconds=10)
}

def read_data_file():
    files = os.listdir(RAW_DATA_PATH)
    if not files:
        return None
    file = random.choice(files)
    return os.path.join(RAW_DATA_PATH, file)

def validate_data(file_path: str):
    import pandas as pd
    from great_expectations import PandasDataset

    df = pd.read_csv(file_path)
    ge_df = PandasDataset(df)
    ge_df.expect_column_values_to_not_be_null("Age")
    ge_df.expect_column_values_to_be_between("Age", 18, 65)
    ge_df.expect_column_values_to_be_in_set("Gender", ["Male", "Female"])
    validation_result = ge_df.validate()
    return df, validation_result

def save_statistics(df, result, file_path):
    from db_operations import log_data_stats
    log_data_stats(df, result, file_path)

def move_data_file(df, result, file_path):
    if result['success']:
        shutil.move(file_path, os.path.join(GOOD_DATA_PATH, os.path.basename(file_path)))
    else:
        shutil.move(file_path, os.path.join(BAD_DATA_PATH, os.path.basename(file_path)))

def alert_team():
    from alerting import send_alert
    send_alert("Data ingestion validation alert triggered")

with DAG(
    dag_id='data_ingestion_dag',
    default_args=DEFAULT_ARGS,
    start_date=datetime(2025, 6, 1),
    schedule_interval='*/1 * * * *',
    catchup=False
) as dag:

    def ingestion_pipeline():
        file_path = read_data_file()
        if file_path is None:
            return 'No file to ingest'
        df, result = validate_data(file_path)
        save_statistics(df, result, file_path)
        move_data_file(df, result, file_path)
        if not result['success']:
            alert_team()

    ingestion_task = PythonOperator(
        task_id='ingest_and_validate_data',
        python_callable=ingestion_pipeline
    )

    ingestion_task
