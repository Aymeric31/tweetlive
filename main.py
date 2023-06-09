import tweepy
# from tweepy import OAuth1UserHandler, API
import json
import requests
import os

# Charger les clés et jetons depuis le fichier de configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# Credentials twitch & twitter
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
username = os.environ.get('TWITCH_USERNAME')
client_id = os.environ.get('TWITCH_CLIENT_ID')
twitch_bearer = os.environ.get('TWITTER_CONSUMER_SECRET')

def is_user_live(username, client_id):
    url = f"https://api.twitch.tv/helix/streams?user_login={username}"
    headers = {
        "Client-ID": client_id,
        "Authorization": f'Bearer {twitch_bearer}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    if "data" in data and len(data["data"]) > 0:
        return True, data["data"][0]["game_name"]  # L'utilisateur est en direct
    else:
        return False, None  # L'utilisateur n'est pas en direct
    
def send_tweet(consumer_key, consumer_secret, access_token, access_token_secret, tweet_text):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    api.update_status(tweet_text)

def check_user_live(username, client_id, consumer_key, consumer_secret, access_token, access_token_secret):
    is_live, game = is_user_live(username, client_id)

    if is_live:
        tweet_text = f"Je suis en direct sur Twitch sur {game} rejoins moi ! https://www.twitch.tv/pepepizza31"
        send_tweet(consumer_key, consumer_secret, access_token, access_token_secret, tweet_text)
        print(f"L'utilisateur {username} est en direct sur Twitch à 21h15.")
        print(f"Tweet envoyé : {tweet_text}")
    else:
        tweet_text = f"L'utilisateur {username} n'est pas en direct sur Twitch à 21h15. https://www.twitch.tv/pepepizza31"
        print(f"L'utilisateur {username} n'est pas en direct sur Twitch à 21h15.")

# Sans le schedule
check_user_live(username, client_id, consumer_key, consumer_secret, access_token, access_token_secret)

