FROM apache/airflow:2.9.0

# Copiar requirements antes (mejora cache)
COPY requirements.txt /requirements.txt

# Instalar paquetes como usuario airflow (ya es el default en la imagen)
RUN pip install --no-cache-dir -r /requirements.txt

# Crear carpetas para dags, scripts y data (como airflow)
RUN mkdir -p /opt/airflow/dags /opt/airflow/scripts /opt/airflow/data

# Copiar código
COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts
