#!/usr/bin/python3
# Search Twitter using Tweepy
# This program uses the module Tweepy to search Twitter for tweets with the two given tags.

import tweepy
import time
import csv
import configparser

# Location of the config file
CONFIG_FILE = 'config.ini'

# Read config file
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

#authorize
username = config['common']['username']
password = config['common']['password']
consumer_token = config['common']['consumer_token']
consumer_secret = config['common']['consumer_secret']

auth = tweepy.OAuthHandler( consumer_token, consumer_secret )

access_token = config['common']['access_token']
access_secret = config['common']['access_secret']

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#ask user
user = str(input("Search: "))

#write into a code
output = user + "_output_Oct31.csv" #CHANGE
output_file = open(output, "w")
csvWriter = csv.writer(output_file)

#search parameters
startSince = '2015-010-31' #CHANGE
endUntil = '2015-011-01' #CHANGE
search1 = "'" + user + "'"
searchitems = search1 + 'AND "#HurricanePatricia"' #CHANGE

#actually search stuff
count = 0
mysearch = tweepy.Cursor(api.search,q=searchitems, since=startSince, until=endUntil, lang="en").items()

while True:    
    try:
        tweet = mysearch.next()
        csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
        count +=1
        
    except tweepy.TweepError:
        time.sleep(60 * 15)
        continue
    
    except StopIteration:
        break

output_file.close()
