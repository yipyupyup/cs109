# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

########################################################
#General code taken from homeworks, don't worry about it
########################################################

%matplotlib inline
from collections import defaultdict
import json

import requests
from pattern import web

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib import rcParams
import matplotlib.cm as cm
import matplotlib as mpl

#colorbrewer2 Dark2 qualitative color table
dark2_colors = [(0.10588235294117647, 0.6196078431372549, 0.4666666666666667),
                (0.8509803921568627, 0.37254901960784315, 0.00784313725490196),
                (0.4588235294117647, 0.4392156862745098, 0.7019607843137254),
                (0.9058823529411765, 0.1607843137254902, 0.5411764705882353),
                (0.4, 0.6509803921568628, 0.11764705882352941),
                (0.9019607843137255, 0.6705882352941176, 0.00784313725490196),
                (0.6509803921568628, 0.4627450980392157, 0.11372549019607843)]

rcParams['figure.figsize'] = (10, 6)
rcParams['figure.dpi'] = 150
rcParams['axes.color_cycle'] = dark2_colors
rcParams['lines.linewidth'] = 2
rcParams['axes.facecolor'] = 'white'
rcParams['font.size'] = 14
rcParams['patch.edgecolor'] = 'white'
rcParams['patch.facecolor'] = dark2_colors[0]
rcParams['font.family'] = 'StixGeneral'


def remove_border(axes=None, top=False, right=False, left=True, bottom=True):
    """
    Minimize chartjunk by stripping out unnecesasry plot borders and axis ticks
    
    The top/right/left/bottom keywords toggle whether the corresponding plot border is drawn
    """
    ax = axes or plt.gca()
    ax.spines['top'].set_visible(top)
    ax.spines['right'].set_visible(right)
    ax.spines['left'].set_visible(left)
    ax.spines['bottom'].set_visible(bottom)
    
    #turn off all ticks
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')
    
    #now re-enable visibles
    if top:
        ax.xaxis.tick_top()
    if bottom:
        ax.xaxis.tick_bottom()
    if left:
        ax.yaxis.tick_left()
    if right:
        ax.yaxis.tick_right()
        
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 100)

########################################################

# <codecell>

#Read in Diana's electiondata 
electiondata = pd.read_csv("state_data/electiondata.txt", sep="\t", skipinitialspace=True, error_bad_lines=False, skiprows=2, header=0)
electiondata = electiondata[electiondata['Office']=="President"]

#Add column with formatted county names
electiondata['county_format'] = electiondata['Area'].apply(lambda x: x.replace("'", "").lower().replace(" ", ""))

# <codecell>

electiondata.head()

# <codecell>

#Create nested dictionary
#State is a key for County:RepVotesMajorPercent pair

grouping = electiondata.groupby('State')

election_dict = {}
for key, value in grouping:
    election_dict[key] = dict(zip(value['county_format'], value['RepVotesMajorPercent']))

election_dict['Connecticut']

# <codecell>

electiondata.head()

# <codecell>

#Calculate percentages for District of Columbia by summing wards

# perhaps pass groupings as a parameter <- thank you Rabeea!
def get_state_data (state_name, data_col):
    indices = groupings[state_name]
    state_data = []
    for i in indices:
        state_data.append(electiondata.ix[i][data_col])
    return state_data

#Get election data for DC
groupings = electiondata.groupby('State').groups
states = sorted(groupings.keys())
dc_data = pd.DataFrame(get_state_data('District of Columbia', ["RepVotes", "DemVotes"]))

# <codecell>

#Sum votes
rep_total = sum([float(i.replace(",","")) for i in dc_data['RepVotes']])
dem_total = sum([float(i.replace(",","")) for i in dc_data['DemVotes']])

rep_percent = rep_total/(rep_total + dem_total)

#Revise dictionary
election_dict['District of Columbia'] = {'districtofcolumbia':rep_percent}

# <codecell>

#Read in tweets
#tweets = pd.read_csv("tweet_data/geo_tweets_with_dist.csv")
tweets = pd.read_csv("GEO.csv") #contiguous US -> no Alaska/Hawaii

#Include only US tweets and remove rows with missing data for state or county
tweets_us = tweets[(tweets['geo_admin0'] == 'United States') & (tweets['geo_admin1'] != 'Puerto Rico')]
tweets_us = tweets_us[tweets_us['geo_admin1'].apply(pd.notnull) & tweets_us['geo_admin2'].apply(pd.notnull) & (tweets_us['geo_admin2'] != '?')]

#Add column with formatted county names (no spaces, no apostrophes)
tweets_us['county_format'] = tweets_us['geo_admin2'].apply(lambda x: x.replace("'", "").lower().replace(" ", ""))

#Get rid of funny symbol in New Mexico's Dona Ana
import re
#tweets_us[tweets_us['geo_admin1']=='New Mexico']['county_format'] = tweets_us[tweets_us['geo_admin1']=='New Mexico']['county_format'].apply(lambda x: re.sub('d.*ana', 'donaana', x)) #THIS SHOULD WORK WHY DOES IT NOT WORK GRRRR..  
tweets_us['county_format'] = tweets_us.apply(lambda x: re.sub('d.*ana', 'donaana', x['county_format']) if x['geo_admin1']=='New Mexico' else x['county_format'], axis=1)



# <codecell>

tweets_us.head()

# <codecell>

#Takes a nested dict (like election_dict) and looks up value based
# on county and state data from tweet. Returns None otherwise.
def match_table(state_dict, tweet):
    value = None
    try:
        value = state_dict[tweet['geo_admin1']][tweet['county_format']]
    except KeyError:
        try:
            #Some of the counties have a "county" and "city" version in the dict. 
            #Adding "county" to the string solves the problem.
            value = state_dict[tweet['geo_admin1']][(tweet['county_format'] + 'county')]
        except KeyError:
            print tweet['county_format'] + ", " + tweet['geo_admin1'] + " not found."
    return value

# <codecell>

repmaj = tweets_us.apply(lambda x: match_table(election_dict, x), axis=1)

# <codecell>

print len(repmaj) #how many tweets?
sum(pd.isnull(repmaj)) #how many None values?

# <codecell>

#Convert repmaj to floats, then calculate distance from Boston
repmaj_fl = list()
for i in repmaj:
    try: 
        repmaj_fl.append(float(i))
    except TypeError: 
        repmaj_fl.append(None)

 

#BOSTON IS LOCATED IN SUFFOLK COUNTY
suffolk_repmaj = 21.13 #RepVotesMajorPercent from table
suffolk_demmaj = 78.87

repmaj_dist = [(i - suffolk_repmaj) if i is not None else None for i in repmaj_fl]

# <codecell>

tweets_us.drop('county_format', axis=1)
tweets_us['RepVotesMajorPercent'] = repmaj_fl
tweets_us['RepVotesMajorDist'] = repmaj_dist


# <codecell>

#tweets_us.to_csv('geo_tweets_with_dist_with_electiondata.csv')
tweets_us.to_csv('GEO_electiondata.csv')

# <codecell>

tweets_us.head()

# <codecell>


