from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("es_MX")

LABS = {
    "LTI": "AA:BB:CC:DD:EE:01",
    "LÍA": "AA:BB:CC:DD:EE:02",
    "LDS": "AA:BB:CC:DD:EE:03",
    "LIS": "AA:BB:CC:DD:EE:04",
    "LWI": "AA:BB:CC:DD:EE:05",
    "LRD": "AA:BB:CC:DD:EE:06",
}

ANIO = 2026
MES = 1          # mes a simular
NOMBRE_MES = "enero"
archivo_csv = f"{NOMBRE_MES}_{ANIO}.csv"

# intervalo de medición en segundos
INTERVALO_SEGUNDOS = 5

def rango_mes(anio, mes):
    inicio = datetime(anio, mes, 1, 0, 0, 0)
    if mes == 12:
        fin = datetime(anio + 1, 1, 1, 0, 0, 0)
    else:
        fin = datetime(anio, mes + 1, 1, 0, 0, 0)
    return inicio, fin

inicio_mes, fin_mes = rango_mes(ANIO, MES)

with open(archivo_csv, "w", encoding="utf-8") as f:
    f.write("_id,device,temperature,humidity,timestamp\n")

    current_id = 1
    for lab_name, mac in LABS.items():
        timestamp = inicio_mes
        while timestamp < fin_mes:
            temperatura = round(random.uniform(18.0, 30.0), 1)
            humedad = round(random.uniform(30.0, 70.0), 1)

            linea = (
                f'ObjectId("{current_id}"),'
                f"{mac},"
                f"{temperatura},"
                f"{humedad},"
                f"{timestamp.strftime("%Y-%m-%d %H:%M:%S")}\n"
            )

            f.write(linea)
            current_id += 1

            # siguiente medición a los 5 segundos
            timestamp += timedelta(seconds=INTERVALO_SEGUNDOS)

print(f"Archivo {archivo_csv} generado correctamente con mediciones cada 5 segundos.")
