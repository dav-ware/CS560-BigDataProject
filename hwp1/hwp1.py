import tweepy
import csv
import re, string
from typing import List, Text
from os import environ
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob



def main():
    #a,b,c
    #get_tweets()
    with open('hwp1/tweets.csv') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)

    raw_tweets = []
    for i in range(1,len(data)):
        raw_tweets.append(data[i][1])

    #d
    clean_tweets = []
    for tweet in raw_tweets:
        clean_tweets.append(clean_text(tweet))
    
    #e
    tokenized_tweets = []
    for tweet in clean_tweets:
        tokenized_tweets.append(tokenize(tweet))

    #f
    stemmed_tweets = []
    for token_list in tokenized_tweets:
        stemmed_tweets.append(stem(token_list))
    
    #g
    lemmatized_tweets = []
    for token_list in tokenized_tweets:
        lemmatized_tweets.append(lemmatize(token_list))

    #h
    header = ['id', 'raw_text', 'clean_text', 'tokens', 'stemmed_tokens', 'lemmatized_tokens']
    rows = []
    for i in range(len(raw_tweets)):
        row = []
        row.append(data[i+1][0])
        row.append(raw_tweets[i])
        row.append(clean_tweets[i])
        row.append(tokenized_tweets[i])
        row.append(stemmed_tweets[i])
        row.append(lemmatized_tweets[i])
        rows.append(row)
    with open('hwp1/cleantokens.csv', 'w', encoding='utf-8') as file: 
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)

    #i
    token_set = set()
    freq = {}
    for token_list in lemmatized_tweets:
        for token in token_list:
            if token not in token_set:
                token_set.add(token)
                freq[token] = 1
            else:
                freq[token] += 1

    freq_list = []
    for key in freq.keys():
        freq_list.append((key, freq[key]))

    sorted_freq_list = sorted(freq_list, key = lambda x: x[1], reverse=True)
    header = ['token', 'frequency']
    rows = []
    for i in sorted_freq_list:
        row = []
        row.append(i[0])
        row.append(i[1])
        rows.append(row)

    with open('hwp1/frequency.csv', 'w', encoding='utf-8') as file: 
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)

    #j
    sa = []
    for tweet in clean_tweets:
        tb = TextBlob(tweet).sentiment
        sa.append((round(tb.polarity, 3), round(tb.subjectivity, 3)))
    
    header = ['id', 'clean_text', 'polarity', 'subjectivity']
    rows = []
    for i in range(len(sa)):
        row = []
        row.append(data[i+1][0])
        row.append(clean_tweets[i])
        row.append(sa[i][0])
        row.append(sa[i][1])
        rows.append(row)

    with open('hwp1/sentiments.csv', 'w', encoding='utf-8') as file: 
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)





def get_tweets():
    auth = tweepy.AppAuthHandler(environ.get('TWITTER_API_KEY'), environ.get('TWITTER_API_SECRET'))
    api = tweepy.API(auth)
    resp = tweepy.Cursor(api.search_tweets, "#WVU").items(10)

    header = ['id', 'text', 'author', 'datetime', 'retweets', 'likes']
    rows = []
    for tweet in resp:
        row = []
        row.append(tweet.id)
        row.append(re.sub(r'\n|\t', ' ', tweet.text))
        row.append(tweet.user.screen_name)
        row.append(tweet.created_at.strftime('%m/%d/%Y %H:%M:%S'))
        row.append(tweet.retweet_count)
        row.append(tweet.favorite_count)
        rows.append(row)

    with open('hwp1/tweets.csv', 'w', encoding='utf-8') as file: 
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)

#d
def clean_text(orig_text: str) -> str:
    clean_text = re.sub(r"http\S+", "", orig_text)
    clean_text = re.sub(r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za0-9-_]+)", "", clean_text)
    clean_text = clean_text.translate(str.maketrans(dict.fromkeys(string.punctuation)))
    clean_text = re.sub(r"(\r?\n|\r)", " ", clean_text)
    clean_text = re.sub(r"[^\x00-\x7F]+","", clean_text)
    return clean_text

#e
def tokenize(tweet: str) -> List[str]:
    sw = stopwords.words('english')
    tt = TweetTokenizer()
    tokens = tt.tokenize(tweet)
    ret = []
    for token in tokens:
        if len(token) >= 3 and token not in sw:
            ret.append(token.lower())
    return ret


#f
def stem(tokens: List[str]) -> List[str]:
    ps = PorterStemmer()
    stemmed_tokens = []
    for token in tokens:
        stemmed_tokens.append(ps.stem(token))
    return stemmed_tokens

#g
def lemmatize(tokens: List[str]) -> List[str]:
    tagged_tokens = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = []
    for token, tag in tagged_tokens:
        pos=''
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        elif tag.startswith('JJ'):
            pos = 'a'
        elif tag.startswith('RB'):
            pos = 'r'
        lemmatized_tokens.append(lemmatizer.lemmatize(token, pos)) if pos != '' else lemmatized_tokens.append(token)
    return lemmatized_tokens


if __name__ == "__main__":
    main()