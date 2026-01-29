archivo = "clientes.tvs"

with open(archivo, "r", encoding="utf-8") as f:
    for linea in f:
        print(linea.strip())
