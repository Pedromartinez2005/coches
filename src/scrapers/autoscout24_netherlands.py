import time
from typing import Dict ,List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    
import re


#Defino esta función que me ayudará a a extraer cierta información de la web más adelante
def extraer_contenido(pattern, content):
    contenido = re.findall(pattern, content)
    return contenido[0] if contenido else None

def funcion_extraer_coche(marca,modelo,version,coche):
                # Extraer la información de cada coche
    try:
        precio = coche.find_element(By.CLASS_NAME, "PriceAndSeals_current_price__ykUpx").text.split()            
        precio_parte_1 = precio[1][:6]
        precio_parte_2 = precio[0]
        precio_final = precio_parte_1+precio_parte_2
        km = extraer_contenido(r"([\d.,]+)\s*km", coche.find_element(By.CLASS_NAME, "VehicleDetailTable_item__4n35N").text) + "km"
        año_txt = coche.find_element(By.XPATH, ".//div[@class='VehicleDetailTable_container__XhfV1']/span[3]").text.split("/")
        año = año_txt[1]
        return {"marca":marca,"modelo":modelo +" "+ version,"año":año,"kilometros":km,"precio": precio_final}
    except:
        return {}
def funcion_autoscout_holada():
    lista_diccionario_coches :List[Dict]=[]
    driver = webdriver.Chrome()

    # Defino una variable con la URL de la pagina, en mi caso Autoscout24, y accedo a ella
    autoscout24 = "https://www.autoscout24.com/"
    driver.get(autoscout24)
    time.sleep(2)



    #Ahora comienzo a automatizar la búsqueda que nos interesa para nuestro trabajo
    try:
        #Para aceptar las cookies
        cookies = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@class, '_consent-accept_1lphq_114')]"))
        )
        cookies.click()
        time.sleep(.5)

    except Exception as e1:
        print(f'Error al aceptar las cookies {e1}')  
    try:
        # Clico en el boton de refine search para una búsqueda más detallada
        ref_search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'hf-searchmask-form__detail-search')]"))
        )
        ref_search.click()
        time.sleep(.5)

        # Acceso al seleccionador de marca
        buscar_marca = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_marca.click()
        time.sleep(.5)

        # Selecciono Opel que en este caso es la marca de la que quiero extraer información
        opel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "make-input-primary-filter-suggestion-4"))
        )
        opel.click()
        time.sleep(1.5)

        # Acceso al seleccionador de modelo
        buscar_modelo = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_modelo[1].click()
        time.sleep(.5)

        # Selecciono Corsa que en este caso es la marca de la que quiero extraer información
        corsa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "model-input-54||||0-suggestion-16"))
        )
        corsa.click()
        time.sleep(.5)

        # Utilizo 'Keys' para buscar la versión de Opel corsa de la cual queremos extraer información
        version = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "version-input-54|1918|||0"))
        )
        version.send_keys("GS Line")
        time.sleep(.5)

        # Acceso al seleccionador de año
        buscar_año = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_año[2].click()
        time.sleep(.5)

        # Selecciono 2021 que en este caso es el año a partir del cual quiero extraer información
        año = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "firstRegistrationFrom-input-suggestion-3")) 
        )
        año.click()
        time.sleep(1.5)

        # Acceso al seleccionador de país
        buscar_pais = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID,"country-input"))
        )
        buscar_pais.click()
        time.sleep(.5)

        # Selecciono Holanda que en este caso es el país en el que quiero estudiar estos modelos de coche
        holanda = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "country-input-suggestion-8"))
        )
        holanda.click()
        time.sleep(.5)

        # Acceso al seleccionador de klómetros
        buscar_km = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_km[8].click()
        time.sleep(.5)

        # Selecciono 50.000 que en este caso es el número máximo de kilómetros para los coches de los quiero extraer información
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mileageTo-input-suggestion-12"))
        )
        km.click()
        time.sleep(.75)

        # Clico en el botón de búsqueda de resultados para acceder a ellos
        resutados = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//*[@id='__next']/div/div/div[3]/div[3]/button")) 
        )
        resutados.click()
        time.sleep(3)

    except Exception as e:
        print(f"Se produjo un error: {e}")


  
    try:

        lista_diccionario_coches_opel: list[Dict] = []

        main_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ListPage_main___0g2X"))
        )
        
        # Ahora puedo obtener los artículos dentro del main
        coches = main_element.find_elements(By.TAG_NAME, "article")
        
        for coche in coches:
            diccionario_coche=funcion_extraer_coche('Opel','Corsa','Gs Line',coche)
            if diccionario_coche:
                lista_diccionario_coches_opel.append(diccionario_coche)
            
        lista_diccionario_coches.extend(lista_diccionario_coches_opel)
        
    
    except Exception as e:
        print(f"Error al extraer los artículos: {e}")

    #Si hay mas paginas de este coche, accedemos a ellas y sacamos los datos con la misma funcion auxiliar
    numero_paginas_vistar=len(driver.find_elements(By.XPATH,"//div[@class='ListPage_pagination__4Vw9q']//li[contains(@class, 'pagination-item')]"))
    for _ in range(numero_paginas_vistar-1):
        try:
            #Cambiamos de pagina 
            siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='prev-next']/button")))
            siguiente.click()
        
            time.sleep(5)

            try:
                for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
                    diccionario_coche=funcion_extraer_coche('Opel','Corsa','Gs Line',coche)
                    if diccionario_coche:
                     lista_diccionario_coches.append(diccionario_coche)                          
            except Exception as e:
                print("Error al sacar los datos de los coches",e)
        except Exception as e:
            print("No hay mas coches de este tipo")
            
    time.sleep(5)


    # Ahora clico el botón que te hace regresar al home de Autoscout24 y comienzo la búsqueda del segundo coche
    try:
            boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'as24-logo')))
            boton_volver.click()

    except Exception as e:
        print(f"Error al regresar al inicio: {e}")
    time.sleep(3)

    try:
        # Clico en el boton de refine search para una búsqueda más detallada
        ref_search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'hf-searchmask-form__detail-search')]"))
        )
        ref_search.click()
        time.sleep(1)

        # Aprovecho algunos campos que se guardan y automatizo los cambios necesarios
        # Acceso al seleccionador de marca
        buscar_marca = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/input"))
        )
        buscar_marca.click()
        time.sleep(1)
        

        # Selecciono SEAT que en este caso es la marca de la que quiero extraer información
        seat = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[3]/div/ul/li[206]"))
        )
        seat.click()
        time.sleep(3)


        # Acceso al seleccionador de modelo
        buscar_modelo = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_modelo[1].click()
        time.sleep(.5)

        # Selecciono Ibiza que en este caso es la marca de la que quiero extraer información
        ibiza = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "model-input-64||||0-suggestion-9"))
        )
        ibiza.click()
        time.sleep(.5)

        # Utilizo 'Keys' para buscar la versión de SEAT Ibiza de la cual queremos extraer información
        version = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "version-input-64|2006|||0"))
        )
        version.send_keys("FR")
        time.sleep(.5)


        # Acceso al seleccionador de klómetros
        buscar_km = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_km[8].click()
        time.sleep(.5)


        # Selecciono 50.000 que en este caso es el número máximo de kilómetros para los coches de los quiero extraer información
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mileageTo-input-suggestion-12"))
        )
        km.click()
        time.sleep(.75)

        # Clico en el botón de búsqueda de resultados para acceder a ellos
        resutados = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//*[@id='__next']/div/div/div[3]/div[3]/button")) 
        )
        resutados.click()
        time.sleep(3)

        
    except Exception as e:
        print(f"Se produjo un error: {e}")

        
    try:

        lista_diccionario_coches_seat: list[Dict] = []
        
        main_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ListPage_main___0g2X"))
        )
        
        coches = main_element.find_elements(By.TAG_NAME, "article")
        for coche in coches:

            diccionario_coche=funcion_extraer_coche('Seat','Ibiza','FR',coche)
            if diccionario_coche:
                 lista_diccionario_coches_seat.append(diccionario_coche)

            
        lista_diccionario_coches.extend(lista_diccionario_coches_seat)
    
        

    except Exception as e:
        print(f"Error al extraer los artículos: {e}")

    #Si hay mas paginas de este coche, accedemos a ellas y sacamos los datos con la misma funcion auxiliar
    numero_paginas_vistar=len(driver.find_elements(By.XPATH,"//div[@class='ListPage_pagination__4Vw9q']//li[contains(@class, 'pagination-item')]"))
    for _ in range(numero_paginas_vistar-1):
        try:
            #Cambiamos de pagina 
            siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='prev-next']/button")))
            siguiente.click()
        
            time.sleep(5)

            try:
                for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
                    diccionario_coche=funcion_extraer_coche('Seat','Ibiza','FR',coche)
                    if diccionario_coche:
                     lista_diccionario_coches.append(diccionario_coche)                          
            except Exception as e:
                print("Error al sacar los datos de los coches",e)
        except Exception as e:
            print("No hay mas coches de este tipo")
            
    time.sleep(5)

    # Vuelvo a clicar el botón que te hace regresar al home de Autoscout24 y comienzo la búsqueda del tercer coche

    try:
            boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'as24-logo')))
            boton_volver.click()

    except Exception as e:
        print(f"Error al regresar al inicio: {e}")
    time.sleep(3)


    try:
        # Clico en el boton de refine search para una búsqueda más detallada
        ref_search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'hf-searchmask-form__detail-search')]"))
        )
        ref_search.click()
        time.sleep(1)


        # Acceso al seleccionador de marca
        buscar_marca = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/input"))
        )
        buscar_marca.click()
        time.sleep(1)
        

        # Selecciono Renault que en este caso es la marca de la que quiero extraer información
        renault = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[3]/div/ul/li[8]"))
        )
        renault.click()
        time.sleep(3)


        # Acceso al seleccionador de modelo
        buscar_modelo = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_modelo[1].click()
        time.sleep(.5)

        # Selecciono Clio que en este caso es la marca de la que quiero extraer información
        clio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "model-input-60||||0-suggestion-9"))
        )
        clio.click()
        time.sleep(.5)

        # Utilizo 'Keys' para buscar la versión de Renault Clio de la cual queremos extraer información
        version = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "version-input-60|1961|||0"))
        )
        version.send_keys("Alpine")
        time.sleep(.5)

        # Acceso al seleccionador de klómetros
        buscar_km = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_km[8].click()
        time.sleep(.5)

        # Selecciono 50.000 que en este caso es el número máximo de kilómetros para los coches de los quiero extraer información
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mileageTo-input-suggestion-12"))
        )
        km.click()
        time.sleep(.75)

        # Clico en el botón de búsqueda de resultados para acceder a ellos
        resutados = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//*[@id='__next']/div/div/div[3]/div[3]/button")) 
        )
        resutados.click()
        time.sleep(10)

        
    except Exception as e:
        print(f"Se produjo un error: {e}")


    try:

        lista_diccionario_coches_renault: list[Dict] = []

        main_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ListPage_main___0g2X"))
        )
        
        coches = main_element.find_elements(By.TAG_NAME, "article")
        
        for coche in coches:

            # Extraer la información de cada coch
            diccionario_coche=funcion_extraer_coche("Renault",'Clio','Espirit Alpine',coche)
            if diccionario_coche:
                 lista_diccionario_coches_renault.append(diccionario_coche)
        lista_diccionario_coches.extend(lista_diccionario_coches_renault)

    except Exception as e:
        print(f"Error al extraer los artículos: {e}")

    #Si hay mas paginas de este coche, accedemos a ellas y sacamos los datos con la misma funcion auxiliar
    numero_paginas_vistar=len(driver.find_elements(By.XPATH,"//div[@class='ListPage_pagination__4Vw9q']//li[contains(@class, 'pagination-item')]"))
    for _ in range(numero_paginas_vistar-1):
        try:
            #Cambiamos de pagina 
            siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='prev-next']/button")))
            siguiente.click()

            time.sleep(5)

            try:
                for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
                    diccionario_coche=funcion_extraer_coche("Renault",'Clio','Espirit Alpine',coche)
                    if diccionario_coche:
                     lista_diccionario_coches.append(diccionario_coche)                          
            except Exception as e:
                print("Error al sacar los datos de los coches",e)
        except Exception as e:
            print("No hay mas coches de este tipo")
            
    time.sleep(5)



    # Vuelvo a clicar el botón que te hace regresar al home de Autoscout24 y comienzo la búsqueda del tercer coche

    try:
            boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'as24-logo')))
            boton_volver.click()

    except Exception as e:
        print(f"Error al regresar al inicio: {e}")
    time.sleep(3)


    try:
        # Clico en el boton de refine search para una búsqueda más detallada
        ref_search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'hf-searchmask-form__detail-search')]"))
        )
        ref_search.click()
        time.sleep(1)


        # Acceso al seleccionador de marca
        buscar_marca = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/input"))
        )
        buscar_marca.click()
        time.sleep(1)
        

        # Selecciono Hyundai que en este caso es la marca de la que quiero extraer información
        hyundai = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[3]/div/ul/li[117]"))
        )
        hyundai.click()
        time.sleep(3)


        # Acceso al seleccionador de modelo
        buscar_modelo = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_modelo[1].click()
        time.sleep(.5)

        # Selecciono i20 que en este caso es la marca de la que quiero extraer información
        i20 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "model-input-33||||0-suggestion-24"))
        )
        i20.click()
        time.sleep(.5)

        # Utilizo 'Keys' para buscar la versión de Hyundai i20 de la cual queremos extraer información
        version = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "version-input-33|19188|||0"))
        )
        version.send_keys("N-line")
        time.sleep(.5)

        # Acceso al seleccionador de klómetros
        buscar_km = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_km[8].click()
        time.sleep(.5)

        # Selecciono 50.000 que en este caso es el número máximo de kilómetros para los coches de los quiero extraer información
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mileageTo-input-suggestion-12"))
        )
        km.click()
        time.sleep(.75)

        # Clico en el botón de búsqueda de resultados para acceder a ellos
        resutados = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//*[@id='__next']/div/div/div[3]/div[3]/button")) 
        )
        resutados.click()
        time.sleep(10)

        
    except Exception as e:
        print(f"Se produjo un error: {e}")


    try:

        lista_diccionario_coches_hyundai: list[Dict] = []

        main_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ListPage_main___0g2X"))
        )
        
        coches = main_element.find_elements(By.TAG_NAME, "article")
        
        for coche in coches:

            diccionario_coche=funcion_extraer_coche("Hyundai",'i20','N-line',coche)
            if diccionario_coche:
             lista_diccionario_coches_hyundai.append(diccionario_coche)

            
        lista_diccionario_coches.extend(lista_diccionario_coches_hyundai)
        

    except Exception as e:
        print(f"Error al extraer los artículos: {e}")

    #Si hay mas paginas de este coche, accedemos a ellas y sacamos los datos con la misma funcion auxiliar
    numero_paginas_vistar=len(driver.find_elements(By.XPATH,"//div[@class='ListPage_pagination__4Vw9q']//li[contains(@class, 'pagination-item')]"))
    for _ in range(numero_paginas_vistar-1):
        try:
            #Cambiamos de pagina 
            siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='prev-next']/button")))
            siguiente.click()

            time.sleep(5)

            try:
                for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
                    diccionario_coche=funcion_extraer_coche("Hyundai",'i20','N-line',coche)
                    if diccionario_coche:
                     lista_diccionario_coches.append(diccionario_coche)                          
            except Exception as e:
                print("Error al sacar los datos de los coches",e)
        except Exception as e:
            print("No hay mas coches de este tipo")
            
    time.sleep(5)

    # Vuelvo a clicar el botón que te hace regresar al home de Autoscout24 y comienzo la búsqueda del tercer coche

    try:
            boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'as24-logo')))
            boton_volver.click()

    except Exception as e:
        print(f"Error al regresar al inicio: {e}")
    time.sleep(3)


    try:
        # Clico en el boton de refine search para una búsqueda más detallada
        ref_search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'hf-searchmask-form__detail-search')]"))
        )
        ref_search.click()
        time.sleep(1)


        # Acceso al seleccionador de marca
        buscar_marca = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/input"))
        )
        buscar_marca.click()
        time.sleep(1)
        

        # Selecciono Toyota que en este caso es la marca de la que quiero extraer información
        toyota = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[3]/div/ul/li[237]"))
        )
        toyota.click()
        time.sleep(3)


        # Acceso al seleccionador de modelo
        buscar_modelo = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_modelo[1].click()
        time.sleep(.5)

        # Selecciono Yaris que en este caso es la marca de la que quiero extraer información
        yaris = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "model-input-70||||0-suggestion-97"))
        )
        yaris.click()
        time.sleep(.5)

        # Utilizo 'Keys' para buscar la versión de Hyundai i20 de la cual queremos extraer información
        version = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "version-input-70|15663|||0"))
        )
        version.send_keys("GR-Sport")
        time.sleep(.5)

        # Acceso al seleccionador de klómetros
        buscar_km = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_km[8].click()
        time.sleep(.5)

        # Selecciono 50.000 que en este caso es el número máximo de kilómetros para los coches de los quiero extraer información
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mileageTo-input-suggestion-12"))
        )
        km.click()
        time.sleep(.75)

        # Clico en el botón de búsqueda de resultados para acceder a ellos
        resutados = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//*[@id='__next']/div/div/div[3]/div[3]/button")) 
        )
        resutados.click()
        time.sleep(10)

        
    except Exception as e:
        print(f"Se produjo un error: {e}")


    try:

        lista_diccionario_coches_toyota: list[Dict] = []

        main_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ListPage_main___0g2X"))
        )
        
        coches = main_element.find_elements(By.TAG_NAME, "article")
        
        for coche in coches:

            diccionario_coche=funcion_extraer_coche('Toyota','Yaris','GR-Sport',coche)
            if diccionario_coche:
             lista_diccionario_coches_toyota.append(diccionario_coche)
            
        lista_diccionario_coches.extend(lista_diccionario_coches_toyota)
    
    except Exception as e:
        print(f"Error al extraer los artículos: {e}")
    #Si hay mas paginas de este coche, accedemos a ellas y sacamos los datos con la misma funcion auxiliar
    numero_paginas_vistar=len(driver.find_elements(By.XPATH,"//div[@class='ListPage_pagination__4Vw9q']//li[contains(@class, 'pagination-item')]"))
    for _ in range(numero_paginas_vistar-1):
        try:
            #Cambiamos de pagina 
            siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='prev-next']/button")))
            siguiente.click()

            time.sleep(5)

            try:
                for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
                    diccionario_coche=funcion_extraer_coche('Toyota','Yaris','GR-Sport',coche)
                    if diccionario_coche:
                     lista_diccionario_coches.append(diccionario_coche)                          
            except Exception as e:
                print("Error al sacar los datos de los coches",e)
        except Exception as e:
            print("No hay mas coches de este tipo")            
    time.sleep(5)


    # Vuelvo a clicar el botón que te hace regresar al home de Autoscout24 y comienzo la búsqueda del tercer coche

    try:
            boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'as24-logo')))
            boton_volver.click()

    except Exception as e:
        print(f"Error al regresar al inicio: {e}")
    time.sleep(3)


    try:
        # Clico en el boton de refine search para una búsqueda más detallada
        ref_search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'hf-searchmask-form__detail-search')]"))
        )
        ref_search.click()
        time.sleep(1)


        # Acceso al seleccionador de marca
        buscar_marca = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/input"))
        )
        buscar_marca.click()
        time.sleep(1)
        

        # Selecciono Volskwagen que en este caso es la marca de la que quiero extraer información
        volskwagen = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[3]/div/ul/li[7]"))
        )
        volskwagen.click()
        time.sleep(3)


        # Acceso al seleccionador de modelo
        buscar_modelo = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_modelo[1].click()
        time.sleep(.5)

        # Selecciono Polo que en este caso es la marca de la que quiero extraer información
        polo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "model-input-74||||0-suggestion-58"))
        )
        polo.click()
        time.sleep(.5)

        # Utilizo 'Keys' para buscar la versión de Hyundai i20 de la cual queremos extraer información
        version = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "version-input-74||99||0"))
        )
        version.send_keys("R-line")
        time.sleep(.5)

        # Acceso al seleccionador de klómetros
        buscar_km = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'input-icon-button')]"))
        )
        buscar_km[8].click()
        time.sleep(.5)

        # Selecciono 50.000 que en este caso es el número máximo de kilómetros para los coches de los quiero extraer información
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mileageTo-input-suggestion-12"))
        )
        km.click()
        time.sleep(.75)

        # Clico en el botón de búsqueda de resultados para acceder a ellos
        resutados = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,"//*[@id='__next']/div/div/div[3]/div[3]/button")) 
        )
        resutados.click()
        time.sleep(10)

        
    except Exception as e:
        print(f"Se produjo un error: {e}")


    try:

        lista_diccionario_coches_volskwagen: list[Dict] = []

        main_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ListPage_main___0g2X"))
        )
        
        coches = main_element.find_elements(By.TAG_NAME, "article")
        
        for coche in coches:

            # Extraer la información de cada coche
            marca = "Volskwagen"
            modelo = "Polo"
            version = "R-line"
            diccionario_coche=funcion_extraer_coche("Volskwagen","Polo","R-line",coche)
            if diccionario_coche:
              lista_diccionario_coches_volskwagen.append(diccionario_coche)

            
        lista_diccionario_coches.extend(lista_diccionario_coches_volskwagen)
    
    except Exception as e:
        print(f"Error al extraer los artículos: {e}")

        #Si hay mas paginas de este coche, accedemos a ellas y sacamos los datos con la misma funcion auxiliar
    numero_paginas_vistar=len(driver.find_elements(By.XPATH,"//div[@class='ListPage_pagination__4Vw9q']//li[contains(@class, 'pagination-item')]"))
    for _ in range(numero_paginas_vistar-1):
        try:
            #Cambiamos de pagina 
            siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='prev-next']/button")))
            siguiente.click()

            time.sleep(5)

            try:
                for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
                    diccionario_coche=funcion_extraer_coche("Volskwagen","Polo","R-line",coche)
                    if diccionario_coche:
                     lista_diccionario_coches.append(diccionario_coche)                          
            except Exception as e:
                print("Error al sacar los datos de los coches",e)
        except Exception as e:
            print("No hay mas coches de este tipo")
            
    time.sleep(5)

    
    return(lista_diccionario_coches)