from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hola_faker_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # ejecución manual
    catchup=False,
    tags=["ejemplo", "faker", "hola_mundo"],
) as dag:

    tarea_generar_usuarios = BashOperator(
        task_id="generar_usuarios",
        bash_command="python /opt/airflow/scripts/generar_usuarios.py"
    )

    tarea_ver_archivo = BashOperator(
        task_id="ver_archivo",
        bash_command="cat /opt/airflow/data/usuarios.json"
    )
    tarea_generar_usuarios >> tarea_ver_archivo