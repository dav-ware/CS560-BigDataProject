import tweepy
import json
from os import environ
import csv
import re

auth = tweepy.AppAuthHandler(environ.get('TWITTER_API_KEY'), environ.get('TWITTER_API_SECRET'))
api = tweepy.API(auth)

ab = 'AL'
place = 'place:alabama'

cdc_resp = tweepy.Cursor(api.search_full_archive, 'dev', f'cdc OR fauci OR "dr fauci" OR "doctor fauci" OR "cdc guidelines" OR "cdc mandate" {place} lang:en', fromDate=202003010000, toDate=202008010000).items(10000)
lockdown_resp = tweepy.Cursor(api.search_full_archive, 'dev', 'covid place:alabama lang:en', fromDate=202003010000, toDate=202008010000).items()
mask_resp = tweepy.Cursor(api.search_full_archive, 'dev', 'covid place:alabama lang:en', fromDate=202003010000, toDate=202008010000).items()
vaccine_resp = tweepy.Cursor(api.search_full_archive, 'dev', 'covid place:alabama lang:en', fromDate=202003010000, toDate=202008010000).items()

cdc_rows = []
for tweet in cdc_resp:
     cdc_rows.append([re.sub(r'\n|\t', ' ', tweet.text)])
with open(f'data/twitter_raw/202003-202008/cdc/{ab}', 'w', encoding='utf-8') as file: 
    csv_writer = csv.writer(file)
    csv_writer.writerows(cdc_rows)