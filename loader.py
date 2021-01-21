import pandas as pd 
unpickled_df = pd.read_pickle("daten/Politik.pkl")
print(unpickled_df.tail(5))

if "3b06gz" in list(unpickled_df["id"]):
    print("Ja")
else: print(unpickled_df["id"])
#df = unpickled_df[unpickled_df.subreddit != 'futbol']
