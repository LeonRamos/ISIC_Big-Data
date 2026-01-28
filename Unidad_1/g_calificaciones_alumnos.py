from faker import Faker
import csv
import random

fake = Faker("es_MX")
Faker.seed(123)
random.seed(123)

OUTPUT_FILE = "calificaciones_alumnos.csv"
N_ROWS = 1500

MATERIAS = [
    "Matemáticas",
    "Programación",
    "Física",
    "Química",
    "Inglés",
    "Bases de Datos",
]


def grupo_inconsistente():
    """Variantes del mismo grupo para practicar normalización."""
    grado = random.randint(1, 9)
    letra = random.choice(["A", "B", "C"])
    variantes = [
        f"{grado}{letra}",
        f"{grado}-{letra}",
        f"{grado}°{letra}",
        f"{grado} {letra}",
    ]
    return random.choice(variantes)


def nota_con_ruido():
    """Notas normales 0–10, con algunos valores fuera de rango."""
    tipo = random.choices(
        ["normal", "alta", "negativa"],
        weights=[0.85, 0.1, 0.05],
        k=1,
    )[0]

    if tipo == "normal":
        return round(random.uniform(0, 10), 1)
    elif tipo == "alta":
        return round(random.uniform(10.1, 15), 1)
    else:
        return round(random.uniform(-3, -0.1), 1)


def asistencia_con_ruido():
    """Asistencia como número, string con %, nulos y extremos."""
    tipo = random.choices(
        ["normal", "texto", "nulo", "extremo"],
        weights=[0.7, 0.15, 0.1, 0.05],
        k=1,
    )[0]

    if tipo == "normal":
        return round(random.uniform(60, 100), 1)
    elif tipo == "texto":
        return f"{round(random.uniform(60, 100), 1)}%"
    elif tipo == "nulo":
        return ""
    else:
        # extremos fuera de rango
        return random.choice([-10, 150])


def generar_calificaciones():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "student_id",
                "nombre",
                "grupo",
                "materia",
                "parcial_1",
                "parcial_2",
                "parcial_3",
                "asistencia_porcentaje",
            ]
        )

        for i in range(1, N_ROWS + 1):
            student_id = f"S-{i:05d}"
            nombre = fake.name()
            grupo = grupo_inconsistente()
            materia = random.choice(MATERIAS)

            p1 = nota_con_ruido()
            p2 = nota_con_ruido()
            p3 = nota_con_ruido()
            asistencia = asistencia_con_ruido()

            writer.writerow(
                [
                    student_id,
                    nombre,
                    grupo,
                    materia,
                    p1,
                    p2,
                    p3,
                    asistencia,
                ]
            )


if __name__ == "__main__":
    generar_calificaciones()
    print(f"Archivo generado: {OUTPUT_FILE}")
