import pandas as pd
from datetime import datetime
from datetime import timedelta
from collections import Counter
import math

unpickled_df = pd.read_csv("pickled.csv", sep=";")
df = unpickled_df[unpickled_df.subreddit != 'futbol'] #Delete Futbol (Italian)
df['created'] = pd.to_datetime(df['created'],unit='s') #Convert unix timestamp2Datetime


#Split in last 24h and evrything before
today = datetime.today() - timedelta(days=1)  #Immer die letzten 24h nehmen
mask_today = (df['created'] > today) 
df_today = df.loc[mask_today]
print(len(df_today))
df_today.reset_index(inplace=True,drop=True)


mask_before = (df['created'] < today) 
df_before = df.loc[mask_before]
print(len(df_before))
df_before.reset_index(inplace=True,drop=True)

def tokenizer(series):
    series = series.str.lower()
    series = series.str.replace('\d+', '')
    series = series.str.replace('\W+', ' ')
    series = series.str.split(' ')
    return series
    
df['title'] = tokenizer(df['title'])

tf = []
all_tokens = []
for tokens in df['title']:
    dict_ = dict(Counter(tokens))
    len_dict = len(dict_)
    for key in list(dict_.keys()):
        all_tokens.append(key)
        dict_[key] = dict_[key]/len_dict
    tf.append(dict_)

all_tokens = set(all_tokens)


doc_freq = dict.fromkeys(all_tokens, 0)
#print(doc_freq)

for tokens in df['title']:
    for token in list(set(tokens)):
        doc_freq[token] += 1
for key in doc_freq.keys():
    doc_freq[key] = math.log10(len(df) / doc_freq[key]+1 ) #Smoothing +1
#print(doc_freq)

for key in doc_freq.keys():
    