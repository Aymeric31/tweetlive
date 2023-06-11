import tweepy
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Credentials twitch & twitter
twitter_consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
twitter_consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
twitter_access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
twitch_username = os.environ.get('TWITCH_USERNAME')
twitch_client_id = os.environ.get('TWITCH_CLIENT_ID')
twitch_access_token = os.environ.get('TWITCH_ACCESS_TOKEN')

def is_user_live(twitch_username, twitch_client_id):
    url = f"https://api.twitch.tv/helix/streams?user_login={twitch_username}"
    headers = {
        "Client-ID": twitch_client_id,
        "Authorization": f'Bearer {twitch_access_token}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if "data" in data and len(data["data"]) > 0:
        return True, data["data"][0]["game_name"]  # L'utilisateur est en direct sur tel jeu
    else:
        return False, None  # L'utilisateur n'est pas en direct
    
def send_tweet(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, tweet_text):
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)

    api = tweepy.API(auth)
    api.update_status(tweet_text)

def check_user_live(twitch_username, twitch_client_id, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret):
    is_live, game = is_user_live(twitch_username, twitch_client_id)

    if is_live:
        tweet_text = f"Je suis en direct sur Twitch sur {game} rejoins moi ! https://www.twitch.tv/{twitch_username}"
        send_tweet(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, tweet_text)
        print(f"L'utilisateur {twitch_username} est en direct sur Twitch à 21h15.")
        print(f"Tweet envoyé : {tweet_text}")
    else:
        print(f"L'utilisateur {twitch_username} n'est pas en direct sur Twitch à 21h15.")

check_user_live(twitch_username, twitch_client_id, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret)

