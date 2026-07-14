from typing import Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options as Options_chrome
import re

def extraer_contenido(patter,content): #Funcion auxiliar para sacar contenido de una cadena con una regex
    contenido=re.findall(patter,content)
    if contenido:
     return contenido[0]
    else:
            return None

def funcion_cochesmobile():
    driver = webdriver.Chrome()
    # Abrir la página principal
    lista_diccionario_coches=[]

    driver.get("https://www.mobile.de/es")
    # Buscar Renault Clio
    try:
        #aceptamos las cookies 
        cookies = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'mde-consent-accept-btn')]"))
        )
        cookies.click()
        #buscamos el buscador
        buscar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.make"))
        )
        buscar.click()

        # Seleccionar Renault
        renault = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.make']/option[@value='20700']"))
        )
        renault.click()

        # Seleccionar el modelo Clio
        clio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.model']/option[@value='6']"))
        )
        clio.click()

        # Kilómetros
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='maxMileage']/option[@value='125000']"))
        )
        km.click()

        # Año
        año = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='minFirstRegistration']/option[@value='2021']"))
        )
        año.click()

        # Buscar el botón de búsqueda y hacer clic
        buscar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "search-btn.btn.btn--orange.btn--l.js-show-results.js-track-event"))
        )
        buscar_btn.click()

        # Ingresar descripción del modelo, el acabado espirit alpine
        espirit_alpine = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.modelDescription"))
        )
        espirit_alpine.send_keys("esprit alpine")
        #buscamos
        buscar_resultados = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn--orange.btn--s.js-show-results.u-margin-top-18.u-margin-bottom-18"))
        )
        buscar_resultados.click()
        # Ordenar por precio: más bajos primero
        opcion_precio_bajo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@class, 'sorting-dropdown')]/option[text()='Precio: más bajos primero']"))
        )
        opcion_precio_bajo.click()
        time.sleep(2)
        #Bajamos al final para poder hacer click en ver mas coches 
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)
        #Para que muestre los primeros 50 coches 
        mostrar_50 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/section/section[2]/div/div[2]/a[3]"))
        )
        mostrar_50.click()
        time.sleep(3)

    except Exception as e:
        print(f"Se produjo un error al buscar Renault Clio: {e}")
    try:
        lista_diccionario_coches_renault: list[Dict] = []
        
        # Encuentra todos los coches en la lista de resultados
        coches = driver.find_elements(By.XPATH, "//div[@class='result-list-section js-result-list-section u-clearfix']/article[@class='list-entry g-row']")
        for coche in coches[:50]:
            # Extraer la información de cada coche
            marca=extraer_contenido(r"\b(Renault|RENAULT)\b",coche.find_element(By.XPATH,".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
            modelo=extraer_contenido(r"\b(Clio|CLIO)\b",coche.find_element(By.XPATH,".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
            precio = coche.find_element(By.XPATH, ".//p[@class='seller-currency u-text-bold']").text
            añoykm=coche.find_element(By.CLASS_NAME,"u-text-bold").text.split()
            if len(añoykm) >2:
                año=añoykm[0]
                km=añoykm[1] + " km"
                lista_diccionario_coches_renault.append({"marca":marca,"modelo":modelo,"año":año[-5:],"km":km,"precio": precio})

        
        lista_diccionario_coches.extend(lista_diccionario_coches_renault)

    except Exception as e:
        print(f"Error al extraer los precios de Renault Clio: {e}")

    # Volver a la página principal para buscar otro coche
    driver.get("https://www.mobile.de/es")

    # Buscar Seat fr
    try:
        # Esperar a que el elemento esté presente e interactuar con él
        buscar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.make"))
        )
        buscar.click()

        # Seleccionar la opción de seat
        seat = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.make']/option[@value='22500']"))
        )
        seat.click()
        time.sleep(2)
        #seleccionar el modelo ibiza
        ibiza = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.model']/option[@value='7']"))
        )
        ibiza.click()
        #kilomteros
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='maxMileage']/option[@value='125000']"))
        )
        km.click()
        #año
        año = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='minFirstRegistration']/option[@value='2021']"))
        )
        año.click()


        # Buscar el botón de búsqueda y hacer clic
        buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "search-btn.btn.btn--orange.btn--l.js-show-results.js-track-event"))
        )
        buscar.click()
        #el acabado
        FR = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.modelDescription"))
        )
        FR.send_keys("Seat Ibiza FR")
        #buscar
        buscar_resultados = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn--orange.btn--s.js-show-results.u-margin-top-18.u-margin-bottom-18"))
        )
        buscar_resultados.click()
        # Localiza la opción de "Precio: más bajos primero" 
        opcion_precio_bajo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@class, 'sorting-dropdown')]/option[text()='Precio: más bajos primero']"))
        )
        opcion_precio_bajo.click()
        time.sleep(2)
        #Bajamos al final para poder hacer click en ver mas coches 
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)
        #Para que muestre los primeros 50 coches 
        mostrar_50 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/section/section[2]/div/div[2]/a[3]"))
        )
        mostrar_50.click()
        time.sleep(3)

    except Exception as e:
        print(f"Se produjo un error: {e}")

    try:
        lista_diccionario_coches_seat: list[Dict] = []
        
        # Encuentra todos los coches en la lista de resultados
        coches = driver.find_elements(By.XPATH, "//div[@class='result-list-section js-result-list-section u-clearfix']/article[@class='list-entry g-row']")

        for coche in coches[:50]:
            # Extraer la información de cada coche
            marca=extraer_contenido(r"\b(Seat)\b",coche.find_element(By.XPATH,".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
            modelo=extraer_contenido(r"\b(Ibiza | IBIZA)\b",coche.find_element(By.XPATH,".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
            precio = coche.find_element(By.XPATH, ".//p[@class='seller-currency u-text-bold']").text
            añoykm=coche.find_element(By.CLASS_NAME,"u-text-bold").text.split()
            if len(añoykm) >2:
                año=añoykm[0]
                km=añoykm[1] + " km"
                lista_diccionario_coches_seat.append({"marca":marca,"modelo":modelo,"año":año[-5:],"km":km,"precio": precio})
            
        lista_diccionario_coches.extend(lista_diccionario_coches_seat)
    except Exception as e:
        print(f"Error al extraer los precios de Seat Ibiza {e}")

    # Volver a la página principal para buscar otro coche
    driver.get("https://www.mobile.de/es")
    
    # Buscar Volkswagen polo r-line
    try:
        # Esperar a que el elemento esté presente e interactuar con él
        buscar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.make"))
        )
        buscar.click()

        # Seleccionar la opción de Volskwagen
        Volkswagen = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.make']/option[@value='25200']"))
        )
        Volkswagen.click()
        time.sleep(2)
        #seleccionar el modelo polo
        polo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.model']/option[@value='27']"))
        )
        polo.click()
        #kilomteros
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='maxMileage']/option[@value='125000']"))
        )
        km.click()
        #año
        año = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='minFirstRegistration']/option[@value='2021']"))
        )
        año.click()


        # Buscar el botón de búsqueda y hacer clic
        buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "search-btn.btn.btn--orange.btn--l.js-show-results.js-track-event"))
        )
        buscar.click()
        #el acabado
        r_line = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.modelDescription"))
        )
        r_line.send_keys("R-line")
        #buscar
        buscar_resultados = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn--orange.btn--s.js-show-results.u-margin-top-18.u-margin-bottom-18"))
        )
        buscar_resultados.click()
        # Localiza la opción de "Precio: más bajos primero" 
        opcion_precio_bajo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@class, 'sorting-dropdown')]/option[text()='Precio: más bajos primero']"))
        )
        opcion_precio_bajo.click()
        time.sleep(2)
        #Bajamos al final para poder hacer click en ver mas coches 
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)
        #Para que muestre los primeros 50 coches 
        mostrar_50 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/section/section[2]/div/div[2]/a[3]"))
        )
        mostrar_50.click()
        time.sleep(3)

    except Exception as e:
        print(f"Se produjo un error: {e}")

    try:
        lista_diccionario_coches_polo: list[Dict] = []
        
        # Encuentra todos los coches en la lista de resultados
        coches = driver.find_elements(By.XPATH, "//div[@class='result-list-section js-result-list-section u-clearfix']/article[@class='list-entry g-row']")

        for coche in coches[:50]:
            # Extraer la información de cada coche
            marca=extraer_contenido(r"\b(Volkswagen)\b",coche.find_element(By.XPATH,".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
            modelo=extraer_contenido(r"\bPolo\b",coche.find_element(By.XPATH,".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
            precio = coche.find_element(By.XPATH, ".//p[@class='seller-currency u-text-bold']").text
            añoykm=coche.find_element(By.CLASS_NAME,"u-text-bold").text.split()
            if len(añoykm) >2:
                año=añoykm[0]
                km=añoykm[1] + " km"
                lista_diccionario_coches_polo.append({"marca":marca,"modelo":modelo,"año":año[-5:],"km":km,"precio": precio})
            
        lista_diccionario_coches.extend(lista_diccionario_coches_polo)
    except Exception as e:
        print(f"Error al extraer los precios de Volkswagen Polo {e}")

    # Volver a la página principal para buscar otro coche
    driver.get("https://www.mobile.de/es")


     # Buscar Hyundai I20 n-line
    try:
        # Esperar a que el elemento esté presente e interactuar con él
        buscar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.make"))
        )
        buscar.click()

        # Seleccionar la opción de hyundai
        Hyundai = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.make']/option[@value='11600']"))
        )
        Hyundai.click()
        time.sleep(2)
        #seleccionar el modelo i20
        I20 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.model']/option[@value='32']"))
        )
        I20.click()
        #kilomteros
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='maxMileage']/option[@value='125000']"))
        )
        km.click()
        #año
        año = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='minFirstRegistration']/option[@value='2021']"))
        )
        año.click()


        # Buscar el botón de búsqueda y hacer clic
        buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "search-btn.btn.btn--orange.btn--l.js-show-results.js-track-event"))
        )
        buscar.click()
        #el acabado
        n_line = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.modelDescription"))
        )
        n_line.send_keys("N-line")
        #buscar
        buscar_resultados = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn--orange.btn--s.js-show-results.u-margin-top-18.u-margin-bottom-18"))
        )
        buscar_resultados.click()
        # Localiza la opción de "Precio: más bajos primero" 
        opcion_precio_bajo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@class, 'sorting-dropdown')]/option[text()='Precio: más bajos primero']"))
        )
        opcion_precio_bajo.click()
        time.sleep(2)
        #Bajamos al final para poder hacer click en ver mas coches 
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)
        #Para que muestre los primeros 50 coches 
        mostrar_50 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/section/section[2]/div/div[2]/a[3]"))
        )
        mostrar_50.click()
        time.sleep(3)

    except Exception as e:
        print(f"Se produjo un error: {e}")

    try:
        lista_diccionario_coches_hyundai: list[Dict] = []
        
        # Encuentra todos los coches en la lista de resultados
        coches = driver.find_elements(By.XPATH, "//div[@class='result-list-section js-result-list-section u-clearfix']/article[@class='list-entry g-row']")

        for coche in coches[:50]:
            # Extraer la información de cada coche
            marca=extraer_contenido(r"\b(Hyundai)\b",coche.find_element(By.XPATH,".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
            modelo=extraer_contenido(r"\b(i20)\b",coche.find_element(By.XPATH,".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
            precio = coche.find_element(By.XPATH, ".//p[@class='seller-currency u-text-bold']").text
            añoykm=coche.find_element(By.CLASS_NAME,"u-text-bold").text.split()
            if len(añoykm) >2:
                año=añoykm[0]
                km=añoykm[1] + " km"
                lista_diccionario_coches_hyundai.append({"marca":marca,"modelo":"i20","año":año[-5:],"km":km,"precio": precio})
            
        lista_diccionario_coches.extend(lista_diccionario_coches_hyundai)
    except Exception as e:
        print(f"Error al extraer los precios de Hyundai I20 {e}")

    # Volver a la página principal para buscar otro coche
    driver.get("https://www.mobile.de/es")


     # Buscar Toyota Yaris Gr-line
    try:
        # Esperar a que el elemento esté presente e interactuar con él
        buscar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.make"))
        )
        buscar.click()

        # Seleccionar la opción de Toyota
        Toyota = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.make']/option[@value='24100']"))
        )
        Toyota.click()
        time.sleep(2)
        #seleccionar el modelo Yaris
        Yaris = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.model']/option[@value='36']"))
        )
        Yaris.click()
        #kilomteros
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='maxMileage']/option[@value='125000']"))
        )
        km.click()
        #año
        año = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='minFirstRegistration']/option[@value='2021']"))
        )
        año.click()


        # Buscar el botón de búsqueda y hacer clic
        buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "search-btn.btn.btn--orange.btn--l.js-show-results.js-track-event"))
        )
        buscar.click()
        #el acabado
        gr_sport = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.modelDescription"))
        )
        gr_sport.send_keys("Gr Sport")
        #buscar
        buscar_resultados = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn--orange.btn--s.js-show-results.u-margin-top-18.u-margin-bottom-18"))
        )
        buscar_resultados.click()
        # Localiza la opción de "Precio: más bajos primero" 
        opcion_precio_bajo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@class, 'sorting-dropdown')]/option[text()='Precio: más bajos primero']"))
        )
        opcion_precio_bajo.click()
        time.sleep(2)
        #Bajamos al final para poder hacer click en ver mas coches 
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)
        #Para que muestre los primeros 50 coches 
        mostrar_50 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/section/section[2]/div/div[2]/a[3]"))
        )
        mostrar_50.click()
        time.sleep(3)

    except Exception as e:
        print(f"Se produjo un error: {e}")

    try:
        lista_diccionario_coches_toyota: list[Dict] = []
        
        # Encuentra todos los coches en la lista de resultados
        coches = driver.find_elements(By.XPATH, "//div[@class='result-list-section js-result-list-section u-clearfix']/article[@class='list-entry g-row']")

        for coche in coches[:50]:
            # Extraer la información de cada coche
            marca=extraer_contenido(r"\b(Toyota)\b",coche.find_element(By.XPATH,".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
            modelo=extraer_contenido(r"\b(Yaris)\b",coche.find_element(By.XPATH,".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
            precio = coche.find_element(By.XPATH, ".//p[@class='seller-currency u-text-bold']").text
            añoykm=coche.find_element(By.CLASS_NAME,"u-text-bold").text.split()
            if len(añoykm) >2:
                año=añoykm[0]
                km=añoykm[1] + " km"
                lista_diccionario_coches_toyota.append({"marca":marca,"modelo":"Yaris","año":año[-5:],"km":km,"precio": precio})
            
        lista_diccionario_coches.extend(lista_diccionario_coches_toyota)
    except Exception as e:
        print(f"Error al extraer los precios de Toyota Yaris {e}")

    # Volver a la página principal para buscar otro coche
    driver.get("https://www.mobile.de/es")
    

    # Buscar Opel Corsa
    try:
        buscar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.make"))
        )
        buscar.click()

        # Seleccionar Opel
        opel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.make']/option[@value='19000']"))
        )
        opel.click()
        time.sleep(2)

        # Seleccionar el modelo Corsa
        corsa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='makeModelVariant1.model']/option[@value='10']"))
        )
        corsa.click()

        # Kilómetros
        km = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='maxMileage']/option[@value='125000']"))
        )
        km.click()

        # Año
        año = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='minFirstRegistration']/option[@value='2021']"))
        )
        año.click()

        # Buscar el botón de búsqueda y hacer clic
        buscar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "search-btn.btn.btn--orange.btn--l.js-show-results.js-track-event"))
        )
        buscar_btn.click()

        # Ingresar descripción del modelo
        gs_line = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "makeModelVariant1.modelDescription"))
        )
        gs_line.send_keys("Corsa GS-line")

        buscar_resultados = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn--orange.btn--s.js-show-results.u-margin-top-18.u-margin-bottom-18"))
        )
        buscar_resultados.click()

        # Ordenar por precio: más bajos primero
        opcion_precio_bajo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[contains(@class, 'sorting-dropdown')]/option[text()='Precio: más bajos primero']"))
        )
        opcion_precio_bajo.click()
        time.sleep(2)
        #Bajamos al final para poder hacer click en ver mas coches 
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)
        #Para que muestre los primeros 50 coches 
        mostrar_50 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/section/section[2]/div/div[2]/a[3]"))
        )
        mostrar_50.click()
        time.sleep(3)

    except Exception as e:
        print(f"Se produjo un error al buscar Opel Corsa: {e}")

    try:
        lista_diccionario_coches_opel: list[Dict] = []

        # Encuentra todos los coches en la lista de resultados
        coches = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'result-list-section')]//article"))
        )

        for coche in coches[:50]:
            try:
                # Extraer la información de cada coche
                marca = extraer_contenido(r"\b(Opel)\b", coche.find_element(By.XPATH, ".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
                modelo = extraer_contenido(r"\b(Corsa)\b", coche.find_element(By.XPATH, ".//h3[@class='vehicle-title g-col-12 u-text-nowrap']").text)
                precio = coche.find_element(By.XPATH, ".//p[@class='seller-currency u-text-bold']").text
                añoykm=coche.find_element(By.CLASS_NAME,"u-text-bold").text.split()
                if len(añoykm)>2:
                    año=añoykm[0]
                    km=añoykm[1] + " km"
                    lista_diccionario_coches_opel.append({"marca": marca, "modelo": modelo, "año": año[-5:], "km": km, "precio": precio})
            except Exception as e:
                print(f"Error al extraer datos del coche: {e}")

        lista_diccionario_coches.extend(lista_diccionario_coches_opel)

    except Exception as e:
        print(f"Error al extraer los precios de Opel Corsa: {e}")   

    return(lista_diccionario_coches)
    