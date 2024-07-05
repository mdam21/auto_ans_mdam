from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configurar el WebDriver para Firefox
driver = webdriver.Firefox()

try:
    # Abrir la página web
    driver.get("https://www.cambridgeone.org/")
    
    # Esperar a que la página cargue completamente
    time.sleep(5)
    
    # Localizar y hacer clic en el botón de "Log in"
    login_button = driver.find_element(By.ID, "onboarding-header-login-btn")
    login_button.click()
    
    # Esperar a que la página de login cargue completamente
    time.sleep(5)
    
    # Localizar el campo de usuario y rellenarlo
    user_field = driver.find_element(By.ID, "gigya-loginID-56269462240752180")
    user_field.send_keys("victor.yanza@uisek.edu.ec")
    
    # Localizar el campo de contraseña y rellenarlo
    password_field = driver.find_element(By.ID, "gigya-password-56383998600152700")
    password_field.send_keys("g@briel2204")
    
    # Enviar el formulario de acceso
    password_field.send_keys(Keys.RETURN)
    
    # Esperar a que la página de solución cargue completamente
    time.sleep(10)
    
    # Localizar y seleccionar la opción del solucionario
    #homework_button = driver.find_element(By.CLASS_NAME, "homework-button")
    #homework_button.click()

    
    # Esperar a que la página del solucionario cargue completamente
    time.sleep(5)

finally:
    # Cerrar el navegador
    driver.quit()

