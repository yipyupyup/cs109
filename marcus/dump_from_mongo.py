import pandas as pd
import pymongo

client = pymongo.MongoClient(host="localhost", port=27017)
db = client.cs109
tweets = [{
		'ISOdate': tweet['tweet']['created_at'],
		'text': tweet['tweet']['text'],
		'UTC_date': tweet['firstpost_date'],
		'author': tweet['author']['name'],
		'username': tweet['author']['nick'],
		'tokens': "|".join([x[0] for x in tweet['tweet']['topsy']['tokens']]),
		# 'lat': tweet['tweet']['geo']['coordinates'][0] if tweet['tweet']['geo'] is not None else None,
		# 'lng': tweet['tweet']['geo']['coordinates'][1] if tweet['tweet']['geo'] is not None else None,
		# 'city': tweet['tweet']['topsy']['location']['tags']['city'] if 'city' in tweet['tweet']['topsy']['location']['tags'] else None,
		# 'geo_admin1': tweet['tweet']['topsy']['location']['tags']['admin1'] if 'admin1' in tweet['tweet']['topsy']['location']['tags'] else None,
		# 'geo_admin2': tweet['tweet']['topsy']['location']['tags']['admin2'] if 'admin2' in tweet['tweet']['topsy']['location']['tags'] else None,
		# 'geo_admin0': tweet['tweet']['topsy']['location']['tags']['admin0'] if 'admin0' in tweet['tweet']['topsy']['location']['tags'] else None,
		} for tweet in db.tweets.find() if 'retweet' not in tweet['type']]

df = pd.DataFrame.from_records(tweets)

df.to_csv("all_tweets4.csv", encoding="utf-8")
