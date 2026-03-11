from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data_engineer",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="bronze_faker_postgres_dag",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=timedelta(minutes=5),  # cada 5 minutos
    catchup=False,
    tags=["bronce", "faker", "postgres"],
) as dag:

    generar_datos_bronce = BashOperator(
        task_id="generar_datos_bronce",
        bash_command="python /opt/airflow/scripts/generar_usuarios_bronce.py",
    )
