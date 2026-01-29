archivo = "alumnos.tvs"
contador = 0

with open(archivo, "r", encoding="utf-8") as f:
    encabezado = f.readline().strip()
    print("Encabezado:", encabezado)

    for linea in f:
        contador += 1
        print(linea.strip())

print(f"Total de alumnos: {contador}")
