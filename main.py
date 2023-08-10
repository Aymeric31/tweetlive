import tweepy
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import smtplib
import re
import pytz

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

discord_webhook = os.environ.get('DISCORD_WEBHOOK')

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
    print(response)
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

def format_started_at(started_at):
    # Convertir la date et l'heure de début au format ISO 8601 en objet datetime
    started_at_datetime = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
    
    # Convertir en heure française (Europe/Paris)
    timezone_france = pytz.timezone('Europe/Paris')
    started_at_france = started_at_datetime.astimezone(timezone_france)

    formatted_started_at = started_at_france.strftime("Aujourd'hui à %Hh%M")
    return formatted_started_at

class StreamInfo:
    def __init__(self, is_live, game_name_exact=None, game_name_tweet=None, formatted_started_at=None, thumbnail_url=None, title=None):
        self.is_live = is_live
        self.game_name_exact = game_name_exact
        self.game_name_tweet = game_name_tweet
        self.formatted_started_at = formatted_started_at
        self.thumbnail_url = thumbnail_url
        self.title = title

def format_stream_data(stream_data):
    game_name_exact = stream_data["game_name"]
    game_name_tweet = game_name_exact.replace(" ", "")
    game_name_tweet = re.sub(r'[^\w\s]', '', game_name_tweet)
    started_at = stream_data["started_at"]  # Date et heure de début du stream au format ISO 8601
    formatted_started_at = format_started_at(started_at)  # Formatter la date et l'heure de début
    thumbnail_url = stream_data["thumbnail_url"].replace("{width}", "1280").replace("{height}", "720")
    title = stream_data["title"]
    return game_name_exact, game_name_tweet, formatted_started_at, thumbnail_url, title      

def get_twitch_live_info(twitch_username, twitch_client_id, twitch_access_token, twitch_client_secret):
    url = f"https://api.twitch.tv/helix/streams?user_login={twitch_username}"
    headers = {
        "Client-ID": twitch_client_id,
        "Authorization": f'Bearer {twitch_access_token}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    get_remaining_time(twitch_client_id, twitch_client_secret)
    print(data)
    if "data" in data and len(data["data"]) > 0:
        stream_data = data["data"][0]
        print(stream_data)
        game_name_exact, game_name_tweet, formatted_started_at, thumbnail_url, title = format_stream_data(stream_data)
        return StreamInfo(True, game_name_exact, game_name_tweet, formatted_started_at, thumbnail_url, title)  # L'utilisateur est en direct
    else:
        return StreamInfo(False)

def construct_embed_data(twitch_username, twitch_live_info):
    game_name = twitch_live_info.game_name_exact
    formatted_started_at = twitch_live_info.formatted_started_at
    thumbnail_url = twitch_live_info.thumbnail_url
    title = twitch_live_info.title

    embed_data = {
        "title": title,
        "url": f"https://www.twitch.tv/{twitch_username}",
        "color": 9520895,  # Couleur du message (vous pouvez changer cette valeur)
        "image": {
            "url": thumbnail_url,
        },
        "author": {
            "name": f"{twitch_username} est en direct 🍕"
        },
        "fields": [
            {
                "name": ":joystick: Jeu", 
                "value": game_name,
                "inline": True
            },
            {
                "name": ":red_circle: Début du stream",
                "value": formatted_started_at,
                "inline": True
            }
        ]
    }

    return embed_data

def send_discord_message(discord_webhook, twitch_username, twitch_live_info):
    if twitch_live_info:
        embed_data = construct_embed_data(twitch_username, twitch_live_info)
        content = f"@everyone {twitch_username} est en live sur Twitch <:Twitch:707494410778050620>!"
        data = {"content": content, "embeds": [embed_data]}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"https://discord.com/api/webhooks/{discord_webhook}", data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            print("Message Discord envoyé avec succès !")
        else:
            print(f"Échec lors de l'envoi du message Discord : {response.status_code}")


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

def check_user_live(twitch_username, twitch_client_id, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token):
    twitch_live_info = get_twitch_live_info(twitch_username, twitch_client_id, twitch_access_token, twitch_client_secret)

    if twitch_live_info.is_live:
        tweet_text = f"Je suis en direct sur Twitch sur #{twitch_live_info.game_name_tweet} rejoins moi ! ⬇️ https://www.twitch.tv/{twitch_username}"
        send_tweet(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token, tweet_text)
        # Appel de la fonction pour envoyer l'embed Discord
        send_discord_message(discord_webhook, twitch_username, twitch_live_info)
        print(f"L'utilisateur {twitch_username} est en direct sur Twitch à {twitch_live_info.formatted_started_at}.")
        print(f"Tweet envoyé : {tweet_text}")
    else:
        print(f"L'utilisateur {twitch_username} n'est pas en direct sur Twitch.")

check_user_live(twitch_username, twitch_client_id, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token)