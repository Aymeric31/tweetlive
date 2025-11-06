import requests
from datetime import timedelta

def check_access_token_validity(twitch_access_token):
   url = "https://id.twitch.tv/oauth2/validate"
   headers = {
      "Authorization": f"OAuth {twitch_access_token}"
   }

   response = requests.get(url, headers=headers)

   if response.status_code == 200:
      data = response.json()
      return data
   elif response.status_code == 401:
      print("The Twitch token is not valid (401 Unauthorized).")
      return None
   else:
      print(f"⚠️ Erreur inattendue : {response.status_code}")
      return None

def format_duration(seconds):
    duration = timedelta(seconds=seconds)
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} jours, {hours} heures, {minutes} minutes et {seconds} secondes"

