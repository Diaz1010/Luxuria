from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import time

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'src\key.json'


# Escribe aquí el ID de tu documento:
SPREADSHEET_ID = '1fYutUOchgXlJRyKdrq0WX2-Fy5ZdARzqDDmNtRLVPCs'

creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Llamada a la api
#result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Hoja 1!A1:A8').execute()
# Extraemos values del resultado
#values = result.get('values',[])
#print(values)
'''
def monitor_field(range_name):
    last_value = None
    while True:
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        values = result.get('values', [])

        if values:
            current_value = None
            for value in reversed(values):
                if value:  # Verifica si el valor no está vacío
                    current_value = value[0]
                    break

            if current_value and current_value != last_value:
                print(f"New value detected in {range_name}: {current_value}")
                last_value = current_value
        else:
            print(f"No value detected in {range_name}")

        time.sleep(10)  # Espera de 10 segundos antes de la próxima verificación

# Monitorea toda la columna 'A' (puedes cambiarlo al rango que desees monitorear)
monitor_field('Hoja 1!A:A')
'''

def monitor_fields(range_name_a, range_name_d):
    checked_rows = set()
    
    while True:
        # Obtener valores de las columnas A y D
        result_a = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name_a).execute()
        result_d = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name_d).execute()
        
        values_a = result_a.get('values', [])
        values_d = result_d.get('values', [])

        # Rellenar valores de D para que coincidan con el número de filas en A
        while len(values_d) < len(values_a):
            values_d.append([])

        new_values = []
        
        for i, (a_row, d_row) in enumerate(zip(values_a, values_d)):
            if i not in checked_rows and a_row and (not d_row or not d_row[0]):
                new_values.append(a_row[0])
                checked_rows.add(i)

        if new_values:
            print(f"New values in {range_name_a} without consecutives in {range_name_d}: {new_values}")

        time.sleep(5)  # Espera de 10 segundos antes de la próxima verificación

# Monitorea toda la columna 'A' y la columna 'D' (puedes cambiarlo al rango que desees monitorear)
monitor_fields('Hoja 1!A:A', 'Hoja 1!D:D')

