from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
import great_expectations as ge
from sqlalchemy import create_engine
import os

# PostgreSQL Connection String from Environment Variables
DB_CONNECTION_STRING = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/{os.getenv('POSTGRES_DB')}"

# File Path Inside Docker
DATA_FILE_PATH = "../data/raw/employees.csv"

# Airflow Default Arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 6),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Initialize Great Expectations Context
ge_context = ge.data_context.DataContext.create("/opt/airflow/great_expectations")

def validate_data():
    """
    Validate CSV data using Great Expectations before ingestion.
    """
    batch = ge_context.get_batch(
        batch_kwargs={"path": DATA_FILE_PATH, "datasource": "employee_data"},
        expectation_suite_name="employee_data_expectations"
    )
    results = batch.validate()

    if not results["success"]:
        raise ValueError("❌ Data validation failed!")

    print("✅ Data validation passed!")

def load_data_to_postgres():
    """
    Load CSV data into PostgreSQL after validation.
    """
    engine = create_engine(DB_CONNECTION_STRING)
    
    # Read CSV
    df = pd.read_csv(DATA_FILE_PATH)

    # Ensure the connection is established
    with engine.begin() as conn:
        df.to_sql("employees", conn, if_exists="append", index=False)

    print("✅ Data successfully loaded into PostgreSQL!")

# Define DAG
with DAG(
    "data_ingestion",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:

    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data
    )

    load_task = PythonOperator(
        task_id="load_data_to_postgres",
        python_callable=load_data_to_postgres
    )

    validate_task >> load_task  # Ensure validation runs before loading
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
import great_expectations as ge
from sqlalchemy import create_engine
import os

# PostgreSQL Connection String from Environment Variables
DB_CONNECTION_STRING = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/{os.getenv('POSTGRES_DB')}"

# File Path Inside Docker
DATA_FILE_PATH = "/opt/airflow/data/raw/employees.csv"

# Airflow Default Arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 6),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Initialize Great Expectations Context
ge_context = ge.data_context.DataContext.create("/opt/airflow/great_expectations")

def validate_data():
    """
    Validate CSV data using Great Expectations before ingestion.
    """
    batch = ge_context.get_batch(
        batch_kwargs={"path": DATA_FILE_PATH, "datasource": "employee_data"},
        expectation_suite_name="employee_data_expectations"
    )
    results = batch.validate()

    if not results["success"]:
        raise ValueError("❌ Data validation failed!")

    print("✅ Data validation passed!")

def load_data_to_postgres():
    """
    Load CSV data into PostgreSQL after validation.
    """
    engine = create_engine(DB_CONNECTION_STRING)
    
    # Read CSV
    df = pd.read_csv(DATA_FILE_PATH)

    # Ensure the connection is established
    with engine.begin() as conn:
        df.to_sql("employees", conn, if_exists="append", index=False)

    print("✅ Data successfully loaded into PostgreSQL!")

# Define DAG
with DAG(
    "data_ingestion",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:

    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data
    )

    load_task = PythonOperator(
        task_id="load_data_to_postgres",
        python_callable=load_data_to_postgres
    )

    validate_task >> load_task  # Ensure validation runs before loading
