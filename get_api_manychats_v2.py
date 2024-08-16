import requests

# Configura los detalles de la API de ManyChat
MANYCHAT_API_URL = 'https://manychat.com/fb/subscriber/getinfo'
MANYCHAT_API_TOKEN = '789813:e2fc3b624197aa859357b65219100151'

# Función para obtener la información de un suscriptor de ManyChat
def get_subscriber_info(subscriber_id):
    headers = {
        'Authorization': f'Bearer {MANYCHAT_API_TOKEN}',
        'Content-Type': 'application/json'
    }

    params = {
        'subscriber_id': subscriber_id
    }

    response = requests.get(MANYCHAT_API_URL, headers=headers, params=params)
    
    print(f"Código de estado: {response.status_code}")
    print(f"Headers de respuesta: {response.headers}")
    print(f"Contenido de la respuesta: {response.text}")
    
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError as e:
            print(f"Error al parsear JSON: {str(e)}")
            raise Exception("Error al parsear JSON de la respuesta")
    else:
        raise Exception(f"Error al obtener datos de ManyChat: {response.status_code} - {response.text}")

def main():
    try:
        # Aquí debes ingresar el subscriber_id que deseas consultar
        subscriber_id = '28673596'
        
        # Obtener la información del suscriptor de ManyChat
        subscriber_info = get_subscriber_info(subscriber_id)
        print("Información del suscriptor de ManyChat:", subscriber_info)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()