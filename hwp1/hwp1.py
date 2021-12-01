import tweepy
import csv
import re, string
from os import environ

#a
auth = tweepy.AppAuthHandler(environ.get('TWITTER_API_KEY'), environ.get('TWITTER_API_SECRET'))
api = tweepy.API(auth)

#b
resp = tweepy.Cursor(api.search_tweets, "#WVU").items(10)

#c
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

with open('hwp1/tweets.csv', 'w') as file: 
    csv_writer = csv.writer(file)
    csv_writer.writerow(header)
    csv_writer.writerows(rows)

with open('hwp1/tweet_text.csv', 'w', newline='') as file: 
    tweets = []
    csv_writer = csv.writer(file)
    for row in rows:
        tweets.append([row[1]])
    csv_writer.writerows(tweets)

#d
def clean_text(orig_text):
    clean_text = re.sub(r"http\S+", "", orig_text)
    clean_text = re.sub(r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za0-9-_]+)", "", clean_text)
    clean_text = clean_text.translate(str.maketrans(dict.fromkeys(string.punctuation)))
    clean_text = re.sub(r"(\r?\n|\r)", " ", clean_text)
    clean_text = re.sub(r"[^\x00-\x7F]+","", clean_text)
    return clean_text

print(rows[0][1])
print(clean_text(rows[0][1]))