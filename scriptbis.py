import tweepy
from tweepy import OAuth1UserHandler, API
import json
import schedule
import time
import requests

# client secret twitch: cijcymf5w35vo52sjguvnutyzn1dx1

# Charger les clés et jetons depuis le fichier de configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# Credentials twitch & twitter
consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']
access_token = config['access_token']
access_token_secret = config['access_token_secret']
bearer_token = config['bearer_token']
username = "Pepepizza31" 
client_id = "uwu8c9ejrdl3qsf7bdu95nfvegph85"  # Client ID Twitch

# Check les 20 derniers tweet contenant pizzamargherita du compte pepepizza
auth = OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = API(auth)
tweets = api.user_timeline(screen_name='pepepizza31', count=20, tweet_mode='extended')
KEYWORDS = "pizzamargherita"

# Basic keyword search
tweets = api.search_tweets(KEYWORDS)
print(tweets)
# class Client(tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)):
#     def on_status(self, status):
#         if "#pizzamargherita" in status.text:
#             print("Nouveau tweet avec #pizzamargherita :", status.text)

#     def on_error(self, status_code):
#         if status_code == 420:
#             print("Erreur 420 : Trop de demandes. Attente...")
#             return False

# def start_stream():
#     auth = tweepy.OAuthHandler(
#         consumer_key, consumer_secret, access_token, access_token_secret
#     )
#     api = tweepy.API(auth)
#     streaming_client = tweepy.StreamingClient(bearer_token)
#     streaming_client.sample(auth=auth)
#     while True:
#         try:
#             print("Démarrage de la surveillance en temps réel...")
#             streaming_client.filter(track=["#pizzamargherita"], is_async=False)
#         except Exception as e:
#             print("Erreur :", str(e))
#             print("Redémarrage de la surveillance en temps réel...")

# start_stream()

# class TweetPrinterV2(tweepy.StreamingClient):
    
#     def on_tweet(self, tweet):
#         print(f"{tweet.id} {tweet.created_at} ({tweet.author_id}): {tweet.text}")
#         print("-"*50)
 
# printer = TweetPrinterV2(bearer_token)
 
# add new rules    
# printer.add_rules(tweepy.StreamRule(value = "pizzamargherita"))

# printer.filter()

# printer.get_recent_tweets_count()

# user = api.get_user(screen_name="Pepepizza31")
