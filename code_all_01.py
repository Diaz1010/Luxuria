import requests
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import json
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import time

# Configuración de Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'src\key.json'
SPREADSHEET_ID = '1fYutUOchgXlJRyKdrq0WX2-Fy5ZdARzqDDmNtRLVPCs'

creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Configuración de ManyChat
MANYCHAT_API_BASE_URL = 'https://api.manychat.com/fb/subscriber/getInfo'
MANYCHAT_API_TOKEN = '789813:e2fc3b624197aa859357b65219100151'

# Variables Generales

df = pd.read_csv('manychat_all_users_data.csv')


#####################################################################################################


def get_data_from_manychats(subscriber_id):
    url = f"{MANYCHAT_API_BASE_URL}?subscriber_id={subscriber_id}"
    headers = {
        'Authorization': f'Bearer {MANYCHAT_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al obtener datos de ManyChat: {response.status_code}")

def process_custom_fields(custom_fields):
    return {field['name']: field['value'] for field in custom_fields}

def process_manychat_data(data):
    if data['status'] == 'success' and 'data' in data:
        user_data = data['data']
        custom_fields = process_custom_fields(user_data.pop('custom_fields', []))
        
        df_main = pd.DataFrame([user_data])
        df_custom = pd.DataFrame([custom_fields])
        df_combined = pd.concat([df_main, df_custom], axis=1)
        
        return df_combined
    else:
        print("No se encontraron datos válidos en la respuesta.")
        return None

def monitor_and_process(range_name_a, range_name_d):
    checked_rows = set()
    all_data = pd.DataFrame()
    
    while True:
        result_a = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name_a).execute()
        result_d = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name_d).execute()
        
        values_a = result_a.get('values', [])
        values_d = result_d.get('values', [])

        while len(values_d) < len(values_a):
            values_d.append([])

        for i, (a_row, d_row) in enumerate(zip(values_a, values_d)):
            if i not in checked_rows and a_row and (not d_row or not d_row[0]):
                subscriber_id = a_row[0]
                print(f"Procesando nuevo ID: {subscriber_id}")
                
                try:
                    manychat_data = get_data_from_manychats(subscriber_id)
                    df = process_manychat_data(manychat_data)
                    if df is not None:
                        all_data = pd.concat([all_data, df], ignore_index=True)
                        print(f"Datos procesados para ID: {subscriber_id}")
                        
                        # Actualizar la columna D en Google Sheets
                        sheet.values().update(
                            spreadsheetId=SPREADSHEET_ID,
                            range=f'Hoja 1!D{i+1}',
                            valueInputOption='USER_ENTERED',
                            body={'values': [['Procesado']]}
                        ).execute()
                    
                except Exception as e:
                    print(f"Error al procesar ID {subscriber_id}: {e}")
                
                checked_rows.add(i)

        if not all_data.empty:
            all_data.to_csv('manychat_all_users_data.csv', index=False)
            print("Datos guardados en 'manychat_all_users_data.csv'")

        time.sleep(5)  # Espera de 1 minuto antes de la próxima verificación

if __name__ == "__main__":
    monitor_and_process('Hoja 1!A:A', 'Hoja 1!D:D')