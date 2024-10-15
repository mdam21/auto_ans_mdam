import pandas as pd
import json

# Cargar el archivo CSV con la codificación adecuada
file_path = 'Book_completo_11_julio.csv'
try:
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')

# Llenar las secciones vacías
df['seccion'] = df['seccion'].ffill()

# Convertir a una estructura de diccionario
json_structure = {}
for _, row in df.iterrows():
    seccion = row['seccion']
    if seccion not in json_structure:
        json_structure[seccion] = []

    question_data = {
        'header': row['header'],
        'question': row['question'],
        'correct_answer': row['correct_answer'],
        'ans_type': row['ans_type'],
        'extra': row['extra'] if pd.notna(row['extra']) else ""
    }
    json_structure[seccion].append(question_data)

# Guardar como archivo JSON
output_file = 'output.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(json_structure, json_file, ensure_ascii=False, indent=4)

print(f"Archivo JSON guardado como {output_file}")

