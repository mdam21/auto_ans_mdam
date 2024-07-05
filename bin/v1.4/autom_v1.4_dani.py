from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv


# Solicitar datos de entrada al usuario
user_email = input("Introduce tu usuario (email): ")
user_password = input("Introduce tu contraseña: ")
nivel = input("Introduce el nivel que deseas (ejemplo: A1, B1, C1, etc.): ")

# Configurar el WebDriver para Firefox
driver = webdriver.Firefox()

try:
    # Abrir la página web
    driver.get("https://www.cambridgeone.org/")
    
    # Esperar a que la página cargue completamente
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onboarding-header-login-btn")))
    time.sleep(10)
    
    # Localizar el botón de "Log in"
    login_button = driver.find_element(By.ID, "onboarding-header-login-btn")
    
    # Desplazarse hasta el botón de "Log in"
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    
    # Hacer clic en el botón de "Log in"
    login_button.click()
    
    # Esperar a que la página de login cargue completamente
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "gigya-loginID-56269462240752180")))
    
    # Localizar y aceptar las cookies
    try:
        accept_cookies_button = driver.find_element(By.CSS_SELECTOR, "btn btn-white-bg accept-btn")  # Reemplazar "selector_del_boton_aceptar" con el selector correcto del botón de aceptar cookies
        accept_cookies_button.click()
    except:
        print("No se encontró el botón de aceptar cookies o ya estaba aceptado.")
    
    # Localizar el campo de usuario y rellenarlo
    user_field = driver.find_element(By.ID, "gigya-loginID-56269462240752180")
    user_field.send_keys(user_email)
    
    # Localizar el campo de contraseña y rellenarlo
    password_field = driver.find_element(By.ID, "gigya-password-56383998600152700")
    password_field.send_keys(user_password)
    
    # Enviar el formulario de acceso
    password_field.send_keys(Keys.RETURN)
    
    # Esperar a que la página principal cargue completamente después de iniciar sesión
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "homework-button")))
    
    # Localizar y seleccionar la opción del solucionario
    homework_button = driver.find_element(By.CLASS_NAME, "homework-button")
    homework_button.click()

    # Añadir aquí el siguiente clic
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.assignment-header')))
    collapse_button = driver.find_element(By.CSS_SELECTOR, 'a.assignment-header')
    collapse_button.click()

    # Esperar a que el contenido colapsado esté presente y hacer clic en el siguiente elemento
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "clase-deseada")))  # Reemplazar "clase-deseada" con el nombre de la clase real
    #clase_element = driver.find_element(By.CLASS_NAME, "clase-deseada")
    #clase_element.click()

    # Esperar a que la página del solucionario cargue completamente
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_del_solucionario")))  # Reemplaza "id_del_solucionario" con el ID correcto del solucionario
    
     # Aquí añadimos el código para acceder al nodo de la imagen
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "lo-name")))

    # Localizar el elemento con el título específico dentro de la clase "lo-name"
    nodo_imagen = driver.find_element(By.XPATH, "//span[@class='lo-name' and @title='Vocabulary presentation 1: Music']")

    # Interactuar con el elemento inmediatamente después de localizarlo
    print(nodo_imagen.text)
    nodo_imagen.click()  # Si deseas hacer clic en el botón

    # Función para leer el archivo CSV y obtener la respuesta para una pregunta dada
    def obtener_respuesta(pregunta, archivo_csv):
        with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            tema = ""
            for row in reader:
                if row[0].startswith("Tema"):
                    tema = row[0]
                elif len(row) > 1 and row[0].strip() == pregunta:
                    respuestas = row[1].split('-')
                    return respuestas
        return []

    # Interactuar con el elemento inmediatamente después de localizarlo
    print(nodo_imagen.text)
    nodo_imagen.click()  # Si deseas hacer clic en el botón
    
    # Ruta al archivo CSV
    archivo_csv = '/home/dam/Documents/work_automatization/data/data_3b_prueba_para_primera_pregunta.csv'
    
    # Obtener las respuestas para la pregunta específica
    pregunta = "Choose the correct type of music for each definition."
    respuestas = obtener_respuesta(pregunta, archivo_csv)
    
    # Buscar cada respuesta en la página y hacer clic en el elemento correspondiente
    for respuesta in respuestas:
        try:
            elemento_respuesta = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),     '{respuesta.strip()}')]"))
            )
            elemento_respuesta.click()
            print(f"Respuesta encontrada y clickeada: {respuesta.strip()}")
        except:
            print(f"No se encontró la respuesta: {respuesta.strip()}")
    
    # Confirmar que se ha accedido correctamente
    print("Todas las respuestas han sido procesadas.")


    # Confirmar que se ha accedido correctamente
    print("Elemento encontrado y clickeado correctamente")

    
    # Esperar un tiempo para observar la página
    time.sleep(20)
finally:
    # Cerrar el navegador
    driver.quit()

