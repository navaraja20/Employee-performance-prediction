# airflow/dags/prediction_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import requests

GOOD_DATA_PATH = '/opt/airflow/good_data'
USED_LOG = '/opt/airflow/good_data/used_files.log'

def get_new_files():
    all_files = set(os.listdir(GOOD_DATA_PATH)) - {"used_files.log"}
    if os.path.exists(USED_LOG):
        with open(USED_LOG, 'r') as f:
            used = set(f.read().splitlines())
    else:
        used = set()
    new_files = list(all_files - used)
    return new_files

def make_predictions():
    import pandas as pd
    new_files = get_new_files()
    if not new_files:
        return 'SKIP'

    for file in new_files:
        path = os.path.join(GOOD_DATA_PATH, file)
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            _ = requests.post("http://api:8000/predict", json=row.to_dict())

    with open(USED_LOG, 'a') as f:
        for file in new_files:
            f.write(file + '\n')

DEFAULT_ARGS = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

with DAG(
    dag_id='prediction_dag',
    default_args=DEFAULT_ARGS,
    start_date=datetime(2025, 6, 1),
    schedule_interval='*/2 * * * *',
    catchup=False
) as dag:

    predict_task = PythonOperator(
        task_id='predict_on_new_data',
        python_callable=make_predictions
    )

    predict_task
