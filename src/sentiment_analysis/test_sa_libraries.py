import pandas as pd 
import sa_util as util
from textblob import TextBlob
from nltk import NaiveBayesClassifier, classify
from nltk.corpus import twitter_samples
import time
import random
t0 = time.time()

with open('./tweet_sentiments_negative.csv', encoding = "ISO-8859-1") as tweet_sentiments:
    df_neg = pd.read_csv(tweet_sentiments)
    df_neg.columns = ['target', 'id', 'date', 'flag', 'user', 'text']
with open('./tweet_sentiments_positive.csv', encoding = "ISO-8859-1") as tweet_sentiments:
    df_pos = pd.read_csv(tweet_sentiments)
    df_pos.columns = ['target', 'id', 'date', 'flag', 'user', 'text']
raw_positive_tweets = df_pos['text'].head(10000).to_list()
raw_negative_tweets = df_neg['text'].head(10000).to_list()

t1 = time.time()

positive_tokens = util.tokenize_tweets(raw_positive_tweets)
negative_tokens = util.tokenize_tweets(raw_negative_tweets)
cleaned_positive_tokens = util.clean_tokenized_tweets(positive_tokens)
cleaned_negative_tokens = util.clean_tokenized_tweets(negative_tokens)
tagged_positive_tweets = util.tag_tokenized_tweets(cleaned_positive_tokens)
tagged_negative_tweets = util.tag_tokenized_tweets(cleaned_negative_tokens)
lemmatized_positive_tweets = util.lemmatize_tagged_tweets(tagged_positive_tweets)
lemmatized_negative_tweets = util.lemmatize_tagged_tweets(tagged_negative_tweets)

nbc_positive_tweets = util.prep_for_nbc(lemmatized_positive_tweets)
nbc_negative_tweets = util.prep_for_nbc(lemmatized_negative_tweets)
ptrain = ((dict, "Positive") for dict in nbc_positive_tweets)
ntrain = ((dict, "Negative") for dict in nbc_negative_tweets)

t2 = time.time()

positive_dataset = list(ptrain)
negative_dataset = list(ntrain)
dataset = positive_dataset + negative_dataset
random.shuffle(dataset)

t3 = time.time()

train_data = dataset[10000:]
test_data = dataset[:10000]
nb_model = NaiveBayesClassifier.train(train_data)
accuracy = classify.accuracy(nb_model, test_data)*100

detupled_test_data = [i[0] for i in test_data]
correct_prediction = [i[1] for i in test_data]
res = nb_model.prob_classify_many(detupled_test_data)
wrong_count = 0
skip_count = 0

for i in range(10000):
    if res[i].max() != correct_prediction[i]:
        if res[i].prob(res[i].max()) >= 0.9:
            wrong_count += 1
            print(res[i].prob('Positive'), res[i].prob('Negative'), res[i].max(), correct_prediction[i])
        else:
            skip_count += 1
confident_accuracy = (10000-skip_count-wrong_count)/(10000-skip_count)*100
print(f"\naccuracy using full dataset: {accuracy}%\nconfident_accuracy: {confident_accuracy}% using {(10000-skip_count)/10000*100}% of dataset")

t4 = time.time()
print(f'load csv: {t1-t0}\ngenerator code: {t2-t1}\nconvert to list: {t3-t2}\nfull time: {t4-t0}')