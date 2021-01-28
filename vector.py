import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import math
import json

unpickled_df = pd.read_pickle("DatenbasisSportsNew.pkl")
#unpickled_df = pd.read_csv("daten/DatenbasisSportsNew.csv", sep=";")
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
            tf.append({key:value/len(dict_) for key, value in dict_.items()})
            all_tokens.extend(dict_.keys())

        return tf, set(all_tokens), all_tokens

    def idf(self, df, all_tokens):
        """
        inverse document frequence, smoothed and with log10
        return: doc_freq(dict)
        """
        doc_freq = dict()
        for tokens in df['title']:
            for token in list(set(tokens)):
                doc_freq[token] = doc_freq.get(token, 0) + 1

        doc_freq = {key:math.log10(len(df) / value+1) for key, value  in doc_freq.items()}
        
        return doc_freq

    def tf_idf_modify(self):
        pass
    

    
    
test = Vektor(df)

# Hier dann zwischen dem before und now df unterscheiden
# test.df durch test.df_before und test.df_today ersetzen


test.df_before['title'] = test.tokenizer(test.df_before)
test.df_today['title'] = test.tokenizer(test.df_today)

counter = 0
today = {}
before = {}
for i in [test.df_before, test.df_today]:

    tf, set_all_tokens, all_tokens = test.tf(i)
    idf = test.idf(i, set_all_tokens)
    #print(idf)

    oa_tf = dict(Counter(all_tokens))
    #oa_tf * idf

    final = dict()
    for key in idf.keys():
        final[key] = math.log10((oa_tf[key]/len(i)) * idf[key])

    final = {k: v for k, v in sorted(final.items(), key=lambda item: item[1],reverse = False)}

    if not counter:
        before = final
    else:
        today = final
    counter += 1

#print(today)


final_final = dict()
for key in today.keys():
    final_final[key] = today[key] / before.get(key, 0.1)
final_final = {k: v for k, v in sorted(final_final.items(), key=lambda item: item[1],reverse = True)}
print(final_final)
    #doc_freq[token] = doc_freq.get(token, 0) + 1
