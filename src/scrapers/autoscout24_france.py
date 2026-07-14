from typing import Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options as Options_chrome


def limpiar_km(km:str)->str: #funcion auxuliar de la pagina AutoScout que nos permite mostrar los kilometros 
    limpio=km.replace("\u202f"," ")
    return limpio
def extraer_coche_AutoScout23(coche)->Dict: #Funcion que nos permite extraer todos los datos de la pagina 
        diccionario={}
        marca_modelo=coche.find_element(By.XPATH,".//a[@class='ListItem_title__ndA4s ListItem_title_new_design__QIU2b Link_link__Ajn7I']/h2").text.split() 
        marca=marca_modelo[0] #Extraemos la marca
        modelo=" ".join(marca_modelo[1:])#extraemos el modelo
        #En este try sacamos el precio de aquellos con rebajas y sin rebajas 
        try:
                     precio=coche.find_element(By.XPATH,".//p[@data-testid='regular-price']").text.split()
            
        except:
                    precio=coche.find_element(By.XPATH,".//div[@class='PriceAndSeals_current_price__ykUpx']/span").text.split()            
        precio_parte_1=precio[1]
        precio_parte_2=precio[2][:3]
        precio_final=precio_parte_1+"."+precio_parte_2
        km=limpiar_km(coche.find_element(By.XPATH,".//div[@class='VehicleDetailTable_container__XhfV1']/span[1]").text) #Obtencion de los kilometros
        año=coche.find_element(By.XPATH,".//div[@class='VehicleDetailTable_container__XhfV1']/span[3]").text #Obtenemos el año del coche y nos quedamos con los que en la pagina indican su año
        if not "- (Année)" in año:
                año=año[-4:]
                diccionario=({"marca":marca, "modelo":modelo,"año":año,"kilometros":km,"precio":precio_final})
        return(diccionario)
def auxiliar_busqueda_avanzada(driver:webdriver):
        configuracion=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/a[2]')
        configuracion.click()
        time.sleep(4)
        km=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"mileageTo-input")))
        km.click()
        km_1=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"mileageTo-input-suggestion-12")))
        time.sleep(1)
        km_1.click()
        time.sleep(5)
        buscador=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='DetailSearchPage_buttonWrapper__GXAjO']/button")))
        buscador.click()
def elegir_modelo(driver,modelo:str) :
        click_modelo =  WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[5]/div[3]/div[2]/aside/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[3]/div/input')))
        click_modelo.click()  
        time.sleep(2)
        for character in modelo:
            click_modelo.send_keys(character)
            time.sleep(0.1) 
        click_modelo.send_keys(Keys.TAB)
        time.sleep(2)
