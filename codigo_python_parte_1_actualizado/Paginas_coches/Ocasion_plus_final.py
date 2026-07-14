from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options as Options_chrome



def move_slider_left(boton_barra_izquierda, steps,driver):
        action = ActionChains(driver)
        for _ in range(steps):
            action.click_and_hold(boton_barra_izquierda).move_by_offset(-5, 0).release().perform()
            time.sleep(0.01)
def funcion_ocasionplus():
    options = Options_chrome()
    # Lo añado para ignorar los errores relacionados con certificados de seguridad
    options.add_argument('--ignore-certificate-errors')
    # Ignoramos todos los errores SSL
    options.add_argument('--ignore-ssl-errors')
    # Deshabilitamos la GPU para tener más estabilidad 
    options.add_argument('--disable-gpu') 
    driver = webdriver.Chrome(options= options)
    # Escribimos en una variable la URL de la pagina en este caso OcasionPlus
    urlOcacion_plus = 'https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwiZ_sWru6yJAxXSsYMHHfycITcYABAAGgJlZg&co=1&ase=2&gclid=Cj0KCQjwpvK4BhDUARIsADHt9sT9P5UebEh_VKF2exGOzVXhbRZ-aqDdqOyX47MHBW5u4FSxXR0V4ooaAluXEALw_wcB&ohost=www.google.com&cid=CAESVuD2NTSMXQu2GGCVEyp3zmEHh_7_mne9w6luqJtM-oZnQe-Q8n9q5vmoEFEUuvB727AlfkTxFcXxU-JzN7j4AsQk9zJDBYAU-KrGX0C6NcvzZ3AFk2Ia&sig=AOD64_1GOBvneDvyfXWKt7HgZS-ymAH6WQ&q&nis=4&adurl&ved=2ahUKEwjylsCru6yJAxU-QvEDHat3PBoQ0Qx6BAgJEAE'
    # Accedemos a la URL 
    driver.get(urlOcacion_plus)
    # Esperamos 5 segundos hasta que cargue la pagina
    time.sleep(5)
    # Generamos el resultado general donde vamos a guardar los diccionarios con cada coche y sus campos
    lista_diccionarios_coches = []

    try:
        # Espero a que salga el pop-up de las cookies y lo acepto
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')))
        boton_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')))
        boton_cookies.click()
    except Exception as e1:
        print(f'el error es de cookies {e1}')  

    try:
        # Buscamos la parte de la pagina donde esta el boton de lo kilómetros 
        pestaña_botones = driver.find_element(By.XPATH, '//div[@class="dropdownFilters_dropdownItem__pAWVD" and @data-test="filter-dropdown-kms"]')
        # Buscamos dentro de esa parte el boton de los km y hacemos click
        boton_km = pestaña_botones.find_element(By.XPATH, './/span[@class="Dropdown_icon__5GYY_ dropdownFilters_icon__Ztj1s"]')
        boton_km.click()
        # Buscamos la barra para ajustar los km
        botones_barra = driver.find_elements(By.XPATH, '//div[@tabindex="0" and @role="slider" and @aria-valuemax="200000" and @aria-valuemin="0" and @class= "InputRange_thumb__0IrEi range_thumb__Y_9k_"]')
        # Accedemos al boton de la izquierda para que vaya de 0 hasta lo que ajustemos ese boton en este caso vamos a querer 50.000 km
        boton_barra_izquierda = botones_barra[1]
        
        # Aplicamos la funcion al boton de la izquierda hasta que llegue a 50.000 km
        move_slider_left(boton_barra_izquierda, 15,driver)
    except Exception as e3:
        print(f'el error es boton_km {e3}')

    try:
        # Buscamos la parte de la pagina donde se encuentra el boton de los años
        pestaña_botones = driver.find_element(By.XPATH, '//div[@class="dropdownFilters_dropdownItem__pAWVD" and @data-test="filter-dropdown-kms"]')
        # Buscamos dentro de esa pestaña el boton de años que en este caso es el 5º elemento
        elementos_pestaña_botones = pestaña_botones.find_elements(By.XPATH, '//div[contains(@class, "Dropdown_titleContainer__gypzE dropdownFilters_dropdown__C1g48")]')
        año = elementos_pestaña_botones[5]
        # Buscamos la flecha de los años para abrir el desplegable y hacemos click
        flecha_años= año.find_element(By.XPATH, './/span[contains(@class, "Dropdown_icon__5GYY_ dropdownFilters_icon__Ztj1s")]')
        flecha_años.click()
    except Exception as e4:
        print(f'el error es de años {e4}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que sea visble el elemento para introducir a partir de que año queremos los coches
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form-input-year[0]"]/div/div[2]/div[2]/child::*[1]')))
        elementos_para_escribir_años= driver.find_element(By.XPATH, '//*[@id="form-input-year[0]"]/div/div[2]/div[2]/child::*[1]')
        # Hacemos click e introducimos el año que en este caso es 2021
        elementos_para_escribir_años.click()
        elementos_para_escribir_años.send_keys('2021' + Keys.ENTER)
    except Exception as e5:
        print(f'el error es introducir los años {e5}')

    try:
        # Esperamos a que sea visible la barra de texto donde queremos introducir la marca y el modelo en este caso Seat Ibiza
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form-input-searchText"]/div/div[2]/div[2]/div[2]/*[1]')))
        # Lo encontramos, hacemos click e introducimos 'Seat Ibiza'
        barra_texto = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-input-searchText"]/div/div[2]/div[2]/div[2]/*[1]')))
        barra_texto.click()
        barra_texto.send_keys('Seat Ibiza' + Keys.ENTER)
    except Exception as e2:
        print(f'el error es la barra de texto as {e2}')

    try:
        # Esperamos a que esten todos los coches
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class= "cardVehicle_card__LwFCi"]')))
        # Buscamos todos los coches y se lo asignamos a la variable coches
        coches = driver.find_elements(By.XPATH, './/div[@class= "cardVehicle_card__LwFCi"]')
        # Creamos el resultado parcial
        resultado = []
        for coche in coches:
            # Dentro de cada coche buscamos la marca y el modelo 
            marca_modelo = coche.find_element(By.XPATH, './/span[@class = "cardVehicle_spot__e6YZx" and @data-test= "span-brand-model"]').text
            # Dividimos el texto para tener por separado la marca y el modelo por separado, lo dividimos por el espacio que los une
            marca_modelo_dividir = marca_modelo.split(' ')
            # La marca es la primera parte del texto dividido
            marca = marca_modelo_dividir[0]
            # El modelo es la segunda parte del texto dividido
            modelo = marca_modelo_dividir[1]
            # Buscamo la version del coche
            version = coche.find_element(By.XPATH, './/span[@class= "cardVehicle_finance__SG6JV" and @data-test= "span-version"]').text
            # Buscamos el precio dle coche
            precio = coche.find_element(By.XPATH, './/span[@class= "cardVehicle_finance__SG6JV" and @data-test= "span-finance"]').text
            # Para tener unidos el modelo y la version los unimos 
            modelo_version = modelo + ' ' + version
            # Buscamos el año de fabricacion del coche
            años = coche.find_element(By.XPATH, './/span[@class= "characteristics_elements__Mb1S_" and @data-test= "span-registration-date"]').text
            # Buscamos cuantos km tiene el coche
            kilometros = coche.find_element(By.XPATH, './/span[@class= "characteristics_elements__Mb1S_" and @data-test= "span-km"]').text
            # Limpiamos el precio ya que por razones de encoding el resultado nos salia con la cadena "\u202f" y la eliminamos
            precio_limpio = precio.replace("\u202f", '')
            # Añadimos al resultado parcial el diccionario con el coche, que incluye los elementos: marca, modelo, años, kilometros y precio
            resultado.append({
                'marca': marca,
                'modelo': modelo_version,
                'año': años,
                'kilometros': kilometros,
                'precio': precio_limpio
            })
    except Exception as e6:
        print(f"Error en el for: {e6}")
    # Filtramos el resultado parcial para quedarnos solo con los coches que contienen FR en su elemento modelo
    resultados_filtrados = [coche for coche in resultado if 'FR' in coche['modelo'].upper()]
    # Añadimos al resultado el resultado parcial filtrado
    lista_diccionarios_coches.extend(resultados_filtrados)
    # Esperamos 5 segundo y quitamos la pagina
    time.sleep(5)

    # Volvemos a abrir otra pagina con las mimas opciones de apertura que antes y buscamos el siguiente coche

    driver.get(urlOcacion_plus)

    time.sleep(5)

    try:
        # Buscamos la parte de la pagina donde esta el boton de kilómetros
        pestaña_botones = driver.find_element(By.XPATH, '//div[@class="dropdownFilters_dropdownItem__pAWVD" and @data-test="filter-dropdown-kms"]')
        # Buscamos dentro de esa pestaña el boton kilómetros y hacemos click
        boton_km = pestaña_botones.find_element(By.XPATH, './/span[@class="Dropdown_icon__5GYY_ dropdownFilters_icon__Ztj1s"]')
        boton_km.click()
        # Buscamos la barra para ajustar los km
        botones_barra = driver.find_elements(By.XPATH, '//div[@tabindex="0" and @role="slider" and @aria-valuemax="200000" and @aria-valuemin="0" and @class= "InputRange_thumb__0IrEi range_thumb__Y_9k_"]')
        # Pulsamos el boton izquierdo para ajustarlo
        boton_barra_izquierda = botones_barra[1]
        
        # Aplicamos la funcion al boton de la izquierda de la barra para ajustar los kilómetros
        move_slider_left(boton_barra_izquierda, 15 ,driver)
    except Exception as e3:
        print(f'el error es boton_km {e3}')

    try:
        # Buscamos de nuevo la ventana donde se encuntran los años
        pestaña_botones = driver.find_element(By.XPATH, '//div[@class="dropdownFilters_dropdownItem__pAWVD" and @data-test="filter-dropdown-kms"]')
        # Buscamos el boton de años que dentro de esa pestaña es el 5º campo
        elementos_pestaña_botones = pestaña_botones.find_elements(By.XPATH, '//div[contains(@class, "Dropdown_titleContainer__gypzE dropdownFilters_dropdown__C1g48")]')
        año = elementos_pestaña_botones[5]
        # Buscamos la flecha para abrir el desplegable y hacemos click
        flecha_años= año.find_element(By.XPATH, './/span[contains(@class, "Dropdown_icon__5GYY_ dropdownFilters_icon__Ztj1s")]')
        flecha_años.click()
    except Exception as e4:
        print(f'el error es de años {e4}')

    time.sleep(2)

    try:
        # Esperamos hasta que la parte del despegable de años sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form-input-year[0]"]/div/div[2]/div[2]/child::*[1]')))
        # Buscamos la parte para introducir desde que año queremos los coches en este caso 2021, lo cual lo introducimos
        elementos_para_escribir_años= driver.find_element(By.XPATH, '//*[@id="form-input-year[0]"]/div/div[2]/div[2]/child::*[1]')
        elementos_para_escribir_años.click()
        elementos_para_escribir_años.send_keys('2021' + Keys.ENTER)
    except Exception as e5:
        print(f'el error es introducir los años {e5}')

    try:
        # Esperamos hasta que sea visible la barra para escribir la marca y modelo del coche que queremos
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form-input-searchText"]/div/div[2]/div[2]/div[2]/*[1]')))
        # Una vez sea visible hacemos click y escribimos la marca y el modelo en este caso Opel Corsa
        barra_texto = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-input-searchText"]/div/div[2]/div[2]/div[2]/*[1]')))
        barra_texto.click()
        barra_texto.send_keys('Opel Corsa' + Keys.ENTER)
    except Exception as e2:
        print(f'el error es la barra de texto as {e2}')

    try:
        # Esperamos hasta que sean visibles los coches, los buscamos todos y se lo asignamos a la variable coches
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class= "cardVehicle_card__LwFCi"]')))
        coches = driver.find_elements(By.XPATH, './/div[@class= "cardVehicle_card__LwFCi"]')
        resultado = []
        for coche in coches:
            # Dentro de cada coche buscamos el texto donde se incluye la marca y modelo
            marca_modelo = coche.find_element(By.XPATH, './/span[@class = "cardVehicle_spot__e6YZx" and @data-test= "span-brand-model"]').text
            # Como estan en un mismo string la marca y modelo lo dividimos a partir del espacio que los une
            marca_modelo_dividir = marca_modelo.split(' ')
            # La marca es la primera parte al dividir el texto
            marca = marca_modelo_dividir[0]
            # El modelo es la segunda parte al dividir el texto
            modelo = marca_modelo_dividir[1]
            # Buscamos la version del coche
            version = coche.find_element(By.XPATH, './/span[@class= "cardVehicle_finance__SG6JV" and @data-test= "span-version"]').text
            # Buscamo el precio del coche
            precio = coche.find_element(By.XPATH, './/span[@class= "cardVehicle_finance__SG6JV" and @data-test= "span-finance"]').text
            # Para hacer que haya menos campos en la solucion unimos el modelo sacado anteriormente con la version
            modelo_version = modelo + ' ' + version
            # Buscamos el año de la fabricación del coche
            años = coche.find_element(By.XPATH, './/span[@class= "characteristics_elements__Mb1S_" and @data-test= "span-registration-date"]').text
            # Buscamos los km que tiene el coche
            kilometros = coche.find_element(By.XPATH, './/span[@class= "characteristics_elements__Mb1S_" and @data-test= "span-km"]').text
            # Limpiamos el texto ya que por razones de encoding en el resultado salía la cadena "\u202f" y la eliminamos
            precio_limpio = precio.replace("\u202f", '')
            # Añadimos al resultado parcial el diccionario formado por los campos: marca, modelo, año, kilómetros y precio
            resultado.append({
                'marca': marca,
                'modelo': modelo_version,
                'año': años,
                'kilometros': kilometros,
                'precio': precio_limpio
            })
    except Exception as e6:
        print(f"Error en el for: {e6}")
    # Filtramos el resultado parcial para quedarnos unicamente con aquellos coches que en modelo este la cadena 'GS-Line'
    resultados_filtrados2 = [coche for coche in resultado if 'GS-Line' in coche['modelo']]
    # Lo añadimos al resultado general
    lista_diccionarios_coches.extend(resultados_filtrados2)

    # Esperamos 5 segundo y quitamos la pagina
    time.sleep(5)
    # Volvemos a abrir otra pagina con las mismas opciones de apertura que en los dos coches anteriores
    driver.get(urlOcacion_plus)

    time.sleep(5)

    try:
        # Buscamos la parte de la pagina donde se encuentra el boton de kilómetros
        pestaña_botones = driver.find_element(By.XPATH, '//div[@class="dropdownFilters_dropdownItem__pAWVD" and @data-test="filter-dropdown-kms"]')
        # Buscamos dentro de la pestaña el boton de kilómetros y hacemos click
        boton_km = pestaña_botones.find_element(By.XPATH, './/span[@class="Dropdown_icon__5GYY_ dropdownFilters_icon__Ztj1s"]')
        boton_km.click()
        # Buscamos la barra para ajustar los kilómetros
        botones_barra = driver.find_elements(By.XPATH, '//div[@tabindex="0" and @role="slider" and @aria-valuemax="200000" and @aria-valuemin="0" and @class= "InputRange_thumb__0IrEi range_thumb__Y_9k_"]')
        # Buscamos el boton de la izquierda de la barra para que los kilómetros vayan de 0 hasta 50.000 en este caso
        boton_barra_izquierda = botones_barra[1]

        # Aplicamos la funcion anterior para mover el boton de la izquierda hasta llegar a 50.000 km
        move_slider_left(boton_barra_izquierda, 15 ,driver)
    except Exception as e3:
        print(f'el error es boton_km {e3}')

    try:
        # Buscamos la parte de la pagina donde se encuentra el boton de años
        pestaña_botones = driver.find_element(By.XPATH, '//div[@class="dropdownFilters_dropdownItem__pAWVD" and @data-test="filter-dropdown-kms"]')
        # Dentro de esa pestaña buscamos el boton de años que en este caso es el 5º elemento
        elementos_pestaña_botones = pestaña_botones.find_elements(By.XPATH, '//div[contains(@class, "Dropdown_titleContainer__gypzE dropdownFilters_dropdown__C1g48")]')
        año = elementos_pestaña_botones[5]
        # Hacemos click en la flecha de años para abrir el desplegable
        flecha_años= año.find_element(By.XPATH, './/span[contains(@class, "Dropdown_icon__5GYY_ dropdownFilters_icon__Ztj1s")]')
        flecha_años.click()
    except Exception as e4:
        print(f'el error es de años {e4}')

    # Esperamos 2 segundos
    time.sleep(2)

    try:
        # Esperamos a que sea visible la parte donde vamos a introducir a partir de que año queremos que sea el coche
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form-input-year[0]"]/div/div[2]/div[2]/child::*[1]')))
        # Buscamos el elemento para escribir el año a partir del cual queremos los coches
        elementos_para_escribir_años= driver.find_element(By.XPATH, '//*[@id="form-input-year[0]"]/div/div[2]/div[2]/child::*[1]')
        # Hacemos click e introducion el año en este caso 2021
        elementos_para_escribir_años.click()
        elementos_para_escribir_años.send_keys('2021' + Keys.ENTER)
    except Exception as e5:
        print(f'el error es introducir los años {e5}')

    try:
        # Esperamos a que sea visible la barra de texto para introducir la marca y el modelo
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form-input-searchText"]/div/div[2]/div[2]/div[2]/*[1]')))
        # Buscamos la barra para escribir la marca y el modelo
        barra_texto = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-input-searchText"]/div/div[2]/div[2]/div[2]/*[1]')))
        # Hacemos click e introducimos la marca y modelo en este caso Renault Clio
        barra_texto.click()
        barra_texto.send_keys('Renault Clio' + Keys.ENTER)
    except Exception as e2:
        print(f'el error es la barra de texto as {e2}')

    try:
        # Esperamos a que sean visibles todos los coches
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class= "cardVehicle_card__LwFCi"]')))
        # Buscamos todos los coches y los añadimos a la variable coches
        coches = driver.find_elements(By.XPATH, './/div[@class= "cardVehicle_card__LwFCi"]')
        # Creamos el resultado parcial
        resultado = []
        for coche in coches:
            # Dentro de cada coche buscamos la marca y modelo
            marca_modelo = coche.find_element(By.XPATH, './/span[@class = "cardVehicle_spot__e6YZx" and @data-test= "span-brand-model"]').text
            # Dividimos la cadena ya que queremos la marca y modelo por separado, lo dividimos por el espacio que los une
            marca_modelo_dividir = marca_modelo.split(' ')
            # La marca es la primera parte del texto dividido
            marca = marca_modelo_dividir[0]
            # El modelo es la segunda parte del texto dividido
            modelo = marca_modelo_dividir[1]
            # Buscamos la version del coche
            version = coche.find_element(By.XPATH, './/span[@class= "cardVehicle_finance__SG6JV" and @data-test= "span-version"]').text
            # Buscamos el precio del coche
            precio = coche.find_element(By.XPATH, './/span[@class= "cardVehicle_finance__SG6JV" and @data-test= "span-finance"]').text
            # Como queremos el modelo y la version unidas las juntamos
            modelo_version = modelo + ' ' + version
            # Buscamos el año de fabricacion del coche
            años = coche.find_element(By.XPATH, './/span[@class= "characteristics_elements__Mb1S_" and @data-test= "span-registration-date"]').text
            # Buscamos cuantos km tiene el coche
            kilometros = coche.find_element(By.XPATH, './/span[@class= "characteristics_elements__Mb1S_" and @data-test= "span-km"]').text
            # Limpiamos el precio ya que por razones de encoding nos encontramos la cadena "\u202f" y la eliminamos
            precio_limpio = precio.replace("\u202f", '')
            # Añadimos al resultado parcial el diccionario con el coche con los siguientes elementos: marca, modelo, año, kilometros, precio
            resultado.append({
                'marca': marca,
                'modelo': modelo_version,
                'año': años,
                'kilometros': kilometros,
                'precio': precio_limpio
            })
    except Exception as e6:
        print(f"Error en el for: {e6}")
    # Filtramos el resultado parcial para quedarnos unicamente con los coches que contienen la cadena Esprit Alpine en su modelo
    resultados_filtrados2 = [coche for coche in resultado if 'Esprit Alpine' in coche['modelo']]
    # Añadimos al resultado el resultado parcial filtrado
    lista_diccionarios_coches.extend(resultados_filtrados2)
    # Esperamos 5 segundos y cerramos el navegador
    time.sleep(5)
    driver.get(urlOcacion_plus)

    time.sleep(5)

    try:
        # Buscamos la parte de la pagina donde esta el boton de kilómetros
        pestaña_botones = driver.find_element(By.XPATH, '//div[@class="dropdownFilters_dropdownItem__pAWVD" and @data-test="filter-dropdown-kms"]')
        # Buscamos dentro de esa pestaña el boton kilómetros y hacemos click
        boton_km = pestaña_botones.find_element(By.XPATH, './/span[@class="Dropdown_icon__5GYY_ dropdownFilters_icon__Ztj1s"]')
        boton_km.click()
        # Buscamos la barra para ajustar los km
        botones_barra = driver.find_elements(By.XPATH, '//div[@tabindex="0" and @role="slider" and @aria-valuemax="200000" and @aria-valuemin="0" and @class= "InputRange_thumb__0IrEi range_thumb__Y_9k_"]')
        # Pulsamos el boton izquierdo para ajustarlo
        boton_barra_izquierda = botones_barra[1]
        
        # Aplicamos la funcion al boton de la izquierda de la barra para ajustar los kilómetros
        move_slider_left(boton_barra_izquierda, 15 ,driver)
    except Exception as e3:
        print(f'el error es boton_km {e3}')

    try:
        # Buscamos de nuevo la ventana donde se encuntran los años
        pestaña_botones = driver.find_element(By.XPATH, '//div[@class="dropdownFilters_dropdownItem__pAWVD" and @data-test="filter-dropdown-kms"]')
        # Buscamos el boton de años que dentro de esa pestaña es el 5º campo
        elementos_pestaña_botones = pestaña_botones.find_elements(By.XPATH, '//div[contains(@class, "Dropdown_titleContainer__gypzE dropdownFilters_dropdown__C1g48")]')
        año = elementos_pestaña_botones[5]
        # Buscamos la flecha para abrir el desplegable y hacemos click
        flecha_años= año.find_element(By.XPATH, './/span[contains(@class, "Dropdown_icon__5GYY_ dropdownFilters_icon__Ztj1s")]')
        flecha_años.click()
    except Exception as e4:
        print(f'el error es de años {e4}')

    time.sleep(2)

    try:
        # Esperamos hasta que la parte del despegable de años sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form-input-year[0]"]/div/div[2]/div[2]/child::*[1]')))
        # Buscamos la parte para introducir desde que año queremos los coches en este caso 2021, lo cual lo introducimos
        elementos_para_escribir_años= driver.find_element(By.XPATH, '//*[@id="form-input-year[0]"]/div/div[2]/div[2]/child::*[1]')
        elementos_para_escribir_años.click()
        elementos_para_escribir_años.send_keys('2021' + Keys.ENTER)
    except Exception as e5:
        print(f'el error es introducir los años {e5}')

    try:
        # Esperamos hasta que sea visible la barra para escribir la marca y modelo del coche que queremos
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form-input-searchText"]/div/div[2]/div[2]/div[2]/*[1]')))
        # Una vez sea visible hacemos click y escribimos la marca y el modelo en este caso Opel Corsa
        barra_texto = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-input-searchText"]/div/div[2]/div[2]/div[2]/*[1]')))
        barra_texto.click()
        barra_texto.send_keys('Toyota Yaris' + Keys.ENTER)
    except Exception as e2:
        print(f'el error es la barra de texto as {e2}')

    try:
        # Esperamos hasta que sean visibles los coches, los buscamos todos y se lo asignamos a la variable coches
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class= "cardVehicle_card__LwFCi"]')))
        coches = driver.find_elements(By.XPATH, './/div[@class= "cardVehicle_card__LwFCi"]')
        resultado = []
        for coche in coches:
            # Dentro de cada coche buscamos el texto donde se incluye la marca y modelo
            marca_modelo = coche.find_element(By.XPATH, './/span[@class = "cardVehicle_spot__e6YZx" and @data-test= "span-brand-model"]').text
            # Como estan en un mismo string la marca y modelo lo dividimos a partir del espacio que los une
            marca_modelo_dividir = marca_modelo.split(' ')
            # La marca es la primera parte al dividir el texto
            marca = marca_modelo_dividir[0]
            # El modelo es la segunda parte al dividir el texto
            modelo = marca_modelo_dividir[1]
            # Buscamos la version del coche
            version = coche.find_element(By.XPATH, './/span[@class= "cardVehicle_finance__SG6JV" and @data-test= "span-version"]').text
            # Buscamo el precio del coche
            precio = coche.find_element(By.XPATH, './/span[@class= "cardVehicle_finance__SG6JV" and @data-test= "span-finance"]').text
            # Para hacer que haya menos campos en la solucion unimos el modelo sacado anteriormente con la version
            modelo_version = modelo + ' ' + version
            # Buscamos el año de la fabricación del coche
            años = coche.find_element(By.XPATH, './/span[@class= "characteristics_elements__Mb1S_" and @data-test= "span-registration-date"]').text
            # Buscamos los km que tiene el coche
            kilometros = coche.find_element(By.XPATH, './/span[@class= "characteristics_elements__Mb1S_" and @data-test= "span-km"]').text
            # Limpiamos el texto ya que por razones de encoding en el resultado salía la cadena "\u202f" y la eliminamos
            precio_limpio = precio.replace("\u202f", '')
            # Añadimos al resultado parcial el diccionario formado por los campos: marca, modelo, año, kilómetros y precio
            resultado.append({
                'marca': marca,
                'modelo': modelo_version,
                'año': años,
                'kilometros': kilometros,
                'precio': precio_limpio
            })
    except Exception as e6:
        print(f"Error en el for: {e6}")
    # Filtramos el resultado parcial para quedarnos unicamente con aquellos coches que en modelo este la cadena 'GS-Line'
    resultados_filtrados2 = [coche for coche in resultado if 'GR sport' in coche['modelo']]
    # Lo añadimos al resultado general
    lista_diccionarios_coches.extend(resultados_filtrados2)
    # Esperamos 5 segundo y quitamos la pagina
    time.sleep(5)
    driver.get(urlOcacion_plus)

    time.sleep(5)

    try:
        # Buscamos la parte de la pagina donde esta el boton de kilómetros
        pestaña_botones = driver.find_element(By.XPATH, '//div[@class="dropdownFilters_dropdownItem__pAWVD" and @data-test="filter-dropdown-kms"]')
        # Buscamos dentro de esa pestaña el boton kilómetros y hacemos click
        boton_km = pestaña_botones.find_element(By.XPATH, './/span[@class="Dropdown_icon__5GYY_ dropdownFilters_icon__Ztj1s"]')
        boton_km.click()
        # Buscamos la barra para ajustar los km
        botones_barra = driver.find_elements(By.XPATH, '//div[@tabindex="0" and @role="slider" and @aria-valuemax="200000" and @aria-valuemin="0" and @class= "InputRange_thumb__0IrEi range_thumb__Y_9k_"]')
        # Pulsamos el boton izquierdo para ajustarlo
        boton_barra_izquierda = botones_barra[1]
        
        # Aplicamos la funcion al boton de la izquierda de la barra para ajustar los kilómetros
        move_slider_left(boton_barra_izquierda, 15 ,driver)
    except Exception as e3:
        print(f'el error es boton_km {e3}')

    try:
        # Buscamos de nuevo la ventana donde se encuntran los años
        pestaña_botones = driver.find_element(By.XPATH, '//div[@class="dropdownFilters_dropdownItem__pAWVD" and @data-test="filter-dropdown-kms"]')
        # Buscamos el boton de años que dentro de esa pestaña es el 5º campo
        elementos_pestaña_botones = pestaña_botones.find_elements(By.XPATH, '//div[contains(@class, "Dropdown_titleContainer__gypzE dropdownFilters_dropdown__C1g48")]')
        año = elementos_pestaña_botones[5]
        # Buscamos la flecha para abrir el desplegable y hacemos click
        flecha_años= año.find_element(By.XPATH, './/span[contains(@class, "Dropdown_icon__5GYY_ dropdownFilters_icon__Ztj1s")]')
        flecha_años.click()
    except Exception as e4:
        print(f'el error es de años {e4}')

    time.sleep(2)

    try:
        # Esperamos hasta que la parte del despegable de años sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form-input-year[0]"]/div/div[2]/div[2]/child::*[1]')))
        # Buscamos la parte para introducir desde que año queremos los coches en este caso 2021, lo cual lo introducimos
        elementos_para_escribir_años= driver.find_element(By.XPATH, '//*[@id="form-input-year[0]"]/div/div[2]/div[2]/child::*[1]')
        elementos_para_escribir_años.click()
        elementos_para_escribir_años.send_keys('2021' + Keys.ENTER)
    except Exception as e5:
        print(f'el error es introducir los años {e5}')

    try:
        # Esperamos hasta que sea visible la barra para escribir la marca y modelo del coche que queremos
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="form-input-searchText"]/div/div[2]/div[2]/div[2]/*[1]')))
        # Una vez sea visible hacemos click y escribimos la marca y el modelo en este caso Opel Corsa
        barra_texto = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form-input-searchText"]/div/div[2]/div[2]/div[2]/*[1]')))
        barra_texto.click()
        barra_texto.send_keys('Volkswagen Polo' + Keys.ENTER)
    except Exception as e2:
        print(f'el error es la barra de texto as {e2}')

    try:
        # Esperamos hasta que sean visibles los coches, los buscamos todos y se lo asignamos a la variable coches
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class= "cardVehicle_card__LwFCi"]')))
        coches = driver.find_elements(By.XPATH, './/div[@class= "cardVehicle_card__LwFCi"]')
        resultado = []
        for coche in coches:
            # Dentro de cada coche buscamos el texto donde se incluye la marca y modelo
            marca_modelo = coche.find_element(By.XPATH, './/span[@class = "cardVehicle_spot__e6YZx" and @data-test= "span-brand-model"]').text
            # Como estan en un mismo string la marca y modelo lo dividimos a partir del espacio que los une
            marca_modelo_dividir = marca_modelo.split(' ')
            # La marca es la primera parte al dividir el texto
            marca = marca_modelo_dividir[0]
            # El modelo es la segunda parte al dividir el texto
            modelo = marca_modelo_dividir[1]
            # Buscamos la version del coche
            version = coche.find_element(By.XPATH, './/span[@class= "cardVehicle_finance__SG6JV" and @data-test= "span-version"]').text
            # Buscamo el precio del coche
            precio = coche.find_element(By.XPATH, './/span[@class= "cardVehicle_finance__SG6JV" and @data-test= "span-finance"]').text
            # Para hacer que haya menos campos en la solucion unimos el modelo sacado anteriormente con la version
            modelo_version = modelo + ' ' + version
            # Buscamos el año de la fabricación del coche
            años = coche.find_element(By.XPATH, './/span[@class= "characteristics_elements__Mb1S_" and @data-test= "span-registration-date"]').text
            # Buscamos los km que tiene el coche
            kilometros = coche.find_element(By.XPATH, './/span[@class= "characteristics_elements__Mb1S_" and @data-test= "span-km"]').text
            # Limpiamos el texto ya que por razones de encoding en el resultado salía la cadena "\u202f" y la eliminamos
            precio_limpio = precio.replace("\u202f", '')
            # Añadimos al resultado parcial el diccionario formado por los campos: marca, modelo, año, kilómetros y precio
            resultado.append({
                'marca': marca,
                'modelo': modelo_version,
                'año': años,
                'kilometros': kilometros,
                'precio': precio_limpio
            })
    except Exception as e6:
        print(f"Error en el for: {e6}")
    # Filtramos el resultado parcial para quedarnos unicamente con aquellos coches que en modelo este la cadena 'GS-Line'
    resultados_filtrados2 = [coche for coche in resultado if 'R-Line' in coche['modelo']]
    # Lo añadimos al resultado general
    lista_diccionarios_coches.extend(resultados_filtrados2)
    # Esperamos 5 segundo y quitamos la pagina
    time.sleep(5)
    driver.quit()
    # Devolvemos el resultado final
    return (lista_diccionarios_coches)