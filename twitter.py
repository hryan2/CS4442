import tweepy
import re

API_KEY = ''
API_KEY_SECRET = ''
BEARER_TOKEN = ''
ACCESS_TOKEN =  ''
ACCESS_TOKEN_SECRET = ''

class TwitterV2():
    def __init__(self):
        credentials = open("credentials.txt", 'r')
        lines = credentials.readlines()
        API_KEY = lines[0].strip("\n")
        API_KEY_SECRET = lines[1].strip("\n")
        BEARER_TOKEN = lines[2].strip("\n")
        ACCESS_TOKEN = lines[3].strip("\n")
        ACCESS_TOKEN_SECRET = lines[4].strip("\n")
        self.client = tweepy.Client(consumer_key = API_KEY, consumer_secret=API_KEY_SECRET, bearer_token=BEARER_TOKEN, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

    def get_account(self, id):
        try:
            user = self.client.get_user(id=id, user_fields=['public_metrics', 'verified', 'favourites_count', 'created_at', "description", "location", "profile_image_url"])
            return user
        except Exception as e:
            return None

    def get_tweets(self, id):
        results = []
        tweets = self.client.get_users_tweets(id=id, exclude='retweets', max_results=10,tweet_fields=['context_annotations'], user_auth=True)
        if tweets is None or tweets.data is None:
            return None

        for tweet in tweets.data:
            tweet_text = str(tweet)
            result = re.sub(r'http\S+', '', tweet_text)
            results.append(result)
        return results

    def get__tweet_from_id(self, id):
        tweet = self.client.get_tweet(id=id, tweet_fields=['context_annotations'])
        return tweet.data


    def get_retweets(self, id):
        results = []
        tweets = self.client.get_users_tweets(id=id, max_results=10, tweet_fields=['context_annotations'], user_auth=True)
        if tweets is None:
            return None

        for tweet in tweets.data:
            tweet_text = str(tweet)
            result = re.sub(r'http\S+', '', tweet_text)
            if 'RT @' in result:
                results.append(result)
        return results

    def get_id_from_username(self, username):
        user = self.client.get_user(username=username, user_auth=True)
        if user is None:
            return None
        return user.data.id

class TwitterV1():
    def __init__(self):
        credentials = open("credentials.txt", 'r')
        lines = credentials.readlines()
        API_KEY = lines[0].strip("\n")
        API_KEY_SECRET = lines[1].strip("\n")
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        self.api = tweepy.API(auth=auth, wait_on_rate_limit=True)

    def get_account(self, id):
        try:
            user = self.api.get_user(user_id=id)
            return user
        except Exception as e:
            return None