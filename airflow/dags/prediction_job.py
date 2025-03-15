from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import pandas as pd
import requests
from sqlalchemy import create_engine

# API & Database Config
API_URL = "http://api:8000/predict"
DB_CONN = "postgresql://user:password@db:5432/employees_db"
GOOD_DATA_DIR = "/opt/airflow/good-data"

# Ensure folder exists
os.makedirs(GOOD_DATA_DIR, exist_ok=True)

def check_for_new_data():
    """Check for new files in good-data/"""
    files = [f for f in os.listdir(GOOD_DATA_DIR) if f.endswith(".csv")]
    return files if files else None

def make_predictions(**kwargs):
    """Call the API for predictions"""
    files = kwargs['ti'].xcom_pull(task_ids='check_for_new_data')
    if not files:
        return "no_data"

    predictions = []
    for file in files:
        df = pd.read_csv(os.path.join(GOOD_DATA_DIR, file))
        response = requests.post(API_URL, json=df.to_dict(orient="records"))

        if response.status_code == 200:
            pred_data = response.json()
            for row, pred in zip(df.to_dict(orient="records"), pred_data):
                row["prediction"] = pred["prediction"]
                predictions.append(row)

    # Save predictions to DB
    engine = create_engine(DB_CONN)
    pred_df = pd.DataFrame(predictions)
    pred_df.to_sql("predictions", engine, if_exists="append", index=False)

    return "success"

# Define DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "prediction_job",
    default_args=default_args,
    schedule_interval="*/2 * * * *",  # Run every 2 minutes
    catchup=False,
)

check_task = PythonOperator(
    task_id="check_for_new_data",
    python_callable=check_for_new_data,
    dag=dag,
)

predict_task = PythonOperator(
    task_id="make_predictions",
    python_callable=make_predictions,
    provide_context=True,
    dag=dag,
)

check_task >> predict_task
