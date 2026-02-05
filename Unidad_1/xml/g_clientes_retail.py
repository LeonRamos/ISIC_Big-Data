# practica_xml1_generar_clientes.py
from faker import Faker
import random
import xml.etree.ElementTree as ET

N_REGISTROS = 50  # súbelo para más volumen

fake = Faker("es_MX")
Faker.seed(1234)

def generar_xml_clientes(ruta_salida: str):
    root = ET.Element("clientes")

    for i in range(1, N_REGISTROS + 1):
        cliente = ET.SubElement(root, "cliente", attrib={"id_cliente": str(i)})

        nombre = ET.SubElement(cliente, "nombre")
        nombre.text = fake.name()

        email = ET.SubElement(cliente, "email")
        email.text = fake.email()

        telefono = ET.SubElement(cliente, "telefono")
        telefono.text = fake.phone_number()

        segmento = ET.SubElement(cliente, "segmento")
        segmento.text = random.choice(["gold", "silver", "bronze"])

        ingreso = ET.SubElement(cliente, "ingreso_mensual")
        ingreso.text = str(round(random.uniform(5000, 80000), 2))

    tree = ET.ElementTree(root)
    tree.write(ruta_salida, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generar_xml_clientes("clientes_retail.xml")
    print("Archivo clientes_retail.xml generado.")
