import locale # to format currency as USD
locale.setlocale( locale.LC_ALL, '' )
import json
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter # to format currency on charts axis
from pandas.io.json import json_normalize
import config
import tweepy


api_key = config.api_key
api_key_secret = config.api_key_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def tweettable(quest):

    tweets = tweepy.Cursor(api.search, q=quest, lang="en").items(100)
    dfs = pd.DataFrame()
    for tweet in tweets:
        file=tweet._json
        df=pd.DataFrame()
        df=json_normalize(file)
        dfs = pd.concat([df, dfs], sort=False)
    dfs.reset_index(inplace=True,drop=True)
    return dfs