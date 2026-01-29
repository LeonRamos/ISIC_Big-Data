archivo = "ventas.tvs"

with open(archivo, "r", encoding="utf-8") as f:
    encabezado = f.readline().strip()
    print(encabezado)

    for linea in f:
        linea = linea.strip()
        print(linea)

