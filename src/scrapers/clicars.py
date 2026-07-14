from typing import Dict, List
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.firefox.options import Options as Options_firefox
import re


def extraer_contenido(patter,content): #Funcion auxiliar para sacar contenido de una cadena con una regex
    contenido=re.findall(patter,content)
    return contenido[0]
#Funcion auxiliar que nos permite mover el slide de los años y los kilometros a la posicion  2021 y 50000
def funcion_ajustar_datos(driver): 
        click_km= WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="filtros-desplegables"]/div/div/div[7]/div/div[1]/div/a/span[1]')))
        click_km.click()
        km_max=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="km-and-years"]/div/div[1]/div[1]/div/div[2]/div[7]')))
        año=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="km-and-years"]/div/div[1]/div[2]/div/div[2]/div[5]')))
        actions=ActionChains(driver)
        actions.click_and_hold(km_max).move_by_offset(-120,0).release()
        actions.move_to_element(año)
        actions.click_and_hold(año).move_by_offset(400,0).release()
        actions.perform()
        time.sleep(2)
        aceptar= WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="km-and-years"]/div/div[2]/div/sr-button')))
        aceptar.click()
        time.sleep(5)
#Funcion que busca los coches establecidos en la pagina cliclars
def funcion_clicars():
    lista_diccionario_coches :List[Dict]=[]   
    opciones_firefox=Options_firefox()
    driver=webdriver.Firefox(options=opciones_firefox)
    driver.get("https://www.clicars.com/")
    time.sleep(3.5)
    #aceptar cookies si las hay
    try:
        WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CLASS_NAME, 'banner-actions-container')))
        cookie_botton= WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        cookie_botton.click()
    except :
        print ("No hay cookies")
    time.sleep(3)
    #Quitar ventana emergente 
    try:
        ventana=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="campaign-modal"]/div/div/div')))
        ventana.click()
    except  :
        print("No hay ventana emergente ")
    #busqueda de coche Opel corsa gs-line
    try:
        click_bar= WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,'autocomplete-1-input')))
        click_bar.send_keys("Opel Corsa gs-line" +Keys.ENTER)
    except Exception as e:
        print("Coche no encontrado")
    time.sleep(3)
     #Ajuste de los datos de los coches 
    try:
        funcion_ajustar_datos(driver)
    except  Exception as e:
        print("Error al ajustar los datos",e)
    #Obtencion de los datos del corsa 
    try:
        for coche in driver.find_elements(By.XPATH,'//div[@id="vehicles_list"]/article[@class="sale-list__item"]'):
            marca=coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/strong').text
            marca_final=extraer_contenido(r'Opel',marca)
            parte_modelo=extraer_contenido(r'Corsa',marca)
            modelo= parte_modelo+" "+coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[1]').text
            año= extraer_contenido(r"\b\d{4}\b",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            km= extraer_contenido(r"(\d+[.]\d+km|\d+km)",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            precio=coche.find_element(By.XPATH, './/div[@class="car-card-data right pl-4 col-auto"]/span[2]/strong').text
            lista_diccionario_coches.append({"marca":marca_final, "modelo":modelo,"año":año,"kilometros":km,"precio":precio})
    except :
        print("La busqueda no tiene coches ")

    #Busqueda de coche Seat Ibiza fr
    try: 
        click_bar=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,'autocomplete-1-input')))
        click_bar.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
        click_bar.send_keys("Seat Ibiza fr"+Keys.ENTER)
    except:
        print("No existe el coche buscado")
    #Ajuste de los datos de los coches 
    try:
        funcion_ajustar_datos(driver)

    except Exception as e:
        print("Error al ajustar los datos ")
    #Obtenemos los datos de los coches 
    try:
        for coche in driver.find_elements(By.XPATH,'//div[@id="vehicles_list"]/article[@class="sale-list__item"]'):
            marca=coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/strong').text
            marca_final=extraer_contenido(r'SEAT',marca)
            parte_modelo=extraer_contenido(r'Ibiza',marca)
            modelo= parte_modelo +" "+coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[1]').text
            año= extraer_contenido(r"\b\d{4}\b",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            km= extraer_contenido(r"(\d+[.]\d+km|\d+km)",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            precio=coche.find_element(By.XPATH, './/div[@class="car-card-data right pl-4 col-auto"]/span[2]/strong').text
            lista_diccionario_coches.append({"marca":marca_final, "modelo":modelo,"año":año,"kilometros":km,"precio":precio})
    except:
        print("La busqueda no tiene coches ")
    time.sleep(4)
    #Busqueda del coche renaul clio esprit alpine 
    try: 
        click_bar=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,'autocomplete-1-input')))
        click_bar.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
        click_bar.send_keys("Renault clio esprit alpine"+Keys.ENTER)
    except :
        print("No existe el coche buscado")
    #Ajuste de los datos de los coches 
    try:
        funcion_ajustar_datos(driver)
    except:
        print("Error al ajustar datos")
    #Obtenemos los datos de los coches 
    try:
        for coche in driver.find_elements(By.XPATH,'//div[@id="vehicles_list"]/article[@class="sale-list__item"]'):
            marca=coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/strong').text
            marca_final=extraer_contenido(r'Renault',marca)
            parte_modelo=extraer_contenido(r'Clio',marca)
            modelo=parte_modelo +" "+coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[1]').text
            año= extraer_contenido(r"\b\d{4}\b",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            km= extraer_contenido(r"(\d+[.]\d+km|\d+km)",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            precio=coche.find_element(By.XPATH, './/div[@class="car-card-data right pl-4 col-auto"]/span[2]/strong').text
            lista_diccionario_coches.append({"marca":marca_final, "modelo":modelo,"año":año,"kilometros":km,"precio":precio})
    except Exception as e:
        print("La busqueda no tiene coches ")
    time.sleep(3)
    #Busqueda del coche Hyundai i20 n-line
    try: 
        click_bar=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,'autocomplete-1-input')))
        click_bar.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
        click_bar.send_keys(" Hyundai i20 n-line"+Keys.ENTER)
    except :
        print("No existe el coche buscado")

    #Ajuste de los datos de los coches 
    try:
        funcion_ajustar_datos(driver)

    except Exception as e:
        print("Error al ajustar los datos ")

    #Obtenemos los datos de los coches 
    
    try:
        for coche in driver.find_elements(By.XPATH,'//div[@id="vehicles_list"]/article[@class="sale-list__item"]'):
            marca=coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/strong').text
            marca_final=extraer_contenido(r'Hyundai',marca)
            parte_modelo=extraer_contenido(r'i20',marca)
            modelo=parte_modelo +" "+coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[1]').text
            año= extraer_contenido(r"\b\d{4}\b",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            km= extraer_contenido(r"(\d+[.]\d+km|\d+km)",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            precio=coche.find_element(By.XPATH, './/div[@class="car-card-data right pl-4 col-auto"]/span[2]/strong').text
            lista_diccionario_coches.append({"marca":marca_final, "modelo":modelo,"año":año,"kilometros":km,"precio":precio})
    except:
        print("La busqueda no tiene coches ")

        #Busqueda del coche  Volkswagen polo r-line
    try: 
        click_bar=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,'autocomplete-1-input')))
        click_bar.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
        click_bar.send_keys("  Volkswagen polo r-line"+Keys.ENTER)
    except :
        print("No existe el coche buscado")

    #Ajuste de los datos de los coches 
    try:
        funcion_ajustar_datos(driver)

    except:
        print("Error al ajustar los datos ")

    #Obtenemos los datos de los coches 
    
    try:
        for coche in driver.find_elements(By.XPATH,'//div[@id="vehicles_list"]/article[@class="sale-list__item"]'):
            marca=coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/strong').text
            marca_final=extraer_contenido(r'Volskwagen',marca)
            parte_modelo=extraer_contenido(r'Polo',marca)
            modelo=parte_modelo +" "+coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[1]').text
            año= extraer_contenido(r"\b\d{4}\b",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            km= extraer_contenido(r"(\d+[.]\d+km|\d+km)",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            precio=coche.find_element(By.XPATH, './/div[@class="car-card-data right pl-4 col-auto"]/span[2]/strong').text
            lista_diccionario_coches.append({"marca":marca_final, "modelo":modelo,"año":año,"kilometros":km,"precio":precio})
    except Exception as e:
        print("La busqueda no tiene coches ")
    
    #Busqueda del coche  Toyota Yaris gr sport
    try: 
        click_bar=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,'autocomplete-1-input')))
        click_bar.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
        click_bar.send_keys("Toyota Yaris gr sport"+Keys.ENTER)
    except :
        print("No existe el coche buscado")

    #Ajuste de los datos de los coches 
    try:
        funcion_ajustar_datos(driver)

    except:
        print("Error al ajustar los datos ")
    #Obtenemos los datos de los coches 
    try:
        for coche in driver.find_elements(By.XPATH,'//div[@id="vehicles_list"]/article[@class="sale-list__item"]'):
            marca=coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/strong').text
            marca_final=extraer_contenido(r'Toyota',marca)
            parte_modelo=extraer_contenido(r'Yaris',marca)
            modelo=parte_modelo +" "+coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[1]').text
            año= extraer_contenido(r"\b\d{4}\b",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            km= extraer_contenido(r"(\d+[.]\d+km|\d+km)",coche.find_element(By.XPATH, './/h2[@class="maker ellipsis"]/span[2]').text)
            precio=coche.find_element(By.XPATH, './/div[@class="car-card-data right pl-4 col-auto"]/span[2]/strong').text
            lista_diccionario_coches.append({"marca":marca_final, "modelo":modelo,"año":año,"kilometros":km,"precio":precio})
    except Exception as e:
        print("La busqueda no tiene coches ")

    

    #Esperamos y cerramos, luego devolvemos el diccionario
    time.sleep(5)
    driver.quit()
    return(lista_diccionario_coches)
