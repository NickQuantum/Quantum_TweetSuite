# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 00:53:54 2015

@author: Gerald Varghese
"""
import flask, flask.views
import json
import pprint

from utils import login_required

class Result(flask.views.MethodView):
    @login_required
    def get(self):
        ##tweets_data_path = 'C://Temp//tweet_search.txt' 
        tweets_data_path = '/tmp/tweet_search.txt' 
        tweets_data = []
        tweets_file = open(tweets_data_path, "r")
        
        for line in tweets_file:
                try:
                    tweet = json.loads(line)
                    #pprint.pprint(tweet["text"])
                    pprint.pprint(tweet["user"]["screen_name"])
                   #print tweet
                    #tweet["text"]
                    #tweets_data.append(tweet)
                    hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
                    print(hashtags)
                    tweets_data.append([tweet["text"],tweet["user"]["screen_name"],
                                       hashtags])
                    pprint.pprint(tweets_data)
                    
                except:
                    continue
        tweets = tweets_data
        return flask.render_template('show_table.html', tweets=tweets)