#!/usr/bin/env python
# coding: utf-8

# In[16]:


import config # to hide TMDB API keys
import requests # to make TMDB API calls
import locale # to format currency as USD
locale.setlocale( locale.LC_ALL, '' )
import json

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter # to format currency on charts axis

api_key = config.tmdb_api # get TMDB API key from config.py file




def tmdbtable(quest):
    response = requests.get(' https://api.themoviedb.org/3/search/movie?api_key='+api_key+'&query='+quest)
    from pandas.io.json import json_normalize
    highest_revenue = response.json() 
    df = json_normalize(highest_revenue['results'])
    #print(df)
    # del df['genre_ids']
    return df
    


