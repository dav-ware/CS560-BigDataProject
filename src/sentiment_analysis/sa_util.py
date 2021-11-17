import re, string
from typing import Generator, List
from nltk.tokenize import TweetTokenizer
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords


def tokenize_tweets(raw_tweets: List[str]) -> Generator[List[str], None, None]:
    tt = TweetTokenizer()
    for tweet in raw_tweets:
        yield tt.tokenize(tweet)

def clean_tokenized_tweets(tokenized_tweets: Generator[List[str], None, None]) -> Generator[List[str], None, None]:
    sw = stopwords.words('english')
    for token_list in tokenized_tweets:
        cleaned_tweets = []
        for token in token_list:   
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
            token = re.sub("(@[A-Za-z0-9_]+)","", token)
            token = re.sub("(#.+)","", token)
            token = token.lower()
            if len(token) > 0 and token not in string.punctuation and token not in sw:
                cleaned_tweets.append(token)
        yield cleaned_tweets

def tag_tokenized_tweets(tokenized_tweets: Generator[List[str], None, None]) -> Generator[List[tuple], None, None]:
    for token_list in tokenized_tweets:
        yield pos_tag(token_list)

def lemmatize_tagged_tweets(tagged_tweets: Generator[List[tuple], None, None]) -> Generator[List[str], None, None]:
    lemmatizer = WordNetLemmatizer()
    for token_list in tagged_tweets:
        lemmatized_tweets = []
        for token, tag in token_list:
            pos=''
            if tag.startswith('NN'):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            elif tag.startswith('JJ'):
                pos = 'a'
            elif tag.startswith('RB'):
                pos = 'r'
            lemmatized_tweets.append(lemmatizer.lemmatize(token, pos)) if pos != '' else lemmatized_tweets.append(token)
        yield lemmatized_tweets   

def prep_for_nbc(processed_tweets: Generator[dict, None, None]):
    for token_list in processed_tweets:
        yield dict([token, True] for token in token_list)
