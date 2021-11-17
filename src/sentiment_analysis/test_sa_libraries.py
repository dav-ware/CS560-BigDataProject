import pandas as pd 
import sa_util as util
from textblob import TextBlob
from nltk import NaiveBayesClassifier, classify
from nltk.corpus import twitter_samples
import time
import random

with open('./tweet_sentiments_negative.csv', encoding = "ISO-8859-1") as tweet_sentiments:
    df_neg = pd.read_csv(tweet_sentiments)
    df_neg.columns = ['target', 'id', 'date', 'flag', 'user', 'text']
with open('./tweet_sentiments_positive.csv', encoding = "ISO-8859-1") as tweet_sentiments:
    df_pos = pd.read_csv(tweet_sentiments)
    df_pos.columns = ['target', 'id', 'date', 'flag', 'user', 'text']
t0 = time.time()
positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')

clean_pos_tweets = []
clean_neg_tweets = []
for i in range(100):
    pos_tagged_token_list = util.tag_tokens(util.tokenize(positive_tweets[i]))
    clean_pos_tweets.append(util.clean_tokens(pos_tagged_token_list))
    neg_tagged_token_list = util.tag_tokens(util.tokenize(negative_tweets[i]))
    clean_neg_tweets.append(util.clean_tokens(neg_tagged_token_list))
pos = util.prep_for_nbc(clean_pos_tweets)
neg = util.prep_for_nbc(clean_neg_tweets)

positive_dataset = [(dict, "Positive") for dict in pos]
negative_dataset = [(dict, "Negative") for dict in neg]

dataset = positive_dataset + negative_dataset
random.shuffle(dataset)

train_data = dataset[:100]
test_data = []
for i in dataset[100:]:
    test_data.append(i[0])

classifier = NaiveBayesClassifier.train(train_data)
t1 = time.time()

res = classifier.prob_classify_many(test_data)
for i in res:
    print(i.prob('Positive'), i.prob('Negative'), i.max())