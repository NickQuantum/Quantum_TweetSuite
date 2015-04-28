# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 00:58:09 2015

@author: Gerald Varghese
"""
import flask, flask.views
import tweepy
import json


import login
from utils import login_required


class Search(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('search.html')
    
    @login_required    
    def post(self):
        ## tweet collector code here --
        #query = 'python'
        query = flask.request.form['Query']
        max_tweets = 50

        api = login.sapi
        searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
        ##filepath = 'C://Temp//tweet_search.txt' 
        filepath = '/tmp/tweet_search.txt' 
        target = open(filepath, 'w')
        
        for tweet in searched_tweets:
            tweet_str = json.dumps(tweet._json)
            target.write(tweet_str + "\n")
        
        target.close()
        #result = flask.request.form['searchtxt']
        #flask.flash(result)
        return flask.redirect(flask.url_for('result'))