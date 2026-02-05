# practica_xml2_generar_transacciones.py
from faker import Faker
import random
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

N_TRANSACCIONES = 100

fake = Faker("es_MX")
Faker.seed(5678)

def fecha_aleatoria():
    now = datetime.now()
    hace_1_anio = now - timedelta(days=365)
    delta = now - hace_1_anio
    segundos = random.randint(0, int(delta.total_seconds()))
    return (hace_1_anio + timedelta(seconds=segundos)).isoformat()

def generar_xml_transacciones(ruta_salida: str):
    root = ET.Element("transacciones")

    for i in range(1, N_TRANSACCIONES + 1):
        t = ET.SubElement(root, "transaccion", attrib={"id_transaccion": str(i)})

        id_cliente = ET.SubElement(t, "id_cliente")
        id_cliente.text = str(random.randint(1, 1000))

        timestamp = ET.SubElement(t, "timestamp")
        timestamp.text = fecha_aleatoria()

        monto = ET.SubElement(t, "monto")
        monto.text = str(round(random.uniform(50, 5000), 2))

        moneda = ET.SubElement(t, "moneda")
        moneda.text = random.choice(["MXN", "USD"])

        metodo = ET.SubElement(t, "metodo_pago")
        metodo.text = random.choice(["tarjeta_credito", "tarjeta_debito", "efectivo"])

    tree = ET.ElementTree(root)
    tree.write(ruta_salida, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generar_xml_transacciones("transacciones.xml")
    print("Archivo transacciones.xml generado.")
