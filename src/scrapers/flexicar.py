from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options as Options_chrome
from selenium.webdriver.common.action_chains import ActionChains 


def move_slider_left(boton_barra_izquierda, steps,driver):
        action = ActionChains(driver)
        for _ in range(steps):
            action.click_and_hold(boton_barra_izquierda).move_by_offset(-5, 0).release().perform()
            time.sleep(0.01)

# Añadimos una funcion llamada flexicar para llamarlo desde la funcion general
def flexicar():
    options = Options_chrome()
    # Le decimos al navegador que ignore los errores de certificados SSL
    options.add_argument('--ignore-certificate-errors')
    # Le decimos al navegador que ignore todos los errores SSL en general.
    options.add_argument('--ignore-ssl-errors')
    # Desactivamos el uso de la GPU
    options.add_argument('--disable-gpu') 

    # Creamos un driver con las opciones anteriores
    driver = webdriver.Chrome(options=options)
    # Buscamos la página de Flexicar
    driver.get('https://www.flexicar.es/')
    
    # Creamos la lista donde vamos a guardar todos los coches
    lista_diccionarios_coches=[]
    # Esperamos a que aparezca el pop-up de las coockies y las aceptamos
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'CybotCookiebotDialogContentWrapper')))
        aceptar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')))

        aceptar_button.click()
    except Exception as e1:
        print(f'la excepcion es {e1}')
    
    ActionChains(driver).move_by_offset(10, 10).click().perform()

    try:
        # Esperamos a que sea visible el boton para seleccionar la marca
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div')))
        # Esperamos a que ese boton sea clickeable
        boton_marca = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div/div/div[1]/div[2]')))
        # Hacemos click
        boton_marca.click()
    except Exception as e2:
        print(f'la excepcion es {e2}')
    # Esperamos 2 segundo para realizar la siguiente accion
    time.sleep(2)
    
    try:
        # Esperamos a que aparezca la marca de Seat y hacemos click
        boton_seat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div/div/div[2]/div/div/div/div/div/label[43]/span[1]/span')))
        boton_seat.click()
    except Exception as e9:
        print(f'el error es seat: {e9}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    try:
        # Esperamos a que sea visible el boton de los modelos
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div')))
        # Esperamos a que sea clickeable y le hacemos click
        boton_modelos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[2]')))
        boton_modelos.click()
    except Exception as e4:
        print(f'el error es el siguiente {e4}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que sea clickeable el elemento del modelo Ibiza
        boton_ibiza = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/label[5]/span[1]/span')))
        # Hacemos click en ese boton
        boton_ibiza.click()
    except Exception as e:
        print(f'el error es ibiza: {e}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que sea visible el boton de los modelos
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div')))
        # Esperamos a que sea clickeable y le hacemos click
        boton_modelos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[2]')))
        boton_modelos.click()
    except Exception as e4:
        print(f'el error es el siguiente {e4}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    driver.maximize_window()

    try:
        # Esperamos a que el boton para ver los coches sea clickeable
        boton_coches = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[2]/div/a')))
        # Hacemos click
        boton_coches.click()
    except Exception as e5:
        print(f'el error es:{e5}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    
    try: 
        resultados=[]
        # Creamos el conjunto para almacenar coches únicos
        resultados_unicos = set()

        for _ in range(60):  
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(2)  # Esperamos dos segundos para realizar la siguiente acción
            
            # Extraemos los coches de la página
            coches = driver.find_elements(By.CSS_SELECTOR, '.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-6.MuiGrid-grid-md-6.MuiGrid-grid-lg-4')
            
            for coche in coches:
                # Extraemos la marca y modelo
                texto_marca_modelo = coche.find_element(By.XPATH, './/h2[@class="MuiTypography-root jss78 MuiTypography-h6"]').text
                partes = texto_marca_modelo.split(' ')
                
                if len(partes) >= 2:
                    marca = partes[0].replace('"', '').strip()
                    modelo = ' '.join(partes[1:]).replace('"', '').strip()
                else:
                    print("No se encontró suficiente información de marca y modelo.")
                    continue
                
                # Extraemos el paquete, año, kilómetros y precio
                paquete_deportivo_entero = coche.find_element(By.XPATH, './/p[@class="MuiTypography-root jss79 MuiTypography-body1"]').text
                

                años_coche = coche.find_element(By.XPATH, './/ul[@class="jss123 jss124"]/li[@class="jss127"][1]').text
                km_coche = coche.find_element(By.XPATH, './/ul[@class="jss123 jss124"]/li[@class="jss127"][2]').text
                
                try:
                    años_num = int(años_coche)
                    km_num = int(km_coche.replace('.', '').replace('km', ''))
                except ValueError as e:
                    print(f"Error en la conversión de años o km: {e}")
                    continue
                
                precio = coche.find_element(By.XPATH, './/p[@class="MuiTypography-root jss81 MuiTypography-h6"]').text
                precio_limpio = precio.replace("\u202f", '')
                
                # Filtramos por los años y kilómetros
                if años_num >= 2021 and km_num <= 125000:
                    # Creamos una cadena única para identificar cada coche
                    coche_clave = f"{marca}-{modelo}-{años_num}-{km_num}-{precio_limpio}"
                    # Verificamos si el coche ya está en el conjunto
                    if coche_clave not in resultados_unicos:
                        # Si no está en el conjunto, lo agregamos
                        resultados_unicos.add(coche_clave)
                        # Agregamos el coche a los resultados finales
                        print(modelo + " " +paquete_deportivo_entero)
                        resultados.append({
                            'marca': marca,
                            'modelo': modelo + " " + paquete_deportivo_entero,
                            'año': años_coche,
                            'kilometros': km_coche,
                            'precio': precio_limpio
                        })
        # Filtras el resultado parcial para quedarnos unicamente con los coches cuyo modelo es Clio Esprit Alpine
        resultados_filtrados = [
        coche for coche in resultados 
        if 'FR' in coche['modelo'] 
        ]
        # Si esta vacio mostramos que no hay este tipo de coches
        if len(resultados_filtrados) == 0:
            print('No hay Ibiza FR')
        # Añadimos los coches que tengan ese modelo a la solucion final
        else:
            lista_diccionarios_coches.extend(resultados_filtrados)
          
# Al final, `resultados` contendrá solo coches únicos.

    except Exception as e:
        print(e)
    
    # Esperamos 10 segundos y buscamos de nuevo la pagina para realizar la siguiente busqueda
    time.sleep(10)
    
    driver.get('https://www.flexicar.es/')
    # Esperamos 5 segundos para que cargue todo correctamente
    time.sleep(5)
    ActionChains(driver).move_by_offset(10, 10).click().perform()
    try:
        # Esperamos a que sea visible el boton de las marcas
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div')))
        # Esperamos a que el boton de las marcas sea clickeable y hacemos click
        boton_marca = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div/div/div[1]/div[2]')))
        boton_marca.click()
    except Exception as e2:
        print(f'la excepcion es {e2}')
    # Esperamos dos segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que el elemento de la marca Opel sea clickeable y hacemos click
        boton_opel = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div/div/div[2]/div/div/div/div/div/label[38]/span[1]')))
        boton_opel.click()
    except Exception as e9:
        print(f'el error es opel: {e9}')
    # Esperamos dos segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que sea visible el boton de los modelos
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div')))
        # Esperamos a que sea clickeable el boton de los modelos y hacemos click
        boton_modelos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[2]')))
        boton_modelos.click()
    except Exception as e4:
        print(f'el error es el siguiente {e4}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    try:
        # Esperamos a que el boton del modelo Corsa sea clickeable y hacemos click
        boton_corsa = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/label[8]/span[1]/span')))
        boton_corsa.click()
    except Exception as e10:
        print(f'el error es corsa: {e10}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    try:
        # Esperamos a que sea visible el boton de los modelos
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div')))
        # Esperamos a que sea clickeable el boton de los modelos y hacemos click
        boton_modelos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[2]')))
        boton_modelos.click()
    except Exception as e4:
        print(f'el error es el siguiente {e4}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    driver.maximize_window()

    try:
        # Esperamos a que el boton para mostrar los coches sea clickeable y hacemos click
        boton_coches = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[2]/div/a')))
        boton_coches.click()
    except Exception as e5:
            print(f'el error es:{e5}')
    # Esperamos dos segundos para realizar la siguiente accion 
    time.sleep(2)

    try: 
        resultados=[]
        # Creamos el conjunto para almacenar coches únicos
        resultados_unicos = set()

        for _ in range(60):  
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(2)  # Esperamos dos segundos para realizar la siguiente acción
            
            # Extraemos los coches de la página
            coches = driver.find_elements(By.CSS_SELECTOR, '.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-6.MuiGrid-grid-md-6.MuiGrid-grid-lg-4')
            
            for coche in coches:
                # Extraemos la marca y modelo
                texto_marca_modelo = coche.find_element(By.XPATH, './/h2[@class="MuiTypography-root jss78 MuiTypography-h6"]').text
                partes = texto_marca_modelo.split(' ')
                
                if len(partes) >= 2:
                    marca = partes[0].replace('"', '').strip()
                    modelo = ' '.join(partes[1:]).replace('"', '').strip()
                else:
                    print("No se encontró suficiente información de marca y modelo.")
                    continue
                
                # Extraemos el paquete, año, kilómetros y precio
                paquete_deportivo_entero = coche.find_element(By.XPATH, './/p[@class="MuiTypography-root jss79 MuiTypography-body1"]').text
                

                años_coche = coche.find_element(By.XPATH, './/ul[@class="jss123 jss124"]/li[@class="jss127"][1]').text
                km_coche = coche.find_element(By.XPATH, './/ul[@class="jss123 jss124"]/li[@class="jss127"][2]').text
                
                try:
                    años_num = int(años_coche)
                    km_num = int(km_coche.replace('.', '').replace('km', ''))
                except ValueError as e:
                    print(f"Error en la conversión de años o km: {e}")
                    continue
                
                precio = coche.find_element(By.XPATH, './/p[@class="MuiTypography-root jss81 MuiTypography-h6"]').text
                precio_limpio = precio.replace("\u202f", '')
                
                # Filtramos por los años y kilómetros
                if años_num >= 2021 and km_num <= 125000:
                    # Creamos una cadena única para identificar cada coche
                    coche_clave = f"{marca}-{modelo}-{años_num}-{km_num}-{precio_limpio}"
                    # Verificamos si el coche ya está en el conjunto
                    if coche_clave not in resultados_unicos:
                        # Si no está en el conjunto, lo agregamos
                        resultados_unicos.add(coche_clave)
                        # Agregamos el coche a los resultados finales
                        print(modelo + " " +paquete_deportivo_entero)
                        resultados.append({
                            'marca': marca,
                            'modelo': modelo + " " + paquete_deportivo_entero,
                            'año': años_coche,
                            'kilometros': km_coche,
                            'precio': precio_limpio
                        })
        # Filtras el resultado parcial para quedarnos unicamente con los coches cuyo modelo es Clio Esprit Alpine
        resultados_filtrados = [
            coche for coche in resultados 
            if 'GS-Line' in coche['modelo'] or 'GS' in coche['modelo']
        ]
        # Si esta vacio mostramos que no hay este tipo de coches
        if len(resultados_filtrados) == 0:
            print('No hay CORSA GS LINE ')
        # Añadimos los coches que tengan ese modelo a la solucion final
        else:
            lista_diccionarios_coches.extend(resultados_filtrados)
            
# Al final, `resultados` contendrá solo coches únicos.
    
    except Exception as e:
        print(e)
    
    # Esperamos 10 segundo para abrir de nuevo una nueva pestaña
    time.sleep(10)
    driver.get('https://www.flexicar.es/')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    ActionChains(driver).move_by_offset(10, 10).click().perform()
    try:
        # Esperamos a que el boton de las marcas sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div')))
        # Esperamos a que el boton de las marcas sea clickeable y hacemos click
        boton_marca = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div/div/div[1]/div[2]')))
        boton_marca.click()
    except Exception as e2:
        print(f'la excepcion es {e2}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos que el boton de Reanult sea clickeable y hacemos click
        boton_renault = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div/div/div[2]/div/div/div/div/div/label[42]/span[1]/span')))
        boton_renault.click()
    except Exception as e10:
        print(f'el error es renault {e10}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que el boton de los modelos sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div')))
        # Esperamos a que el boton de los modelos sea clickeable y hacemos click
        boton_modelos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[2]')))
        boton_modelos.click()
    except Exception as e4:
        print(f'el error es el siguiente {e4}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que el boton de clio sea clickeable y hacemos click
        boton_clio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/label[4]/span[1]/span')))
        boton_clio.click()
    except Exception as e9:
        print(f'el error es clio {e9}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    try:
        # Esperamos a que el boton de los modelos sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div')))
        # Esperamos a que el boton de los modelos sea clickeable y hacemos click
        boton_modelos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[2]')))
        boton_modelos.click()
    except Exception as e4:
        print(f'el error es el siguiente {e4}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    driver.maximize_window()

    try:
        # Esperamos a que el boton para ver los coches sea clickeable y hacemos click
        boton_coches = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[2]/div/a')))
        boton_coches.click()
    except Exception as e5:
        print(f'el error es:{e5}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try: 
        resultados=[]
        # Creamos el conjunto para almacenar coches únicos
        resultados_unicos = set()

        for _ in range(60):  
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(2)  # Esperamos dos segundos para realizar la siguiente acción
            
            # Extraemos los coches de la página
            coches = driver.find_elements(By.CSS_SELECTOR, '.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-6.MuiGrid-grid-md-6.MuiGrid-grid-lg-4')
            
            for coche in coches:
                # Extraemos la marca y modelo
                texto_marca_modelo = coche.find_element(By.XPATH, './/h2[@class="MuiTypography-root jss78 MuiTypography-h6"]').text
                partes = texto_marca_modelo.split(' ')
                
                if len(partes) >= 2:
                    marca = partes[0].replace('"', '').strip()
                    modelo = ' '.join(partes[1:]).replace('"', '').strip()
                else:
                    print("No se encontró suficiente información de marca y modelo.")
                    continue
                
                # Extraemos el paquete, año, kilómetros y precio
                paquete_deportivo_entero = coche.find_element(By.XPATH, './/p[@class="MuiTypography-root jss79 MuiTypography-body1"]').text
                

                años_coche = coche.find_element(By.XPATH, './/ul[@class="jss123 jss124"]/li[@class="jss127"][1]').text
                km_coche = coche.find_element(By.XPATH, './/ul[@class="jss123 jss124"]/li[@class="jss127"][2]').text
                
                try:
                    años_num = int(años_coche)
                    km_num = int(km_coche.replace('.', '').replace('km', ''))
                except ValueError as e:
                    print(f"Error en la conversión de años o km: {e}")
                    continue
                
                precio = coche.find_element(By.XPATH, './/p[@class="MuiTypography-root jss81 MuiTypography-h6"]').text
                precio_limpio = precio.replace("\u202f", '')
                
                # Filtramos por los años y kilómetros
                if años_num >= 2021 and km_num <= 125000:
                    # Creamos una cadena única para identificar cada coche
                    coche_clave = f"{marca}-{modelo}-{años_num}-{km_num}-{precio_limpio}"
                    # Verificamos si el coche ya está en el conjunto
                    if coche_clave not in resultados_unicos:
                        # Si no está en el conjunto, lo agregamos
                        resultados_unicos.add(coche_clave)
                        # Agregamos el coche a los resultados finales
                        print(modelo + " " +paquete_deportivo_entero)
                        resultados.append({
                            'marca': marca,
                            'modelo': modelo + " " + paquete_deportivo_entero,
                            'año': años_coche,
                            'kilometros': km_coche,
                            'precio': precio_limpio
                        })
        # Filtras el resultado parcial para quedarnos unicamente con los coches cuyo modelo es Clio Esprit Alpine
        resultados_filtrados = [
        coche for coche in resultados 
        if 'ESPRIT' in coche['modelo'] 
        ]
        # Si esta vacio mostramos que no hay este tipo de coches
        if len(resultados_filtrados) == 0:
            print('No hay Clio Esprit Alpine ')
        # Añadimos los coches que tengan ese modelo a la solucion final
        else:
            lista_diccionarios_coches.extend(resultados_filtrados)
            
# Al final, `resultados` contendrá solo coches únicos.

    except Exception as e:
        print(e)

    # Esperamos 10 segundo para abrir de nuevo una nueva pestaña
    time.sleep(10)
    driver.get('https://www.flexicar.es/')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    ActionChains(driver).move_by_offset(10, 10).click().perform()
    try:
        # Esperamos a que el boton de las marcas sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div')))
        # Esperamos a que el boton de las marcas sea clickeable y hacemos click
        boton_marca = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div/div/div[1]/div[2]')))
        boton_marca.click()
    except Exception as e2:
        print(f'la excepcion es {e2}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos que el boton de Reanult sea clickeable y hacemos click
        boton_toyota = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div/div/div[2]/div/div/div/div/div/label[50]/span[1]/span')))
        boton_toyota.click()
    except Exception as e10:
        print(f'el error es toyota {e10}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que el boton de los modelos sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div')))
        # Esperamos a que el boton de los modelos sea clickeable y hacemos click
        boton_modelos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[2]')))
        boton_modelos.click()
    except Exception as e4:
        print(f'el error es el siguiente {e4}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que el boton de clio sea clickeable y hacemos click
        boton_yaris = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/label[25]/span[1]/span')))
        boton_yaris.click()
    except Exception as e9:
        print(f'el error es yaris {e9}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    try:
        # Esperamos a que el boton de los modelos sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div')))
        # Esperamos a que el boton de los modelos sea clickeable y hacemos click
        boton_modelos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[2]')))
        boton_modelos.click()
    except Exception as e4:
        print(f'el error es el siguiente {e4}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    driver.maximize_window()

    try:
        # Esperamos a que el boton para ver los coches sea clickeable y hacemos click
        boton_coches = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[2]/div/a')))
        boton_coches.click()
    except Exception as e5:
        print(f'el error es:{e5}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try: 
        resultados=[]
        # Creamos el conjunto para almacenar coches únicos
        resultados_unicos = set()

        for _ in range(60):  
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(2)  # Esperamos dos segundos para realizar la siguiente acción
            
            # Extraemos los coches de la página
            coches = driver.find_elements(By.CSS_SELECTOR, '.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-6.MuiGrid-grid-md-6.MuiGrid-grid-lg-4')
            
            for coche in coches:
                # Extraemos la marca y modelo
                texto_marca_modelo = coche.find_element(By.XPATH, './/h2[@class="MuiTypography-root jss78 MuiTypography-h6"]').text
                partes = texto_marca_modelo.split(' ')
                
                if len(partes) >= 2:
                    marca = partes[0].replace('"', '').strip()
                    modelo = ' '.join(partes[1:]).replace('"', '').strip()
                else:
                    print("No se encontró suficiente información de marca y modelo.")
                    continue
                
                # Extraemos el paquete, año, kilómetros y precio
                paquete_deportivo_entero = coche.find_element(By.XPATH, './/p[@class="MuiTypography-root jss79 MuiTypography-body1"]').text
                

                años_coche = coche.find_element(By.XPATH, './/ul[@class="jss123 jss124"]/li[@class="jss127"][1]').text
                km_coche = coche.find_element(By.XPATH, './/ul[@class="jss123 jss124"]/li[@class="jss127"][2]').text
                
                try:
                    años_num = int(años_coche)
                    km_num = int(km_coche.replace('.', '').replace('km', ''))
                except ValueError as e:
                    print(f"Error en la conversión de años o km: {e}")
                    continue
                
                precio = coche.find_element(By.XPATH, './/p[@class="MuiTypography-root jss81 MuiTypography-h6"]').text
                precio_limpio = precio.replace("\u202f", '')
                
                # Filtramos por los años y kilómetros
                if años_num >= 2021 and km_num <= 125000:
                    # Creamos una cadena única para identificar cada coche
                    coche_clave = f"{marca}-{modelo}-{años_num}-{km_num}-{precio_limpio}"
                    # Verificamos si el coche ya está en el conjunto
                    if coche_clave not in resultados_unicos:
                        # Si no está en el conjunto, lo agregamos
                        resultados_unicos.add(coche_clave)
                        # Agregamos el coche a los resultados finales
                        print(modelo + " " +paquete_deportivo_entero)
                        resultados.append({
                            'marca': marca,
                            'modelo': modelo + " " + paquete_deportivo_entero,
                            'año': años_coche,
                            'kilometros': km_coche,
                            'precio': precio_limpio
                        })
        # Filtras el resultado parcial para quedarnos unicamente con los coches cuyo modelo es Clio Esprit Alpine
        resultados_filtrados = [
        coche for coche in resultados 
        if 'GR' in coche['modelo'] 
        ]
        # Si esta vacio mostramos que no hay este tipo de coches
        if len(resultados_filtrados) == 0:
            print('No hay CORSA GS LINE ')
        # Añadimos los coches que tengan ese modelo a la solucion final
        else:
            lista_diccionarios_coches.extend(resultados_filtrados)
            
# Al final, `resultados` contendrá solo coches únicos.

    except Exception as e:
        print(e)

    # Esperamos 10 segundo para abrir de nuevo una nueva pestaña
    time.sleep(10)
    driver.get('https://www.flexicar.es/')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    ActionChains(driver).move_by_offset(10, 10).click().perform()
    try:
        # Esperamos a que el boton de las marcas sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div')))
        # Esperamos a que el boton de las marcas sea clickeable y hacemos click
        boton_marca = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div/div/div[1]/div[2]')))
        boton_marca.click()
    except Exception as e2:
        print(f'la excepcion es {e2}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos que el boton de Reanult sea clickeable y hacemos click
        boton_Volkswagen = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[1]/div/div/div[2]/div/div/div/div/div/label[51]/span[1]/span')))
        boton_Volkswagen.click()
    except Exception as e10:
        print(f'el error es renault {e10}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que el boton de los modelos sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div')))
        # Esperamos a que el boton de los modelos sea clickeable y hacemos click
        boton_modelos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[2]')))
        boton_modelos.click()
    except Exception as e4:
        print(f'el error es el siguiente {e4}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que el boton de clio sea clickeable y hacemos click
        boton_polo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div/label[16]/span[1]/span')))
        boton_polo.click()
    except Exception as e9:
        print(f'el error es clio {e9}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try:
        # Esperamos a que el boton de los modelos sea visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div')))
        # Esperamos a que el boton de los modelos sea clickeable y hacemos click
        boton_modelos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div[2]')))
        boton_modelos.click()
    except Exception as e4:
        print(f'el error es el siguiente {e4}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)
    driver.maximize_window()

    try:
        # Esperamos a que el boton para ver los coches sea clickeable y hacemos click
        boton_coches = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div/div[2]/div/a')))
        boton_coches.click()
    except Exception as e5:
        print(f'el error es:{e5}')
    # Esperamos 2 segundos para realizar la siguiente accion
    time.sleep(2)

    try: 
        resultados=[]
        # Creamos el conjunto para almacenar coches únicos
        resultados_unicos = set()

        for _ in range(60):  
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(2)  # Esperamos dos segundos para realizar la siguiente acción
            
            # Extraemos los coches de la página
            coches = driver.find_elements(By.CSS_SELECTOR, '.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-6.MuiGrid-grid-md-6.MuiGrid-grid-lg-4')
            
            for coche in coches:
                # Extraemos la marca y modelo
                texto_marca_modelo = coche.find_element(By.XPATH, './/h2[@class="MuiTypography-root jss78 MuiTypography-h6"]').text
                partes = texto_marca_modelo.split(' ')
                
                if len(partes) >= 2:
                    marca = partes[0].replace('"', '').strip()
                    modelo = ' '.join(partes[1:]).replace('"', '').strip()
                else:
                    print("No se encontró suficiente información de marca y modelo.")
                    continue
                
                # Extraemos el paquete, año, kilómetros y precio
                paquete_deportivo_entero = coche.find_element(By.XPATH, './/p[@class="MuiTypography-root jss79 MuiTypography-body1"]').text
                

                años_coche = coche.find_element(By.XPATH, './/ul[@class="jss123 jss124"]/li[@class="jss127"][1]').text
                km_coche = coche.find_element(By.XPATH, './/ul[@class="jss123 jss124"]/li[@class="jss127"][2]').text
                
                try:
                    años_num = int(años_coche)
                    km_num = int(km_coche.replace('.', '').replace('km', ''))
                except ValueError as e:
                    print(f"Error en la conversión de años o km: {e}")
                    continue
                
                precio = coche.find_element(By.XPATH, './/p[@class="MuiTypography-root jss81 MuiTypography-h6"]').text
                precio_limpio = precio.replace("\u202f", '')
                
                # Filtramos por los años y kilómetros
                if años_num >= 2021 and km_num <= 125000:
                    # Creamos una cadena única para identificar cada coche
                    coche_clave = f"{marca}-{modelo}-{años_num}-{km_num}-{precio_limpio}"
                    # Verificamos si el coche ya está en el conjunto
                    if coche_clave not in resultados_unicos:
                        # Si no está en el conjunto, lo agregamos
                        resultados_unicos.add(coche_clave)
                        # Agregamos el coche a los resultados finales
                        print(modelo + " " +paquete_deportivo_entero)
                        resultados.append({
                            'marca': marca,
                            'modelo': modelo + " " + paquete_deportivo_entero,
                            'año': años_coche,
                            'kilometros': km_coche,
                            'precio': precio_limpio
                        })
        # Filtras el resultado parcial para quedarnos unicamente con los coches cuyo modelo es Clio Esprit Alpine
        resultados_filtrados = [
        coche for coche in resultados 
        if 'R' in coche['modelo'] 
        ]
        # Si esta vacio mostramos que no hay este tipo de coches
        if len(resultados_filtrados) == 0:
            print('No hay CORSA GS LINE ')
        # Añadimos los coches que tengan ese modelo a la solucion final
        else:
            lista_diccionarios_coches.extend(resultados_filtrados)
            
# Al final, `resultados` contendrá solo coches únicos.

    except Exception as e:
        print(e)
    
    # Finalmente cerramos todos los buscadores
    driver.quit()
    # Devolvemos el resultado final que sera una lista de diccionarios donde cada diccionario es un coche representado por su informacion
    return(lista_diccionarios_coches)