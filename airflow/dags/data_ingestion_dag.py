# airflow/dags/data_ingestion_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import random
import pandas as pd
import shutil
import json
from sqlalchemy import create_engine

# === Paths ===
RAW_DATA_PATH = "/opt/airflow/raw-data"
GOOD_DATA_PATH = "/opt/airflow/good_data"
BAD_DATA_PATH = "/opt/airflow/bad_data"
VALIDATION_REPORT_PATH = "/opt/airflow/validation_reports"

os.makedirs(GOOD_DATA_PATH, exist_ok=True)
os.makedirs(BAD_DATA_PATH, exist_ok=True)
os.makedirs(VALIDATION_REPORT_PATH, exist_ok=True)

DB_URL = os.getenv("DB_URL", "postgresql://mlops_user:mlops_pass@postgres:5432/mlops_db")

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 7, 2),
}

dag = DAG(
    dag_id="data_ingestion_dag",
    schedule_interval="*/1 * * * *",  # every 1 minute
    catchup=False,
    default_args=default_args,
    tags=["ingestion", "validation"],
)


def read_data(ti):
    files = os.listdir(RAW_DATA_PATH)
    if not files:
        raise FileNotFoundError("No data files found.")
    file = random.choice(files)
    path = os.path.join(RAW_DATA_PATH, file)
    ti.xcom_push(key="file_path", value=path)


def validate_data(ti):
    path = ti.xcom_pull(key="file_path")
    df = pd.read_csv(path)

    issues = {}
    critical = False

    for col in df.columns:
        if df[col].isnull().any():
            issues[col] = "Missing values"
            if df[col].isnull().sum() / len(df) > 0.2:
                critical = True

    ti.xcom_push(key="validation_issues", value=issues)
    ti.xcom_push(key="critical", value=critical)


def save_statistics(ti):
    file_path = ti.xcom_pull(key="file_path")
    issues = ti.xcom_pull(key="validation_issues")
    critical = ti.xcom_pull(key="critical")

    stats = {
        "filename": os.path.basename(file_path),
        "issues_found": json.dumps(issues),
        "is_critical": critical,
        "timestamp": datetime.utcnow().isoformat()
    }

    engine = create_engine(DB_URL)
    df_stats = pd.DataFrame([stats])
    try:
        df_stats.to_sql("validation_statistics", con=engine, if_exists="append", index=False)
    except Exception as e:
        print("Error saving statistics:", e)


def send_alerts(ti):
    path = ti.xcom_pull(key="file_path")
    issues = ti.xcom_pull(key="validation_issues")
    critical = ti.xcom_pull(key="critical")

    report = f"Validation Report for {os.path.basename(path)}\n"
    report += f"Issues:\n{json.dumps(issues, indent=2)}\n"
    report += f"Critical: {critical}\n"

    # Save report locally
    with open(os.path.join(VALIDATION_REPORT_PATH, f"{os.path.basename(path)}.txt"), "w") as f:
        f.write(report)

    # Optionally send alert to Microsoft Teams
    import requests
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
    if webhook_url:
        payload = {
            "text": report
        }
        requests.post(webhook_url, json=payload)


def split_and_save_data(ti):
    path = ti.xcom_pull(key="file_path")
    critical = ti.xcom_pull(key="critical")
    destination = BAD_DATA_PATH if critical else GOOD_DATA_PATH
    shutil.copy(path, destination)
    print(f"Moved {os.path.basename(path)} to {destination}")


# === Task Definitions ===
t1 = PythonOperator(task_id="read_data", python_callable=read_data, dag=dag)
t2 = PythonOperator(task_id="validate_data", python_callable=validate_data, dag=dag)
t3 = PythonOperator(task_id="save_statistics", python_callable=save_statistics, dag=dag)
t4 = PythonOperator(task_id="send_alerts", python_callable=send_alerts, dag=dag)
t5 = PythonOperator(task_id="split_and_save_data", python_callable=split_and_save_data, dag=dag)

t1 >> t2 >> [t3, t4, t5]
