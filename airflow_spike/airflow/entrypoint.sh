# Inside ./airflow_spike/airflow/entrypoint.sh
#!/bin/bash
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
airflow webserver & airflow scheduler
