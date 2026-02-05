# practica_xml1_leer_clientes.py
import xml.etree.ElementTree as ET
from collections import Counter

RUTA_ARCHIVO = "clientes_retail.xml"

def leer_y_agrupar_por_segmento(ruta: str):
    tree = ET.parse(ruta)
    root = tree.getroot()

    segmentos = []
    for cliente in root.findall("cliente"):
        seg_elem = cliente.find("segmento")
        if seg_elem is not None:
            segmentos.append(seg_elem.text)

    conteos = Counter(segmentos)
    print("Clientes por segmento:")
    for seg in ["bronze", "silver", "gold"]:
        print(seg, ":", conteos.get(seg, 0))

if __name__ == "__main__":
    leer_y_agrupar_por_segmento(RUTA_ARCHIVO)
