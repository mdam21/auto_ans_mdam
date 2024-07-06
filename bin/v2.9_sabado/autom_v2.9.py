from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Solicitar datos de entrada al usuario
user_email = "miryam.nepas@uisek.edu.ec"
user_password = "eQNh-DhR9"
nivel_buscado = "Level 3B"  # Puedes cambiar este valor según lo que quieras buscar

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
        
        # Buscar el nivel específico entre los contenedores de cursos
        nivel_encontrado = False
        for i, container in enumerate(course_containers):
            try:
                course_name = container.find_element(By.CSS_SELECTOR, "p.bundle-title").text
                print(f"Curso {i+1}: {course_name}")
                if nivel_buscado in course_name:
                    print(f"¡Nivel '{nivel_buscado}' encontrado en el curso {i+1}!")
                    nivel_encontrado = True
                    # Buscar el botón "Student's Course" dentro del mismo contenedor
                    boton = container.find_element(By.XPATH, ".//p[contains(text(), \"Student's Course\")]")
                    boton.click()
                    time.sleep(5)
                    break
            except Exception as e:
                print(f"Curso {i+1}: No se pudo obtener el nombre del curso o hacer clic en el botón. Error: {e}")
        
        if not nivel_encontrado:
            print(f"Nivel '{nivel_buscado}' no encontrado entre los cursos.")
    
    # Después de hacer clic en el botón, buscar el subnodo con "In progress" y hacer clic en él
    time.sleep(5)
    subnodos = driver.find_elements(By.XPATH, "/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div")
    for j, subnodo in enumerate(subnodos, 1):
        try:
            estado_subnodo = subnodo.find_element(By.XPATH, ".//div/div[1]/div/div/div[2]/p").text
            if estado_subnodo == "In progress":
                print(f"Subnodo {j} con estado 'In progress' encontrado.")
                subnodo.click()
                break
        except Exception as e:
            print(f"Subnodo {j}: No se pudo verificar el estado. Error: {e}")

    # Hacer clic en el primer nodo
    time.sleep(5)
    primer_nodo = driver.find_element(By.XPATH, "/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div[2]/div/div/div[1]/a/div[2]/div[1]/p")
    primer_nodo.click()

    # Listar los nombres de los botones desplegados
    time.sleep(2)
    botones = driver.find_elements(By.XPATH, "/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div[2]/div/div/div[1]/div/div/a/span[3]/p")
    for l, boton in enumerate(botones, 1):
        try:
            nombre_boton = boton.text
            print(f"Botón {l}: {nombre_boton}")
        except Exception as e:
            print(f"Botón {l}: No se pudo obtener el nombre. Error: {e}")

    # Volver a hacer clic en el nodo inicial
    time.sleep(1)
    primer_nodo.click()

finally:
    # Cerrar el navegador
    driver.quit()

