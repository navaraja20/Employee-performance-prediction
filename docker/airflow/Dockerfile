# Use official Apache Airflow image
FROM apache/airflow:2.5.1

# Set Airflow environment
ENV AIRFLOW_HOME=/opt/airflow

# Install additional dependencies
RUN pip install --no-cache-dir apache-airflow-providers-postgres

# Copy DAGs
COPY ../airflow/dags /opt/airflow/dags

# Set working directory
WORKDIR $AIRFLOW_HOME

# Expose Airflow ports
EXPOSE 8080

# Run Airflow webserver
CMD ["airflow", "webserver"]
