from faker import Faker
import csv
import random
from datetime import datetime

fake = Faker("es_MX")
Faker.seed(123)
random.seed(123)

OUTPUT_FILE = "pacientes_clinica.csv"
N_ROWS = 2000


def fecha_nacimiento_ruidosa():
    """Distintos formatos de fecha para que el alumno limpie."""
    date_obj = fake.date_of_birth(minimum_age=0, maximum_age=100)
    formatos = [
        "%Y-%m-%d",        # 1980-03-15
        "%d/%m/%Y",        # 15/03/1980
        "%d-%m-%Y",        # 15-03-1980
        "%d-%b-%Y",        # 15-Mar-1980
    ]
    return date_obj.strftime(random.choice(formatos))


def sexo_inconsistente():
    base = random.choice(["M", "F"])
    if base == "M":
        variantes = ["M", "H", "Hombre", "masculino", "m"]
    else:
        variantes = ["F", "Mujer", "femenino", "FEM", "f"]
    return random.choice(variantes)


def fumador_inconsistente():
    base = random.choice([True, False])
    if base:
        variantes = ["S", "Sí", "Yes", "1", "true"]
    else:
        variantes = ["N", "No", "0", "false"]
    return random.choice(variantes)


def altura_peso_con_ruido():
    """Valores plausibles + algunos errores (0, nulos, extremos)."""
    # Altura normal entre 140 y 190, peso normal entre 45 y 120
    altura = round(random.uniform(140, 190), 1)
    peso = round(random.uniform(45, 120), 1)

    tipo_error = random.choices(
        ["normal", "cero", "nulo", "extremo"],
        weights=[0.8, 0.05, 0.1, 0.05],
        k=1
    )[0]

    if tipo_error == "cero":
        if random.random() < 0.5:
            altura = 0
        else:
            peso = 0
    elif tipo_error == "nulo":
        if random.random() < 0.5:
            altura = ""
        else:
            peso = ""
    elif tipo_error == "extremo":
        if random.random() < 0.5:
            altura = round(random.uniform(50, 250), 1)   # niño muy pequeño o gigante
        else:
            peso = round(random.uniform(10, 250), 1)

    return altura, peso


def fecha_ultima_visita_ruidosa():
    date_obj = fake.date_between(start_date="-3y", end_date="today")
    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y",
    ]
    return date_obj.strftime(random.choice(formatos))


def diagnostico_con_typos():
    base = random.choice(
        [
            "Hipertension",
            "Diabetes tipo 2",
            "Asma",
            "Colesterol alto",
            "Gripe estacional",
            "COVID-19",
            "Migraña cronica",
            "Depresion",
            "Ansiedad",
            "Dolor lumbar",
        ]
    )
    # Introducir algunos errores ortográficos simples
    reemplazos = {
        "Hipertension": ["Hiperension", "Hipertesion"],
        "Diabetes tipo 2": ["Diavetes tipo 2", "Diabetes tpo 2"],
        "Asma": ["Azma", "Asmaa"],
        "Colesterol alto": ["Colestero alto", "Colesterol ato"],
        "Depresion": ["Deprecion", "Depreson"],
    }
    if base in reemplazos and random.random() < 0.3:
        return random.choice(reemplazos[base])
    return base


def generar_pacientes():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "patient_id",
                "nombre",
                "fecha_nacimiento",
                "sexo",
                "altura_cm",
                "peso_kg",
                "fumador",
                "fecha_ultima_visita",
                "diagnostico_principal",
            ]
        )

        for i in range(1, N_ROWS + 1):
            patient_id = f"P-{i:05d}"
            nombre = fake.name()
            fecha_nacimiento = fecha_nacimiento_ruidosa()
            sexo = sexo_inconsistente()
            altura_cm, peso_kg = altura_peso_con_ruido()
            fumador = fumador_inconsistente()
            fecha_ultima_visita = fecha_ultima_visita_ruidosa()
            diagnostico = diagnostico_con_typos()

            writer.writerow(
                [
                    patient_id,
                    nombre,
                    fecha_nacimiento,
                    sexo,
                    altura_cm,
                    peso_kg,
                    fumador,
                    fecha_ultima_visita,
                    diagnostico,
                ]
            )


if __name__ == "__main__":
    generar_pacientes()
    print(f"Archivo generado: {OUTPUT_FILE}")
