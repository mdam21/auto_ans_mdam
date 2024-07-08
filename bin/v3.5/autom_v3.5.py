from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Solicitar datos de entrada al usuario
user_email = "danny.nazamuez@uisek.edu.ec"
user_password = "Uisek2023"
nivel_buscado = "Level 3B"  # Puedes cambiar este valor según lo que quieras buscar

# Configurar el WebDriver para Firefox
driver = webdriver.Firefox()

# Lista para guardar los XPaths de los elementos vacíos
elementos_vacios = []

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
    print("he hecho clic en el que tiene progress")
    
    # Verificar si el menú está extendido antes de hacer clic en el primer nodo
    try:
        primer_nodo = driver.find_element(By.XPATH, "/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div[2]/div/div/div[1]/a/div[2]/div[1]/p")
        # Verificar si el nodo está visible
        if not primer_nodo.is_displayed():
            # Hacer clic en el primer nodo si no está visible
            primer_nodo.click()
    except Exception as e:
        print(f"No se pudo verificar o hacer clic en el primer nodo. Error: {e}")

    # Listar los nombres de los botones desplegados y verificar la presencia del check específico y la estrella
    time.sleep(2)

    def get_botones():
        return driver.find_elements(By.XPATH, "/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div[2]/div/div/div[1]/div/div/a/span[3]/p")

    botones = get_botones()
    for l, boton in enumerate(botones, 1):
        try:
            nombre_boton = boton.text
            # Verificar la presencia del elemento específico
            elemento_xpath_check = f"/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div[2]/div/div/div[1]/div/div/a[{l}]/span[2]"
            elemento_xpath_star = f"/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div[2]/div/div/div[1]/div/div/a[{l}]/span[4]/i"
            
            elemento_span_check = driver.find_element(By.XPATH, elemento_xpath_check)
            elemento_span_star_container = driver.find_element(By.XPATH, f"/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div[2]/div/div/div[1]/div/div/a[{l}]/span[4]")
            elemento_span_star = elemento_span_star_container.find_elements(By.XPATH, "i")
            
            # Verificar el estado del check
            if elemento_span_check.find_elements(By.XPATH, "./i[@class='lch-green-tick nemo-font nemo-tick']"):
                check_presente = "Presente"
            elif elemento_span_check.find_elements(By.XPATH, "./span/img[@src='https://assets.cambridgeone.org/nlp/1715082149084/./node_modules/libs-content-helper/dist/assets/img/inprogress_purple.png']"):
                check_presente = "En progreso"
            else:
                check_presente = "Vacío"
                elementos_vacios.append(elemento_xpath_check)
            
            # Verificar el estado de la estrella
            if elemento_span_star:
                star_class = elemento_span_star[0].get_attribute("class")
                if "lch-star-abovethreshold" in star_class:
                    star_presente = "Completa"
                elif "lch-star-belowthreshold" in star_class:
                    star_presente = "Parcialmente pintada"
                elif "lch-star-not-started" in star_class:
                    star_presente = "Vacía"
                else:
                    star_presente = "NoExiste"
            else:
                star_presente = "NoExiste"
            
            # Imprimir el estado del botón
            print(f"Botón {l}: {nombre_boton} - Check: {check_presente} - Star: {star_presente}")
            
            # Hacer clic en el botón si el check está en progreso o vacío
            if check_presente in ["En progreso", "Vacío"]:
                boton.click()
                # Esperar hasta que el contenido del botón seleccionado esté completamente cargado
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//elemento_esperado")))  # Reemplaza //elemento_esperado con el XPath de un elemento que debería estar presente después de que la página cargue completamente
                print("He ingresado al botón en progreso y con estrella vacía")
                break   # Añade esta línea para detener la búsqueda después de hacer clic
            
        except Exception as e:
            print(f"Botón {l}: No se pudo obtener el nombre o verificar los elementos. Error: {e}")
            continue  # Continuar con el siguiente botón si hay un error
        
finally:
    # Cerrar el navegador
    driver.quit()
        
# Mostrar la lista de elementos vacíos
print("Lista de elementos vacíos:")
for xpath in elementos_vacios:
    print(xpath)

