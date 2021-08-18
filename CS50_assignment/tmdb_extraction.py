import config 
import requests 
import pandas as pd


api_key = config.TMDB_API # get TMDB API key from config.py file


def tmdbtable(quest):
    response = requests.get(' https://api.themoviedb.org/3/search/movie?api_key='+api_key+'&query='+quest)
    data = response.json() 
    df = pd.json_normalize(data['results'])

    return df
