from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os
import requests
import pandas as pd

API_URL = "http://backend:8000/predict-batch"
GOOD_DATA_PATH = "/opt/airflow/good-data"

def check_for_new_data():
    files = [f for f in os.listdir(GOOD_DATA_PATH) if f.endswith(".csv")]
    if not files:
        raise ValueError("No new data found")  # DAG run will be marked as skipped
    return files

def make_predictions(**kwargs):
    files = kwargs['ti'].xcom_pull(task_ids='check_for_new_data')
    for file in files:
        file_path = os.path.join(GOOD_DATA_PATH, file)
        df = pd.read_csv(file_path)
        
        response = requests.post(API_URL, json={"data": df.to_dict(orient="records")})
        if response.status_code == 200:
            print(f"Predictions for {file} saved successfully!")
        else:
            print(f"Failed to process {file}: {response.text}")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1
}

with DAG("prediction_job",
         default_args=default_args,
         schedule_interval="*/5 * * * *",
         catchup=False) as dag:

    check_for_new_data = PythonOperator(
        task_id="check_for_new_data",
        python_callable=check_for_new_data
    )

    make_predictions = PythonOperator(
        task_id="make_predictions",
        python_callable=make_predictions,
        provide_context=True
    )

    check_for_new_data >> make_predictions
