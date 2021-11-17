import re, string
from typing import List
from nltk.tokenize import TweetTokenizer
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords


def tokenize(sentence: str) -> List[str]:
    tt = TweetTokenizer()
    return tt.tokenize(sentence)

def tag_tokens(token_list: List[str]) -> List[tuple]:
    return pos_tag(token_list)

def lemmatize_token(token: str, tag: str) -> str:
    lemmatizer = WordNetLemmatizer()
    pos=''
    if tag.startswith('NN'):
        pos = 'n'
    elif tag.startswith('VB'):
        pos = 'v'
    elif tag.startswith('JJ'):
        pos = 'a'
    elif tag.startswith('RB'):
        pos = 'r'
    return lemmatizer.lemmatize(token, pos) if pos != '' else lemmatizer.lemmatize(token)

def clean_tokens(tagged_token_list: List[str]) -> List[str]:
    cleaned_tokens = []
    sw = stopwords.words('english')
    for token, tag in tagged_token_list:
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        token = re.sub("(#.+)","", token)
        if len(token) > 0 and token not in string.punctuation and token.lower() not in sw:
            token = lemmatize_token(token, tag)
            cleaned_tokens.append(token)
    return cleaned_tokens

def prep_for_nbc(cleaned_token_list):
    for token in cleaned_token_list:
        yield dict([token, True] for token in token)
