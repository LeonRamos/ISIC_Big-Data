from faker import Faker
import random

fake = Faker("es_MX")

archivo = "alumnos.tvs"
num_registros = 60

with open(archivo, "w", encoding="utf-8") as f:
    f.write("matricula,nombre,apellido,grupo,correo,calificacion\n")

    for i in range(1, num_registros + 1):
        matricula = f"A{i:04d}"
        nombre = fake.first_name()
        apellido = fake.last_name()
        grupo = random.choice(["1A", "1B", "2A", "2B", "3A", "3B"])
        correo = fake.email()
        calificacion = round(random.uniform(5, 10), 1)
        linea = f"{matricula},{nombre},{apellido},{grupo},{correo},{calificacion}\n"
        f.write(linea)

print(f"Archivo {archivo} generado correctamente.")
