import requests
import time

API_KEY = "b8ccf001-6129-48e8-b5a1-3e6ce6083af4"  # Reemplaza con tu API key real
BASE_URL = "https://api.userapi.ai/midjourney/v2"

def imagine(prompt):
    url = f"{BASE_URL}/imagine"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    data = {
        "prompt": prompt
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()["hash"]

def check_status(hash):
    url = f"{BASE_URL}/status"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    params = {
        "hash": hash
    }
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if data["status"] == "done":
            return data["result"]["url"]
        elif data["status"] == "failed":
            raise Exception("Image generation failed")
        
        time.sleep(5)  # Espera 5 segundos antes de verificar nuevamente

def generate_image(prompt):
    hash = imagine(prompt)
    image_url = check_status(hash)
    return image_url

# Uso del código
prompt = "/imagine Lobo Estepario, poster advertisement, Ornate"
try:
    image_url = generate_image(prompt)
    print(f"Imagen generada: {image_url}")
except Exception as e:
    print(f"Error: {str(e)}")