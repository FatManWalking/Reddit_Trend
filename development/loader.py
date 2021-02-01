import pandas as pd 
unpickled_df = pd.read_pickle("daten/news.pkl")
print(unpickled_df.head(5))
print(set(unpickled_df.subreddit))

#df = unpickled_df[unpickled_df.subreddit != 'futbol']
