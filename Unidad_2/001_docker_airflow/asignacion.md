# Hola Mundo con Python, Faker, Docker y Apache Airflow

Esta práctica guía para crear un **pipeline sencillo** que genera datos sintéticos con Python y Faker, ejecutado dentro de un contenedor Docker usando Apache Airflow como orquestador.

---

## Objetivos de aprendizaje

- Crear un script en Python que genere datos sintéticos con la librería Faker. 
- Construir una imagen Docker personalizada basada en Apache Airflow.  
- Definir un DAG sencillo en Airflow que ejecute el script y genere un archivo JSON.  
- Levantar Airflow con `docker compose` y ejecutar el DAG desde la interfaz web.

---

## Requisitos previos

Antes de iniciar, asegúrate de tener instalado:

- Python 3.9 o superior.  
- Docker Desktop (Windows, macOS o Linux). 
- Docker Compose (incluido en Docker Desktop en versiones recientes). 
- Visual Studio Code como editor (recomendado).

No se requiere experiencia previa con Airflow; esta práctica funciona como una introducción tipo “Hola Mundo”.

---

## Estructura del proyecto

Dentro de una carpeta llamada `hola_airflow_faker` trabajaremos con esta estructura:

```text
hola_airflow_faker/
├─ dags/
│  └─ hola_faker_dag.py
├─ scripts/
│  └─ generar_usuarios.py
├─ data/           # se creará automáticamente para los resultados
├─ Dockerfile
└─ docker-compose.yml
```


---

## Paso 1: Crear la carpeta del proyecto

En una terminal:

```bash
mkdir hola_airflow_faker
cd hola_airflow_faker
code .
```

Esto abre la carpeta en Visual Studio Code.

---

## Paso 2: Script Python con Faker (Hola Mundo de datos sintéticos)

1. Instala Faker en tu entorno local (para probar el script fuera de Docker si lo deseas):

```bash
pip install Faker
```

2. Crea la carpeta `scripts` y dentro el archivo `generar_usuarios.py` con el siguiente contenido:

```python
from faker import Faker
import json
from pathlib import Path

def main():
    fake = Faker("es_MX")  # datos en español (México)
    usuarios = []

    for i in range(10):
        usuarios.append({
            "id": i + 1,
            "nombre": fake.name(),
            "email": fake.email(),
            "direccion": fake.address(),
        })

    # guarda el archivo en /opt/airflow/data dentro del contenedor
    output_path = Path("/opt/airflow/data/usuarios.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)

    print("Archivo usuarios.json generado correctamente")

if __name__ == "__main__":
    main()
```


Este script genera un archivo `usuarios.json` con 10 usuarios falsos.

---

## Paso 3: Definir el DAG de Airflow

Crea la carpeta `dags` y dentro el archivo `hola_faker_dag.py`:

```python
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
```

Este DAG tiene dos tareas: una genera los datos con Faker y la otra muestra el contenido del archivo en los logs.

---

## Paso 4: Dockerfile para extender la imagen de Airflow

Crea un archivo `Dockerfile` en la raíz del proyecto:

```dockerfile
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
```

La imagen base `apache/airflow` es la recomendada para despliegues en Docker.

---

## Paso 5: docker-compose.yml para levantar Airflow

Crea el archivo `docker-compose.yml` en la raíz:

```yaml
version: "3.8"

services:
  airflow:
    build: .
    container_name: hola_airflow_faker
    restart: unless-stopped
    environment:
      - AIRFLOW__CORE__LOAD_EXAMPLES=False
      - AIRFLOW__CORE__EXECUTOR=SequentialExecutor
      - AIRFLOW__CORE__FERNET_KEY=MI_FERNET_KEY_1234567890123456789012
      - AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=False
      - AIRFLOW__WEBSERVER__RBAC=True
      - _AIRFLOW_WWW_USER_USERNAME=admin
      - _AIRFLOW_WWW_USER_PASSWORD=admin
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
```

Usamos `SequentialExecutor` para un entorno simple de desarrollo con un solo contenedor.

---

## Paso 6: Construir y levantar el contenedor

En la terminal (ubicado en la carpeta del proyecto):

1. Construir la imagen:

```bash
docker compose build
```

2. Levantar el servicio:

```bash
docker compose up
```


Espera a que termine la inicialización de la base de datos y se levanten el **webserver** y el **scheduler**.

---

## Paso 7: Acceder a la interfaz web de Airflow

1. Abre tu navegador y entra a:

```text
http://localhost:8080
```

2. Autentícate con:
    - Usuario: `admin`
    - Contraseña: `admin`
3. En la lista de DAGs, ubica `hola_faker_dag`.
4. Si está pausado, activa el DAG con el switch.
5. Haz clic en el botón **Play / Trigger DAG** para ejecutar una corrida.

Puedes revisar el estado de las tareas, los logs y el grafo del DAG desde la interfaz web.

---

## Paso 8: Verificar el archivo generado

En tu máquina (host), revisa el archivo `usuarios.json`:

```bash
cat data/usuarios.json
```

Deberías ver un arreglo de 10 usuarios con nombre, email y dirección generados por Faker.

---

## Actividades adicionales para el estudiante

- Modificar el script para generar más registros (por ejemplo, 100 o 1000).
- Agregar nuevos campos: teléfono, empresa, RFC, fecha de nacimiento, etc.
- Cambiar el formato de salida de JSON a CSV.
- Agregar una tercera tarea al DAG que cuente cuántos registros hay y lo imprima en los logs.
- Definir una programación automática cambiando `schedule_interval` (por ejemplo, `@daily` o `@hourly`).

---
