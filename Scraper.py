import tweepy
import datetime
import xlsxwriter
import sys
import pandas as pd
from tqdm import tqdm
from IPython.display import clear_output
import json
import string

consumer_key = ""
consumer_secret = ""
accessToken=""
accessTokenSecret=""

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(accessToken,accessTokenSecret)

usernames = ["CNBC","MarketWatch","verge","YahooFinance"]
api = tweepy.API(auth)

time_delta = datetime.timedelta(hours=1)
start_date = datetime.datetime(2020,12,13,0,0,0)
end_date = start_date + time_delta



def create_dictionary(username="",tweet_id="",time="",text="",retweet_count=0,favourite_count=0):
    
    return { 
        "USERNAME": username,
        "TWEET_ID": tweet_id,
        "TIME": time,
        "TWEET": text,
        "RETWEET_COUNT":retweet_count,
        "FAVOURITE_COUNT":favourite_count
    }   

tweet_id = []
time = []
tweet = []
rt_count = []
fav_count = []

for i,username in enumerate(usernames):
    print("Scraping for {}".format(username))
    for status in tweepy.Cursor(api.user_timeline,id=username).items():
        print(f'Last status had timestamp @ {status.created_at}')
        if status.created_at < start_date:
            break
        if (status.created_at >= start_date and status.created_at <= end_date) :
            tweet_id.append(str(status.id))
            time.append(str(status.created_at))
            tweet.append(status.text)
            rt_count.append(status.retweet_count)
            fav_count.append(status.favorite_count)
    dictionary = [
        create_dictionary(username=username,
                        tweet_id = val[0],time=val[1],text=val[2],retweet_count=val[3],favourite_count=val[4])
        for val in zip(tweet_id,time,tweet,rt_count,fav_count)
    ]
    clear_output(wait=True)
    try:
        print("Going for the next username {}".format(usernames[i+1]))
    except:
        print("Done")
        pass
    with open('tweets.json', 'a') as fp:
        json.dump(dictionary, fp,indent=4)
