import tweepy
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import smtplib
import re

load_dotenv()

# Credentials twitch & twitter
twitter_consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
twitter_consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
twitter_access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
twitter_bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
twitch_username = os.environ.get('TWITCH_USERNAME')
twitch_client_id = os.environ.get('TWITCH_CLIENT_ID')
twitch_access_token = os.environ.get('TWITCH_ACCESS_TOKEN')
twitch_client_secret = os.environ.get('TWITCH_CLIENT_SECRET')

def get_remaining_time(twitch_client_id, twitch_client_secret):
    # Endpoint de validation du token
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
        # Conversion de la réponse en JSON
        data = json.loads(response.text)

        # Récupération du timestamp d'expiration du token
        expires_at = data["expires_in"]

        # Conversion du timestamp en objet de date et heure
        expires_at_datetime = datetime.now() + timedelta(seconds=expires_at)

        # Calcul de la durée restante avant l'expiration
        remaining_time = expires_at_datetime - datetime.now()

        print(f"Temps restant avant expiration : {remaining_time}")
        
        # Vérification si la durée restante est de 7 jours
        if remaining_time.days <= 7:
            send_email()
    elif response.status_code == 401:
        print("Le token Twitch n'est pas valide (401 Unauthorized).")
    else:
        print("Échec de la validation du token")

# Fonction pour envoyer un e-mail
def send_email():
    # Configuration du serveur SMTP et des informations d'authentification
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    # Informations de l'expéditeur et du destinataire
    sender_email = os.environ.get('SENDER_EMAIL')
    recipient_email = os.environ.get('RECIPIENT_EMAIL')

    # Ajouter le lien vers le référentiel GitHub
    repo_name = os.environ.get('REPO_NAME')
    github_secrets_url = f"https://github.com/{repo_name}/settings/secrets"

    # Création du message
    subject = '[APP Tweetlive] Token expiration notification'
    body = f"Your token will expire in less than 7 days. Please take necessary actions here: {github_secrets_url}."

    message = f'Subject: {subject}\n\n{body}'

    try:
        # Connexion au serveur SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Envoi de l'e-mail
        server.sendmail(sender_email, recipient_email, message)
        print('E-mail sent successfully')

    except Exception as e:
        print(f'Error sending e-mail: {str(e)}')

    finally:
        # Fermeture de la connexion au serveur SMTP
        server.quit()

def is_user_live(twitch_username, twitch_client_id):
    url = f"https://api.twitch.tv/helix/streams?user_login={twitch_username}"
    headers = {
        "Client-ID": twitch_client_id,
        "Authorization": f'Bearer {twitch_access_token}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    get_remaining_time(twitch_client_id, twitch_client_secret)
    game = data["data"][0]["game_name"].replace(" ", "")
    game = re.sub(r'[^\w\s]', '', game)

    if "data" in data and len(data["data"]) > 0:
        return True, game  # L'utilisateur est en direct sur tel jeu
    else:
        return False, None  # L'utilisateur n'est pas en direct
    
def send_tweet(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token, tweet_text):
    client = tweepy.Client( 
        twitter_bearer_token, 
        twitter_consumer_key, 
        twitter_consumer_secret, 
        twitter_access_token, 
        twitter_access_token_secret, 
        wait_on_rate_limit=True
        )
    # Envoi du tweet
    response = client.create_tweet(text=tweet_text)
    tweet_id = str(response.data['id'])

    with open("tweet-id.txt", "w") as file:
        file.write(tweet_id)

def check_user_live(twitch_username, twitch_client_id, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret):
    is_live, game = is_user_live(twitch_username, twitch_client_id)

    if is_live:
        tweet_text = f"Je suis en direct sur Twitch sur #{game} rejoins moi ! ⬇️ https://www.twitch.tv/{twitch_username}"
        send_tweet(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, tweet_text)
        print(f"L'utilisateur {twitch_username} est en direct sur Twitch à 21h10.")
        print(f"Tweet envoyé : {tweet_text}")
    else:
        print(f"L'utilisateur {twitch_username} n'est pas en direct sur Twitch à 21h10.")

check_user_live(twitch_username, twitch_client_id, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token)