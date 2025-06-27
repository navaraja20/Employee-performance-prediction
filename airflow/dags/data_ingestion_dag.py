from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import random
from scripts.data_validator import validate_data

default_args = {
       'owner': 'airflow',
       'depends_on_past': False,
       'email_on_failure': False,
       'email_on_retry': False,
       'retries': 1,
       'retry_delay': timedelta(minutes=5),
   }

def read_data():
       raw_data_path = '/opt/airflow/raw_data'
       files = [f for f in os.listdir(raw_data_path) if f.endswith('.csv')]
       if not files:
           return None
       file = random.choice(files)
       return os.path.join(raw_data_path, file)

with DAG(
       'data_ingestion_dag',
       default_args=default_args,
       description='Data ingestion and validation DAG',
       schedule_interval=timedelta(minutes=1),
       start_date=datetime(2025, 5, 31),
       catchup=False,
   ) as dag:
       read_data_task = PythonOperator(
           task_id='read_data',
           python_callable=read_data
       )
       validate_data_task = PythonOperator(
           task_id='validate_data',
           python_callable=validate_data,
           op_kwargs={
               'file_path': '{{ ti.xcom_pull(task_ids="read_data") }}',
               'good_data_path': '/opt/airflow/good_data',
               'bad_data_path': '/opt/airflow/bad_data',
               'report_path': '/opt/airflow/reports'
           }
       )

       read_data_task >> validate_data_task