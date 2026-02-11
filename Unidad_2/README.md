# Pipeline de Datos Big Data

[![Data Engineering](https://img.shields.io/badge/Data%20Engineering-Spark%20%7C%20Kafka%20%7C%20Parquet-blue)](https://spark.apache.org/)
[![Big Data](https://img.shields.io/badge/Big%20Data-Hadoop%20Ecosystem-orange)](https://spark.apache.org/)
[![DevOps](https://img.shields.io/badge/DevOps-Docker%20%7C%20Kubernetes%20%7C%20GitOps-success)](https://github.com/topics/devops)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions%20%7C%20GitLab%20CI-yellow)](https://github.com/topics/ci-cd)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-ML%20Pipelines%20%7C%20MLOps-purple)](https://github.com/tensorchord/Awesome-LLMOps)

---

## ¿Qué es un Data Pipeline?

Un **data pipeline** es una secuencia de pasos automatizados por donde fluyen los datos, desde que se generan en el origen (sensores, sistemas, archivos) hasta que llegan a un destino útil (data lake, dashboard, modelo de ML, etc.).

 Cada etapa toma la salida de la anterior, la transforma o valida, y la entrega al siguiente paso de forma repetible, escalable y orquestada (por ejemplo, con Airflow o herramientas similares).

En Big Data, un pipeline suele incluir: ingesta, almacenamiento bruto (RAW/Bronze), limpieza y normalización (Silver), agregaciones y features (Gold), y finalmente consumo analítico o modelos de machine learning.

## Arquitecturas modernas de Big Data 
 - **Data Lakehouse**
    1. [Databricks – What is a Data Lakehouse?](https://www.databricks.com/glossary/data-lakehouse)
   2. [Google Cloud – What is a data lakehouse, and how does it work?](https://cloud.google.com/discover/what-is-a-data-lakehouse)
   3. [Azure Databricks (Microsoft Learn) – ¿Qué es un data lakehouse?](https://learn.microsoft.com/es-es/azure/databricks/lakehouse/)

      >[(extra opcional muy bueno, por si quieres un cuarto: Apache Hudi – What is a data lakehouse? )](https://hudi.apache.org/blog/2024/07/11/what-is-a-data-lakehouse/ )
 - **Arquitectura Medallion (Bronze–Silver–Gold)**
   1. [Informatica – Data Lakehouse Architecture: components and medallion layer](https://www.informatica.com/resources/articles/data-lakehouse-architecture-ai-guide.html)
   2. [ER/Studio – Understanding the Three Layers of Medallion Architecture](https://erstudio.com/blog/understanding-the-three-layers-of-medallion-architecture/)
   3. [Clarifai – What Is Medallion Architecture? Bronze, Silver \& Gold](https://www.clarifai.com/blog/medallion-architecture/)
 - **Lambda Architecture**
   1. [Microsoft Azure – Big Data Architectures (sección Lambda architecture)](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/big-data-architectures)
   2. [Wikipedia – Lambda architecture (buena visión general y referencias)](https://en.wikipedia.org/wiki/Lambda_architecture)
   3. [(Blog técnico) LumenData – ETL Data Architectures – Medallion, Lambda \& Kappa](https://lumendata.com/blogs/etl-data-architectures-part-1/)
 - **Kappa Architecture**
   1. [Confluent – Streaming Machine Learning with Tiered Storage (ejemplo claro de Kappa con Kafka)](https://www.confluent.io/blog/streaming-machine-learning-with-tiered-storage/)
   2. [Confluent – Show Me How: Confluent Makes Kappa Architecture a Reality (charla on‑demand)](https://www.confluent.io/resources/online-talk/show-me-how-confluent-makes-kappa-architecture-a-reality/)
   3. [Microsoft Azure (mismo artículo, sección de arquitecturas de streaming donde se contrasta con Lambda/Kappa)](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/big-data-architectures)
 - **Arquitecturas de Streaming en Tiempo Real**


---

## Arquitectura de Alto Nivel (ESP32 + SD → Big Data)

Flujo propuesto:

ESP32 → SD (CSV/JSON/TXT)  
↓  
Ingesta  
↓  
Raw Data Lake (Bronze)  
↓  
Limpieza / Normalización (Silver)  
↓  
Procesamiento / Agregaciones (Gold)  
↓  
Análisis / Dashboard / ML

---

### 1. Origen: ESP32 + SD

- ESP32 captura lecturas de sensores (temperatura, humedad, distancia, GPS, etc.) y las guarda en la SD en formatos como CSV, JSON o TXT. 
- Es importante registrar siempre: `sensor_id`, `timestamp` en UTC, versión de firmware y, si es posible, un checksum básico para validar integridad.

Ejemplo de estructura CSV:

```text
timestamp,sensor_id,temperature,humidity,firmware_version
2026-02-11 13:00:00,ESP32_001,24.5,45,1.0.3
```
---

### 2. Fase de Ingesta

Como los datos están inicialmente en la tarjeta SD, tienes dos estrategias principales de ingesta hacia el entorno Big Data.

#### Opción A: Ingesta manual / batch

- Extraer la SD periódicamente (por ejemplo, cada día o cada semana).
- Usar un script en Python o una pequeña herramienta que copie los archivos al servidor o a la nube.
- Cargar los archivos directamente a un Data Lake en bruto (zona RAW/Bronze).


#### Opción B: Ingesta automatizada

- El ESP32 envía en intervalos definidos (cada n minutos/horas) los archivos o registros usando:
    - MQTT
    - HTTP (REST)
    - FTP o SFTP
- Alternativamente, usar un gateway local (por ejemplo, una Raspberry Pi) que lea la SD y sincronice con la nube o un servidor on‑premise.

---

### 3. Data Lake RAW (Bronze)

Recomendación de enfoque Big Data: **subir primero todo en bruto, sin modificar nada**.

Ejemplos de tecnologías para Data Lake:

- AWS S3
- Azure Data Lake Storage
- HDFS (Hadoop)
- MinIO en un entorno local/on‑premise.

Estructura de carpetas sugerida:

```text
/raw/
  /sensor_id=ESP32_001/
    2026-02-10.csv
    2026-02-11.csv
  /sensor_id=ESP32_002/
    2026-02-10.csv
```

Esta organización por particiones (por `sensor_id` y fecha) facilita el procesamiento posterior con motores como Spark.

---

### 4. Problemas típicos en datos IoT

En sensores IoT es habitual encontrar:

- Valores nulos en campos críticos (ej. `timestamp`, `temperature`, `humidity`).
- Datos corruptos por fallos de escritura o cortes de energía.
- `timestamp` incorrecto (zona horaria, formato, reloj desajustado).
- Formato inconsistente entre archivos (cambio de columnas, separadores).
- Valores fuera de rango físico (ej. temperatura menor a −40 o mayor a 85 °C).
- Registros duplicados (mismo `sensor_id` y `timestamp`).
- Datos truncados o líneas incompletas.

Un buen pipeline se diseña para detectar y tratar sistemáticamente estos casos.

---

### 5. Estrategia de Limpieza (zona Silver)

Aquí entra el componente **Big Data**: usar herramientas como PySpark para procesar grandes volúmenes de archivos distribuidos.

#### Paso 1: Validación de formato

- Verificar separador (coma, punto y coma, tabulador).
- Confirmar columnas esperadas (schema).
- Confirmar encoding (UTF‑8 recomendado).
- Validar tipos de datos (timestamp, numéricos, etc.).

Ejemplo con PySpark:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("IoT Cleaning").getOrCreate()

df = spark.read.csv(
    "s3://raw/sensor_id=ESP32_001/*.csv",
    header=True,
    inferSchema=True
)

df.printSchema()
```


#### Paso 2: Eliminación de nulos críticos

Campos como `timestamp` y `temperature` son esenciales para análisis de series de tiempo y cálculos estadísticos, por lo que se pueden descartar registros con nulos en esos campos.

```python
df = df.dropna(subset=["timestamp", "temperature"])
```


#### Paso 3: Validación de rangos físicos

Aplicar filtros según el rango esperado de los sensores:

```python
df = df.filter((df.temperature >= -40) & (df.temperature <= 85))
df = df.filter((df.humidity >= 0) & (df.humidity <= 100))
```


#### Paso 4: Eliminación de duplicados

Evitar conteos inflados o análisis distorsionados:

```python
df = df.dropDuplicates(["sensor_id", "timestamp"])
```


#### Paso 5: Normalización de timestamp

Unificar el formato de fecha/hora para todo el sistema:

```python
from pyspark.sql.functions import to_timestamp

df = df.withColumn(
    "timestamp",
    to_timestamp(df.timestamp, "yyyy-MM-dd HH:mm:ss")
)
```


#### Paso 6: Manejo de outliers

- Usar métodos como Z‑score, IQR o ventanas temporales para detectar valores atípicos.
- Dependiendo del caso, se pueden marcar, imputar o descartar.

Ejemplo simple de cálculo de media:

```python
mean_temp = df.selectExpr("avg(temperature)").collect()
```

En un entorno de producción se usan métodos más robustos (por ejemplo, modelos estadísticos o de ML para detección de anomalías).

---

### 6. Almacenamiento de Datos Limpios (Silver)

Tras la limpieza, se recomienda almacenar los datos en formato **Parquet** en una zona Silver:

```python
df.write.mode("overwrite").parquet("s3://silver/sensor_id=ESP32_001/")
```

Ventajas de Parquet:

- Almacenamiento comprimido y columnar.
- Lecturas mucho más rápidas para analytics.
- Integración nativa con motores como Spark, Presto/Trino, Hive y sistemas de ML.

Este patrón suele llamarse arquitectura **Medallion**:

- Bronze: datos crudos (RAW).
- Silver: datos limpios y normalizados.
- Gold: datos agregados y listos para consumo de negocio o modelos.

---

### 7. Procesamiento Posterior (Gold)

A partir de la zona Silver puedes:

- Calcular agregados por hora, día, semana, etc.
- Detectar anomalías (picos de temperatura, fallos de sensor).
- Generar features para machine learning (promedios móviles, desviaciones, tendencias).
- Servir datos a dashboards en Power BI, Grafana o herramientas similares.

Ejemplos de tecnologías de procesamiento streaming/batch:

- Spark (batch y streaming).
- Kafka + Spark/Flink para flujos en tiempo casi real.

---

### 8. Pipeline Big Data Completo

```text
ESP32
  ↓
SD (CSV/JSON/TXT)
  ↓
Uploader (Python / Gateway)
  ↓
Data Lake RAW (Bronze)
  ↓
Spark Job (Limpieza / Normalización)
  ↓
Parquet limpio (Silver)
  ↓
Agregaciones / Features (Gold)
  ↓
Dashboard / ML
```


---

### 9. Recomendaciones según escala

| Escala | Tecnologías sugeridas |
| :-- | :-- |
| Proyecto pequeño | Python + Pandas, orquestación con Airflow simple, base de datos relacional (PostgreSQL) para análisis. |
| Proyecto mediano | Spark, MinIO u otro Data Lake, Airflow para orquestar jobs, almacenamiento en Parquet. |
| Proyecto grande | Kafka, Spark Streaming o Flink, Delta Lake/lakehouse, despliegue en Kubernetes y MLOps avanzado. |


---

### 10. Buenas prácticas para sensores ESP32

- Registrar siempre `sensor_id`, `timestamp` en UTC, versión de firmware y algún identificador de lote o sesión.
- Guardar siempre una copia RAW sin modificar para trazabilidad y re‑proceso.
- Versionar el esquema (por ejemplo, con metadatos o documentación en el repo).
- Diseñar el pipeline pensando en que, a futuro, puedas reemplazar la fuente (no solo ESP32) sin reescribir toda la arquitectura.

---
