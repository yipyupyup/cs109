import csv 
with open("geo_tweets_content.csv", "rU") as f:
	dr = csv.DictReader(f)
	us = [tweet for tweet in dr if tweet['geo_admin0'] == "United States" and tweet['geo_admin1'] != "Puerto Rico"]

with open("us_geo_tweets.csv", "wb") as out:
	dw = csv.DictWriter(out, us[0].keys())
	dw.writeheader()
	dw.writerows(us)