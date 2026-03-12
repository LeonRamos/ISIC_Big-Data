import os
import glob
import pandas as pd
from datetime import datetime

# =========================
# CONFIGURACIÓN BÁSICA
# =========================
BRONZE_PATH = "data/bronze"
SILVER_PATH = "data/silver"

os.makedirs(BRONZE_PATH, exist_ok=True)
os.makedirs(SILVER_PATH, exist_ok=True)

def log(msg: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")

# =========================
# 1) INGESTA DESDE CAPA BRONZE
#    (VOLUMEN + VELOCIDAD)
# =========================

def read_bronze_files(pattern="*.csv", chunksize=None):
    """
    Lee todos los CSV en la carpeta bronze.
    - Volumen: si el archivo es muy grande, podemos usar 'chunksize'
      para procesar por partes.
    - Velocidad: simularíamos varios archivos llegando en distintos momentos.
    """
    files = glob.glob(os.path.join(BRONZE_PATH, pattern))
    if not files:
        log("No se encontraron archivos en capa bronze.")
        return pd.DataFrame()

    df_list = []
    for f in files:
        log(f"Leyendo archivo bronze: {f}")
        if chunksize:
            # Ejemplo de lectura por volumen alto
            for chunk in pd.read_csv(f, chunksize=chunksize):
                df_list.append(chunk)
        else:
            df_list.append(pd.read_csv(f))
    if not df_list:
        return pd.DataFrame()
    return pd.concat(df_list, ignore_index=True)

# =========================
# 2) PERFILADO RÁPIDO
#    (VOLUMEN + VARIEDAD + VERACITY)
# =========================

def profile_dataframe(df: pd.DataFrame, name="bronze"):
    if df.empty:
        log("DataFrame vacío, nada que perfilar.")
        return

    log(f"Perfilado rápido de capa {name}")
    log(f"Número de filas: {len(df)}")
    log(f"Número de columnas: {len(df.columns)}")
    log("Tipos de datos detectados:")
    print(df.dtypes)

    log("Conteo de nulos por columna:")
    print(df.isna().sum())

    log("Ejemplo de filas:")
    print(df.head())

# =========================
# 3) LIMPIEZA Y TRANSFORMACIÓN
#    (VARIEDAD -> TIPOS; VERACITY,
#     VALIDITY, VALUE)
# =========================

def clean_to_silver(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica transformaciones básicas típicas de la capa silver.
    Ajusta las reglas según tu dataset.
    """

    if df.empty:
        return df.copy()

    df_clean = df.copy()

    # EJEMPLO: estandarizar nombres de columnas (Variedad: vocabulario)
    df_clean.columns = (
        df_clean.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Ejemplo de supuestos de columnas comunes
    # Ajusta según tu caso real:
    possible_date_cols = [c for c in df_clean.columns if "fecha" in c or "date" in c]
    possible_amount_cols = [c for c in df_clean.columns if "monto" in c or "amount" in c or "precio" in c or "total" in c]

    # --- Fechas ---
    for col in possible_date_cols:
        log(f"Convirtiendo columna fecha: {col}")
        df_clean[col] = pd.to_datetime(df_clean[col], errors="coerce")

    # --- Números ---
    for col in possible_amount_cols:
        log(f"Convirtiendo columna numérica: {col}")
        df_clean[col] = (
            df_clean[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.replace("[^0-9.-]", "", regex=True)
        )
        df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

    # --- Manejo de nulos ---
    # Aquí puedes demostrar decisiones de veracidad/validity:
    for col in df_clean.columns:
        if df_clean[col].dtype == "float64" or df_clean[col].dtype == "int64":
            median_val = df_clean[col].median()
            df_clean[col] = df_clean[col].fillna(median_val)
        elif df_clean[col].dtype == "datetime64[ns]":
            # Ejemplo: rellenar con la fecha mínima válida o dejar nulos
            df_clean[col] = df_clean[col].fillna(df_clean[col].min())
        else:
            df_clean[col] = df_clean[col].fillna("DESCONOCIDO")

    # --- Eliminar duplicados (Veracity / Validity) ---
    before = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    after = len(df_clean)
    log(f"Filas antes de eliminar duplicados: {before}, después: {after}")

    return df_clean

# =========================
# 4) ESCRIBIR A CAPA SILVER
#    (VALUE + VISIBILITY/ACCESS)
# =========================

def write_to_silver(df: pd.DataFrame, table_name: str):
    if df.empty:
        log("DataFrame vacío, nada que guardar en silver.")
        return

    filename = f"{table_name}_silver.parquet"
    path = os.path.join(SILVER_PATH, filename)

    log(f"Escribiendo DataFrame limpio a silver: {path}")
    # Parquet es más eficiente que CSV (mejor para volumen y velocidad)
    df.to_parquet(path, index=False)

# =========================
# 5) PIPELINE COMPLETO
# =========================

def bronze_to_silver_pipeline():
    log("=== INICIO PIPELINE BRONZE -> SILVER ===")

    # 1) Leer datos crudos (Bronze)
    df_bronze = read_bronze_files(pattern="*.csv", chunksize=None)
    profile_dataframe(df_bronze, name="bronze")

    # 2) Limpiar y transformar a Silver
    df_silver = clean_to_silver(df_bronze)
    profile_dataframe(df_silver, name="silver")

    # 3) Persistir en formato optimizado (Silver)
    write_to_silver(df_silver, table_name="ventas")

    log("=== FIN PIPELINE BRONZE -> SILVER ===")

if __name__ == "__main__":
    bronze_to_silver_pipeline()
