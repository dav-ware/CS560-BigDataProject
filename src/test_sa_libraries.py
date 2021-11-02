import pandas as pd 
import csv

with open('./tweet_sentiments_0.csv') as tweet_sentiments:
    df = pd.read_csv(tweet_sentiments)
    df.columns = ['target', 'id', 'date', 'flag', 'user', 'text']
    

print(df)

