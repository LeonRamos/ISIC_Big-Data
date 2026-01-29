from faker import Faker
import csv
import random
from datetime import datetime

fake = Faker("es_MX")
Faker.seed(123)
random.seed(123)

OUTPUT_FILE = "transacciones_bancarias.csv"
N_ROWS = 3000


def fecha_transaccion_ruidosa():
    dt = fake.date_time_between(start_date="-2y", end_date="now")
    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y",
        "%d-%m-%Y %H:%M",
        "%m-%d-%Y",
    ]
    return dt.strftime(random.choice(formatos))


def tipo_inconsistente():
    base = random.choice(["DEPOSITO", "RETIRO"])
    if base == "DEPOSITO":
        variantes = ["DEPOSITO", "deposito", "dep", "INGRESO"]
    else:
        variantes = ["RETIRO", "retiro", "ret", "wd"]
    return random.choice(variantes)


def moneda_inconsistente():
    base = random.choice(["MXN", "USD", "EUR"])
    variantes = {
        "MXN": ["MXN", "mxn", "Peso", "Pesos"],
        "USD": ["USD", "usd", "Dolar", "Dólar"],
        "EUR": ["EUR", "eur", "Euro"],
    }
    return random.choice(variantes[base])


def canal():
    return random.choice(["app", "sucursal", "cajero", "web", "App", "WEB"])


def monto_con_ruido():
    """Montos normales, negativos y outliers, a veces con coma decimal."""
    tipo = random.choices(
        ["normal", "negativo", "outlier"],
        weights=[0.85, 0.05, 0.10],
        k=1,
    )[0]

    if tipo == "normal":
        amt = round(random.uniform(50, 5000), 2)
    elif tipo == "negativo":
        amt = round(random.uniform(-5000, -10), 2)
    else:
        amt = round(random.uniform(10000, 200000), 2)

    if random.random() < 0.1:
        return str(amt).replace(".", ",")
    return amt


def generar_transacciones():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "transaction_id",
                "customer_id",
                "fecha",
                "tipo",
                "monto",
                "moneda",
                "canal",
            ]
        )

        ids_generados = []

        for i in range(1, N_ROWS + 1):
            # 3% de filas repiten un transaction_id (posibles duplicados)
            if ids_generados and random.random() < 0.03:
                transaction_id = random.choice(ids_generados)
            else:
                transaction_id = f"T-{100000 + i}"
                ids_generados.append(transaction_id)

            customer_id = f"C-{random.randint(1, 1500)}"
            fecha = fecha_transaccion_ruidosa()
            tipo = tipo_inconsistente()
            monto = monto_con_ruido()
            moneda = moneda_inconsistente()
            canal_val = canal()

            writer.writerow(
                [
                    transaction_id,
                    customer_id,
                    fecha,
                    tipo,
                    monto,
                    moneda,
                    canal_val,
                ]
            )


if __name__ == "__main__":
    generar_transacciones()
    print(f"Archivo generado: {OUTPUT_FILE}")
