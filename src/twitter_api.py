from typing import get_origin
import tweepy
import json
from os import environ
import csv
import re
import time

auth = tweepy.AppAuthHandler(environ.get(
    'TWITTER_API_KEY'), environ.get('TWITTER_API_SECRET'))
api = tweepy.API(auth)

location_info = [('AL', '32.760095,-86.579700,223.27km'), ('AZ', '34.153271,-111.716503,335.66km'), ('AR', '34.913483,-92.424427,223.27km'), ('CA', '35.488046,-123.142285,703.60km'), 
('CO', '38.951376,-105.652050,299.25km'), ('CT', '41.533746,-72.671093,66.04km'), ('DE', '39.045289,-75.439624,62.28km'), ('FL', '27.279366,-83.816372,423.66km'), ('GA', ' 32.718283,-83.684536,232.17km'),
('ID', '44.863954,-114.353434,343.03km'), ('IL', '39.901973,-89.129911,272.19km'), ('IN', '39.901973,-86.317411,197.44km'), ('IA', '41.993224,-93.481008,259.14km'), ('KS', '38.575056,-98.534719,335.69km'),
('KY', '37.363064,-85.351563,227.16km'), ('LA', '31.082931,-92.075196,243.92km'), ('ME', '45.356190,-69.013639,189.02km'), ('MD', '38.818049,-76.804999,127.38km'), ('MA', '42.306751,-72.015724,77.83km'),
('MI', '43.617165,-84.768416,238.62km'), ('MN', '46.182854,-94.189798,326.90km'), ('MS', '32.659524,-89.382429,236.64km'), ('MO', '38.308222,-92.470392,286.49km'), ('MT', '47.126939,-109.543360,430.51km'),
('NE', '41.502499,-99.909858,317.41km'), ('NV', '39.160900,-116.186571,372.27km'), ('NH', '43.813606,-71.381115,90.52km'), ('NJ', '40.386607,-74.645462,61.52km'), ('NM', '34.512400,-106.126199,351.96km'), 
('NY', '42.258333,-74.930005,202.91km'), ('NC', '35.516473,-79.272286,178.99km'), ('ND', '47.613199,-100.607657,250.41km'), ('OH', '40.553863,-82.609485,179.94km'), ('OK', '35.737896,-97.456056,259.51km'),
('OR', '43.902234,-120.579062,280.65km'), ('PA', '40.835990,-77.104589,196.19km'), ('RI', '41.708555,-71.470253,41.84km'), ('SC', '33.617580,-80.786729,169.72km'), ('SD', '44.455511,-100.070740,252.61km'),
('TN', '35.740878,-86.069866,197.28km'), ('TX', '31.673990,-99.491042,557.23km'), ('UT', '39.431233,-111.601250,278.34km'), ('VT', '43.993943,-72.667867,79.35km'), ('VA', '37.457075,-77.823474,160.94km'), 
('WA', '47.495277,-120.094531,246.63km'), ('WV', '38.689385,-80.404140,159.41km'), ('WI', '44.603680,-89.792397,241.39km'), ('WY', '42.962848,-107.443370,302.03km')]

cdc_query = '"cdc covid" OR fauci OR "dr fauci" OR "doctor fauci" OR "cdc guidelines" OR "cdc mandate" exclude:retweets'
mask_query = 'mask OR masks OR "mask mandate" OR (mask make wear) OR (mask right) exclude:retweets'
vaccine_query = 'vaccine OR "covid vaccine" OR pfizer OR moderna OR "booster shot" OR "vaccine mandate" exclude:retweets'
trump_query = 'trump OR (trump covid) exclude:retweets'
biden_query = 'biden OR (biden covid) exclude:retweets'

for i in range(3, len(location_info)):
     complete = False
     while complete == False:
          try:
               print('cdc')
               cdc_resp = tweepy.Cursor(api.search_tweets, cdc_query, lang='en', geocode=location_info[i][1]).items(1000)
               cdc_rows = []
               for tweet in cdc_resp:
                    cdc_rows.append([re.sub(r'\n|\t', ' ', tweet.text)])
               with open(f'data/twitter_raw/cdc/{location_info[i][0]}.csv', 'w', encoding='utf-8') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(cdc_rows)
               complete = True
          except:
               print('waiting on cdc')
               time.sleep(300)

     complete = False
     while complete == False:
          try:
               print('mask')
               mask_resp = tweepy.Cursor(api.search_tweets, mask_query, lang='en', geocode=location_info[i][1]).items(1000)
               mask_rows = []
               for tweet in mask_resp:
                    mask_rows.append([re.sub(r'\n|\t', ' ', tweet.text)])
               with open(f'data/twitter_raw/mask/{location_info[i][0]}.csv', 'w', encoding='utf-8') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(mask_rows)
               complete = True
          except:
               print('waiting on mask')
               time.sleep(300)

     complete = False
     while complete == False:
          try:
               print('vaccine')
               vaccine_resp = tweepy.Cursor(api.search_tweets, vaccine_query, lang='en', geocode=location_info[i][1]).items(1000)
               vaccine_rows = []
               for tweet in vaccine_resp:
                    vaccine_rows.append([re.sub(r'\n|\t', ' ', tweet.text)])
               with open(f'data/twitter_raw/vaccine/{location_info[i][0]}.csv', 'w', encoding='utf-8') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(vaccine_rows)
               complete = True
          except:
               print('waiting on vaccine')
               time.sleep(300)

     complete = False
     while complete == False:
          try:
               print('trump')
               trump_resp = tweepy.Cursor(api.search_tweets, trump_query, lang='en', geocode=location_info[i][1]).items(1000)
               trump_rows = []
               for tweet in trump_resp:
                    trump_rows.append([re.sub(r'\n|\t', ' ', tweet.text)])
               with open(f'data/twitter_raw/trump/{location_info[i][0]}.csv', 'w', encoding='utf-8') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(trump_rows)
               complete = True
          except:
               print('waiting on trump')
               time.sleep(300)

     complete = False
     while complete == False:     
          try:
               print('biden')
               biden_resp = tweepy.Cursor(api.search_tweets, biden_query, lang='en', geocode=location_info[i][1]).items(1000)
               biden_rows = []
               for tweet in biden_resp:
                    biden_rows.append([re.sub(r'\n|\t', ' ', tweet.text)])
               with open(f'data/twitter_raw/biden/{location_info[i][0]}.csv', 'w', encoding='utf-8') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(biden_rows)
               complete = True
          except:
               print('waiting on biden')
               time.sleep(300)






