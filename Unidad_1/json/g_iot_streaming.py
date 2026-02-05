# practica3_eventos_iot_stream.py
from faker import Faker
import json
import random
import time
from datetime import datetime

fake = Faker()
Faker.seed(9999)

DISPOSITIVOS = [f"sensor_{i}" for i in range(1, 101)]  # 100 sensores

def generar_evento_iot() -> dict:
    dispositivo = random.choice(DISPOSITIVOS)
    temperatura = round(random.uniform(15, 40), 2)
    humedad = round(random.uniform(10, 90), 2)

    return {
        "id_dispositivo": dispositivo,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ubicacion": {
            "latitud": float(fake.latitude()),
            "longitud": float(fake.longitude())
        },
        "temperatura_c": temperatura,
        "humedad_relativa": humedad,
        "estado": random.choice(["OK", "WARN", "ERROR"]),
        "tipo_evento": random.choice(["lectura_periodica", "alerta", "mantenimiento"])
    }

def main():
    try:
        while True:
            evento = generar_evento_iot()
            print(json.dumps(evento, ensure_ascii=False))
            # Simula frecuencia de llegada de eventos
            time.sleep(random.uniform(0.1, 1.0))
    except KeyboardInterrupt:
        print("\nStream detenido por el usuario.")

if __name__ == "__main__":
    main()
