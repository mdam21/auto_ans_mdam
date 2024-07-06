from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Solicitar datos de entrada al usuario
user_email = "christian.montalvo@uisek.edu.ec"
user_password = "Chris2023"

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
    time.sleep(5)
    
    # Función para localizar y devolver los contenedores de cursos
    def get_course_containers():
        main_node = driver.find_element(By.CSS_SELECTOR, "main[class*='user-space-container']")
        return main_node.find_elements(By.CSS_SELECTOR, "div.courses.d-flex.flex-column.w-100")

    # Localizar los contenedores de cursos
    course_containers = get_course_containers()
    
    if not course_containers:
        print("No se encontraron los contenedores de cursos.")
    else:
        print(f"Se encontraron {len(course_containers)} contenedores de cursos.")
        
        # Mostrar los nombres de todos los contenedores de cursos encontrados
        for i, container in enumerate(course_containers):
            try:
                course_name = container.find_element(By.CSS_SELECTOR, "p.bundle-title").text
                print(f"Curso {i+1}: {course_name}")
            except:
                print(f"Curso {i+1}: No se pudo obtener el nombre del curso.")
    
    time.sleep(2)
finally:
    # Cerrar el navegador
    driver.quit()

