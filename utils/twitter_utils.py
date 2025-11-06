import tweepy

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
        with open("./tweet-id.txt", "w") as file:
            file.write(tweet_id)
        SystemExit

        print(f"Tweet sent successfully! Tweet ID: {tweet_id}")
    except tweepy.TweepyException as e:
        print(f"Error while sending the tweet: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while sending the tweet: {e}")