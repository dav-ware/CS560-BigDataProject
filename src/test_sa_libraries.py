import pandas as pd 
import csv
from nltk.corpus import twitter_samples, stopwords
from nltk.tokenize import TweetTokenizer

with open('./tweet_sentiments_negative.csv', encoding = "ISO-8859-1") as tweet_sentiments:
    df_neg = pd.read_csv(tweet_sentiments)
    df_neg.columns = ['target', 'id', 'date', 'flag', 'user', 'text']

with open('./tweet_sentiments_positive.csv', encoding = "ISO-8859-1") as tweet_sentiments:
    df_pos = pd.read_csv(tweet_sentiments)
    df_pos.columns = ['target', 'id', 'date', 'flag', 'user', 'text']

positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
positive_tweets = twitter_samples.strings('positive_tweets.json')
t = TweetTokenizer()

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

a = get_tweets_for_model(positive_tweet_tokens[0])
positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in a]
print(positive_dataset)