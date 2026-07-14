import os
import csv
from typing import List, Dict

from scrapers import (
    autoscout24_france,
    clicars,
    autoscout24_netherlands,
    flexicar,
    mobile_de,
    ocasion_plus,
    autocasion,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")


# Funcion auxiliar para escribir los datos en un csv
def escrbir_csv(nombre_archivo: str, listado: List[Dict]) -> None:
    output_path = os.path.join(RAW_DATA_DIR, nombre_archivo + ".csv")
    with open(output_path, "w", newline="\n", encoding="utf-8") as csvfile:
        if listado:
            # Obtenemos del primer elemento el nombre de las llaves, para asi saber como nombrar a las columnas
            campos = listado[0].keys()
            csvtool = csv.DictWriter(csvfile, fieldnames=campos)
            csvtool.writeheader()
            for elem in listado:
                # Escritura de cada diccionario de un coche
                csvtool.writerow(elem)


if __name__ == "__main__":
    # Cada par es una llamada a la funcion de la respectiva pagina, la cual genera una lista de
    # diccionarios de coches y seguidamente se genera un csv con el nombre indicado

    # coches_clicars = clicars.funcion_clicars()
    # escrbir_csv("clicars_raw", coches_clicars)

    # coches_mobile_de = mobile_de.funcion_cochesmobile()
    # escrbir_csv("mobile_de_raw", coches_mobile_de)

    # coches_autoscout24_francia = autoscout24_france.funcion_AutoScout24()
    # escrbir_csv("autoscout24_france_raw", coches_autoscout24_francia)

    # coches_flexicar = flexicar.flexicar()
    # escrbir_csv("flexicar_raw", coches_flexicar)

    coches_autocasion = autocasion.funcion_autocar()
    escrbir_csv("autocasion_raw", coches_autocasion)

    # coches_ocasionplus = ocasion_plus.funcion_ocasionplus()
    # escrbir_csv("ocasion_plus_raw", coches_ocasionplus)

    coches_autoscout24_holanda = autoscout24_netherlands.funcion_autoscout_holada()
    escrbir_csv("autoscout24_netherlands_raw", coches_autoscout24_holanda)
