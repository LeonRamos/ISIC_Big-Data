import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RUTA = BASE_DIR / "ventas_ecommerce.csv"

def explorar_csv(ruta=RUTA):
    df = pd.read_csv(ruta, encoding="utf-8")
    print("Primeras filas:")
    print(df.head())
    print("\nInfo del DataFrame:")
    print(df.info())
    print("\nResumen estadístico de 'amount':")
    print(df["amount"].describe())

if __name__ == "__main__":
    explorar_csv()
