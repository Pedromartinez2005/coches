from typing import Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options as Options_chrome





def sacar_coches(coche):
    diccinario={}
    marca_modelo=coche.find_element(By.XPATH, "./a/div[2]/h2").text.split()
    marca=marca_modelo[0]
    modelo=" ".join(marca_modelo[1:])
    precio=coche.find_element(By.XPATH, "./a/div[2]/p[@class='precio']").text[11:]
    año=coche.find_element(By.XPATH, "./a/div[2]/ul/li[1]").text
    km=coche.find_element(By.XPATH, "./a/div[2]/ul/li[3]").text
    if año=="2021" or año=="2022" or año=="2023" or año=="2024":
        diccinario=({"marca":marca, "modelo":modelo,"año":año,"kilometros":km,"precio":precio})
        return diccinario

def filtros_avanzados(driver,version_coche):
              #Buscamos el boton de version
        version=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"free-version-search-filled")))
        version.click()
        time.sleep(4)
        #Buscamos la version 
        buscador=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"free-version-search")))
        buscador.click()
        buscador.send_keys(version_coche + Keys.ENTER)

        time.sleep(2)
        #Buscamos el boton de año
        año=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"filter4")))
        año.click()
        time.sleep(2)
        #Seleccionamos el año minimo y clickamos en 2021
        año_filtro=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH," /html/body/div[2]/div[2]/form/div[7]/div/div[1]/p")))
        año_filtro.click()
        time.sleep(2)
        sleccion=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div[2]/form/div[7]/div/div[1]/ul/li/div/ul/li[5]/label/span")))
        sleccion.click()
        time.sleep(2)

        aplicar_sleccion=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div[2]/form/div[7]/div/div[3]/button/span[2]")))
        aplicar_sleccion.click()

        time.sleep(2)
        #Buscamos el boton de km
        km=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"filter5")))
        km.click()
        time.sleep(2)
        #Seleccinamos los km maximo y  escribimos 125000
        km_filtro=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div[2]/form/div[8]/div/div[2]/p")))
        km_filtro.click()
        time.sleep(2)
        sleccion=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"km-hasta")))
        sleccion.click()
        sleccion.send_keys("125000" + Keys.ENTER)
        time.sleep(2)
        aplicar_sleccion=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div[2]/form/div[8]/div/div[3]/button")))
        aplicar_sleccion.click()
