# practica2_transacciones_json.py
from faker import Faker
import json
import random
from datetime import datetime, timedelta

fake = Faker("es_MX")
Faker.seed(5678)

N_TRANSACCIONES = 50000   # escala para big data
N_CLIENTES = 10000        # alinéalo con práctica 1

def fecha_aleatoria_entre(inicio: datetime, fin: datetime) -> datetime:
    delta = fin - inicio
    segundos_aleatorios = random.randint(0, int(delta.total_seconds()))
    return inicio + timedelta(seconds=segundos_aleatorios)

def generar_transaccion(id_transaccion: int) -> dict:
    now = datetime.now()
    hace_2_anios = now - timedelta(days=365 * 2)
    fecha = fecha_aleatoria_entre(hace_2_anios, now)

    return {
        "id_transaccion": id_transaccion,
        "id_cliente": random.randint(1, N_CLIENTES),
        "timestamp": fecha.isoformat(),
        "monto": round(random.uniform(50, 5000), 2),
        "moneda": random.choice(["MXN", "USD"]),
        "metodo_pago": random.choice(["tarjeta_credito", "tarjeta_debito", "efectivo", "transferencia"]),
        "categoria": random.choice(["electronica", "ropa", "hogar", "alimentos", "servicios"]),
        "tienda": fake.company(),
        "ciudad": fake.city(),
        "estado": fake.state(),
        "resultado_fraude": random.choice(["no_sospechoso", "sospechoso", "confirmado"])
    }

def generar_archivo_ndjson(ruta_salida: str):
    with open(ruta_salida, mode="w", encoding="utf-8") as f:
        for i in range(1, N_TRANSACCIONES + 1):
            registro = generar_transaccion(i)
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    generar_archivo_ndjson("transacciones.ndjson")
    print("Archivo transacciones.ndjson generado.")
