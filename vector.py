import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import math

unpickled_df = pd.read_csv("pickled.csv", sep=";")
#TODO: das hier vor dem pickeln machen
df = unpickled_df[unpickled_df.subreddit != 'futbol'] #Delete Futbol (Italian, Spanish, Pizza, Pasta)
df['created'] = pd.to_datetime(df['created'], unit='s') #Convert unix timestamp2Datetime


class Vektor():

    def __init__(self,df):
        self.df = df
        self.df_today, self.df_before = self.split()

    def split(self):
        """
        splits dateframe in posts of the last 24h and before
        returns: 2 Dataframes (today, before)
        """
        today = datetime.today() - timedelta(days=1)  #Immer die letzten 24h nehmen
        mask_today = (self.df['created'] > today)
        df_today = self.df.loc[mask_today]
        #len_today = len(df_today)
        df_today.reset_index(inplace=True,drop=True)

        mask_before = (df['created'] < today) 
        df_before = df.loc[mask_before]
        #print(len(df_before))
        df_before.reset_index(inplace=True,drop=True)

        return df_today, df_before

    def tokenizer(self, df):
        """
        splits the title of all posts in tokens
        return: dataframe series
        """
        series = df['title']
        series = series.str.lower()
        series = series.str.replace('\d+', '')
        series = series.str.replace('\W+', ' ')
        series = series.str.split(' ')

        return series

    def tf(self, df):
        """
        calcs all tf frequencies and builds a general word vector
        return: term frequencies(list of dicts), all tokens(set of keys)
        """
        tf = []
        all_tokens = []

        for tokens in df['title']:
            dict_ = dict(Counter(tokens))
            tf.append({key:value for key,value/len(dict_) in dict_.items()})
            all_tokens.extend(dict_.keys())

        return tf, set(all_tokens)

    def idf(self, df, all_tokens):
        """
        inverse document frequence, smoothed and with log10
        return: doc_freq(dict)
        """
        doc_freq = dict()
        for tokens in df['title']:
            for token in list(set(tokens)):
                doc_freq[token] = doc_freq.get(token, 0) + 1

        doc_freq = {key:value for key, math.log10(len(df) / value+1 in doc_freq.items()}
        
        return doc_freq

    def tf_idf_modify(self):
        pass
    

    
    
test = Vektor(df)

# Hier dann zwischen dem before und now df unterscheiden
# test.df durch test.df_before und test.df_today ersetzen
test.df['title'] = test.tokenizer(test.df)

tf, all_tokens = test.tf(test.df)
idf = idf(test.df, all_tokens)
print(idf)