def funcion_autocar():
    lista_diccionario_coches :List[Dict]=[]  #usamos una lista de diccionarios para guardar cada coche  
    #Establecemos los ajustes del drive 
    options=Options_chrome()
    options.add_argument("--disable-blink-feature=AutomationControlled")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-gpu')


    driver = webdriver.Chrome(options=options)
    driver.get('https://www.autocasion.com/?utm_source=google&utm_campaign=Autocasion%20BRAND&utm_medium=cpc&utm_term=autocasion&gad_source=1&gclid=Cj0KCQiA3sq6BhD2ARIsAJ8MRwUpaWXdFP-hHx_SIRj_TU-wKx3T6VNP9xl2LqA9PBX-G8uBbsC8Wn4aAvt2EALw_wcB')


    time.sleep(5)
        #Nos aseguramos de buscar las cookies
    try:
            cookies=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"didomi-notice-agree-button")))
            cookies.click()
    except Exception as e:
            print("No hay cookies ",e)
        #Seleccion de los parametros del Renault CLio
    try:
            #Abrimos el desplegable de marca 
            click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/p")))
            click_marca.click()
            time.sleep(4)
            #Seleccionamos la marca Seat 

            seat=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/div/ul/li[84]")))
            seat.click()
            #Abrimos el desplegable de modelo
            modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/p")))
            modelo.click()
            time.sleep(4)
            #Seleccionamos el modelo ibiza
            ibiza=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/div/ul/li[11]")))
            ibiza.click()
            time.sleep(3)
            #Buscamos 
            buscar=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[1]/button")))
            buscar.click()
    except Exception as error:
            print(error)
    time.sleep(2)

    try:
            filtros_avanzados(driver,"FR")
    except Exception as error:
            print(error)

    time.sleep(2)

    try:
        #Sacamos los coches de la pagina 
        for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)

    except Exception as e: 
        print (e)


    time.sleep(3)
    try:
        #Numero de paginas que hay 
        numero_paginas=driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[6]/div/p").text[-2:]
        print(numero_paginas)
        for _ in range(int(numero_paginas)):
            try:
                #Cambiamos de pagina 
                siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".last > span:nth-child(1)")))
                siguiente.click()

            except Exception as e:
                print("No hay mas coches de este tipo ")
            time.sleep(5)
            try:
                #Sacamos los coches de las otras paginas 
                for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)
            except Exception as e:
                print(e)

    except Exception as e:
        print (e)

        #Volvemos al inicio
    try:
            boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.logo')))
            boton_volver.click()
    except Exception as e:
            print("Error al volver al inicio",e)
    time.sleep(3)


    #Sacamos el coche Opel COrsa 
    try:
            #Abrimos el desplegable de marca 
            click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/p")))
            click_marca.click()
            time.sleep(4)
            #Seleccionamos la marca Opel 

            opel=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/div/ul/li[71]")))
            opel.click()
            #Abrimos el desplegable de modelo
            modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/p")))
            modelo.click()
            time.sleep(4)
            #Seleccionamos el modelo Corsa
            corsa=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/div/ul/li[10]")))
            corsa.click()
            time.sleep(3)
            #Buscamos 
            buscar=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[1]/button")))
            buscar.click()
    except Exception as error:
            print(error)
    time.sleep(2)

    try:
        filtros_avanzados(driver,"Gs Line")

    except Exception as error:
            print(error)

    time.sleep(2)

    try:
        #Sacamos los coches de la pagina 
        for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)

    except Exception as e: 
        print (e)


    time.sleep(3)
    try:
        #Numero de paginas que hay 
        numero_paginas=driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[5]/div/p").text[-2:]
        print(numero_paginas)
        for _ in range(int(numero_paginas)):
            try:
                #Cambiamos de pagina 
                siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".last > span:nth-child(1)")))
                siguiente.click()

            except Exception as e:
                print("No hay mas coches de este tipo ")
            time.sleep(5)
            try:
                #Sacamos los coches de las otras paginas 
                for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)
            except Exception as e:
                print(e)

    except Exception as e:
        print (e)

        #Volvemos al inicio
    try:
            boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.logo')))
            boton_volver.click()
    except Exception as e:
            print("Error al volver al inicio",e)
    time.sleep(3)
    #Sacamos el Renaul CLio
    try:
            #Abrimos el desplegable de marca 
            click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/p")))
            click_marca.click()
            time.sleep(4)
            #Seleccionamos la marca Renault 

            renault=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/div/ul/li[79]")))
            renault.click()
            #Abrimos el desplegable de modelo
            modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/p")))
            modelo.click()
            time.sleep(4)
            #Seleccionamos el modelo Clio
            clio=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/div/ul/li[5]")))
            clio.click()
            time.sleep(3)
            #Buscamos 
            buscar=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[1]/button")))
            buscar.click()
    except Exception as error:
            print(error)
    time.sleep(2)

    try:
            filtros_avanzados(driver,"Esprit Alpine")

    except Exception as error:
            print(error)

    time.sleep(2)

    try:
        #Sacamos los coches de la pagina 
        for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)

    except Exception as e: 
        print (e)


    time.sleep(3)
    try:
        #Numero de paginas que hay 
        numero_paginas=driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[6]/div/p").text[-2:]
        print(numero_paginas)
        for _ in range(1,int(numero_paginas)):
            try:
                #Cambiamos de pagina 
                siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".last > span:nth-child(1)")))
                
                siguiente.click()

            except Exception as e:
                print("No hay mas coches de este tipo ")
            time.sleep(5)
            try:
                #Sacamos los coches de las otras paginas 
                for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)
            except Exception as e:
                print(e)

    except Exception as e:
        print (e)

        #Volvemos al inicio
    try:
            boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.logo')))
            boton_volver.click()
    except Exception as e:
            print("Error al volver al inicio",e)
    time.sleep(3)
    #Sacamos el Volskwagen Polo
    try:
            #Abrimos el desplegable de marca 
            click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/p")))
            click_marca.click()
            time.sleep(4)
            #Seleccionamos la marca Volskwagen 

            Vols=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/div/ul/li[95]")))
            Vols.click()
            #Abrimos el desplegable de modelo
            modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/p")))
            modelo.click()
            time.sleep(4)
            #Seleccionamos el modelo Polo
            Polo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/div/ul/li[30]")))
            Polo.click()
            time.sleep(3)
            #Buscamos 
            buscar=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[1]/button")))
            buscar.click()
    except Exception as error:
            print(error)
    time.sleep(2)

    try:
        filtros_avanzados(driver,"r line")

    except Exception as error:
            print(error)

    time.sleep(2)

    try:
        #Sacamos los coches de la pagina 
        for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)

    except Exception as e: 
        print (e)


    time.sleep(3)
    try:
        #Numero de paginas que hay 
        numero_paginas=driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[6]/div/p").text[-2:]
        print(numero_paginas)
        for _ in range(int(numero_paginas)):
            try:
                #Cambiamos de pagina 
                siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".last > span:nth-child(1)")))
                siguiente.click()

            except Exception as e:
                print("No hay mas coches de este tipo ")
            time.sleep(5)
            try:
                #Sacamos los coches de las otras paginas 
                for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)
            except Exception as e:
                print(e)

    except Exception as e:
        print (e)

        #Volvemos al inicio
    try:
            boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.logo')))
            boton_volver.click()
    except Exception as e:
            print("Error al volver al inicio",e)
    time.sleep(3)
    #Sacamos el coche Hyundai i20
    try:
            #Abrimos el desplegable de marca 
            click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/p")))
            click_marca.click()
            time.sleep(4)
            #Seleccionamos la marca Hyundai 

            Hyundai=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/div/ul/li[37]")))
            Hyundai.click()
            #Abrimos el desplegable de modelo
            modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/p")))
            modelo.click()
            time.sleep(4)
            #Seleccionamos el modelo i20
            i20=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/div/ul/li[11]")))
            i20.click()
            time.sleep(3)
            #Buscamos 
            buscar=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[1]/button")))
            buscar.click()
    except Exception as error:
            print(error)
    time.sleep(2)

    try:
            filtros_avanzados(driver,"n line")

    except Exception as error:
            print(error)

    time.sleep(2)

    try:
        #Sacamos los coches de la pagina 
        for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)

    except Exception as e: 
        print (e)


    time.sleep(3)
    try:
        #Numero de paginas que hay 
        numero_paginas=driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[6]/div/p").text[-2:]
        print(numero_paginas)
        for _ in range(int(numero_paginas)):
            try:
                #Cambiamos de pagina 
                siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".last > span:nth-child(1)")))
                siguiente.click()

            except Exception as e:
                print("No hay mas coches de este tipo ")
            time.sleep(5)
            try:
                #Sacamos los coches de las otras paginas 
                for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)
            except Exception as e:
                print(e)

    except Exception as e:
        print (e)
    time.sleep(2)
    #Volvemos al inicio
    try:
            boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.logo')))
            boton_volver.click()
    except Exception as e:
            print("Error al volver al inicio",e)
    time.sleep(3)
    #Sacamos el coche Toyota Yaris
    try:
            #Abrimos el desplegable de marca 
            click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/p")))
            click_marca.click()
            time.sleep(4)
            #Seleccionamos la marca Toyota 

            toyta=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[1]/div/ul/li[94]")))
            toyta.click()
            #Abrimos el desplegable de modelo
            modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/p")))
            modelo.click()
            time.sleep(4)
            #Seleccionamos el modelo Yaris
            yaris=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div[1]/div[2]/div/ul/li[34]")))
            yaris.click()
            time.sleep(3)
            #Buscamos 
            buscar=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[1]/button")))
            buscar.click()
    except Exception as error:
            print(error)
    time.sleep(2)

    try:
        filtros_avanzados(driver,"Gr Sport")


    except Exception as error:
            print(error)

    time.sleep(2)

    try:
        #Sacamos los coches de la pagina 
        for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)

    except Exception as e: 
        print (e)


    time.sleep(3)
    try:
        #Numero de paginas que hay 
        numero_paginas=driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[6]/div/p").text[-2:]
        print(numero_paginas)
        for _ in range(int(numero_paginas)):
            try:
                #Cambiamos de pagina 
                siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".last > span:nth-child(1)")))
                siguiente.click()

            except Exception as e:
                print("No hay mas coches de este tipo ")
            time.sleep(5)
            try:
                #Sacamos los coches de las otras paginas 
                for coche in driver.find_elements(By.XPATH, "//div[@id='results-html']/article"):
                    diccionario=sacar_coches(coche)
                    if diccionario:
                        lista_diccionario_coches.append(diccionario)
            except Exception as e:
                print(e)

    except Exception as e:
        print (e)

        #Volvemos al inicio
    try:
            boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.logo')))
            boton_volver.click()
    except Exception as e:
            print("Error al volver al inicio",e)
    time.sleep(3)
    #Cerramos
    driver.quit()


    return lista_diccionario_coches

        