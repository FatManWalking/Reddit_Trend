import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import math

unpickled_df = pd.read_csv("pickled.csv", sep=";")



class Hallo():

    def __init__(self):
        #TODO: das hier vor dem pickeln machen
        df = unpickled_df[unpickled_df.subreddit != 'futbol'] #Delete Futbol (Italian, Spanish, Pizza, Pasta)
        df['created'] = pd.to_datetime(df['created'], unit='s') #Convert unix timestamp2Datetime

    def split(self):
        """splits dateframe in posts of the last 24h and before"""
        today = datetime.today() - timedelta(days=1)  #Immer die letzten 24h nehmen
        mask_today = (self.df['created'] > today) 
        
    def tf(self):
        pass
    def idf(self):
        pass
    def tf_idf_modify(self):
        pass
    
    def tokenizer(self):
        pass
    