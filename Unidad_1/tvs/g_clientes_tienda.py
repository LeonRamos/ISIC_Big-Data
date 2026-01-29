from faker import Faker
import random

fake = Faker("es_MX")  # español México

archivo = "clientes.tvs"
num_registros = 50

with open(archivo, "w", encoding="utf-8") as f:
    # cabecera
    f.write("id_cliente,nombre,email,telefono,ciudad,edad\n")

    for i in range(1, num_registros + 1):
        nombre = fake.name()
        email = fake.email()
        telefono = fake.phone_number()
        ciudad = fake.city()
        edad = random.randint(18, 80)
        linea = f"{i},{nombre},{email},{telefono},{ciudad},{edad}\n"
        f.write(linea)

print(f"Archivo {archivo} generado correctamente.")
