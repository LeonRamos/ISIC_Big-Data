# practica1_clientes_json.py
from faker import Faker
import json
import random

N_REGISTROS = 10000  # Ajusta para más/menos volumen

fake = Faker("es_MX")  # o es_ES
Faker.seed(1234)       # reproducible

def generar_registro_cliente(id_cliente: int) -> dict:
    return {
        "id_cliente": id_cliente,
        "nombre": fake.name(),
        "email": fake.email(),
        "telefono": fake.phone_number(),
        "fecha_registro": fake.date_between(start_date="-5y", end_date="today").isoformat(),
        "pais": fake.country(),
        "ciudad": fake.city(),
        "segmento": random.choice(["gold", "silver", "bronze"]),
        "ingreso_mensual": round(random.uniform(5000, 80000), 2),
        "activo": random.choice([0, 1])  # 0 = inactivo, 1 = activo
    }

def crear_json_clientes(ruta_salida: str):
    clientes = []
    for i in range(1, N_REGISTROS + 1):
        clientes.append(generar_registro_cliente(i))
    
    # Guardamos la lista de diccionarios como un array JSON
    with open(ruta_salida, mode="w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    crear_json_clientes("clientes_retail.json")
    print("Archivo clientes_retail.json generado.")
