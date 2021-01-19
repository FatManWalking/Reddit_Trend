import pandas as pd 
unpickled_df = pd.read_pickle("Datenbasis.pkl")
print(unpickled_df.tail(5))