def funcion_AutoScout24():
    lista_diccionario_coches :List[Dict]=[]  #usamos una lista de diccionarios para guardar cada coche  
    #Establecemos los ajustes del drive 
    options=Options_chrome()
    options.add_argument("--disable-blink-feature=AutomationControlled")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-gpu')


    driver = webdriver.Chrome(options=options)
    driver.get('https://www.autoscout24.fr/')
    time.sleep(5)
    #Nos aseguramos de buscar las cookies
    try:
        cookies=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CLASS_NAME,"_consent-accept_1lphq_114")))
        cookies.click()
    except Exception as e:
        print("No hay cookies ",e)
    
    #Seleccion de los parametros del Renault CLio
    try:
        #Seleccionamos la marca Renault 
        click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"make")))
        click_marca.click()
        valor=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[1]/select/optgroup[1]/option[8]')
        valor.click()
        time.sleep(1)
        #Seleccionamos el model Clio
        click_modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"model")))
        click_modelo.click()
        valor_model=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[2]/select/option[11]')
        valor_model.click()
        time.sleep(1)
        #Establecemos el año minimo de matriculacion
        click_año=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"firstRegistration")))
        click_año.click()
        valor_año=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[4]/select/option[5]')
        valor_año.click()
    except Exception as e:
        print("Ocurrio un error al elegir los parametros ",e)
    time.sleep(5)
    #Hacemos busqueda avanzada del modelo Esprit Alpine 
    try:
        auxiliar_busqueda_avanzada(driver)
        time.sleep(10)
        elegir_modelo(driver,"Esprit Alpine")
        time.sleep(5)
    except Exception as e:
        print("Error en la busqueda avanzada ",e)
    time.sleep(5)
    try:
        #obttenemos los datos de los coches de la primera pagina 
        for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
            diccionario_coche=extraer_coche_AutoScout23(coche)
            if diccionario_coche:
                 lista_diccionario_coches.append(diccionario_coche)
    except Exception as e:
        print("error",e)
    time.sleep(5)
    #Si hay mas paginas de este coche, accedemos a ellas y sacamos los datos con la funcion auxiliar
    numero_paginas_vistar=len(driver.find_elements(By.XPATH,"//div[@class='ListPage_pagination__4Vw9q']//li[contains(@class, 'pagination-item')]"))
    for _ in range(numero_paginas_vistar-1):
        try:
            #Cambiamos de pagina 
            siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='prev-next']/button")))
            siguiente.click()

            time.sleep(5)
            try:
                for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
                    diccionario_coche=extraer_coche_AutoScout23(coche)
                    if diccionario_coche:
                     lista_diccionario_coches.append(diccionario_coche)
                                
            except Exception as e:
                print("Error al sacar los datos del coche ",e)
        except Exception as e:
            print("No hay mas coches de este tipo ")
    time.sleep(5)
    #Volvemos al inicio
    try:
        boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'as24-logo')))
        boton_volver.click()
    except Exception as e:
        print("Error al volver al inicio",e)
    time.sleep(3)
    
    #Ajustamos los datos del Opel Corsa 
    try:
        #Seleccionamos la marca Opel
        click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"make")))
        click_marca.click()
        valor=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[1]/select/optgroup[2]/option[176]')
        valor.click()
        time.sleep(1)
        #Seleccionamo el modelo Corsa
        click_modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"model")))
        click_modelo.click()
        valor_model=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[2]/select/option[18]')
        valor_model.click()
        time.sleep(1)
        #Establecemos el año minimo de matriculacion 
        click_año=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"firstRegistration")))
        click_año.click()
        valor_año=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[4]/select/option[5]')
        valor_año.click()
    except Exception as e:
        print("Error al ajustar los datos ",e)
    time.sleep(2)
    #Hacemos busqueda avanzada del modelo Gs Line  
    try:
        #Llamamos a la funcion auxiliar de busqueda avanzada
        auxiliar_busqueda_avanzada(driver)
        time.sleep(10)
        elegir_modelo(driver,"Gs Line")
        time.sleep(5)        


    except Exception as e:
        print("Error en la busqueda avanzada",e)
    time.sleep(5)
    try:
        #Extraemos los coches de la primera pagina inicial con ayuda de la funcion auxuliar
        for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
            diccionario_coche=extraer_coche_AutoScout23(coche)
            if diccionario_coche:
              lista_diccionario_coches.append(diccionario_coche)
                    
    except Exception as e:
        print("Error al sacar los datos de los coches",e)
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
                    diccionario_coche=extraer_coche_AutoScout23(coche)
                    if diccionario_coche:
                      lista_diccionario_coches.append(diccionario_coche)                           
            except Exception as e:
                print("Error al sacar los datos de los coches",e)
        except Exception as e:
                print("No hay mas coches de este tipo ")
    time.sleep(5)
    #Volvemos al inicio
    try:
        boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'as24-logo')))
        boton_volver.click()
    except Exception as e:
        print("Error al volver al incio",e)
    time.sleep(3)
    #Busqueda del seat Ibiza 
    try:
        #Seleccionamos la marca Seat
        click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"make")))
        click_marca.click()
        valor=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[1]/select/optgroup[2]/option[195]')
        valor.click()
        time.sleep(1)
        #Seleccionamos el modelo Ibiza
        click_modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"model")))
        click_modelo.click()
        valor_model=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[2]/select/option[11]')
        valor_model.click()
        time.sleep(1)
        #Establecemos el año minimo de matriculacion
        click_año=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"firstRegistration")))
        click_año.click()
        valor_año=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[4]/select/option[5]')
        valor_año.click()
    except Exception as e:
        print("Error al ajustar los datos del coche ",e)
    time.sleep(2)
    #Busqueda avanzada del seat ibiza fr 
    try:
        #Usamos la funcion auxiliar para la busqueda avanzada 
        auxiliar_busqueda_avanzada(driver)
        time.sleep(10)
        elegir_modelo(driver,"FR")
        time.sleep(5)

    except Exception as e:
        print("Error en la busqueda avanza",e)
    time.sleep(5)
    try:
        #Extraemos los coches de la primera pagina inicial con ayuda de la funcion auxuliar
        for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
            diccionario_coche=extraer_coche_AutoScout23(coche)
            if diccionario_coche:
             lista_diccionario_coches.append(diccionario_coche)
    except Exception as e:
        print("Error al sacar los datos del coche")
    time.sleep(5)
    #Si hay mas paginas de este coche, accedemos a ellas y  sacamos los datos con la funcion auxiliar 
    numero_paginas_vistar=len(driver.find_elements(By.XPATH,"//div[@class='ListPage_pagination__4Vw9q']//li[contains(@class, 'pagination-item')]"))
    for _ in range(numero_paginas_vistar-1):
        try:
            #Cambiamos de pagina 
            siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='prev-next']/button")))
            siguiente.click()

            time.sleep(5)
            try:
                for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
                    diccionario_coche=extraer_coche_AutoScout23(coche)
                    if diccionario_coche:
                        lista_diccionario_coches.append(diccionario_coche)
                                
            except Exception as e:
                print("error",e)
        except Exception as e:
            print("No hay mas coches de este tipo ")
    
    try:
        boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'as24-logo')))
        boton_volver.click()
    except Exception as e:
        print("Error al volver al incio",e)
    time.sleep(3)
    

    #Busqueda del coche Hyundai i20 n-line 
    try:
        #Seleccionamos la marca Hyundai
        click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"make")))
        click_marca.click()
        valor=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[1]/select/optgroup[2]/option[108]')
        valor.click()
        time.sleep(1)
        #Seleccionamos el modeloi20
        click_modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"model")))
        click_modelo.click()
        valor_model=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[2]/select/option[26]')
        valor_model.click()
        time.sleep(1)
        #Establecemos el año minimo de matriculacion
        click_año=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"firstRegistration")))
        click_año.click()
        valor_año=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[4]/select/option[5]')
        valor_año.click()
    except Exception as e:
        print("Error al ajustar los datos del coche ",e)
    time.sleep(2)
    #Busqueda de la marca   n-line
    try:
        #Usamos la funcion auxiliar para la busqueda avanzada 
        auxiliar_busqueda_avanzada(driver)
        time.sleep(5)
        elegir_modelo(driver,'n-line')
        time.sleep(10)

    except Exception as e:
        print("Error en la busqueda avanza",e)
    time.sleep(5)
    try:
        #Extraemos los coches de la primera pagina inicial con ayuda de la funcion auxuliar
        for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
            diccionario_coche=extraer_coche_AutoScout23(coche)
            if diccionario_coche:
             lista_diccionario_coches.append(diccionario_coche)
    except Exception as e:
        print("Error al sacar los datos del coche")
    time.sleep(5)
    #Si hay mas paginas de este coche, accedemos a ellas y  sacamos los datos con la funcion auxiliar 
    numero_paginas_vistar=len(driver.find_elements(By.XPATH,"//div[@class='ListPage_pagination__4Vw9q']//li[contains(@class, 'pagination-item')]"))
    for _ in range(numero_paginas_vistar-1):
        try:
            #Cambiamos de pagina 
            siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='prev-next']/button")))
            siguiente.click()

            time.sleep(5)
            try:
                for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
                    diccionario_coche=extraer_coche_AutoScout23(coche)
                    if diccionario_coche:
                        lista_diccionario_coches.append(diccionario_coche)
                                
            except Exception as e:
                print("error",e)
        except Exception as e:
            print("No hay mas coches de este tipo ")

    try:
        boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'as24-logo')))
        boton_volver.click()
    except Exception as e:
        print("Error al volver al incio",e)
    time.sleep(3)
   #Busqueda del coche Volkswagen polo r-line 
    try:
        #Seleccionamos la marca Hyundai
        click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"make")))
        click_marca.click()
        valor=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[1]/select/optgroup[1]/option[4]')
        valor.click()
        time.sleep(1)
        #Seleccionamos el modelo Ibiza
        click_modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"model")))
        click_modelo.click()
        valor_model=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[2]/select/option[61]')
        valor_model.click()
        time.sleep(1)
        #Establecemos el año minimo de matriculacion
        click_año=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"firstRegistration")))
        click_año.click()
        valor_año=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[4]/select/option[5]')
        valor_año.click()
    except Exception as e:
        print("Error al ajustar los datos del coche ",e)
    time.sleep(2)
    #Busqueda del modelo  r-line 
    try:
        #Usamos la funcion auxiliar para la busqueda avanzada 
        auxiliar_busqueda_avanzada(driver)
        time.sleep(5)
        elegir_modelo(driver,'r-line')
        time.sleep(10)

    except Exception as e:
        print("Error en la busqueda avanza",e)
    time.sleep(5)
    try:
        #Extraemos los coches de la primera pagina inicial con ayuda de la funcion auxuliar
        for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
            diccionario_coche=extraer_coche_AutoScout23(coche)
            if diccionario_coche:
             lista_diccionario_coches.append(diccionario_coche)
    except Exception as e:
        print("Error al sacar los datos del coche")
    time.sleep(5)
    #Si hay mas paginas de este coche, accedemos a ellas y  sacamos los datos con la funcion auxiliar 
    numero_paginas_vistar=len(driver.find_elements(By.XPATH,"//div[@class='ListPage_pagination__4Vw9q']//li[contains(@class, 'pagination-item')]"))
    for _ in range(numero_paginas_vistar-1):
        try:
            #Cambiamos de pagina 
            siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='prev-next']/button")))
            siguiente.click()

            time.sleep(5)
            try:
                for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
                    diccionario_coche=extraer_coche_AutoScout23(coche)
                    if diccionario_coche:
                        lista_diccionario_coches.append(diccionario_coche)
                                
            except Exception as e:
                print("error",e)
        except Exception as e:
            print("No hay mas coches de este tipo ")
    try:
        boton_volver=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'as24-logo')))
        boton_volver.click()
    except Exception as e:
        print("Error al volver al incio",e)
    time.sleep(3)

    #Busqueda del coche Toyota yaris gr sport
    try:
        #Seleccionamos la marca Toyota
        click_marca=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"make")))
        click_marca.click()
        valor=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[1]/select/optgroup[1]/option[5]')
        valor.click()
        time.sleep(1)
        #Seleccionamos el modelo Yaris
        click_modelo=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"model")))
        click_modelo.click()
        valor_model=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[2]/select/option[99]')
        valor_model.click()
        time.sleep(1)
        #Establecemos el año minimo de matriculacion
        click_año=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"firstRegistration")))
        click_año.click()
        valor_año=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/section[1]/div[1]/div/section/div[2]/div/div[4]/select/option[5]')
        valor_año.click()
    except Exception as e:
        print("Error al ajustar los datos del coche ",e)
    time.sleep(2)
    #Busqueda del modelo gr sport
    try:
        #Usamos la funcion auxiliar para la busqueda avanzada 
        auxiliar_busqueda_avanzada(driver)
        time.sleep(5)
        elegir_modelo(driver,'gr sport')
        time.sleep(10)

    except Exception as e:
        print("Error en la busqueda avanza",e)
    time.sleep(5)
    try:
        #Extraemos los coches de la primera pagina inicial con ayuda de la funcion auxuliar
        for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
            diccionario_coche=extraer_coche_AutoScout23(coche)
            if diccionario_coche:
             lista_diccionario_coches.append(diccionario_coche)
    except Exception as e:
        print("Error al sacar los datos del coche")
    time.sleep(5)
    #Si hay mas paginas de este coche, accedemos a ellas y  sacamos los datos con la funcion auxiliar 
    numero_paginas_vistar=len(driver.find_elements(By.XPATH,"//div[@class='ListPage_pagination__4Vw9q']//li[contains(@class, 'pagination-item')]"))
    for _ in range(numero_paginas_vistar-1):
        try:
            #Cambiamos de pagina 
            siguiente=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//li[@class='prev-next']/button")))
            siguiente.click()

            time.sleep(5)
            try:
                for coche in driver.find_elements(By.XPATH,"//main[@class='ListPage_main___0g2X']/article[@class='cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7']"):
                    diccionario_coche=extraer_coche_AutoScout23(coche)
                    if diccionario_coche:
                        lista_diccionario_coches.append(diccionario_coche)
                                
            except Exception as e:
                print("error",e)
        except Exception as e:
            print("No hay mas coches de este tipo ")


    #Esperamos y cerramos
    time.sleep(5)
    driver.quit()
    return(lista_diccionario_coches)