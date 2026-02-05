# leer_y_filtrar_transacciones_por_monto.py
import json

RUTA_ARCHIVO = "transacciones.ndjson"

def leer_transacciones_ndjson(ruta: str):
    """Genera transacciones (dict) leyendo el archivo NDJSON línea por línea."""
    with open(ruta, mode="r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            yield json.loads(linea)

def separar_por_monto(ruta_entrada: str,
                      ruta_salida_menor_igual_3000: str,
                      ruta_salida_mayor_igual_3001: str):
    transacciones_menor_igual_3000 = []
    transacciones_mayor_igual_3001 = []

    for t in leer_transacciones_ndjson(ruta_entrada):
        monto = t.get("monto", 0)
        if monto <= 3000:
            transacciones_menor_igual_3000.append(t)
        else:  # monto >= 3001 (o cualquier otro valor mayor de 3000)
            transacciones_mayor_igual_3001.append(t)

    # Guardamos cada grupo en archivos JSON (array)
    with open(ruta_salida_menor_igual_3000, mode="w", encoding="utf-8") as f1:
        json.dump(transacciones_menor_igual_3000, f1, ensure_ascii=False, indent=2)

    with open(ruta_salida_mayor_igual_3001, mode="w", encoding="utf-8") as f2:
        json.dump(transacciones_mayor_igual_3001, f2, ensure_ascii=False, indent=2)

    print(f"Transacciones <= 3000: {len(transacciones_menor_igual_3000)}")
    print(f"Transacciones >= 3001: {len(transacciones_mayor_igual_3001)}")

def main():
    separar_por_monto(
        RUTA_ARCHIVO,
        "transacciones_menor_igual_3000.json",
        "transacciones_mayor_igual_3001.json"
    )

if __name__ == "__main__":
    main()
