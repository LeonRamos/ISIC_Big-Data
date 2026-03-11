FROM apache/airflow:2.9.0

# Primero haz lo que necesites como root (crear directorios, etc.)
USER root
RUN mkdir -p /opt/airflow/dags /opt/airflow/scripts /opt/airflow/data

# Cambia al usuario airflow ANTES de usar pip
USER airflow
RUN pip install --no-cache-dir Faker psycopg2-binary

# Copias (se pueden hacer también como airflow)
COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts
