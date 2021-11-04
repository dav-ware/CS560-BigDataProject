import tweepy
import json
from os import environ

auth = tweepy.AppAuthHandler(environ.get('TWITTER_API_KEY'), environ.get('TWITTER_API_SECRET'))
api = tweepy.API(auth)

resp = api.search_full_archive('dev', '"covid-19" place:"new york city"', fromDate=202003010000, toDate=202005010000, maxResults=10)

print(json.dumps(resp[0]._json, indent=4, sort_keys=True))