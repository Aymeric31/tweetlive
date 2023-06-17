import requests
import os
from dotenv import load_dotenv

load_dotenv()

twitch_client_id = os.environ.get('TWITCH_CLIENT_ID')
twitch_client_secret = os.environ.get('TWITCH_CLIENT_SECRET')

def generate_token():
    endpoint = "https://id.twitch.tv/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": twitch_client_id,
        "client_secret": twitch_client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(endpoint, headers=headers, data=data)

    if response.status_code == 200:
        data = response.json()
        access_token = data['access_token']
        print("Nouveau bearer token généré avec succès. Voici le nouveau token: " + access_token)
    else:
        print("Échec de la génération du bearer token.")

generate_token()