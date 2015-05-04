# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 00:53:54 2015

@author: Gerald Varghese
"""
import flask, flask.views
import json
##import pprint

from sys import platform as _platform
from utils import login_required

class Result(flask.views.MethodView):
    @login_required
    def get(self):
        if _platform == "linux" or _platform == "linux2":
            # linux
            tweets_data_path = '/tmp/'+flask.session['uid']+'.txt' 
        elif _platform == "win32":
            # Windows...
            tweets_data_path = 'static//tweets//'+flask.session['uid']+'.txt' 
        print('finished reading file')
        tweets_data = []
        tweets_file = open(tweets_data_path, "r")
        print('file read')
        for line in tweets_file:
                try:
                    tweet = json.loads(line)
                    #pprint.pprint(tweet["text"])
                    #pprint.pprint(tweet["user"]["screen_name"])
                   #print tweet
                    #tweet["text"]
                    #tweets_data.append(tweet)
                    hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
                    #print(hashtags)
                    tweets_data.append([tweet["text"],tweet["user"]["screen_name"],
                                       hashtags])
                    #pprint.pprint(tweets_data)
                    
                except:
                    print('error found')
                    continue
        print('finished reading from file')
        tweets = tweets_data
        print('assigned data to file parameter')
        return flask.render_template('show_table.html', tweets=tweets, filename=flask.session['uid'])