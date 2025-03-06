from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Default DAG settings
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 6),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Initialize DAG
dag = DAG(
    "model_training",
    default_args=default_args,
    description="Logs model training metadata",
    schedule_interval=None,  # Trigger manually
)

# Function to log model training execution
def log_training_execution():
    hook = PostgresHook(postgres_conn_id="postgres_default")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO training_logs (dag_name, execution_time)
        VALUES (%s, %s)
    """, ("model_training", datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Model training execution logged.")

# Manually execute this DAG from Airflow UI, no need for PythonOperator
log_training_execution()
