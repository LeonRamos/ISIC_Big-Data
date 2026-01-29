from faker import Faker
import pandas as pd
import random

fake = Faker("es_MX")

num_registros = 1000

datos = {
    "id_tx": [],
    "fecha": [],
    "cliente_id": [],
    "monto": [],
    "tipo": [],
    "ciudad": []
}

for i in range(1, num_registros + 1):
    datos["id_tx"].append(i)
    datos["fecha"].append(fake.date_between(start_date="-6M", end_date="today"))
    datos["cliente_id"].append(random.randint(1, 200))
    datos["monto"].append(round(random.uniform(50, 5000), 2))
    datos["tipo"].append(random.choice(["compra", "retiro", "transferencia", "pago_servicio"]))
    datos["ciudad"].append(fake.city())

df = pd.DataFrame(datos)
df.to_excel("transacciones.xlsx", index=False, engine="openpyxl")
print("Archivo transacciones.xlsx generado.")
