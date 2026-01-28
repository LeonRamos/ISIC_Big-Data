from faker import Faker
import csv
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(123)
random.seed(123)

OUTPUT_FILE = "sensores_iot_fabrica.csv"
N_ROWS = 5000

LINEAS = ["A", "B", "C"]


def timestamp_con_gaps():
    """Genera timestamps con ciertos saltos y formatos distintos."""
    base = fake.date_time_between(start_date="-30d", end_date="now")
    # Pasos entre 1 y 60 minutos
    delta = timedelta(minutes=random.randint(1, 60))
    ts = base + delta

    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%dT%H:%M:%S",
    ]
    return ts.strftime(random.choice(formatos))


def linea_inconsistente():
    linea = random.choice(LINEAS)
    variantes = [linea, linea.lower(), f"Linea {linea}", f"línea {linea}"]
    return random.choice(variantes)


def estado_inconsistente():
    base = random.choices(
        ["OK", "WARN", "FAIL"],
        weights=[0.8, 0.15, 0.05],
        k=1,
    )[0]

    mapping = {
        "OK": ["OK", "ok", "0", "NORMAL"],
        "WARN": ["WARN", "warning", "1", "Alerta"],
        "FAIL": ["FAIL", "fail", "ERROR", "2"],
    }
    return random.choice(mapping[base])


def temperatura_con_ruido():
    """Valores alrededor de 25–80°C, con algunos extremos y nulos."""
    tipo = random.choices(
        ["normal", "extremo", "nulo"],
        weights=[0.85, 0.1, 0.05],
        k=1,
    )[0]

    if tipo == "normal":
        temp = round(random.uniform(25, 80), 2)
    elif tipo == "extremo":
        temp = round(random.uniform(-10, 200), 2)
    else:
        return ""

    # A veces como string con coma decimal
    if random.random() < 0.1:
        return str(temp).replace(".", ",")
    return temp


def vibracion_con_ruido():
    """Vibración en m/s^2, con algunos valores extremos o 0."""
    tipo = random.choices(
        ["normal", "extremo", "cero"],
        weights=[0.85, 0.1, 0.05],
        k=1,
    )[0]

    if tipo == "normal":
        vib = round(random.uniform(0.1, 5.0), 3)
    elif tipo == "extremo":
        vib = round(random.uniform(5.1, 50.0), 3)
    else:
        vib = 0.0

    return vib


def generar_sensores():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "timestamp",
                "device_id",
                "temperatura_c",
                "vibracion_ms2",
                "estado",
                "linea_produccion",
            ]
        )

        device_ids = [f"SENSOR-{i:03d}" for i in range(1, 51)]

        # Para introducir duplicados
        filas_guardadas = []

        for i in range(N_ROWS):
            if filas_guardadas and random.random() < 0.03:
                # 3% de duplicados exactos
                writer.writerow(random.choice(filas_guardadas))
                continue

            ts = timestamp_con_gaps()
            device_id = random.choice(device_ids)
            temp = temperatura_con_ruido()
            vib = vibracion_con_ruido()
            estado = estado_inconsistente()
            linea = linea_inconsistente()

            fila = [ts, device_id, temp, vib, estado, linea]
            filas_guardadas.append(fila)
            writer.writerow(fila)


if __name__ == "__main__":
    generar_sensores()
    print(f"Archivo generado: {OUTPUT_FILE}")
