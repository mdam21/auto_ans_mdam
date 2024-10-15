from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
#from bs4 import BeautifulSoup
#import requests

def navigate_courses(driver, nivel_buscado, elementos_vacios):
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
                print(f"Curso {i + 1}: {course_name}")
                if nivel_buscado in course_name:
                    print(f"¡Nivel '{nivel_buscado}' encontrado en el curso {i + 1}!")
                    nivel_encontrado = True
                    # Buscar el botón "Student's Course" dentro del mismo contenedor
                    boton = container.find_element(By.XPATH, ".//p[contains(text(), \"Student's Course\")]")
                    boton.click()
                    time.sleep(5)
                    break
            except Exception as e:
                print(f"Curso {i + 1}: No se pudo obtener el nombre del curso o hacer clic en el botón. Error: {e}")

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
        primer_nodo = driver.find_element(By.XPATH,
                                          "/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div[2]/div/div/div[1]/a/div[2]/div[1]/p")
        # Verificar si el nodo está visible
        if not primer_nodo.is_displayed():
            # Hacer clic en el primer nodo si no está visible
            primer_nodo.click()
    except Exception as e:
        print(f"No se pudo verificar o hacer clic en el primer nodo. Error: {e}")

    # Listar los nombres de los botones desplegados y verificar la presencia del check específico y la estrella
    time.sleep(2)

    def get_botones():
        return driver.find_elements(By.XPATH,
                                    "/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div[2]/div/div/div[1]/div/div/a/span[3]/p")

    botones = get_botones()
    for l, boton in enumerate(botones, 1):
        try:
            nombre_boton = boton.text
            # Verificar la presencia del elemento específico
            elemento_xpath_check = f"/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div[2]/div/div/div[1]/div/div/a[{l}]/span[2]"
            elemento_xpath_star = f"/html/body/app/div/learner/product-view/div[1]/main/div/div[2]/div[2]/div/div/div[1]/div/div/a[{l}]/span[4]" #BORRE EL /i del final

            elemento_span_check = driver.find_element(By.XPATH, elemento_xpath_check)
            elemento_span_star_container = driver.find_element(By.XPATH, elemento_xpath_star)
            elemento_span_star = elemento_span_star_container.find_elements(By.XPATH, "i")

            # Verificar el estado del check
            if elemento_span_check.find_elements(By.XPATH, "./i[@class='lch-green-tick nemo-font nemo-tick']"):
                check_presente = "Presente"
            elif elemento_span_check.find_elements(By.XPATH,
                                                   "./span/img[@src='https://assets.cambridgeone.org/nlp/1715082149084/./node_modules/libs-content-helper/dist/assets/img/inprogress_purple.png']"):
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

                print("Aqui mocharon cabezas xd")

                if star_presente in ["Completa","Parcialmente pintada","Vacía"]:
                    print("Existe estrella, resultados correctos.")

                    # Intentar encontrar y hacer clic en el botón "Check" o "Next"
                    try:
                        check_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                 "//a[contains(@class, 'btn green-btn') and (@title='Check' or @title='Next')]"))
                        )
                        check_button.click()
                        print("Botón 'Check' o 'Next' encontrado y presionado.")
                        time.sleep(1)  # Esperar 10 segundos después de hacer clic en el botón "Check" o "Next"
                    except Exception as e:
                        print("Botón 'Check' o 'Next' no encontrado. Buscando pregunta...")
                        # Aquí debo encontrar la sección y la pregunta para poder llamar a la función correspondiente dependiendo del tipo de respuesta
                        # lo que no consigo es obtener el texto de la sección para poder llamar a la función que llenará dependiendo si es list_check,
                        # o llenar, o seleccionar. Esta función llamará cuando encuentre la pregunta, como ejemplo te dejo las dos variables de abajo



                        # Encontrar el elemento por XPath y obtener su texto
                        seccion_text = "Grammar practice 1: \"used to\"" #Esta es la seccion que debe buscar (debería leerla del DOM.)

                        # Cargar el JSON
                        with open('output.json', 'r') as file:
                            data = json.load(file)

                        # Función para manejar dropdowns
                        def manejar_dropdown(elemento_pregunta, respuesta_correcta):
                            print("Estoy en dropdowns.")
                            #elemento_dropdown = elemento_pregunta.find_element(By.XPATH, "following-sibling::select")
                            #select = Select(elemento_dropdown)
                            #select.select_by_visible_text(respuesta_correcta)

                        # Función para manejar inputs
                        def manejar_input(elemento_pregunta, respuesta_correcta):
                            print("Estoy en llenar texto")
                            #elemento_input = elemento_pregunta.find_element(By.XPATH, "following-sibling::input")
                            #elemento_input.send_keys(respuesta_correcta)

                        # Función para manejar listbox
                        def manejar_listbox(elemento_pregunta, respuesta_correcta):
                            print("Estoy en list_box")
                            #opciones = elemento_pregunta.find_elements(By.XPATH, "following-sibling::option")
                            #for opcion in opciones:
                            #    if opcion.text == respuesta_correcta:
                            #        opcion.click()
                        #        break

                        # Función para manejar buttons
                        def manejar_buttons(elemento_pregunta, respuesta_correcta):
                            print("Estoy en botones")
                            #botones = elemento_pregunta.find_elements(By.XPATH, "following-sibling::button")
                            #for boton in botones:
                            #   if boton.text == respuesta_correcta:
                            #       boton.click()
                        #       break

                        # Iterar sobre las secciones en el JSON
                        if seccion_text in data:
                            preguntas = data[seccion_text]

                            for pregunta in preguntas:
                                pregunta_texto = pregunta['question']
                                respuesta_correcta = pregunta['correct_answer']
                                tipo_respuesta = pregunta['ans_type']
                                print(pregunta_texto)

                                # Buscar la pregunta en el área visible de la página
                                try:
                                    # Esperar hasta que el elemento sea visible
                                    wait = WebDriverWait(driver, 10)
                                    contenedor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-10")))
                                    print("Contenedor encontrado")

                                    # Verificar el contenido del contenedor
                                    print(contenedor.get_attribute('innerHTML'))




                                    # Buscar el elemento de la pregunta dentro del contenedor
                                    elemento_pregunta = contenedor.find_element(By.XPATH,
                                                                                f".//*[contains(text(), '{pregunta_texto.strip()}')]")
                                    print("Elemento de la pregunta encontrado")

                                    if tipo_respuesta == 'dropdown':
                                        manejar_dropdown(elemento_pregunta, respuesta_correcta)
                                    elif tipo_respuesta == 'text_input':
                                        manejar_input(elemento_pregunta, respuesta_correcta)
                                    elif tipo_respuesta == 'listbox':
                                        manejar_listbox(elemento_pregunta, respuesta_correcta)
                                    elif tipo_respuesta == 'buttons_sel':
                                        manejar_buttons(elemento_pregunta, respuesta_correcta)

                                except Exception as e:
                                    print(f"No se pudo encontrar la pregunta: {pregunta_texto}. Error: {e}")




                else:
                    # Intentar encontrar y hacer clic en el botón "Check" o "Next"
                    try:
                        check_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//a[contains(@class, 'btn green-btn') and (@title='Check' or @title='Next')]"))
                        )
                        time.sleep(10)
                        check_button.click()
                        print("Botón 'Check' o 'Next' encontrado y presionado.")
                        time.sleep(30)  # Esperar 10 segundos después de hacer clic en el botón "Check" o "Next"
                    except Exception as e:
                        print("Botón 'Check' o 'Next' no encontrado. Buscando pregunta...")
                        # En esta parte lo que necesito es que seleccione la primera respuesta de cualquier pregunta, pero creo que tiene que hacer uso de una función similar
                        # o muy parecida a la función de cuando responde en la sección con estrella, pero en esta parte no necesita asociarse con la base de datos para responder.
                        try:
                            # Localizar la pregunta
                            pregunta = driver.find_element(By.CSS_SELECTOR, "div.interaction p").text
                            print(f"Pregunta encontrada: {pregunta}")
                        except Exception as e:
                            print(f"No se pudo encontrar la pregunta. Error: {e}")

                break  # Detener la búsqueda después de hacer clic
        except Exception as e:
            print(f"Botón {l}: No se pudo obtener el nombre o verificar los elementos. Error: {e}")
            continue  # Continuar con el siguiente botón si hay un error
