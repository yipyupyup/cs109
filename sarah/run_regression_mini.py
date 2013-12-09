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

tweets = pd.read_csv("/Users/Sarah/Documents/CS109 Data Science/Final/sarah/GEO_electiondata.csv")

# <codecell>

tweets.head()

# <codecell>

from sklearn.linear_model import LinearRegression
smaller_frame=tweets[['emotionverbscore', 'dist_from_boston', 'RepVotesMajorDist']]
X_HD=smaller_frame[['emotionverbscore', 'dist_from_boston', 'RepVotesMajorDist']].values #20054 tweets
X_HD=X_HD[np.isnan(X_HD[:,0])==False] #some nans in emotionverbscore, 19200 tweets
X_HDn=(X_HD - X_HD.mean(axis=0))/X_HD.std(axis=0)

dist_miles_std_vec=X_HDn[:,1]
dist_miles_std=dist_miles_std_vec.reshape(-1,1)
dist_electoral_std_vec=X_HDn[:,2]
dist_electoral_std=dist_electoral_std_vec.reshape(-1,1)
emotionverb_std_vec=X_HDn[:,0]
emotionverb_std=emotionverb_std_vec.reshape(-1,1)


# <codecell>

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(np.column_stack((dist_miles_std, dist_electoral_std)), emotionverb_std_vec)

# <codecell>

clf1 = LinearRegression()
clf1.fit(X_train, y_train)
predicted_train = clf1.predict(X_train)
predicted_test = clf1.predict(X_test)
trains=X_train.reshape(1,-1).flatten()
tests=X_test.reshape(1,-1).flatten()
print clf1.coef_, clf1.intercept_


# <codecell>

# Explained variance score: 1 is perfect prediction
print "Explained variance: ", clf1.score(X_train, y_train)

# The mean square error
print("Residual sum of squares: %.2f" % np.mean((clf1.predict(X_train) - y_train) ** 2))

# Plot of residuals
plt.scatter(predicted_train, predicted_train-y_train, c='b', s=20, alpha=0.5)

# <codecell>


# <codecell>


