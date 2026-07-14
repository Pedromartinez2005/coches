from typing import List,Dict
from Paginas_coches import Autoscout24_francia, clicars,Autoscout24_holanda,Flexicar,cochesmobile,Ocasion_plus_final, autocasion
from io import open
import csv



 #Funcion auxiliar para escrbir los datos en un csv
def escrbir_csv(nombre_archivo:str,listado:List[Dict]) ->csv: 
        with open(nombre_archivo + ".csv" , "w", newline="\n") as csvfile:
         if listado:
            #Obtenemos del primer elemento el nombre de las llaves,para asi saber como nombrar a las columnas
            campos=listado[0].keys()
            csvtool = csv.DictWriter(csvfile, fieldnames=campos)
            csvtool.writeheader()
            for elem in listado:
                #Escritura de cada diccionario de un coche 
                csvtool.writerow(elem)


if __name__=="__main__":
    #Cada par es una llamada a la funcion de la respectiva pagina, la cual genera una lista de 
    # diccionarios de coches y  seguidamentes se genera un csv con el nombre indicado y el diccionario generado


    
    #coches_cliclars=clicars.funcion_clicars()
    #escrbir_csv("clicar",coches_cliclars)
    #coches_cochesmobile=cochesmobile.funcion_cochesmobile()
    #escrbir_csv("cochesmobile",coches_cochesmobile)    
    #coches_autoscout24_francia=Autoscout24_francia.funcion_AutoScout24()
    #escrbir_csv("Autoscout24_francia",coches_autoscout24_francia)
    #coches_flexicar=Flexicar.flexicar()
    #escrbir_csv("flexicar",coches_flexicar)
    coches_autocasion=autocasion.funcion_autocar()
    escrbir_csv("autocasion",coches_autocasion)
    #coches_ocasioplus=Ocasion_plus_final.funcion_ocasionplus()
    #escrbir_csv("ocasionplus",coches_ocasioplus)
    coches_autoscout24_holanda=Autoscout24_holanda.funcion_autoscout_holada()
    escrbir_csv("Autoscout24_holanda",coches_autoscout24_holanda)