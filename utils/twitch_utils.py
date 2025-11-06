import requests
import re
import pytz
from datetime import datetime

class StreamInfo:
    def __init__(self, is_live, game_name_exact=None, game_name_tweet=None, formatted_started_at=None, thumbnail_url=None, title=None):
        self.is_live = is_live
        self.game_name_exact = game_name_exact
        self.game_name_tweet = game_name_tweet
        self.formatted_started_at = formatted_started_at
        self.thumbnail_url = thumbnail_url
        self.title = title

def format_started_at(started_at):
    # Convert the start date and time from ISO 8601 format to a datetime object
    started_at_datetime = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
    
    # Convert to French time (Europe/Paris)
    timezone_france = pytz.timezone('Europe/Paris')
    started_at_france = started_at_datetime.astimezone(timezone_france)

    formatted_started_at = started_at_france.strftime("Aujourd'hui à %Hh%M")
    return formatted_started_at

def format_stream_data(stream_data):
    game_name_exact = stream_data["game_name"]
    game_name_tweet = game_name_exact.replace(" ", "")
    game_name_tweet = re.sub(r'[^\w\s]', '', game_name_tweet)
    started_at = stream_data["started_at"]  # Date and time of the start of the stream in ISO 8601 format
    formatted_started_at = format_started_at(started_at)  # Format date and time of the start of the stream
    thumbnail_url = stream_data["thumbnail_url"].replace("{width}", "1280").replace("{height}", "720")
    title = stream_data["title"]
    return game_name_exact, game_name_tweet, formatted_started_at, thumbnail_url, title     

def get_twitch_live_info(twitch_username, twitch_client_id, twitch_access_token):
    url = f"https://api.twitch.tv/helix/streams?user_login={twitch_username}"
    headers = {
        "Client-ID": twitch_client_id,
        "Authorization": f'Bearer {twitch_access_token}'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    
    if "data" in data and len(data["data"]) > 0:
        stream_data = data["data"][0]
        game_name_exact, game_name_tweet, formatted_started_at, thumbnail_url, title = format_stream_data(stream_data)
        return StreamInfo(True, game_name_exact, game_name_tweet, formatted_started_at, thumbnail_url, title)  # User is live
    else:
        return StreamInfo(False)
