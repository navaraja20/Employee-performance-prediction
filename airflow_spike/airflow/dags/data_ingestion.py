from airflow import DAG

from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

import pandas as pd

import great_expectations as ge

from sqlalchemy import create_engine

DB_CONNECTION_STRING = "postgresql://username:password@db:5432/employee_db"

DATA_FILE_PATH = "/opt/airflow/data/raw/employees.csv"

default_args = {

    "owner": "airflow",

    "depends_on_past": False,

    "start_date": datetime(2024, 3, 6),

    "retries": 1,

    "retry_delay": timedelta(minutes=5),

}

ge_context = ge.data_context.DataContext("/opt/airflow/great_expectations")

def validate_data():

    batch = ge_context.get_batch(batch_kwargs={

        "path": DATA_FILE_PATH,

        "datasource": "employee_data"

    }, expectation_suite_name="employee_data_expectations")

    results = batch.validate()

    if not results["success"]:

        raise ValueError("❌ Data validation failed!")

def load_data_to_postgres():

    engine = create_engine(DB_CONNECTION_STRING)

    df = pd.read_csv(DATA_FILE_PATH)

    df.to_sql("employees", engine, if_exists="append", index=False)

    print("✅ Data successfully loaded into PostgreSQL!")

with DAG("data_ingestion", default_args=default_args, schedule_interval="@daily", catchup=False) as dag:

    validate_task = PythonOperator(task_id="validate_data", python_callable=validate_data)

    load_task = PythonOperator(task_id="load_data_to_postgres", python_callable=load_data_to_postgres)

    validate_task >> load_task  # Validate before loading

