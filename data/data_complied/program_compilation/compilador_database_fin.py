import csv
import json

# Ruta al archivo CSV de entrada y al archivo JSON de salida
csv_file_path = 'tu_archivo.csv'
json_file_path = 'output.json'

# Inicializar un diccionario para almacenar los datos
data = {}

# Leer el archivo CSV
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    current_section = None

    for row in reader:
        # Si la sección no está vacía, actualizar la sección actual
        if row['section']:
            current_section = row['section']
            data[current_section] = []

        # Añadir la pregunta y respuesta a la sección actual
        question_data = {
            'header': row['header'],
            'question': row['question'],
            'correct_answer': row['correct_answer'],
            'extra': row['extra'],
            'ans_type': row['ans_type']
        }
        
        if current_section:
            data[current_section].append(question_data)

# Escribir los datos en un archivo JSON
with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)

print(f'Datos convertidos y guardados en {json_file_path}')

