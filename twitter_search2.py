import twitter
import json
import pickle
import time
import random
import sys
import csv
import datetime
import twitter_creds

OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET = twitter_creds.my_creds()

twitter_stream = twitter.TwitterStream(auth=twitter.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET))

res = twitter_stream.statuses.filter(track='typhoon,Yolanda,philippines,philippine,haiyan,tacloban')

for r in res:
    if 'geo' in r.keys() and r['geo'] is not None and 'lang' in r.keys() and r['lang'] == 'en':
        now = datetime.datetime.now()
        fname = 'typhoon_Yolanda_tweets_'+str(now.year)+'_'+str(now.month)+'_'+str(now.day)+'.csv'
        f = open(fname,'a+')
        thistext = r['text'].encode('utf-8')
        thistext = thistext.replace(',','')
	thistext = thistext.replace('\n', ' ')
        thistime = r['created_at'].encode('utf-8')
        thisgeo = str(r['geo']['coordinates']).encode('utf-8')
        thisgeo = thisgeo.strip('[]')
        print thistext
                                                                                                
        f.write(thistext + ',' + thistime + ',' + thisgeo + '\n')
        f.close()

