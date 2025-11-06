import requests
import json

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