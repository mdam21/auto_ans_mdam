from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    
    # Localizar el botón de "Log in"
    login_button = driver.find_element(By.ID, "onboarding-header-login-btn")
    
    # Desplazarse hasta el botón de "Log in"
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    
    # Hacer clic en el botón de "Log in"
    login_button.click()
    
    # Esperar a que la página de login cargue completamente
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "gigya-loginID-56269462240752180")))
    
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

   # Esperar a que la página del solucionario cargue completamente
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_del_solucionario")))  # Reemplaza "id_del_solucionario" con el ID correcto del solucionario
    

    # Esperar un tiempo para observar la página
    time.sleep(20)
finally:
    # Cerrar el navegador
    driver.quit()

