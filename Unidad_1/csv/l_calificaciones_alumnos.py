import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RUTA = BASE_DIR / "calificaciones_alumnos.csv"


def explorar_calificaciones(ruta=RUTA):
    df = pd.read_csv(ruta, encoding="utf-8")

    print("Primeras filas:")
    print(df.head())

    print("\nInfo del DataFrame:")
    print(df.info())

    print("\nConteo de grupos (sin limpiar):")
    print(df["grupo"].value_counts(dropna=False).head(20))

    print("\nConteo de materias:")
    print(df["materia"].value_counts(dropna=False))

    print("\nDescripción estadística de parciales (sin filtrar outliers):")
    print(df[["parcial_1", "parcial_2", "parcial_3"]].describe())

    print("\nEjemplos de valores de asistencia:")
    print(df["asistencia_porcentaje"].head(20))


if __name__ == "__main__":
    explorar_calificaciones()
