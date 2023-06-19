import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

# Credentials twitch & twitter
twitter_bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
twitter_consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
twitter_consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
twitter_access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

def delete_tweet(tweet_id):
    # Utiliser l'API Twitter pour supprimer le tweet
    client = tweepy.Client( 
        twitter_bearer_token, 
        twitter_consumer_key, 
        twitter_consumer_secret, 
        twitter_access_token, 
        twitter_access_token_secret, 
        wait_on_rate_limit=True
        )
    client.delete_tweet(tweet_id)

# Lire l'ID du tweet à partir du fichier texte
with open('tweet-id.txt', 'r') as file:
    tweet_id = file.read().strip()

# Supprimer le tweet en utilisant l'ID du tweet
delete_tweet(tweet_id)