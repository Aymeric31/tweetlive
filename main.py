import tweepy
import requests
import os
import json
import smtplib
import re
import pytz
from datetime import datetime, timedelta
from dotenv import load_dotenv

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
    # Token validation endpoint
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
        # Convert the response to JSON
        data = json.loads(response.text)

        # Retrieve the token expiration timestamp
        expires_at = data["expires_in"]

        # Convert the expiration timestamp to a datetime object
        expires_at_datetime = datetime.now() + timedelta(seconds=expires_at)

        # Calculate the remaining duration before expiration
        remaining_time = expires_at_datetime - datetime.now()

        print(f"Temps restant avant expiration : {remaining_time}")
        
        # Check if the remaining duration is 7 days or less
        if remaining_time.days <= 7:
            send_email()

    elif response.status_code == 401:
        print("The Twitch token is not valid (401 Unauthorized).")

    else:
        print("Token validation failed")

# Function to send an email
def send_email():
    # SMTP server configuration and authentication information
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    # Sender and recipient information
    sender_email = os.environ.get('SENDER_EMAIL')
    recipient_email = os.environ.get('RECIPIENT_EMAIL')

    # Add link to GitHub secrets of the repository
    repo_name = os.environ.get('REPO_NAME')
    github_secrets_url = f"https://github.com/{repo_name}/settings/secrets"

    # Message creation
    subject = '[APP Tweetlive] Token expiration notification'
    body = f"Your token will expire in less than 7 days. Please take necessary actions here: {github_secrets_url}."

    message = f'Subject: {subject}\n\n{body}'

    try:
        # SMTP server connexion 
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message)
        print('E-mail sent successfully')

    except Exception as e:
        print(f'Error sending e-mail: {str(e)}')

    finally:
        # Close the connection to the SMTP server
        server.quit()

def format_started_at(started_at):
    # Convert the start date and time from ISO 8601 format to a datetime object
    started_at_datetime = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
    
    # Convert to French time (Europe/Paris)
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
    started_at = stream_data["started_at"]  # Date and time of the start of the stream in ISO 8601 format
    formatted_started_at = format_started_at(started_at)  # Format date and time of the start of the stream
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
    
    if "data" in data and len(data["data"]) > 0:
        stream_data = data["data"][0]
        print(stream_data)
        game_name_exact, game_name_tweet, formatted_started_at, thumbnail_url, title = format_stream_data(stream_data)
        return StreamInfo(True, game_name_exact, game_name_tweet, formatted_started_at, thumbnail_url, title)  # User is live
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
        "color": 9520895,  # Color of the message (you can change this value)
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
        # Set content for the message, emoji ID for the Twitch emoji
        content = f"@everyone {twitch_username} est en live sur Twitch <:Twitch:707494410778050620>!"
        data = {"content": content, "embeds": [embed_data]}
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(f"https://discord.com/api/webhooks/{discord_webhook}", data=json.dumps(data), headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print("Discord message sent successfully!")
        except requests.exceptions.RequestException as e:
            print(f"Error while sending the Discord message: {e}")


def send_tweet(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token, tweet_text):
    client = tweepy.Client( 
        twitter_bearer_token, 
        twitter_consumer_key, 
        twitter_consumer_secret, 
        twitter_access_token, 
        twitter_access_token_secret, 
        wait_on_rate_limit=True
        )
    
    try:
        # Send the tweet
        response = client.create_tweet(text=tweet_text)
        tweet_id = str(response.data['id'])

        # Save the tweet ID to a file
        with open("tweet-id.txt", "w") as file:
            file.write(tweet_id)

        print(f"Tweet sent successfully! Tweet ID: {tweet_id}")
    except tweepy.TweepyException as e:
        print(f"Error while sending the tweet: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while sending the tweet: {e}")

def check_user_live(twitch_username, twitch_client_id, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token):
    try:
        # Check if the user is live on Twitch
        twitch_live_info = get_twitch_live_info(twitch_username, twitch_client_id, twitch_access_token, twitch_client_secret)

        if twitch_live_info.is_live:

            tweet_text = f"Je suis en direct sur Twitch sur #{twitch_live_info.game_name_tweet} rejoins moi ! ⬇️ https://www.twitch.tv/{twitch_username}"
            
            # Send the tweet
            send_tweet(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token, tweet_text)

            # Send the message on Discord
            send_discord_message(discord_webhook, twitch_username, twitch_live_info)

            print(f"The user {twitch_username} has been live on Twitch since {twitch_live_info.formatted_started_at}.")
        else:
            print(f"The user {twitch_username} is not live on Twitch.")
    except Exception as e:
        print(f"Error while checking Twitch status: {e}")

check_user_live(twitch_username, twitch_client_id, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token)