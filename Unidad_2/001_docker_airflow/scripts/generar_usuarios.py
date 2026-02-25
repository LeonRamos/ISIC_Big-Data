from faker import Faker
import json
from pathlib import Path

def main():
    fake = Faker("es_MX")  # datos en español (México)
    usuarios = []

    for i in range(10):
        usuarios.append({
            "id": i + 1,
            "nombre": fake.name(),
            "email": fake.email(),
            "direccion": fake.address(),
        })

    # guarda el archivo en /opt/airflow/data dentro del contenedor
    output_path = Path("/opt/airflow/data/usuarios.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)

    print("Archivo usuarios.json generado correctamente")

if __name__ == "__main__":
    main()