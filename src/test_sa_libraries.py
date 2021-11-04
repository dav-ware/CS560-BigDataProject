import pandas as pd 
import csv
from nltk.corpus import twitter_samples, stopwords

with open('./tweet_sentiments_negative.csv') as tweet_sentiments:
    df_neg = pd.read_csv(tweet_sentiments)
    df_neg.columns = ['target', 'id', 'date', 'flag', 'user', 'text']
    
