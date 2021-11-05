import pandas as pd 
import csv
import sa_util as util
from textblob import TextBlob
from nltk.corpus import twitter_samples

with open('./tweet_sentiments_negative.csv', encoding = "ISO-8859-1") as tweet_sentiments:
    df_neg = pd.read_csv(tweet_sentiments)
    df_neg.columns = ['target', 'id', 'date', 'flag', 'user', 'text']

with open('./tweet_sentiments_positive.csv', encoding = "ISO-8859-1") as tweet_sentiments:
    df_pos = pd.read_csv(tweet_sentiments)
    df_pos.columns = ['target', 'id', 'date', 'flag', 'user', 'text']

#positive_tweets = df_pos['text'].to_list()
negative_tweets = df_neg['text'].to_list()
positive_tweets = twitter_samples.strings('positive_tweets.json')
res=[]
for i in range(1000):
    p = TextBlob(positive_tweets[i])
    
print(res)

