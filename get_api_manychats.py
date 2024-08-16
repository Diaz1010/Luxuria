import requests
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import json
import pandas as pd

# Configura Firebase
#cred = credentials.Certificate('ruta/al/archivo/clave-firebase.json')
#firebase_admin.initialize_app(cred)
#db = firestore.client()

# Configura los detalles de la API de ManyChat
MANYCHAT_API_URL = 'https://api.manychat.com/fb/subscriber/getInfo?subscriber_id=28673596'
MANYCHAT_API_TOKEN = '789813:e2fc3b624197aa859357b65219100151'

# Función para obtener datos de ManyChat
def get_data_from_manychats():
    headers = {
        'Authorization': f'Bearer {MANYCHAT_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    params = {
    'last_seen_after': start_date,
    'last_seen_before': end_date
}

    response = requests.get(MANYCHAT_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        print(response)
        return response.json()
    else:
        raise Exception(f"Error al obtener datos de ManyChat: {response.status_code}")



# Define los parámetros de la consulta

'''
# Función para enviar datos a Firebase
def send_data_to_firebase(data):
    doc_ref = db.collection('manychat_data').document()
    doc_ref.set(data)
    '''
def process_custom_fields(custom_fields):
    return {field['name']: field['value'] for field in custom_fields}
def main():
    try:
        data = get_data_from_manychats()
        
        print("Datos recibidos de ManyChat:")
        print(json.dumps(data, indent=2))
        
        if data['status'] == 'success' and 'data' in data:
            user_data = data['data']
            
            # Procesar campos personalizados
            custom_fields = process_custom_fields(user_data.pop('custom_fields', []))
            
            # Crear DataFrame principal
            df_main = pd.DataFrame([user_data])
            
            # Crear DataFrame de campos personalizados
            df_custom = pd.DataFrame([custom_fields])
            
            # Combinar los DataFrames
            df_combined = pd.concat([df_main, df_custom], axis=1)
            
            print("\nDataFrame combinado:")
            print(df_combined)
            
            print("\nInformación del DataFrame:")
            print(df_combined.info())
            
            # Opcional: guardar en CSV
            df_combined.to_csv('manychat_user_data.csv', index=False)
            print("\nDatos guardados en 'manychat_user_data.csv'")
        else:
            print("No se encontraron datos válidos en la respuesta.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()