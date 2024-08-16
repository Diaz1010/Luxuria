import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('manychat_all_users_data.csv')

# Crear una lista para almacenar los prompts
prompts = []

# Iterar sobre cada fila del DataFrame
for index, row in df.iterrows():
    pregunta1 = row['pregunta1']
    pregunta2 = row['pregunta2']
    estilo1 = row['estilo1']
    estilo2 = row['estilo2']
    
    # Generar los 4 prompts
    prompts.append(f"/imagine {pregunta1}, poster advertisement, {estilo1}")
    prompts.append(f"/imagine {pregunta1}, poster advertisement, {estilo2}")
    prompts.append(f"/imagine {pregunta2}, poster advertisement, {estilo1}")
    prompts.append(f"/imagine {pregunta2}, poster advertisement, {estilo2}")

# Guardar los prompts en un archivo de texto
with open('prompts.txt', 'w') as file:
    for prompt in prompts:
        file.write(prompt + '\n')