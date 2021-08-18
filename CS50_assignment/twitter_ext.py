import pandas as pd
import config
import tweepy


# Authenticate the API keys using tweepy package
auth = tweepy.OAuthHandler(config.API_KEY, config.API_KEY_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def tweettable(quest):
    tweets = tweepy.Cursor(api.search, q=quest, lang="en").items(100)
    tweets_df = pd.DataFrame()
    for tweet in tweets:
        df=pd.DataFrame()
        df=pd.json_normalize(tweet._json)
        tweets_df = pd.concat([df, tweets_df], sort=False)
    tweets_df.reset_index(inplace=True,drop=True)
    return tweets_df