# airflow/dags/prediction_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
import os
import requests
import shutil

# === Paths and Config ===
GOOD_DATA_PATH = "/opt/airflow/good_data"
PROCESSED_DATA_PATH = "/opt/airflow/processed_data"
API_URL = "http://api:8000/predict"

os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 7, 2)
}

dag = DAG(
    dag_id="prediction_dag",
    schedule_interval="*/2 * * * *",  # every 2 minutes
    default_args=default_args,
    catchup=False,
    tags=["prediction"]
)

def check_for_new_data():
    files = os.listdir(GOOD_DATA_PATH)
    return "trigger_prediction" if files else "mark_skip"

def trigger_prediction():
    files = os.listdir(GOOD_DATA_PATH)
    if not files:
        print("No files to process.")
        return

    for file in files:
        file_path = os.path.join(GOOD_DATA_PATH, file)
        try:
            with open(file_path, "r") as f:
                lines = f.read().splitlines()
            header = lines[0].split(",")
            values = lines[1].split(",")
            data = dict(zip(header, values))

            response = requests.post(API_URL, json=data, timeout=10)
            if response.status_code == 200:
                print(f"[✓] Prediction for {file}: {response.json()}")
            else:
                print(f"[✗] Failed for {file}: Status {response.status_code} | Response: {response.text}")
        except Exception as e:
            print(f"[!] Error predicting {file}: {e}")

        # Move processed file to processed_data
        try:
            shutil.move(file_path, os.path.join(PROCESSED_DATA_PATH, file))
            print(f"Moved {file} to processed_data/")
        except Exception as e:
            print(f"Failed to move {file}: {e}")

def mark_skip():
    print("No new data found. Skipping prediction.")


# === Task Definitions ===

t1 = BranchPythonOperator(
    task_id="check_for_new_data",
    python_callable=check_for_new_data,
    dag=dag
)

t2 = PythonOperator(
    task_id="trigger_prediction",
    python_callable=trigger_prediction,
    dag=dag
)

t3 = PythonOperator(
    task_id="mark_skip",
    python_callable=mark_skip,
    dag=dag
)

end = EmptyOperator(task_id="end", dag=dag)

# === DAG Flow ===
t1 >> [t2, t3]
t2 >> end
t3 >> end
