from selenium import webdriver
import time
from login import login_to_cambridge
from navigate_courses import navigate_courses
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


# Opciones para Firefox
options = Options()
# options.add_argument("--headless")  # Ejecuta Firefox en modo headless (sin interfaz gráfica) - Esta línea ha sido comentada

# Ruta al geckodriver
gecko_path = '/snap/bin/geckodriver'  # Cambia esto por la ruta correcta en tu sistema

# Configuración del servicio de Firefox
service = Service(gecko_path)

driver = webdriver.Firefox(service=service, options=options)

# Solicitar datos de entrada al usuario
user_email = "victor.yanza@uisek.edu.ec"
user_password = "g@briel2204"
nivel_buscado = "Level 3B"  # Puedes cambiar este valor según lo que quieras buscar

# Lista para guardar los XPaths de los elementos vacíos
elementos_vacios = []

try:
    # Iniciar sesión en Cambridge
    login_to_cambridge(driver, user_email, user_password)

    # Navegar por los cursos y realizar las acciones necesarias
    navigate_courses(driver, nivel_buscado, elementos_vacios)

finally:
    # Cerrar el navegador
    driver.quit()

# Mostrar la lista de elementos vacíos
print("Lista de elementos vacíos:")
for xpath in elementos_vacios:
    print(xpath)