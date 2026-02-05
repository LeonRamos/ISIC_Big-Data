# practica_xml3_generar_sensores.py
from faker import Faker
import random
import xml.etree.ElementTree as ET

N_EVENTOS = 80

fake = Faker()
Faker.seed(9999)

def generar_xml_sensores(ruta_salida: str):
    root = ET.Element("eventos_sensores")

    for i in range(1, N_EVENTOS + 1):
        evento = ET.SubElement(root, "evento", attrib={"id_evento": str(i)})

        dispositivo = ET.SubElement(evento, "id_dispositivo")
        dispositivo.text = f"sensor_{random.randint(1, 20)}"

        temperatura = ET.SubElement(evento, "temperatura_c")
        temperatura.text = str(round(random.uniform(15, 45), 2))

        humedad = ET.SubElement(evento, "humedad_relativa")
        humedad.text = str(round(random.uniform(10, 90), 2))

        estado = ET.SubElement(evento, "estado")
        estado.text = random.choice(["OK", "WARN", "ERROR"])

    tree = ET.ElementTree(root)
    tree.write(ruta_salida, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generar_xml_sensores("sensores.xml")
    print("Archivo sensores.xml generado.")
