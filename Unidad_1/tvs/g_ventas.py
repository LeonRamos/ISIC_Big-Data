from faker import Faker
import random
from datetime import datetime

fake = Faker("es_MX")

archivo = "ventas.tvs"
num_registros = 2108000

with open(archivo, "w", encoding="utf-8") as f:
    f.write("id_venta,fecha,producto,categoria,cantidad,precio_unitario,total\n")

    for i in range(1, num_registros + 1):
        fecha = fake.date_between(start_date="-1y", end_date="today")
        producto = fake.word().capitalize()
        categoria = random.choice(["Electrónica", "Ropa", "Alimentos", "Hogar", "Juguetes"])
        cantidad = random.randint(1, 10)
        precio = round(random.uniform(10, 500), 2)
        total = round(cantidad * precio, 2)
        linea = f"{i},{fecha},{producto},{categoria},{cantidad},{precio},{total}\n"
        f.write(linea)

print(f"Archivo {archivo} generado correctamente.")
