from typing import List
from nltk.tokenize import TweetTokenizer
from nltk.corpus import twitter_samples, stopwords



def tokenize(input: List[str]) -> List[List[str]]:
    tokenized_input = []
    tt = TweetTokenizer()
    for tweet in input:
        tokenized_input.append(tt.tokenize(tweet))
    return tokenized_input

