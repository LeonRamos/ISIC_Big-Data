# leer_y_ordenar_clientes_por_segmento.py
import json

RUTA_ARCHIVO = "clientes_retail.json"

# Definimos el orden deseado para los segmentos
ORDEN_SEGMENTO = {
    "bronze": 0,  # bronce
    "silver": 1,  # plata
    "gold": 2     # oro
}

def cargar_clientes(ruta: str):
    with open(ruta, mode="r", encoding="utf-8") as f:
        datos = json.load(f)  # lista de diccionarios
    return datos

def ordenar_por_segmento(clientes: list) -> list:
    # Usamos sorted con una función key que mira ORDEN_SEGMENTO
    return sorted(
        clientes,
        key=lambda c: ORDEN_SEGMENTO.get(c.get("segmento", "bronze"), 0)
    )

def guardar_json_ordenado(clientes_ordenados: list, ruta_salida: str):
    with open(ruta_salida, mode="w", encoding="utf-8") as f:
        json.dump(clientes_ordenados, f, ensure_ascii=False, indent=2)

def main():
    clientes = cargar_clientes(RUTA_ARCHIVO)
    clientes_ordenados = ordenar_por_segmento(clientes)

    # Si solo quieres ver un resumen:
    print("Totales por segmento:")
    total_bronze = sum(1 for c in clientes_ordenados if c["segmento"] == "bronze")
    total_silver = sum(1 for c in clientes_ordenados if c["segmento"] == "silver")
    total_gold = sum(1 for c in clientes_ordenados if c["segmento"] == "gold")
    print("bronze:", total_bronze)
    print("silver:", total_silver)
    print("gold:", total_gold)

    # Y también guardar archivo ya ordenado
    guardar_json_ordenado(clientes_ordenados, "clientes_retail_ordenado_por_segmento.json")
    print("Archivo clientes_retail_ordenado_por_segmento.json generado.")

if __name__ == "__main__":
    main()
