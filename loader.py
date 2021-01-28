import pandas as pd 
unpickled_df = pd.read_pickle("daten/memes.pkl")
print(unpickled_df.head(5))

#df = unpickled_df[unpickled_df.subreddit != 'futbol']
