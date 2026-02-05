# practica_xml3_leer_sensores.py
import xml.etree.ElementTree as ET

RUTA_ENTRADA = "sensores.xml"

def ordenar_y_detectar_alertas(ruta: str):
    tree = ET.parse(ruta)
    root = tree.getroot()

    eventos = []
    for ev in root.findall("evento"):
        temp_elem = ev.find("temperatura_c")
        estado_elem = ev.find("estado")
        disp_elem = ev.find("id_dispositivo")

        if temp_elem is None or estado_elem is None or disp_elem is None:
            continue

        eventos.append({
            "elemento": ev,
            "temperatura": float(temp_elem.text),
            "estado": estado_elem.text,
            "dispositivo": disp_elem.text
        })

    # Ordenar por temperatura descendente
    eventos_ordenados = sorted(eventos, key=lambda e: e["temperatura"], reverse=True)

    print("Top 5 temperaturas más altas:")
    for e in eventos_ordenados[:5]:
        print(f"{e['dispositivo']} -> {e['temperatura']} °C, estado={e['estado']}")

    print("\nEventos en estado WARN/ERROR:")
    for e in eventos_ordenados:
        if e["estado"] in ("WARN", "ERROR"):
            print(f"{e['dispositivo']} -> {e['temperatura']} °C, estado={e['estado']}")

if __name__ == "__main__":
    ordenar_y_detectar_alertas(RUTA_ENTRADA)
