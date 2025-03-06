FROM apache/airflow:2.5.0

USER root

# Install additional dependencies if needed
RUN pip install psycopg2-binary

# Set the working directory
WORKDIR /opt/airflow

# Copy DAGs and requirements
COPY airflow/dags /opt/airflow/dags
COPY airflow/requirements.txt /opt/airflow/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Expose Airflow webserver port
EXPOSE 8080

# Set entry point
ENTRYPOINT ["/entrypoint.sh"]
