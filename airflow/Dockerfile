FROM apache/airflow:2.5.1

# Install necessary dependencies
RUN pip install psycopg2-binary
RUN pip install great_expectations

USER root
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

USER airflow

WORKDIR /opt/airflow
COPY dags /opt/airflow/dags
COPY requirements.txt .

# Install Python dependencies for Airflow
RUN pip install --no-cache-dir -r requirements.txt

# Set Airflow to use PostgreSQL instead of SQLite
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow_db
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

CMD ["bash", "-c", "airflow db upgrade && airflow webserver & airflow scheduler"]

