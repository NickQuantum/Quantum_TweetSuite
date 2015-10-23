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
        
        print('Result GET is called')
        sessionid = flask.session['uid']
        try:
            query = flask.session['query']
        except:
            query=''
        
        if query:
        
            if _platform == "linux" or _platform == "linux2":
                # linux
                tweets_data_path = 'static/tweets/'+sessionid+'.txt'
                html_data_path = 'static/tweets/'+sessionid+'1.json'
            elif _platform == "win32"  or  _platform == "win64":
                # Windows...
                tweets_data_path = 'static//tweets//'+sessionid+'.txt' 
                html_data_path = 'static/tweets/'+sessionid+'1.json'
            
            filename = sessionid
            print('result json filename in result.py  ' + filename)
            print('finished reading file')
            tweets_data = []
            html_data = []
         
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
            
    
            ## read the html 
    
            html_file = open(html_data_path, "r")
            
            print('html file read')
            for line in html_file:
                try:
                    data = json.loads(line)
                   
                except:
                    print('error found')
                    continue        
                
                
            for key,value in data.iteritems():
               
               try:
                   html_data.append([data[key]["html"],data[key]["url"]])
             
                #pprint.pprint(tweets_data)
               except Exception, err:
                    print Exception, err
                   
                
            ##print html_data
            print('finished reading from html file')
            html = html_data
           
            print('assigned data to html file parameter')
         
            return flask.render_template('show_table.html', tweets=tweets, filename=filename,html=html)
        else:
            #tweets = ''
            #filename = ''
            #return flask.render_template('show_table.html') #,tweets,filename)
            flask.session.pop('query', None)
            return flask.render_template('index.html')