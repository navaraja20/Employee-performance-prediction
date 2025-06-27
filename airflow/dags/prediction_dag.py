from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from datetime import datetime, timedelta
import pandas as pd
import os
import requests
from airflow.exceptions import AirflowSkipException

default_args = {
       'owner': 'airflow',
       'depends_on_past': False,
       'email_on_failure': False,
       'email_on_retry': False,
       'retries': 1,
       'retry_delay': timedelta(minutes=5),
   }

def check_for_new_data():
       good_data_path = '/opt/airflow/good_data'
       files = [f for f in os.listdir(good_data_path) if f.endswith('.csv')]
       if not files:
           raise AirflowSkipException("No new data files found")
       return files

def make_predictions(ti):
       files = ti.xcom_pull(task_ids='check_for_new_data')
       if not files:
           raise AirflowSkipException("No files to process")
       for file in files:
           df = pd.read_csv(os.path.join('/opt/airflow/good_data', file))
           data = df.to_dict(orient='records')
           response = requests.post("http://api:8000/predict", json=data, params={"source": "scheduled"})
           if response.status_code != 200:
               raise Exception("Prediction failed")

with DAG(
       'prediction_dag',
       default_args=default_args,
       description='Scheduled prediction DAG',
       schedule_interval=timedelta(minutes=2),
       start_date=datetime(2025, 5, 31),
       catchup=False,
   ) as dag:
       check_for_new_data_task = PythonOperator(
           task_id='check_for_new_data',
           python_callable=check_for_new_data
       )
       make_predictions_task = PythonOperator(
           task_id='make_predictions',
           python_callable=make_predictions
       )
       skip_task = EmptyOperator(task_id='skip_task')

       check_for_new_data_task >> make_predictions_task