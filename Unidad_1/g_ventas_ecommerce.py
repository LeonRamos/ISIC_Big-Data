from faker import Faker
import csv
import random
from datetime import datetime

fake = Faker()          # Puedes usar Faker('es_MX') si quieres datos más locales
Faker.seed(123)         # Para resultados reproducibles
random.seed(123)

OUTPUT_FILE = "ventas_ecommerce.csv"
N_ROWS = 5000           # Ajusta el tamaño según tus necesidades

def random_date_string():
    """Devuelve la misma fecha en distintos formatos para forzar limpieza."""
    date_obj = fake.date_between(start_date="-2y", end_date="today")
    formatos = [
        "%Y-%m-%d",        # 2024-03-15
        "%d/%m/%Y",        # 15/03/2024
        "%m-%d-%Y",        # 03-15-2024
        "%d-%b-%Y",        # 15-Mar-2024
    ]
    fmt = random.choice(formatos)
    return date_obj.strftime(fmt)

def random_country():
    """Combina código, nombre y variantes en minúsculas/mayúsculas."""
    opciones = [
        ("MX", "México"),
        ("US", "Estados Unidos"),
        ("ES", "España"),
        ("AR", "Argentina"),
    ]
    code, name = random.choice(opciones)
    variantes = [code, name, code.lower(), name.lower()]
    return random.choice(variantes)

def random_payment_method():
    """Genera categorías inconsistentes para practicar normalización."""
    base = random.choice(["tarjeta_credito", "debito", "efectivo", "paypal"])
    mapping = {
        "tarjeta_credito": ["card", "credito", "TC", "tarjeta", "tarjeta crédito"],
        "debito": ["debit", "TD", "debito"],
        "efectivo": ["cash", "efectivo"],
        "paypal": ["paypal", "pp"],
    }
    return random.choice(mapping[base])

def random_amount():
    """Genera montos normales, algunos negativos y outliers."""
    tipo = random.choices(
        ["normal", "negativo", "outlier"],
        weights=[0.85, 0.05, 0.10],
        k=1
    )[0]

    if tipo == "normal":
        amt = round(random.uniform(10, 300), 2)
    elif tipo == "negativo":
        amt = round(random.uniform(-200, -1), 2)
    else:  # outlier
        amt = round(random.uniform(1000, 10000), 2)

    # A veces como string con coma decimal para complicar un poco más
    if random.random() < 0.1:
        return str(amt).replace(".", ",")
    return amt

def random_discount_code():
    """Introduce nulos y valores ruidosos."""
    opciones = [
        "",                     # vacío
        "NULL",                 # texto
        None,                   # nulo real
        "DESC10",
        "BLACKFRIDAY",
        "WELCOME",
        "cupón",                # acento
    ]
    # Sesgo hacia nulos/ausentes
    pesos = [0.25, 0.15, 0.25, 0.1, 0.1, 0.1, 0.05]
    return random.choices(opciones, weights=pesos, k=1)[0]

def generar_ventas():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "order_id",
            "order_date",
            "customer_id",
            "country",
            "payment_method",
            "amount",
            "discount_code",
        ])

        # Para introducir algunos order_id duplicados
        order_ids_generados = []

        for i in range(N_ROWS):
            # 5% de las filas reutilizan un order_id anterior
            if order_ids_generados and random.random() < 0.05:
                order_id = random.choice(order_ids_generados)
            else:
                order_id = f"O-{100000 + i}"
                order_ids_generados.append(order_id)

            order_date = random_date_string()
            customer_id = f"C-{random.randint(1, 1000)}"
            country = random_country()
            payment_method = random_payment_method()
            amount = random_amount()
            discount_code = random_discount_code()

            # csv.writer no escribe None como vacío automáticamente, lo convertimos
            row = [
                order_id,
                order_date,
                customer_id,
                country,
                payment_method,
                "" if discount_code is None else discount_code,
            ]

            writer.writerow(row)

if __name__ == "__main__":
    generar_ventas()
    print(f"Archivo generado: {OUTPUT_FILE}")
