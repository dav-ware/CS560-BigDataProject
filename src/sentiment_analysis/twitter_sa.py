import pandas as pd 
import sa_util as util
from nltk import NaiveBayesClassifier, classify
import time
import random


with open('datasets/test_tweet_sentiments_negative.csv', encoding = "ISO-8859-1") as tweet_sentiments:
    df_neg = pd.read_csv(tweet_sentiments)
    df_neg.columns = ['target', 'id', 'date', 'flag', 'user', 'text']
with open('datasets/test_tweet_sentiments_positive.csv', encoding = "ISO-8859-1") as tweet_sentiments:
    df_pos = pd.read_csv(tweet_sentiments)
    df_pos.columns = ['target', 'id', 'date', 'flag', 'user', 'text']
raw_positive_tweets = df_pos['text'].head(50000).to_list()
raw_negative_tweets = df_neg['text'].head(50000).to_list()

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

t0 = time.time()
positive_dataset = list(ptrain)
negative_dataset = list(ntrain)
t1 = time.time()
dataset = positive_dataset + negative_dataset
random.shuffle(dataset)

train_data = dataset[50000:]
test_data = dataset[:50000]

nb_model = NaiveBayesClassifier.train(train_data)
accuracy = classify.accuracy(nb_model, test_data)*100

detupled_test_data = [i[0] for i in test_data]
correct_prediction = [i[1] for i in test_data]
res = nb_model.prob_classify_many(detupled_test_data)
wrong_count = 0
skip_count = 0

for i in range(50000):
    if res[i].max() != correct_prediction[i]:
        if res[i].prob(res[i].max()) >= 0.9995:
            wrong_count += 1
        else:
            skip_count += 1

t2 = time.time()
confident_accuracy = round((50000-skip_count-wrong_count)/(50000-skip_count)*100, 2)
print(f'time to convert generator to list: {t1-t0}')
print(f'time to do SA: {t2-t1}')
print(f"accuracy using full dataset: {accuracy}%\nconfident accuracy: {confident_accuracy}% using {(50000-skip_count)/50000*100}% of dataset")
