FROM apache/airflow:2.9.0

# Cambiamos a root para instalar dependencias
USER root

# Instalar Faker dentro del contenedor
RUN pip install Faker

# Crear carpetas para dags, scripts y data
RUN mkdir -p /opt/airflow/dags /opt/airflow/scripts /opt/airflow/data

# Copiar nuestro código al contenedor
COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts

# Volver al usuario airflow (recomendado por la documentación oficial)
USER airflow