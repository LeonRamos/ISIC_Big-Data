import pandas as pd

archivo = "transacciones.xlsx"
df = pd.read_excel(archivo, engine="openpyxl")

print("Primeras 5 filas:")
print(df.head())

print("\nEstadísticas del monto:")
print(df["monto"].describe())

print("\nTotal por tipo de transacción:")
print(df.groupby("tipo")["monto"].sum())

print("\nNúmero de transacciones por ciudad (top 10):")
print(df["ciudad"].value_counts().head(10))
