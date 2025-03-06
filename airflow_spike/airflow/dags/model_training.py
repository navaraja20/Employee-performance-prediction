from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

DATA_FILE_PATH = "/opt/airflow/data/raw/employees.csv"
MODEL_PATH = "/opt/airflow/data/models/model.pkl"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 6),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def train_model():
    df = pd.read_csv(DATA_FILE_PATH)
    X = df[["Age", "YearsAtCompany", "MonthlyIncome"]]  # Example features
    y = df["PerformanceRating"]  # Example target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved at {MODEL_PATH}")

with DAG("model_training", default_args=default_args, schedule_interval="@weekly", catchup=False) as dag:
    train_task = PythonOperator(task_id="train_model", python_callable=train_model)