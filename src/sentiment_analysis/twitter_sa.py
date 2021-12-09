import pandas as pd 
import sa_util as util
from nltk import NaiveBayesClassifier
import csv
import random
import os

with open('data/negative.csv', encoding = "ISO-8859-1") as tweet_sentiments:
    df_neg = pd.read_csv(tweet_sentiments)
    df_neg.columns = ['target', 'id', 'date', 'flag', 'user', 'text']
with open('data/positive.csv', encoding = "ISO-8859-1") as tweet_sentiments:
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
positive_dataset = list(ptrain)
negative_dataset = list(ntrain)
training_dataset = positive_dataset + negative_dataset
random.shuffle(training_dataset)
nb_model = NaiveBayesClassifier.train(training_dataset)

header = ['STUSPS', 'VACCINE_SENTIMENT']
rows = []
for subdir, dirs, files in os.walk('data/twitter_raw/vaccine'):
    for filename in files:
        row = []
        filepath = subdir + os.sep + filename
        df_temp = pd.read_csv(filepath)
        state = filepath[-6:-4]
        raw_tweets = df_temp.iloc[:,0].to_list()

        tokens = util.tokenize_tweets(raw_tweets)
        cleaned_tokens = util.clean_tokenized_tweets(tokens)
        tagged_tweets = util.tag_tokenized_tweets(cleaned_tokens)
        lemmatized_tweets = util.lemmatize_tagged_tweets(tagged_tweets)
        nbc_tweets = util.prep_for_nbc(lemmatized_tweets)
        sa = nb_model.prob_classify_many(nbc_tweets)

        p_count = 0
        n_count = 0
        for i in range(len(sa)):
            if sa[i].prob(sa[i].max()) >= 0.9:
                if sa[i].max() == 'Positive':
                    p_count += 1
                else:
                    n_count += 1
        if n_count == 0:
            n_count += 1
        sentiment = p_count/n_count
        row.append(state)
        row.append(sentiment)
        rows.append(row)
        print(state)
        
with open('data/twitter_sentiments/vaccine.csv', 'w', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(header)
    csv_writer.writerows(rows)

print(rows)