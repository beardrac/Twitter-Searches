# Search Twitter using Tweepy
# This program uses the module Tweepy to search Twitter for tweets with the two given tags.

import tweepy
import time
import xlsxwriter
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
usersearch = str(input("Insert a phrase or phrases you would like to search for separated by spaces: "))
searchtermsinit = usersearch.split(" ")

userdates = str(input("""Insert the start date and end date you would like to search for separated a space and in the format YEAR-0MM-DD
                      (NOTE: only dates within the last week are accessible): """))
searchdates = userdates.split(" ")
startSince = searchdates[0]
endUntil = searchdates[1]

usernews = str(input("Would you like to search for news keywords as well? (Y/N): "))

#write into a code
newfile = searchtermsinit[0] + "_output.xlsx"
openworkbook = xlsxwriter.Workbook(newfile)

#search parameters
searchitems = []

if usernews == "Y" or usernews == "y":
    for item in searchtermsinit:
        searchitems.append( "'" + item + "'" )

elif usernews == "N" or usernews == "n":
    for item in searchtermsinit:
        temp = "'" + item + "'"
        searchitems.append( temp + 'AND "CNN"' )
        searchitems.append( temp + 'AND "Fox News"' )
        searchitems.append( temp + 'AND "MSNBC"' )
        searchitems.append( temp + 'AND "BBC"' )

# define search function
def search( searchitem, start, end, workbook ):
    
    # add worksheet to workbook
    worksheet = workbook.add_worksheet()
    
    # create titles for columns
    worksheet.write("A1", "Number of Tweets")
    worksheet.write("B1", "Date")
    worksheet.write("C1", "Time")
    worksheet.write("D1", "Username")
    worksheet.write("E1", "News Org")
    worksheet.write("F1", "Source")
    worksheet.write("G1", "Code")
    worksheet.write("H1", "Tweet")
    
    #define empty list/count
    totaldata = []
    
    #run search
    itsasearch = tweepy.Cursor(api.search,q=searchitem, since=start, until=end, lang="en").items()
    
    #write search into spreadsheet
    while True:
        try:
            # define initial parameters
            NewsOrg = "Random Person"
            retweet = "N"
            
            # data from tweet defined
            tweetdata = itsasearch.next()
            
            # tweet data split into a list
            tweetnums = str(tweetdata.created_at).split(" ")
            # date taken from list
            date = tweetnums[0]
            # time taken from list
            tweettime = tweetnums[1]
            
            # username, display name and tweet taken from data
            username = tweetdata.user.screen_name
            Source = tweetdata.user.name
            tweettext = tweetdata.text
            
            # code define as search terms
            Code = searchitem
            
            # check if source is a news organization or a random person
            if Source.find("CNN") != -1 or Source.find("FoxNews") != -1 or Source.find("BBC") != -1 or Source.find("MSNBC") != -1:
                NewsOrg = "News Org"
            
            # check if tweet is original or not
            if hasattr(tweetdata, 'retweeted_status'):
                retweet = "Y"
            
            # if tweet is not a retweet, create a list of relevant info
            if retweet == "N":            
                inddata = [ date, tweettime, username, NewsOrg, Source, Code, tweettext ]
                totaldata.append( inddata )
        
        # if search quota met, wait 15 min and continue search
        except tweepy.TweepError:
            print("Waiting to continue search...")
            time.sleep(60 * 15)
            print("Continuing Search!")
            print("\n")
            continue
        
        # break loop when search ends
        except StopIteration:
            break
        
    # write data from every tweet into worksheet
    for i in range(1, len(totaldata)):
        worksheet.write("A" + str(i+1), i)
        worksheet.write("B" + str(i+1), totaldata[i-1][0])
        worksheet.write("C" + str(i+1), totaldata[i-1][1])
        worksheet.write("D" + str(i+1), totaldata[i-1][2])
        worksheet.write("E" + str(i+1), totaldata[i-1][3])
        worksheet.write("F" + str(i+1), totaldata[i-1][4])
        worksheet.write("G" + str(i+1), totaldata[i-1][5])
        worksheet.write("H" + str(i+1), totaldata[i-1][6])

# run searches
for word in searchitems:
    search( word, searchdates[0], searchdates[1], openworkbook )

output_file.close()
