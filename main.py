import os
from datetime import timedelta
from dotenv import load_dotenv
from utils.check_access_token import check_access_token_validity, format_duration
from utils.send_mail import send_email
from utils.twitch_utils import get_twitch_live_info
from utils.twitter_utils import send_tweet
from utils.discord_utils import send_discord_message

load_dotenv()

# Credentials twitter
twitter_consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
twitter_consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
twitter_access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
twitter_bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')

# Credentials twitch
twitch_username = os.environ.get('TWITCH_USERNAME')
twitch_client_id = os.environ.get('TWITCH_CLIENT_ID')
twitch_access_token = os.environ.get('TWITCH_ACCESS_TOKEN')

discord_webhook = os.environ.get('DISCORD_WEBHOOK')

def check_user_live(twitch_username, twitch_client_id, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token):
    try:
        # Check if the user is live on Twitch
        twitch_live_info = get_twitch_live_info(twitch_username, twitch_client_id, twitch_access_token)

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

def main():
    token_data = check_access_token_validity(twitch_access_token)

    if token_data:
        expires_in = token_data['expires_in']
        remaining_time = timedelta(seconds=expires_in)
        print("Valid token ✅")
        print(f"Expire in : {format_duration(expires_in)}")
        check_user_live(twitch_username, twitch_client_id, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret, twitter_bearer_token)

        if remaining_time.days <= 7:
            print(f"Expire in : {format_duration(expires_in)}")
            send_email()

    else:
        print("Invalid Token ❌")

if __name__ == "__main__":
    main()