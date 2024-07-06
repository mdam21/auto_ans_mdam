import csv
import json

csv_file = 'input.csv'
json_file = 'output3.json'

def clean_cell(cell):
    """Elimina las comillas simples y espacios innecesarios de una celda."""
    return cell.strip().strip("'")

# Lee el archivo CSV de entrada en modo binario y elimina caracteres NUL
with open(csv_file, 'rb') as infile:
    content = infile.read().replace(b'\x00', b'').decode('ISO-8859-1')

# Procesa el contenido como líneas de texto
lines = content.splitlines()

# Prepara el lector de CSV
reader = csv.reader(lines, delimiter=';')

# Estructura de datos para el JSON
output_data = []
current_tema = None
current_items = []
question_number = 1

for row in reader:
    # Filtrar filas vacías o con valores vacíos
    if not any(row):
        continue

    if row[0]:  # Si hay un valor en la primera columna, es un nuevo tema
        if current_tema:  # Guarda el tema anterior en el output_data
            output_data.append({
                'Tema': current_tema,
                'Items': current_items
            })
        current_tema = clean_cell(row[0])
        current_items = []
        question_number = 1
    elif row[1]:  # Si hay un valor en la segunda columna, es un parámetro del tema actual
        param = clean_cell(row[1])
        result = clean_cell(row[2])
        try:
            result_int = int(result)
            current_items.append({
                f'Pregunta{question_number}': param,
                f'Resultado{question_number}': result_int
            })
        except ValueError:
            current_items.append({
                f'Pregunta{question_number}': param,
                f'Resultado{question_number}': result
            })
        question_number += 1

# Agrega el último tema al output_data
if current_tema:
    output_data.append({
        'Tema': current_tema,
        'Items': current_items
    })

# Escribe los datos en un archivo JSON
with open(json_file, 'w', encoding='UTF-8') as outfile:
    json.dump(output_data, outfile, indent=4, ensure_ascii=False)

print(f"Datos transformados y guardados como '{json_file}'")

