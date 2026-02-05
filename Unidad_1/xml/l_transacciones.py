# practica_xml2_leer_transacciones.py
import xml.etree.ElementTree as ET

RUTA_ENTRADA = "transacciones.xml"

def clasificar_por_monto(ruta: str):
    tree = ET.parse(ruta)
    root = tree.getroot()

    baratas = []   # <= 3000
    caras = []     # >= 3001

    for t in root.findall("transaccion"):
        monto_elem = t.find("monto")
        if monto_elem is None:
            continue
        monto = float(monto_elem.text)

        if monto <= 3000:
            baratas.append(t)
        else:
            caras.append(t)

    print("Transacciones baratas (<= 3000):", len(baratas))
    print("Transacciones caras   (>= 3001):", len(caras))

if __name__ == "__main__":
    clasificar_por_monto(RUTA_ENTRADA)
