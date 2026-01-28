import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RUTA = BASE_DIR / "sensores_iot_fabrica.csv"


def explorar_sensores(ruta=RUTA):
    df = pd.read_csv(ruta, encoding="utf-8")

    print("Primeras filas:")
    print(df.head())

    print("\nInfo del DataFrame:")
    print(df.info())

    print("\nConteo de estados:")
    print(df["estado"].value_counts(dropna=False))

    print("\nConteo de líneas de producción:")
    print(df["linea_produccion"].value_counts(dropna=False))

    # Conversión tentativa de temperatura a numérico para ver problemas
    temp_num = pd.to_numeric(df["temperatura_c"].astype(str).str.replace(",", "."), errors="coerce")
    vib_num = pd.to_numeric(df["vibracion_ms2"], errors="coerce")

    print("\nDescripción estadística de temperatura (convertida a numérico):")
    print(temp_num.describe())

    print("\nDescripción estadística de vibración:")
    print(vib_num.describe())

    print("\nNúmero de registros duplicados completos:")
    print(df.duplicated().sum())


if __name__ == "__main__":
    explorar_sensores()
