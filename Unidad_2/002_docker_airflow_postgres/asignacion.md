## Resumen:
 En estas práctica vamos a añadir Postgres dentro de este  una capa **bronce** y ajustaremos el DAG cada 5 minutos para ir generando datos en bruto de forma continua y tenga más forma nuestro pipeline de datos y obtener un ETL completo. 

***

## 1. Nueva arquitectura para esta práctica

Ahora el entorno tendrá:

- Un contenedor Airflow (como antes) que ejecuta el DAG.  
- Un contenedor Postgres usado como almacén bronce.  
- Un DAG que, cada 5 minutos, genera datos sintéticos y los inserta en una tabla de Postgres.

***

## 2. Cambios en `docker-compose.yml`

Extiende tu `docker-compose.yml` para añadir Postgres y que Airflow dependa de él.

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:13
    container_name: bronze_postgres
    environment:
      - POSTGRES_USER=bronze_user
      - POSTGRES_PASSWORD=bronze_pass
      - POSTGRES_DB=bronze_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "bronze_user"]
      interval: 10s
      retries: 5
      start_period: 10s
    restart: unless-stopped

  airflow:
    build: .
    container_name: hola_airflow_faker
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      - AIRFLOW__CORE__LOAD_EXAMPLES=False
      - AIRFLOW__CORE__EXECUTOR=SequentialExecutor
      - AIRFLOW__CORE__FERNET_KEY=MI_FERNET_KEY_1234567890123456789012
      - AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=False
      - AIRFLOW__WEBSERVER__RBAC=True
      - _AIRFLOW_WWW_USER_USERNAME=admin
      - _AIRFLOW_WWW_USER_PASSWORD=admin
      # Conexión interna de Airflow a Postgres bronce (para la capa de datos)
      - BRONZE_PG_HOST=postgres
      - BRONZE_PG_DB=bronze_db
      - BRONZE_PG_USER=bronze_user
      - BRONZE_PG_PASSWORD=bronze_pass
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./scripts:/opt/airflow/scripts
      - ./data:/opt/airflow/data
    command: >
      bash -c "
      airflow db init &&
      airflow users create
        --username admin
        --firstname Admin
        --lastname User
        --role Admin
        --email admin@example.com
        --password admin &&
      airflow webserver & airflow scheduler
      "

volumes:
  pgdata:
```

Este Postgres será tu capa bronce donde se guardan los eventos en bruto.

***

## 3. Ajustes en el Dockerfile (cliente de Postgres)

Añade el cliente de Postgres y el provider de Airflow si quieres usar el `PostgresOperator` más adelante.
```dockerfile
FROM apache/airflow:2.9.0

USER root

# Faker + cliente de Postgres
RUN pip install Faker psycopg2-binary

RUN mkdir -p /opt/airflow/dags /opt/airflow/scripts /opt/airflow/data

COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts

USER airflow
```

Con `psycopg2-binary` podrás conectarte a Postgres desde Python dentro del contenedor. [hevodata](https://hevodata.com/learn/airflow-postgres-operator/)

***

## 4. Script Python para insertar en Postgres (capa bronce)

En lugar de solo generar JSON, ahora el script insertará los datos en la tabla `usuarios_bronce` dentro de Postgres.

Crea/edita `scripts/generar_usuarios_bronce.py`:

```python
from faker import Faker
import os
import psycopg2

def main():
    fake = Faker("es_MX")

    host = os.getenv("BRONZE_PG_HOST", "postgres")
    db = os.getenv("BRONZE_PG_DB", "bronze_db")
    user = os.getenv("BRONZE_PG_USER", "bronze_user")
    password = os.getenv("BRONZE_PG_PASSWORD", "bronze_pass")

    conn = psycopg2.connect(
        host=host,
        dbname=db,
        user=user,
        password=password
    )
    cur = conn.cursor()

    # 1) Crear tabla bronce si no existe
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios_bronce (
            id SERIAL PRIMARY KEY,
            nombre TEXT,
            email TEXT,
            direccion TEXT,
            fecha_insercion TIMESTAMP DEFAULT NOW()
        );
        """
    )

    # 2) Insertar 10 registros sintéticos
    registros = []
    for _ in range(10):
        registros.append((
            fake.name(),
            fake.email(),
            fake.address()
        ))

    insert_sql = """
        INSERT INTO usuarios_bronce (nombre, email, direccion)
        VALUES (%s, %s, %s);
    """
    cur.executemany(insert_sql, registros)

    conn.commit()
    cur.close()
    conn.close()

    print(f"Se insertaron {len(registros)} registros en la tabla usuarios_bronce (capa bronce).")

if __name__ == "__main__":
    main()
```

Aquí la “capa bronce” son todas las filas crudas que se van acumulando con cada ejecución del DAG. 

***

## 5. DAG con scheduler cada 5 minutos

Ahora creamos un nuevo DAG que llame a este script cada 5 minutos para alimentar bronce. [stackoverflow](https://stackoverflow.com/questions/45689391/schedule-a-dag-in-airflow-to-run-every-5-minutes/45697203)

Archivo `dags/bronze_faker_postgres_dag.py`:

```python
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
        bash_command="python /opt/airflow/scripts/generar_usuarios_bronce.py"
    )
```

También podrías usar una expresión cron tipo `*/5 * * * *` como `schedule_interval`
***

## 6. Paso a paso de ejecución (entorno completo)

1. Reconstruir la imagen porque cambiaste el Dockerfile:

   ```bash
   docker compose build
   ```

2. Levantar todos los servicios:

   ```bash
   docker compose up
   ```

3. Entrar a Airflow en el navegador:

   ```text
   http://localhost:8080
   ```

4. Usuario/contraseña:

   - `admin` / `admin`

5. Buscar el DAG `bronze_faker_postgres_dag`.  
   Activarlo (switch) y dejar que corra según la programación cada 5 minutos.

6. Para verificar la tabla bronce desde el host:

   ```bash
   docker exec -it bronze_postgres psql -U bronze_user -d bronze_db -c "SELECT COUNT(*) FROM usuarios_bronce;"
   ```

Verás cómo el conteo crece cada 5 minutos a medida que el DAG inserta nuevos registros crudos. [github](https://github.com/matsudan/airflow-dag-examples/blob/main/docker-compose.yaml)

***

## 7. Siguiente Práctica:  Capa Plata 

Para reforzar la idea de medallion architecture:

- Esta práctica se enfoca solo en la **capa bronce**: datos crudos, redundantes, con posibles inconsistencias, pero completos y sin transformar.  
- En la siguiente práctica (capa plata), puedes:  
  - Crear un DAG nuevo que lea de `usuarios_bronce`,  
  - Aplique reglas de limpieza/curaduría (eliminar duplicados, normalizar campos, validar emails),  
  - Inserte los resultados limpios en una tabla `usuarios_plata` en el mismo Postgres. 