import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RUTA = BASE_DIR / "pacientes_clinica.csv"


def explorar_pacientes(ruta=RUTA):
    df = pd.read_csv(ruta, encoding="utf-8")

    print("Primeras filas:")
    print(df.head())

    print("\nInfo del DataFrame:")
    print(df.info())

    print("\nConteo de valores de 'sexo':")
    print(df["sexo"].value_counts(dropna=False))

    print("\nConteo de valores de 'fumador':")
    print(df["fumador"].value_counts(dropna=False))

    print("\nDescripción estadística de altura y peso:")
    print(df[["altura_cm", "peso_kg"]].describe())


if __name__ == "__main__":
    explorar_pacientes()
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RUTA = BASE_DIR / "pacientes_clinica.csv"


def explorar_pacientes(ruta=RUTA):
    df = pd.read_csv(ruta, encoding="utf-8")

    print("Primeras filas:")
    print(df.head())

    print("\nInfo del DataFrame:")
    print(df.info())

    print("\nConteo de valores de 'sexo':")
    print(df["sexo"].value_counts(dropna=False))

    print("\nConteo de valores de 'fumador':")
    print(df["fumador"].value_counts(dropna=False))

    print("\nDescripción estadística de altura y peso:")
    print(df[["altura_cm", "peso_kg"]].describe())


if __name__ == "__main__":
    explorar_pacientes()
