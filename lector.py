import csv

with open('subvenciones.csv', encoding='latin1') as fichero_csv:
    dict_lector = csv.DictReader(fichero_csv)
    asocs = {}
    for linea in dict_lector:
        centro = linea['Asociación']
        subvencion = float(linea['Importe'])
        asocs[centro] = asocs.get(centro, 0) + subvencion
    print(asocs)
    