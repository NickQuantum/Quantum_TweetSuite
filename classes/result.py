# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 00:53:54 2015

@author: Quantum Solutions
"""
import flask, flask.views
import json
##import pprint

from sys import platform as _platform
from utils import login_required

class Result(flask.views.MethodView):
    @login_required
    def get(self):
        
        print('Search POST called')
        sessionid = flask.session['uid']
        try:
            query = flask.session['query']
        except:
            query=''
        
        if query:
        
            if _platform == "linux" or _platform == "linux2":
                # linux
                tweets_data_path = 'static/tweets/'+sessionid+'.txt' 
            elif _platform == "win32":
                # Windows...
                tweets_data_path = 'static//tweets//'+sessionid+'.txt' 
            
            filename = sessionid
            print('result json filename in result.py  ' + filename)
            print('finished reading file')
            tweets_data = []
            tweets_file = open(tweets_data_path, "r")
            print('file read')
            for line in tweets_file:
                    try:
                        tweet = json.loads(line)
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
    
            
            return flask.render_template('show_table.html', tweets=tweets, filename=filename)
        else:
            tweets = ''
            filename = ''
            return flask.render_template('show_table.html') #,tweets,filename)