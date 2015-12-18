# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 00:58:09 2015

@author: Quantum Solutions
"""
import flask, flask.views
import tweepy
import json
import utils
import requests
from requests_oauthlib import OAuth1



#import login
from utils import login_required
from findsentiment import process_sentiment
from sys import platform as _platform



class Search(flask.views.MethodView):
    @login_required
    def get(self):
        flask.session.pop('query', None)
        #return flask.redirect(flask.url_for('result'))
        return flask.render_template('index.html')
        #return flask.render_template('search.html')
    
    @login_required    
    def post(self):
        ## tweet collector code here --
        #query = 'python'
        print('Search POST called')
        query = flask.request.form['Query']
        flask.session['query'] = query
        max_tweets = 20

        print 'query --> ' + flask.session['query']
        #api = login.sapi
        api = utils.sapi

        print 'retreved api authentication successful'

        searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
        if _platform == "linux" or _platform == "linux2":
            # linux
            filepath = 'static/tweets/'+flask.session['uid']+'.txt'  
        elif _platform == "win32"  or  _platform == "win64":
            # Windows...
            filepath = 'static//tweets//'+flask.session['uid']+'.txt'  

        print('file name =' + flask.session['username'])
        
        ##os.remove(filepath)

        target = open(filepath, 'w')
        
        for tweet in searched_tweets:
            tweet_str = json.dumps(tweet._json)
            target.write(tweet_str + "\n")
        
        target.close()
        #result = flask.request.form['searchtxt']
        #flask.flash(result)
        print('tweets dumpted as json - next preparation for graph')
        import networkx as nx
        from networkx.readwrite import json_graph

        g = nx.Graph()
        

        #initialize a dict
        #iterate through all the tweets and get the user ids and the retweet user ids
        
        #Store user id and retweet user ids in a dict
        #Iterate through retweet user ids and user ids and add node and edge to graph
        tweet_id_dict ={}
        retweet_user_dict = {}
        mention_user_dict = {}
        username_dict = {}
        tweet_dict = {}
        retweet_dict = {}
        mention_tweet_dict = {}
        influencer_dict = {}
        influencer_entities_url = {}
        user_entities_url = {}
        #user_entities_url_list = []
        user_list = []
        retweet_user_list = []
        mention_user_listoflists = []
        mention_user_list = []
        complete_user_list = []
        top_3_influencers ={}
        chunks = []
        tweets_file = open(filepath, "r")
        
        for line in tweets_file:
                try:
                    tweet = json.loads(line)
                    #hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
                    tweet_id = tweet['id']
                    user_id = tweet['user']['id']
                    tweet_dict[user_id] = tweet['text']
                    user_list.append(user_id)
                    tweet_id_dict[user_id] =tweet_id
                    if 'retweeted_status' in tweet: 
                       
                        #pprint.pprint(tweet)
                        retweet_user_id = tweet['retweeted_status']['user']['id']
                        retweet = tweet['retweeted_status']['text']
                        retweet_user_list.append(retweet_user_id)
                        retweet_user_dict[user_id] = retweet_user_id
                        retweet_dict[user_id] = retweet
                    if 'entities' in tweet and len(tweet['entities']['user_mentions']) > 0:
                         mention_user_ids = [mention['id'] for mention in tweet['entities']['user_mentions']]
                         mention_tweet = tweet['text']  
                         mention_user_listoflists.append(mention_user_ids)
                         mention_user_dict[user_id] = mention_user_ids
                         mention_tweet_dict[user_id] = mention_tweet
                    ## The following code gets the urls hosted in the tweet only and not from retweet urls or mention urls
                    if 'entities' in tweet and len(tweet['entities']['urls']) > 0:
                         user_entities_url_list = [reference['url'] for reference in tweet['entities']['urls']]
                         user_entities_url[user_id] = user_entities_url_list
                    #pprint.pprint(user_list)
                    #print(tweets_data)
                except:
                    continue
        
        print('completed reading tweets file')
                    
        def get_user_info(user_ids):
            
            users = api.lookup_users(user_ids)
            for user in users:
                username_dict[user.id] = user.screen_name
            return username_dict            
        
        
        
        for mention_user_ids in mention_user_listoflists:
            for mention_user_id in mention_user_ids:
                mention_user_list.append(mention_user_id)
            
        # Added code to break into chunks of 100 as the api.looup_users has limit of 100 at a time
        ##username_dict = get_user_info(user_list + retweet_user_list + mention_user_list)
        complete_user_list = user_list + retweet_user_list + mention_user_list
        chunks=[complete_user_list[x:x+100] for x in xrange(0, len(complete_user_list), 100)]
        for i in range(len(chunks)):
            username_dict = get_user_info(chunks[i])
            
        ##print mention_user_list
                
        #print username_dict
                
        def add_node_tw(n, weight=None, time=None, source=None):
            if not g.has_node(n):
                screen_name = username_dict.get(n)
                if n in retweet_dict:
                    tweet = retweet_dict.get(n)
                elif n in mention_tweet_dict:
                    tweet = mention_tweet_dict.get(n)
                else:
                    tweet = tweet_dict.get(n)
                g.add_node(n)
                g.node[n]['weight'] = 1
                g.node[n]['screen_name'] = screen_name
                g.node[n]['tweet'] = tweet            
            else:
                g.node[n]['weight']+=1
                
        def add_edge_tw(n1,n2, weight=None):
            if not g.has_edge(n1,n2):
                g.add_edge(n1,n2)
                g[n1][n2]['weight']=1
            else:
                g[n1][n2]['weight']+=1
        

        
        for user_id in user_list:
            add_node_tw(user_id)
            if user_id in retweet_user_dict:
                    retweet_user_id = retweet_user_dict.get(user_id)           
                    add_node_tw(retweet_user_id)
                    add_edge_tw(retweet_user_id,user_id)
            if user_id in mention_user_dict:
                for mention_user_id in mention_user_dict.get(user_id):
                
                    add_node_tw(mention_user_id)
                    add_edge_tw(mention_user_id,user_id)
        
      
        ## loop through the network node dictionary
        ## identify the user ids and build a dictionary with userids and their weights
         
        for userid in g.node:
            ## make sure the user id is not in the retweet user dict or mention user dict and grab that node
            ## logic is to ensure that the user id is there in the user_list
            if userid in user_list:
                influencer_dict[userid] = g.node[userid]['weight']
                influencer_entities_url[userid] = user_entities_url.get(userid)
            
        print influencer_dict
        print('completed creating initial influencers dictionary')
        # create a function which returns the value of a dictionary
        def keyfunction(k):
            return influencer_dict[k]
        
        # sort by dictionary by the values and print top 3 {key, value} pairs
        for key in sorted(influencer_dict, key=keyfunction, reverse=True)[:3]:
           #print "%s: %i" % (key, influencer_dict[key])        
           url_dict = influencer_entities_url.get(key)
           value =''
           if url_dict is not  None:
                 value = url_dict
           top_3_influencers[key] = value
           
        print  top_3_influencers
        print 'Identified the top 3 influencers in top_3_influencers dictionary'
        
        ## mention user dict has list of mention user ids 
        ## need to take cout of each list 
          # sort by dictionary by the values and print top 3 {key, value} pairs
      
        
#        for key,value in top_3_influencers.iteritems():
#            print key
#            inf_tweet = tweet_dict.get(key)
#            inf_screen_name = username_dict.get(key)
#             print inf_tweet
#             print inf_screen_name
#             print value
#             print 'next'
            
        ## gexf is not needed now; until we start using GEPHI    
        ##nx.write_gexf(g, 'C://Temp//test.gexf')
        if _platform == "linux" or _platform == "linux2":
            # linux
            filepathjson = 'static/tweets/'+flask.session['uid']+'.json'  ##'/tmp/tweetgraph.json' 
            print(filepathjson)
        elif _platform == "win32"  or  _platform == "win64":
            # Windows...
            filepathjson = 'static//tweets//'+flask.session['uid']+'.json' 
                
        try:
            print('before readwrite')
            data = json_graph.node_link_data(g)
            print('readwrite successful')
            ##pprint.pprint(data) 
            with open(filepathjson, 'w') as outfile:
                
                json.dump(data, outfile)
                ##print json.dumps(data)       
                print('JSON file Created for network graph!')
        except:
            print('JSON FILE Creation for network graph FAILED')
        
        ## REST API call to build influencers table
        try:
            ## make a REST aPI call 
            ## https://api.twitter.com/1.1/statuses/oembed.json?maxwidth=250&hide_media=1&hide_thread=1&omit_script=1&align=left&id=638229069251899392
            ## get the user id from the above dictionary and make a call  
            ## store the results in html
            ## add oauth
            ##headers = {'consumer_key':'5zvyqirbbnbPxUX67ixXBwQ5G','consumer_secret':'8iGil6zWJvK7qjGj0z7xguSvaiIbZtpH0Z3UumAVetv88e9xbX','access_token':'2995170696-z5tNgtrnhR5zc5tT4sB6knKBTrCKHehOljhs1l2','access_token_secret':'wOcuYhfpvwxFZ6TmNvyPb9fPpEnH1fvfApiEZFnFGUuJk'}
            auth = OAuth1('5zvyqirbbnbPxUX67ixXBwQ5G','8iGil6zWJvK7qjGj0z7xguSvaiIbZtpH0Z3UumAVetv88e9xbX','2995170696-z5tNgtrnhR5zc5tT4sB6knKBTrCKHehOljhs1l2','wOcuYhfpvwxFZ6TmNvyPb9fPpEnH1fvfApiEZFnFGUuJk')
            ##iframe_dict ={userid1: {'url':1,'html':2},userid2: {'url':3,'html':4}, userid3: {'url':5,'html':6}}
            iframe_dict ={}
            
            for key,value in top_3_influencers.iteritems():
                
                tweetid =tweet_id_dict.get(key)
                payload ={}
                payload['id'] = tweetid
                
                r = requests.get('https://api.twitter.com/1.1/statuses/oembed.json?maxwidth=250&hide_media=1&hide_thread=1&omit_script=1&align=left',params =payload,auth =auth)
                
                htmlcontent = r.json()
                iframe_dict[key] ={}
                
                
                internal_dict = {'html':1,'url':2}
                internal_dict['html'] = htmlcontent['html']
               
                internal_dict['url'] = value
                ##iframe_list.append(htmlcontent['html'])
                iframe_dict[key] = internal_dict
                
                ##print htmlcontent['html']
                
            
        except Exception , err:
            print('twitter api call FAILED')
            print Exception, err
        
        ##print iframe_dict
        if _platform == "linux" or _platform == "linux2":
            # linux
            filepathjson = 'static/tweets/'+flask.session['uid']+'1.json'  ##'/tmp/tweetgraph.json' 
            print(filepathjson)
        elif _platform == "win32"  or  _platform == "win64":
            # Windows...
            filepathjson = 'static//tweets//'+flask.session['uid']+'1.json' 
                
        try:
             print('before readwrite')
             
             with open(filepathjson, 'w') as outfile:
             
               json.dump(iframe_dict,outfile)
             print('readwrite successful')
             print('JSON file Created!')      
            
            
           
#            data = iframe_list
#           
#            ##pprint.pprint(data) 
#            with open(filepathjson, 'w') as outfile:
#                json.dumps(data, outfile)
#                ##print json.dumps(data)       
#                
        except Exception,err:
            print('JSON FILE Creation FAILED')
            print Exception, err
        ## process sentiment
        try:
            print('before process sentiment')
            ##process_sentiment();
            print('after process sentiment')
        except:
            print('Process Sentiment FAILED')
        
        return flask.redirect(flask.url_for('result'))