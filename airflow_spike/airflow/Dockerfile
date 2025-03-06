FROM apache/airflow:2.5.0

WORKDIR /opt/airflow

# Install necessary dependencies
RUN pip install psycopg2-binary

# Copy the DAGs directory correctly
COPY ./airflow_spike/airflow/dags /opt/airflow/dags

# Copy the requirements file correctly
COPY ./airflow_spike/airflow/requirements.txt /opt/airflow/requirements.txt

# Install Python dependencies for Airflow
RUN pip install -r /opt/airflow/requirements.txt
