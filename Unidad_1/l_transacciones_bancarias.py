import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RUTA = BASE_DIR / "transacciones_bancarias.csv"


def explorar_transacciones(ruta=RUTA):
    df = pd.read_csv(ruta, encoding="utf-8")

    print("Primeras filas:")
    print(df.head())

    print("\nInfo del DataFrame:")
    print(df.info())

    print("\nConteo de valores de 'tipo':")
    print(df["tipo"].value_counts(dropna=False))

    print("\nConteo de valores de 'moneda':")
    print(df["moneda"].value_counts(dropna=False))

    print("\nConteo de valores de 'canal':")
    print(df["canal"].value_counts(dropna=False))

    print("\nDescripción estadística de 'monto' (sin limpiar):")
    # Intento de conversión a numérico para ver problemas
    monto_num = pd.to_numeric(df["monto"], errors="coerce")
    print(monto_num.describe())


if __name__ == "__main__":
    explorar_transacciones()
