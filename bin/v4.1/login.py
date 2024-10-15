from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def login_to_cambridge(driver, user_email, user_password):
    # Abrir la página web
    driver.get("https://www.cambridgeone.org/")

    # Esperar a que la página cargue completamente
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "onboarding-header-login-btn")))
    time.sleep(1)

    # Localizar y aceptar las cookies
    try:
        accept_cookies_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-white-bg.accept-btn")
        driver.execute_script("arguments[0].click();", accept_cookies_button)
        time.sleep(2)  # Esperar un momento para asegurarse de que el banner de cookies desaparezca
    except:
        print("No se encontró el botón de aceptar cookies o ya estaba aceptado.")

    # Localizar el botón de "Log in"
    login_button = driver.find_element(By.ID, "onboarding-header-login-btn")

    # Desplazarse hasta el botón de "Log in"
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)

    # Hacer clic en el botón de "Log in"
    driver.execute_script("arguments[0].click();", login_button)

    # Esperar a que la página de login cargue completamente
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "gigya-loginID-56269462240752180")))

    # Localizar el campo de usuario y rellenarlo
    user_field = driver.find_element(By.ID, "gigya-loginID-56269462240752180")
    user_field.send_keys(user_email)

    # Localizar el campo de contraseña y rellenarlo
    password_field = driver.find_element(By.ID, "gigya-password-56383998600152700")
    password_field.send_keys(user_password)

    # Enviar el formulario de acceso
    password_field.send_keys(Keys.RETURN)

    try:
        # Esperar a que la página principal cargue completamente después de iniciar sesión
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "tile-section-1")))
    except Exception as e:
        # Verificar si hay un mensaje de error en el proceso de inicio de sesión
        error_message = driver.find_element(By.CSS_SELECTOR, "div.gigya-error-msg").text
        print(f"Error de inicio de sesión: {error_message}")
        raise e
