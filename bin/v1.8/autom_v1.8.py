#ESTA_PERFERCTOOOOOOOOOOOOOOOOOOOOOOOO#



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Solicitar datos de entrada al usuario
user_email = "dennis.tixi@uisek.edu.ec"
user_password = "Santiagotixi01"
nivel = "EVOLVE DIGITAL Level 3B"

# Configurar el WebDriver para Firefox
driver = webdriver.Firefox()

try:
    # Abrir la página web
    driver.get("https://www.cambridgeone.org/")
    
    # Esperar a que la página cargue completamente
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "onboarding-header-login-btn")))
    time.sleep(1)
    
    # Localizar el botón de "Log in"
    login_button = driver.find_element(By.ID, "onboarding-header-login-btn")
    
    # Desplazarse hasta el botón de "Log in"
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    
    # Hacer clic en el botón de "Log in"
    login_button.click()
    
    # Esperar a que la página de login cargue completamente
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "gigya-loginID-56269462240752180")))
    
    # Localizar y aceptar las cookies
    try:
        accept_cookies_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-white-bg.accept-btn")
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
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "tile-section-1")))

    # Esperar un poco más para asegurarse de que todo esté completamente cargado
    time.sleep(2)

    # Localizar la sección específica de "EVOLVE DIGITAL Level 3B" usando aria-label
    level_section = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f"//*[@aria-label='{nivel}']"))
    )
    
    # Desplazarse hasta la sección localizada
    driver.execute_script("arguments[0].scrollIntoView(true);", level_section)

    # Localizar el botón específico dentro de esa sección usando XPath y hacer clic
    try:
        specific_button = driver.find_element(By.XPATH, ".//a[.//p[contains(text(), \"Student's Course\")]]")
        driver.execute_script("arguments[0].click();", specific_button)
    except Exception as e:
        print("No se pudo encontrar el botón o ocurrió un error al hacer clic:", e)

    # Esperar un tiempo para observar la página
    time.sleep(5)

    # Localizar y hacer clic en el elemento con la clase "h5" que contiene el texto "Unit 7: Entertain us"
    try:
        unit_element = driver.find_element(By.XPATH, "//p[@class='h5' and contains(text(), 'Unit 7: Entertain us')]")
        driver.execute_script("arguments[0].click();", unit_element)
        print("Se hizo clic en 'Unit 7: Entertain us'.")
    except Exception as e:
        print("No se pudo encontrar el elemento 'Unit 7: Entertain us' o ocurrió un error al hacer clic:", e)

	# Localizar y hacer clic en el elemento con la clase part-name mb-0 que contiene el texto "Lesson 1: A 50-year playlist"
    try:
        unit_element = driver.find_element(By.XPATH, "//p[@class='part-name mb-0' and contains(text(), 'Lesson 1: A 50-year playlist')]")
        driver.execute_script("arguments[0].click();", unit_element)
        print("Se hizo clic en 'Lesson 1: A 50-year playlist'.")
    except Exception as e:
        print("No se pudo encontrar el elemento Lesson 1: A 50-year playlist' o ocurrió un error al hacer clic:", e)
	
    # Esperar un tiempo para observar la página
    time.sleep(15)
finally:
    # Cerrar el navegador
    driver.quit()

