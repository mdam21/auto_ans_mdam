import json
from collections import Counter

# Variables para los nombres de los archivos
nombre_archivo_entrada = 'database_full_v0.csv'
nombre_archivo_salida_json = 'datos_estructurados.json'
nombre_archivo_log = 'log_depuracion.txt'

# Función para procesar cada línea y extraer la información
def procesar_linea(linea):
    partes = linea.split(',')
    if len(partes) < 3:
        return None, None, None  # Devolver None si no hay suficientes partes
    etiqueta = partes[0].strip('"').strip()
    pregunta = partes[1].strip()
    respuesta = partes[2].strip()
    if '*' in respuesta:
        respuestas = respuesta.split('*')
    else:
        respuestas = [respuesta]
    return etiqueta, pregunta, respuestas

# Función para verificar y registrar caracteres no ASCII y símbolos
def verificar_caracteres(texto, log_file):
    if not texto:
        return
    caracteres_no_ascii = [char for char in texto if ord(char) > 127]
    simbolos = [char for char in texto if not char.isalnum() and not char.isspace()]
    contador_simbolos = Counter(simbolos)
    if caracteres_no_ascii:
        log_file.write(f"Texto con caracteres no ASCII: {texto}\n")
        log_file.write(f"Caracteres no ASCII encontrados: {caracteres_no_ascii}\n")
    if simbolos:
        log_file.write(f"Texto con símbolos: {texto}\n")
        log_file.write(f"Símbolos encontrados: {dict(contador_simbolos)}\n")

# Leer el archivo línea por línea
data = []
with open(nombre_archivo_entrada, 'r') as file, open(nombre_archivo_log, 'w') as log:
    bloque = []
    for linea in file:
        linea = linea.strip()
        if linea:  # Asegurar que la línea no está vacía
            partes = linea.split(',')
            if partes[0].strip():  # Nueva etiqueta encontrada
                if len(bloque) > 1:
                    # Procesar bloque existente
                    etiqueta, pregunta, respuestas = procesar_linea(bloque[1])
                    if pregunta is not None:  # Solo agregamos si hay una pregunta válida
                        verificar_caracteres(etiqueta, log)
                        verificar_caracteres(pregunta, log)
                        for respuesta in respuestas:
                            verificar_caracteres(respuesta, log)
                        data.append({'Etiqueta': bloque[0].split(',')[0].strip(), 'Pregunta': pregunta, 'Respuestas': respuestas})
                bloque = [linea]
            else:
                bloque.append(linea)
    
    # Añadir el último bloque si existe
    if len(bloque) > 1:
        etiqueta, pregunta, respuestas = procesar_linea(bloque[1])
        if pregunta is not None:  # Verificamos nuevamente para evitar agregar datos incompletos
            verificar_caracteres(etiqueta, log)
            verificar_caracteres(pregunta, log)
            for respuesta in respuestas:
                verificar_caracteres(respuesta, log)
            data.append({'Etiqueta': bloque[0].split(',')[0].strip(), 'Pregunta': pregunta, 'Respuestas': respuestas})

# Escribir la salida en formato JSON
with open(nombre_archivo_salida_json, 'w') as f:
    json.dump(data, f, indent=4)

